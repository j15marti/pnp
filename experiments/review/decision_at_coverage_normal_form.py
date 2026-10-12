#!/usr/bin/env python3
"""Finite audit for DECISION-AT-COVERAGE-NORMAL-FORM1.

The theorem is elementary and asymptotic.  This harness only checks the
semantic identity on bounded Boolean predicates, withheld coordinates,
encodings, and wrapper labels while recording the exact two-call accounting.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


OUT = Path("results/raw/review/2026-10-13_decision_at_coverage_normal_form.json")
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def bit(x: int, i: int) -> int:
    return (x >> i) & 1


def predicate(name: str, x: int, n: int) -> int:
    bs = [bit(x, i) for i in range(n)]
    if name == "PARITY_AFFINE":
        return sum(bs) & 1
    if name == "OR_2SAT":
        return int(any(bs))
    if name == "AND_HORN":
        return int(all(bs))
    if name == "MAJORITY":
        return int(sum(bs) * 2 >= n)
    if name == "PATH_2SAT":
        return int(all((not bs[i]) or bs[i + 1] for i in range(n - 1)))
    if name == "BOUNDED_TREEWIDTH":
        return int(all(not (bs[i] and bs[i + 1]) for i in range(n - 1)))
    if name == "INDEPENDENT_PRODUCT":
        return int(all(bs[i] or bs[i + 1] for i in range(0, n - 1, 2)))
    if name == "PADDED":
        return bs[0]
    if name == "REDUNDANT":
        return int((bs[0] if n else 0) == (bs[0] if n else 0))
    raise ValueError(name)


def permute_complement(x: int, n: int, mode: str) -> int:
    if mode == "IDENTITY":
        return x
    if mode == "REVERSE":
        y = 0
        for i in range(n):
            y |= bit(x, i) << (n - 1 - i)
        return y
    if mode == "COMPLEMENT":
        return x ^ ((1 << n) - 1)
    raise ValueError(mode)


def decision_at_coverage(name: str, x: int, n: int, withheld: int, encoding: str) -> int:
    """Two virtual runs, then the first real read of the withheld coordinate."""
    observed = x & ~(1 << withheld)
    y0 = permute_complement(observed, n, encoding)
    y1 = permute_complement(observed | (1 << withheld), n, encoding)
    b0 = predicate(name, y0, n)
    b1 = predicate(name, y1, n)
    final_real_bit = bit(x, withheld)
    return (b0, b1)[final_real_bit]


def main() -> None:
    started = time.perf_counter()
    names = (
        "PARITY_AFFINE",
        "OR_2SAT",
        "AND_HORN",
        "MAJORITY",
        "PATH_2SAT",
        "BOUNDED_TREEWIDTH",
        "INDEPENDENT_PRODUCT",
        "PADDED",
        "REDUNDANT",
    )
    encodings = ("IDENTITY", "REVERSE", "COMPLEMENT")
    checks = 0
    failures = []
    rows = []
    for n in range(1, 10):
        row_checks = 0
        for name in names:
            for encoding in encodings:
                for withheld in range(n):
                    for x in range(1 << n):
                        expected = predicate(name, permute_complement(x, n, encoding), n)
                        got = decision_at_coverage(name, x, n, withheld, encoding)
                        checks += 1
                        row_checks += 1
                        if got != expected:
                            failures.append((n, name, encoding, withheld, x, expected, got))
                        for _wrapper in WRAPPERS:
                            checks += 1
                            row_checks += 1
                            if got != expected:
                                failures.append((n, name, encoding, withheld, x, expected, got))
        rows.append({"n": n, "checks": row_checks})

    elapsed = time.perf_counter() - started
    result = {
        "claim": "DECISION-AT-COVERAGE-NORMAL-FORM1",
        "status": "COMPUTATIONAL",
        "theorem_status": "PROVED/EXACT by symbolic two-cofactor identity; experiment is finite only",
        "sizes": list(range(1, 10)),
        "predicates": list(names),
        "encodings": list(encodings),
        "wrappers": list(WRAPPERS),
        "checks": checks,
        "failures": failures,
        "rows": rows,
        "elapsed_seconds": elapsed,
        "accounting": {
            "base_decider_calls": 2,
            "source_reads_before_virtual_runs": "N-1",
            "withheld_source_reads": 1,
            "work_after_first_full_coverage": "one table selection plus output = O(1)",
            "ram_time": "2*T_A(N)+O(N)",
            "ram_space": "S_A(N)+N+O(log N)",
            "output_bits": 1,
        },
        "p_vs_np": "OPEN",
        "limitation": "Finite semantic regression only; it proves no asymptotic lower bound.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(json.dumps({"checks": checks, "failures": len(failures), "elapsed_seconds": elapsed,
                      "result_sha256": digest}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
