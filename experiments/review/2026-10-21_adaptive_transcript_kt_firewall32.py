#!/usr/bin/env python3
"""Finite audit for ADAPTIVE-TRANSCRIPT-KT-FIREWALL32.

The audit verifies that an adaptive Boolean-oracle interaction can be replayed
from its hardwired answer transcript and that several transcript-dependent
targets have exact indexed generators.  It does not estimate minimum KT.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import asdict, dataclass


def base_template(label: int, h: int) -> bytes:
    head = b"SAT-BASE|" if label else b"UNSAT-BASE|"
    return head + b"+abc;" * (h + 3)


def query_token(base: bytes, prefix: tuple[int, ...], round_index: int) -> int:
    """A deterministic adaptive query identifier in [0,255]."""
    acc = (sum(base) + 17 * round_index + 29 * len(prefix)) & 255
    for i, bit in enumerate(prefix):
        acc = (131 * acc + (i + 1) * (bit + 1)) & 255
    return acc


def interaction(base: bytes, answers: tuple[int, ...]) -> tuple[int, ...]:
    queries = []
    prefix: tuple[int, ...] = ()
    for i, answer in enumerate(answers):
        queries.append(query_token(base, prefix, i))
        prefix += (answer,)
    return tuple(queries)


def code_bit(kind: str, answers: tuple[int, ...], queries: tuple[int, ...], j: int) -> int:
    h = len(answers)
    if h == 0:
        return 0
    if kind == "repeat_answers":
        return answers[j % h]
    if kind == "adaptive_xor":
        return answers[j % h] ^ answers[(3 * j + 1) % h] ^ (queries[j % h] & 1)
    if kind == "rolling_path":
        upto = j % h
        return (sum(answers[: upto + 1]) + queries[upto]) & 1
    if kind == "query_parity":
        q = queries[(j * j + j + 1) % h]
        return ((q >> (j % 8)) & 1) ^ answers[(5 * j + 1) % h]
    raise ValueError(kind)


def materialize(kind: str, base: bytes, answers: tuple[int, ...]) -> bytes:
    if kind == "raw_transcript":
        return base + bytes(answers)
    queries = interaction(base, answers)
    return base + bytes(code_bit(kind, answers, queries, j) for j in range(2 * len(base)))


def indexed_byte(kind: str, base: bytes, answers: tuple[int, ...], j: int) -> int:
    if j < len(base):
        return base[j]
    q = j - len(base)
    if kind == "raw_transcript":
        return answers[q]
    queries = interaction(base, answers)
    return code_bit(kind, answers, queries, q)


@dataclass
class Audit:
    max_answers: int = 10
    transcripts_checked: int = 0
    adaptive_query_checks: int = 0
    targets_checked: int = 0
    indexed_bytes_checked: int = 0
    cardinality_checks: int = 0
    label_separation_checks: int = 0
    failures: int = 0


def check(cond: bool, audit: Audit, field: str) -> None:
    setattr(audit, field, getattr(audit, field) + 1)
    if not cond:
        audit.failures += 1
        raise AssertionError(field)


def run() -> dict:
    audit = Audit()
    kinds = ("raw_transcript", "repeat_answers", "adaptive_xor", "rolling_path", "query_parity")
    rows = []
    for h in range(audit.max_answers + 1):
        outputs = {(label, kind): set() for label in (0, 1) for kind in kinds}
        row_targets = 0
        row_bytes = 0
        for answers in itertools.product((0, 1), repeat=h):
            audit.transcripts_checked += 1
            for label in (0, 1):
                base = base_template(label, h)
                queries = interaction(base, answers)
                prefix: tuple[int, ...] = ()
                for i, query in enumerate(queries):
                    check(query == query_token(base, prefix, i), audit, "adaptive_query_checks")
                    prefix += (answers[i],)
                for kind in kinds:
                    target = materialize(kind, base, answers)
                    outputs[(label, kind)].add(target)
                    audit.targets_checked += 1
                    row_targets += 1
                    for j, byte in enumerate(target):
                        check(indexed_byte(kind, base, answers, j) == byte, audit, "indexed_bytes_checked")
                        row_bytes += 1
            for kind in kinds:
                left = materialize(kind, base_template(0, h), answers)
                right = materialize(kind, base_template(1, h), answers)
                check(left != right, audit, "label_separation_checks")
        for label in (0, 1):
            for kind in kinds:
                check(len(outputs[(label, kind)]) <= (1 << h), audit, "cardinality_checks")
            check(len(outputs[(label, "raw_transcript")]) == (1 << h), audit, "cardinality_checks")
        rows.append({
            "answer_bits": h,
            "transcripts_exhausted": 1 << h,
            "targets_checked": row_targets,
            "indexed_bytes_checked": row_bytes,
            "max_outputs_per_fixed_base_and_encoder": 1 << h,
        })

    theorem_ledger = {
        "ordinary_KT_upper_bound": "KT(y) <= O(c_x+t_x+h+R+log L) on a fixed efficient universal machine",
        "adaptive_answers": "hardwire the realized h-bit transcript; replay adaptively generated queries from prior hardwired answers",
        "high_side_necessity": "if KT(y)>p and base/replay terms are o(p), then the answer transcript or another source-specific component must have Omega(p) cost",
        "cardinality": "for a fixed base and deterministic replay algorithm, h answer bits select at most 2^h outputs",
        "scope": "target-KT upper bound; no oracle-answer acquisition lower bound and no SAT/ARC separation",
    }
    payload = {
        "run_id": "ADAPTIVE-TRANSCRIPT-KT-FIREWALL32",
        "audit": asdict(audit),
        "encoders": list(kinds),
        "rows": rows,
        "theorem_ledger": theorem_ledger,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    return payload


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
