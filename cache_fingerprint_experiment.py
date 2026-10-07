#!/usr/bin/env python3
"""Bounded exact-cache fingerprint experiment for COMBINED-REPLAY1.

The cache fingerprint is only a candidate selector.  Every prospective hit is
verified by full first-occurrence-normalized residual-stream equality.  Thus a
short fingerprint, an adaptive extension decision, or even a SHA collision can
change work and storage, but cannot change the SAT answer.

Run: python cache_fingerprint_experiment.py OUTPUT.json
The experiment has an internal 25-second alarm.
"""

from __future__ import annotations

import hashlib
import json
import signal
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from combined_replay_wrapper import (
    CacheEntry,
    Formula,
    ReplaySolver,
    State,
    pigeonhole,
    repeated_dense_sat,
)


class BucketLedger:
    """Instrumentation shared by fixed and adaptive fingerprint caches."""

    base_digest_bytes: int
    cache: List[CacheEntry]
    metrics: Dict[str, int]

    def initialize_bucket_ledger(self, base_digest_bytes: int) -> None:
        self.base_digest_bytes = base_digest_bytes
        self.metrics.update(
            {
                "hash_streams": 0,
                "max_hash_aux_bits": 0,
                "max_exact_bucket_occupancy": 0,
                "max_base_bucket_occupancy": 0,
                "max_bucket_count": 0,
                "fingerprint_extensions": 0,
                "fingerprint_extension_bits": 0,
                "extension_hash_replays": 0,
            }
        )

    def update_buckets(self) -> None:
        exact = Counter((len(entry.signature), entry.signature) for entry in self.cache)
        base = Counter(entry.signature[: self.base_digest_bytes] for entry in self.cache)
        self.metrics["max_exact_bucket_occupancy"] = max(
            self.metrics["max_exact_bucket_occupancy"], max(exact.values(), default=0)
        )
        self.metrics["max_base_bucket_occupancy"] = max(
            self.metrics["max_base_bucket_occupancy"], max(base.values(), default=0)
        )
        self.metrics["max_bucket_count"] = max(
            self.metrics["max_bucket_count"], len(exact)
        )

    def bucket_summary(self) -> Dict[str, int]:
        exact = Counter((len(entry.signature), entry.signature) for entry in self.cache)
        base = Counter(entry.signature[: self.base_digest_bytes] for entry in self.cache)
        return {
            "cache_entries_final": len(self.cache),
            "cache_bits_final": self.cache_bits,
            "fingerprint_bits_final": sum(8 * len(entry.signature) for entry in self.cache),
            "exact_buckets_final": len(exact),
            "nonsingleton_exact_buckets_final": sum(value > 1 for value in exact.values()),
            "max_exact_bucket_occupancy_final": max(exact.values(), default=0),
            "base_buckets_final": len(base),
            "nonsingleton_base_buckets_final": sum(value > 1 for value in base.values()),
            "max_base_bucket_occupancy_final": max(base.values(), default=0),
        }


class FixedFingerprintSolver(BucketLedger, ReplaySolver):
    """ReplaySolver with fixed-length bucket and hash-work instrumentation."""

    def __init__(self, *args: object, digest_bytes: int, **kwargs: object) -> None:
        super().__init__(*args, digest_bytes=digest_bytes, **kwargs)
        self.initialize_bucket_ledger(digest_bytes)

    def signature(self, state: State, live_bits: int = 0) -> bytes:
        # Charge a 256-bit SHA-256 state concurrently with normalization, then
        # the retained truncated output after finalization.
        self.metrics["hash_streams"] += 1
        self.metrics["max_hash_aux_bits"] = max(
            self.metrics["max_hash_aux_bits"], 256 + 8 * self.digest_bytes
        )
        signature = super().signature(state, live_bits + 256)
        self.update_live(live_bits, 256 + 8 * len(signature))
        return signature

    def cache_lookup(self, state: State, live_bits: int = 0) -> Optional[bool]:
        if self.cache_budget_bits <= 0:
            return None
        self.metrics["cache_lookups"] += 1
        signature = self.signature(state, live_bits)
        signature_bits = 8 * len(signature)
        for entry in reversed(self.cache):
            if entry.signature != signature:
                continue
            self.metrics["cache_candidate_comparisons"] += 1
            if self.residual_equal(state, entry.state, live_bits + signature_bits):
                self.metrics["cache_hits"] += 1
                return entry.answer
            self.metrics["cache_hash_collisions_rejected"] += 1
        self.metrics["cache_misses"] += 1
        return None

    def cache_insert(self, state: State, answer: bool, live_bits: int = 0) -> None:
        if self.cache_budget_bits <= 0:
            return
        descriptor = self.descriptor_bits(state) + 8 * self.digest_bytes + 1
        if descriptor > self.cache_budget_bits:
            return
        signature = self.signature(state, live_bits)
        while self.cache and self.cache_bits + descriptor > self.cache_budget_bits:
            old = self.cache.pop(0)
            self.cache_bits -= old.descriptor_bits
            self.metrics["cache_evictions"] += 1
        self.cache.append(CacheEntry(signature, state, answer, descriptor))
        self.cache_bits += descriptor
        self.metrics["cache_insertions"] += 1
        self.metrics["max_cache_entries"] = max(
            self.metrics["max_cache_entries"], len(self.cache)
        )
        self.metrics["max_cache_descriptor_bits"] = max(
            self.metrics["max_cache_descriptor_bits"], self.cache_bits
        )
        self.update_buckets()
        self.update_live(live_bits)


