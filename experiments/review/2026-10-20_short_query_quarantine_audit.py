#!/usr/bin/env python3
"""Exact arithmetic audit for SHORT-QUERY-QUARANTINE3.

This checks exponent inequalities only.  It is not a SAT lower bound and does
not build the missing SAT-to-MKTP totalization.
"""

from fractions import Fraction
import json
from pathlib import Path


TIME_CAP = Fraction(241, 200)


def first_strict_integer_above(x: Fraction) -> int:
    return x.numerator // x.denominator + 1


def minimum_k(c: int, d: int) -> int:
    # Conservative MMW ledger: O(M p) oracle-bearing outer work and at most
    # O(M p) sequential short-query calls, each solved in p^C time and p^D space.
    time_k = first_strict_integer_above(Fraction(200 * (c + 1), 41))
    space_k = 2 * max(1, d) + 1
    return max(time_k, space_k)


def audit(limit: int = 256) -> dict:
    checked = 0
    maximal = None
    records = []
    for c in range(1, limit + 1):
        for d in range(1, limit + 1):
            k = minimum_k(c, d)
            time_exp = Fraction(1, 1) + Fraction(c + 1, k)
            space_exp = Fraction(max(1, d), k)
            assert time_exp < TIME_CAP
            assert space_exp < Fraction(1, 2)
            if k > 1:
                prior_time = Fraction(1, 1) + Fraction(c + 1, k - 1)
                prior_space = Fraction(max(1, d), k - 1)
                assert prior_time >= TIME_CAP or prior_space >= Fraction(1, 2)
            # An exact M-bit replay table has exponent one regardless of k.
            buffered_space = max(Fraction(1, 1), space_exp)
            assert buffered_space == 1
            assert buffered_space > Fraction(1, 2)
            checked += 1
            rec = {
                "C": c,
                "D": d,
                "minimal_k": k,
                "time_exponent": str(time_exp),
                "space_exponent": str(space_exp),
            }
            if maximal is None or k > maximal["minimal_k"]:
                maximal = rec
            if (c, d) in {(1, 1), (8, 6), (64, 64), (256, 256)}:
                records.append(rec)

    # Exact quantifier-swap counterexample: each indexed constraint is locally
    # satisfiable, but no single two-bit W satisfies all three.
    constraints = [
        lambda w0, w1: w0 == 0,
        lambda w0, w1: w1 == 1 - w0,
        lambda w0, w1: w1 == 0,
    ]
    assignments = [(w0, w1) for w0 in (0, 1) for w1 in (0, 1)]
    local_witness_counts = [sum(pred(*w) for w in assignments) for pred in constraints]
    common_witnesses = [w for w in assignments if all(pred(*w) for pred in constraints)]
    assert all(x > 0 for x in local_witness_counts)
    assert common_witnesses == []

    return {
        "run": "SHORT_QUERY_QUARANTINE3",
        "status": "PASS",
        "scope": "exact exponent and quantifier controls; conditional bridge only",
        "time_cap": str(TIME_CAP),
        "parameter_box": {"C": [1, limit], "D": [1, limit]},
        "pairs_checked": checked,
        "strict_time_checks": checked,
        "strict_space_checks": checked,
        "minimality_checks": checked,
        "full_source_buffer_falsifiers": checked,
        "maximal_minimum_k": maximal,
        "selected_records": records,
        "quantifier_control": {
            "assignments_checked": len(assignments),
            "local_witness_counts": local_witness_counts,
            "common_witness_count": len(common_witnesses),
            "meaning": "forall i exists W_i does not imply exists W forall i",
        },
        "unexpected_failures": 0,
        "p_vs_np": "OPEN",
    }


if __name__ == "__main__":
    result = audit()
    out = Path("results/raw/synthesis/2026-10-20_0148_SHORT_QUERY_QUARANTINE3.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
