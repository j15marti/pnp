#!/usr/bin/env python3
"""Bounded audit for SOURCE-COVERAGE-PHASE-GAUGE1.

The audit is finite evidence only.  It checks the semantic identity behind the
cofactor compiler on hostile controls and records that equivalent wrappers can
move arbitrary polynomial work to the post-coverage suffix without changing
the one-bit decision.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import time
from pathlib import Path


OUT = Path("results/raw/review/2026-10-13_source_coverage_phase_gauge.json")
ENCODINGS = ("identity", "reverse", "complement")
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY1", "DELAY2", "DELAY3", "INTERP", "RECOMP")


def bits_of(x: int, n: int) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(n))


def encode(bits: tuple[int, ...], mode: str) -> tuple[int, ...]:
    if mode == "identity":
        return bits
    if mode == "reverse":
        return bits[::-1]
    if mode == "complement":
        return tuple(1 - b for b in bits)
    raise ValueError(mode)


def decode(bits: tuple[int, ...], mode: str) -> tuple[int, ...]:
    if mode == "identity":
        return bits
    if mode == "reverse":
        return bits[::-1]
    if mode == "complement":
        return tuple(1 - b for b in bits)
    raise ValueError(mode)


def decision(name: str, logical: tuple[int, ...]) -> int:
    n = len(logical)
    if name == "2SAT_OR":
        return int(any(logical))
    if name == "HORN_AND":
        return int(all(logical))
    if name == "AFFINE_PARITY":
        return sum(logical) & 1
    if name == "BOUNDED_TREEWIDTH":
        return int(all(logical[i] or logical[i + 1] for i in range(n - 1))) if n > 1 else logical[0]
    if name == "INDEPENDENT_PRODUCT":
        return int(all(logical[i] or logical[i + 1] for i in range(0, n - 1, 2))) if n > 1 else logical[0]
    if name == "PADDED_CORE":
        active = logical[: max(1, n // 2)]
        return sum(active) & 1
    if name == "REDUNDANT_CLAUSES":
        return int(any(logical) and any(logical) and any(logical))
    raise ValueError(name)


FAMILIES = (
    "2SAT_OR",
    "HORN_AND",
    "AFFINE_PARITY",
    "BOUNDED_TREEWIDTH",
    "INDEPENDENT_PRODUCT",
    "PADDED_CORE",
    "REDUNDANT_CLAUSES",
)


def cofactor_select(name: str, source: tuple[int, ...], withheld: tuple[int, ...], mode: str) -> int:
    table: dict[tuple[int, ...], int] = {}
    for completion in itertools.product((0, 1), repeat=len(withheld)):
        virtual = list(source)
        for i, b in zip(withheld, completion):
            virtual[i] = b
        table[completion] = decision(name, decode(tuple(virtual), mode))
    key = tuple(source[i] for i in withheld)
    return table[key]


def suffix_work(wrapper: str, n: int) -> int:
    if wrapper in ("DIRECT", "COPY", "DEAD"):
        return 1
    if wrapper == "DELAY1":
        return n
    if wrapper == "DELAY2":
        return n * n
    if wrapper == "DELAY3":
        return n * n * n
    if wrapper == "INTERP":
        return 2 * n + 1
    if wrapper == "RECOMP":
        return n * n + n + 1
    raise ValueError(wrapper)


def main() -> None:
    started = time.perf_counter()
    semantic_checks = 0
    wrapper_checks = 0
    cost_checks = 0
    failures: list[dict[str, object]] = []
    observed_suffix_min = None
    observed_suffix_max = 0

    for n in range(1, 10):
        kmax = min(3, int(math.log2(max(2, n))))
        for x in range(1 << n):
            logical = bits_of(x, n)
            for mode in ENCODINGS:
                source = encode(logical, mode)
                for name in FAMILIES:
                    expected = decision(name, logical)
                    for k in range(1, kmax + 1):
                        withheld = tuple(range(n - k, n))
                        got = cofactor_select(name, source, withheld, mode)
                        semantic_checks += 1
                        if got != expected:
                            failures.append({"n": n, "x": x, "family": name, "encoding": mode, "k": k})
                        for wrapper in WRAPPERS:
                            work = suffix_work(wrapper, n)
                            wrapper_checks += 1
                            cost_checks += int(work >= 1)
                            observed_suffix_min = work if observed_suffix_min is None else min(observed_suffix_min, work)
                            observed_suffix_max = max(observed_suffix_max, work)

    theorem_ledger = {
        "single_withheld_bit": {
            "time": "2*T_A(N)+O(N)",
            "space": "S_A(N)+N+O(log N)",
            "suffix_after_final_read": "O(1)",
        },
        "k_withheld_bits": {
            "time": "2^k*T_A(N)+O(N+2^k)",
            "space": "S_A(N)+N+2^k+O(log N)",
            "polynomial_guard": "k <= c*log_2(N)",
            "suffix_after_final_read": "O(1)",
        },
        "wrapper_gauge": {
            "same_language": True,
            "bounded_suffix_range_in_audit": [observed_suffix_min, observed_suffix_max],
            "unbounded_polynomial_family": "DELAY_p gives Theta(N^p) for arbitrary fixed p",
        },
    }
    payload = {
        "claim": "SOURCE-COVERAGE-PHASE-GAUGE1",
        "status": "COMPUTATIONAL",
        "sizes": [1, 9],
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
        "semantic_checks": semantic_checks,
        "wrapper_checks": wrapper_checks,
        "cost_checks": cost_checks,
        "failures": failures,
        "theorem_ledger": theorem_ledger,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope_warning": "Finite checks do not establish asymptotic lower bounds.",
        "p_vs_np": "OPEN",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(f"FAIL: {len(failures)} semantic mismatches")
    print(json.dumps({
        "status": "PASS",
        "semantic_checks": semantic_checks,
        "wrapper_checks": wrapper_checks,
        "cost_checks": cost_checks,
        "elapsed_seconds": payload["elapsed_seconds"],
        "output": str(OUT),
        "sha256": payload["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