class AdaptiveFingerprintSolver(BucketLedger, ReplaySolver):
    """Adaptive fingerprints with exact residual verification.

    Entries begin with ``base_digest_bytes``.  When a query collides with a
    stored prefix, the stored fingerprint is extended just far enough to reach
    a differing byte, up to ``max_digest_bytes``.  No full digest is retained.
    Extending an old entry therefore regenerates its residual stream and is
    charged as source work.
    """

    def __init__(
        self,
        *args: object,
        base_digest_bytes: int,
        max_digest_bytes: int,
        **kwargs: object,
    ) -> None:
        if not 0 < base_digest_bytes <= max_digest_bytes <= 32:
            raise ValueError("require 0 < base <= max <= 32 bytes")
        super().__init__(*args, digest_bytes=base_digest_bytes, **kwargs)
        self.max_digest_bytes = max_digest_bytes
        self.initialize_bucket_ledger(base_digest_bytes)

    def full_signature(self, state: State, live_bits: int = 0) -> bytes:
        self.metrics["hash_streams"] += 1
        self.metrics["max_hash_aux_bits"] = max(
            self.metrics["max_hash_aux_bits"], 512
        )
        digest = hashlib.sha256()
        # A 256-bit hash state is live while the normalization map is built.
        for clause in self.normalized_residual(state, live_bits + 256):
            digest.update(len(clause).to_bytes(4, "big"))
            for literal in clause:
                digest.update(int(literal).to_bytes(8, "big", signed=True))
        output = digest.digest()
        # Hash state plus its full transient output; only a prefix is retained.
        self.update_live(live_bits, 512)
        return output

    @staticmethod
    def required_bytes(left: bytes, right: bytes, maximum: int) -> int:
        for index in range(maximum):
            if left[index] != right[index]:
                return index + 1
        return maximum

    def _make_room(self, extra_bits: int, protected: Optional[CacheEntry]) -> bool:
        while self.cache_bits + extra_bits > self.cache_budget_bits:
            victim_index = next(
                (index for index, entry in enumerate(self.cache) if entry is not protected),
                None,
            )
            if victim_index is None:
                return False
            victim = self.cache.pop(victim_index)
            self.cache_bits -= victim.descriptor_bits
            self.metrics["cache_evictions"] += 1
        return True

    def _extend_entry(
        self,
        entry: CacheEntry,
        full_digest: bytes,
        required: int,
        live_bits: int,
    ) -> None:
        target = min(self.max_digest_bytes, max(len(entry.signature), required))
        if target <= len(entry.signature):
            return
        extra = 8 * (target - len(entry.signature))
        if not self._make_room(extra, entry):
            return
        entry.signature = full_digest[:target]
        entry.descriptor_bits += extra
        self.cache_bits += extra
        self.metrics["fingerprint_extensions"] += 1
        self.metrics["fingerprint_extension_bits"] += extra
        self.metrics["max_cache_descriptor_bits"] = max(
            self.metrics["max_cache_descriptor_bits"], self.cache_bits
        )
        self.update_buckets()
        self.update_live(live_bits, 8 * target)

    def cache_lookup(self, state: State, live_bits: int = 0) -> Optional[bool]:
        if self.cache_budget_bits <= 0:
            return None
        self.metrics["cache_lookups"] += 1
        query_digest = self.full_signature(state, live_bits)
        active_ids = {id(entry) for entry in self.cache}
        for entry in list(reversed(self.cache)):
            if id(entry) not in active_ids or not query_digest.startswith(entry.signature):
                continue
            self.metrics["cache_candidate_comparisons"] += 1
            if self.residual_equal(state, entry.state, live_bits + 256):
                self.metrics["cache_hits"] += 1
                return entry.answer
            self.metrics["cache_hash_collisions_rejected"] += 1
            # The rejected candidate is regenerated to obtain extension bits.
            self.metrics["extension_hash_replays"] += 1
            entry_digest = self.full_signature(entry.state, live_bits + 256)
            required = self.required_bytes(
                query_digest, entry_digest, self.max_digest_bytes
            )
            self._extend_entry(entry, entry_digest, required, live_bits + 256)
            active_ids = {id(current) for current in self.cache}
        self.metrics["cache_misses"] += 1
        return None

    def cache_insert(self, state: State, answer: bool, live_bits: int = 0) -> None:
        if self.cache_budget_bits <= 0:
            return
        query_digest = self.full_signature(state, live_bits)
        new_length = self.base_digest_bytes

        # Separate stored prefixes when their SHA digests differ within the
        # retained limit.  Existing full digests are regenerated, never kept
        # as hidden cache payload.  Prefixes still tied at the limit remain
        # candidates for mandatory exact residual verification.
        active_ids = {id(entry) for entry in self.cache}
        for entry in list(self.cache):
            if id(entry) not in active_ids:
                continue
            new_prefix = query_digest[:new_length]
            if not (
                new_prefix.startswith(entry.signature)
                or entry.signature.startswith(new_prefix)
            ):
                continue
            self.metrics["extension_hash_replays"] += 1
            entry_digest = self.full_signature(entry.state, live_bits + 256)
            required = self.required_bytes(
                query_digest, entry_digest, self.max_digest_bytes
            )
            self._extend_entry(entry, entry_digest, required, live_bits + 512)
            active_ids = {id(current) for current in self.cache}
            new_length = max(new_length, required)

        descriptor = self.descriptor_bits(state) + 8 * new_length + 1
        if descriptor > self.cache_budget_bits:
            return
        if not self._make_room(descriptor, None):
            return
        signature = query_digest[:new_length]
        self.cache.append(CacheEntry(signature, state, answer, descriptor))
        self.cache_bits += descriptor
        if new_length > self.base_digest_bytes:
            self.metrics["fingerprint_extensions"] += 1
            self.metrics["fingerprint_extension_bits"] += 8 * (
                new_length - self.base_digest_bytes
            )
        self.metrics["cache_insertions"] += 1
        self.metrics["max_cache_entries"] = max(
            self.metrics["max_cache_entries"], len(self.cache)
        )
        self.metrics["max_cache_descriptor_bits"] = max(
            self.metrics["max_cache_descriptor_bits"], self.cache_bits
        )
        self.update_buckets()
        self.update_live(live_bits, 8 * new_length)


