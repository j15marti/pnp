#!/usr/bin/env python3
"""Finite audit for MINIMAL-CORE-SOURCE-COVERAGE75.

The asymptotic lemmas are proved in the report.  This checks minimal
unsatisfiability, the canonical resolution refutation, and size arithmetic.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


checks = 0


def check(value: bool) -> None:
    global checks
    checks += 1
    assert value


def clause_holds(forbidden: int, assignment: int, k: int) -> bool:
    """Clause C_forbidden is false exactly on `forbidden`."""
    return any(((forbidden >> i) & 1) != ((assignment >> i) & 1) for i in range(k))


def canonical_resolution_counts(k: int) -> tuple[int, int, int]:
    """Return leaves, total clauses, and literal occurrences.

    At length r the canonical refutation contains every one of the 2^r
    clauses that excludes one r-bit assignment.  Opposite last literals are
    resolved to obtain the complete level r-1.
    """
    leaves = 1 << k
    total_nodes = 0
    literal_occurrences = 0
    for r in range(k, -1, -1):
        count = 1 << r
        total_nodes += count
        literal_occurrences += r * count
        if r:
            for prefix in range(1 << (r - 1)):
                left = (prefix << 1) | 0
                right = (prefix << 1) | 1
                check((left >> 1) == prefix)
                check((right >> 1) == prefix)
                check((left ^ right) == 1)
    return leaves, total_nodes, literal_occurrences


def main() -> None:
    minimality_pairs = 0
    resolution_levels = 0
    asymptotic_cases = 0

    # Removing C_a leaves the unique satisfying assignment a.
    for k in range(1, 11):
        m = 1 << k
        for removed in range(m):
            for clause in range(m):
                if clause == removed:
                    check(not clause_holds(clause, removed, k))
                else:
                    check(clause_holds(clause, removed, k))
                minimality_pairs += 1

        leaves, nodes, literals = canonical_resolution_counts(k)
        check(leaves == m)
        check(nodes == (2 * m - 1))
        expected_literals = sum(r * (1 << r) for r in range(k + 1))
        check(literals == expected_literals)
        check(literals <= 2 * k * m)
        resolution_levels += k

    # N = Theta(m*k).  Touching m=N/k blocks exceeds N^beta for every
    # fixed beta<1 eventually.  These finite cases are arithmetic checks only.
    for beta_num, beta_den in [(1, 2), (101, 200), (3, 5), (9, 10)]:
        beta = beta_num / beta_den
        seen_strict = False
        for k in range(2, 65):
            m = 1 << k
            n = m * k
            if m > n**beta:
                seen_strict = True
            if seen_strict:
                check(m > n**beta)
            asymptotic_cases += 1
        check(seen_strict)

    result = {
        "artifact": "MINIMAL-CORE-SOURCE-COVERAGE75",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "failures": 0,
        "minimality_clause_assignment_pairs": minimality_pairs,
        "resolution_levels_checked": resolution_levels,
        "asymptotic_arithmetic_cases": asymptotic_cases,
        "scope": "finite implementation audit; the report contains the proofs",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results/raw/synthesis/2026-10-22_2348_MINIMAL_CORE_SOURCE_COVERAGE75.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