def deadline(*_: object) -> None:
    raise TimeoutError("25-second cache-fingerprint experiment limit")


def workloads() -> Iterable[Tuple[str, int, Formula, bool]]:
    # PHP(7,6) retains hundreds of distinct cache states.  It produces a
    # reproducible 16-bit collision and many 8-bit collisions while leaving
    # enough time to charge adaptive extension replays under the 25-second
    # experiment guard.
    n, source = pigeonhole(7, 6)
    yield "php_7_6", n, source, False
    n, source = repeated_dense_sat(8, width=5)
    yield "dense_isomorphic_8", n, source, True


def extract_row(
    label: str,
    mode: str,
    hex_digits: str,
    case_name: str,
    answer: bool,
    elapsed: float,
    solver: BucketLedger,
) -> Dict[str, object]:
    metrics = solver.metrics
    return {
        "configuration": label,
        "mode": mode,
        "hex_digits": hex_digits,
        "case": case_name,
        "answer": answer,
        "seconds": elapsed,
        **solver.bucket_summary(),
        "max_cache_bits": metrics["max_cache_descriptor_bits"],
        "max_cache_entries": metrics["max_cache_entries"],
        "max_exact_bucket_occupancy_peak": metrics["max_exact_bucket_occupancy"],
        "max_base_bucket_occupancy_peak": metrics["max_base_bucket_occupancy"],
        "candidate_equality_replays": metrics["cache_candidate_comparisons"],
        "rejected_collisions": metrics["cache_hash_collisions_rejected"],
        "cache_hits": metrics["cache_hits"],
        "cache_evictions": metrics["cache_evictions"],
        "hash_streams": metrics["hash_streams"],
        "fingerprint_extensions": metrics["fingerprint_extensions"],
        "fingerprint_extension_bits": metrics["fingerprint_extension_bits"],
        "extension_hash_replays": metrics["extension_hash_replays"],
        "source_passes": metrics["source_passes"],
        "source_literal_reads": metrics["source_literal_reads"],
        "recursive_calls": metrics["recursive_calls"],
        "peak_workspace_bits_sequential": metrics[
            "max_charged_workspace_bits_sequential"
        ],
        "peak_workspace_bits_random_access": metrics[
            "max_charged_workspace_bits_random_access"
        ],
    }


def summarize(label: str, rows: List[Dict[str, object]]) -> Dict[str, object]:
    additive = (
        "seconds",
        "cache_bits_final",
        "fingerprint_bits_final",
        "candidate_equality_replays",
        "rejected_collisions",
        "cache_hits",
        "cache_evictions",
        "hash_streams",
        "fingerprint_extensions",
        "fingerprint_extension_bits",
        "extension_hash_replays",
        "source_passes",
        "source_literal_reads",
        "recursive_calls",
    )
    maxima = (
        "max_cache_bits",
        "max_cache_entries",
        "max_exact_bucket_occupancy_peak",
        "max_base_bucket_occupancy_peak",
        "peak_workspace_bits_sequential",
        "peak_workspace_bits_random_access",
    )
    return {
        "configuration": label,
        "mode": rows[0]["mode"],
        "hex_digits": rows[0]["hex_digits"],
        **{key: sum(row[key] for row in rows) for key in additive},
        **{key: max(row[key] for row in rows) for key in maxima},
        "answer_checks": len(rows),
    }


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    cache_budget_bits = 131_072
    configurations = [
        ("fixed_2hex", "fixed", 1, 1),
        ("fixed_4hex", "fixed", 2, 2),
        ("fixed_6hex", "fixed", 3, 3),
        ("fixed_8hex", "fixed", 4, 4),
        ("adaptive_2_to_8hex", "adaptive", 1, 4),
        ("adaptive_4_to_8hex", "adaptive", 2, 4),
    ]
    details: List[Dict[str, object]] = []
    summaries: List[Dict[str, object]] = []

    for label, mode, base_bytes, max_bytes in configurations:
        configuration_rows: List[Dict[str, object]] = []
        for case_name, n, source, expected in workloads():
            common = dict(
                source=source,
                n=n,
                frontier_cap=5,
                frontier_block=4,
                cache_budget_bits=cache_budget_bits,
            )
            if mode == "fixed":
                solver = FixedFingerprintSolver(
                    **common, digest_bytes=base_bytes
                )
                digits = str(2 * base_bytes)
            else:
                solver = AdaptiveFingerprintSolver(
                    **common,
                    base_digest_bytes=base_bytes,
                    max_digest_bytes=max_bytes,
                )
                digits = f"{2 * base_bytes}->{2 * max_bytes}"
            case_started = time.perf_counter()
            answer, _ = solver.solve()
            elapsed = time.perf_counter() - case_started
            assert answer == expected, (label, case_name, answer, expected)
            row = extract_row(
                label, mode, digits, case_name, answer, elapsed, solver
            )
            details.append(row)
            configuration_rows.append(row)
        summaries.append(summarize(label, configuration_rows))

    # Every configuration follows the same exact recursive search tree.  Hash
    # collisions only add rejected equality replays and can affect eviction.
    php_calls = {
        row["recursive_calls"]
        for row in details
        if row["case"] == "php_7_6"
    }
    dense_calls = {
        row["recursive_calls"]
        for row in details
        if row["case"] == "dense_isomorphic_8"
    }
    assert len(php_calls) == 1
    assert len(dense_calls) == 1

    result = {
        "status": "COMPUTATIONAL",
        "claim": (
            "All cache reuse is guarded by exact normalized residual-stream "
            "equality; fingerprints select candidates but never certify them."
        ),
        "cache_budget_bits_per_solver": cache_budget_bits,
        "configurations": len(configurations),
        "workloads_per_configuration": 2,
        "answer_checks": len(details),
        "errors": 0,
        "seconds": time.perf_counter() - started,
        "internal_alarm_seconds": 25,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "summaries": summaries,
        "details": details,
        "interpretation": [
            "Short fixed fingerprints save cache bits but can trigger many exact equality replays.",
            "Adaptive fingerprints retain only prefixes and regenerate old residuals when extension bits are needed.",
            "Adaptive extension changes cost only; exact stream verification remains the correctness guard.",
            "These bounded measurements do not prove an asymptotic cache or SAT bound.",
        ],
    }
    destination = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).with_suffix(".json")
    )
    destination.write_text(json.dumps(result, indent=2) + "\n")
    signal.alarm(0)
    print(json.dumps({key: value for key, value in result.items() if key != "details"}, indent=2))


if __name__ == "__main__":
    main()
