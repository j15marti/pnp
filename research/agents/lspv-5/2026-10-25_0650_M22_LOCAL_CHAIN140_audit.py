#!/usr/bin/env python3
"""Finite arithmetic audit for M22-LOCAL-CHAIN140.

This script checks only exact size/incidence arithmetic and the MB3 exponent
ledger.  It does not infer gadget semantics or an SAT lower bound from finite
tests.
"""

from fractions import Fraction
import argparse
import json
import time


def transfer(lam, alpha, beta, setup, t, s):
    return max(setup, lam * t + alpha), max(beta, lam * s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-n", type=int, default=10000)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    start = time.perf_counter()
    checks = 0
    rows = []

    for n0 in range(1, args.max_n + 1):
        # Tagged monotone (3,3): m0=2n0.
        m0 = 2 * n0
        # Corrected Darmann--Doecker fixed block.
        n1, m1 = 15 * n0, 20 * n0
        # Doecker's 99-variable/133-clause enforcer on every source clause.
        n2, m2 = n1 + 99 * m1, 133 * m1
        # Transparent total anchor on the already-valid M22 image.
        n3, m3 = n2 + 6, m2 + 8

        assertions = [
            6 * n0 == 3 * m0,
            n1 == 15 * n0,
            m1 == 20 * n0,
            n2 == 1995 * n0,
            m2 == 2660 * n0,
            3 * m2 == 4 * n2,
            n3 == 1995 * n0 + 6,
            m3 == 2660 * n0 + 8,
            3 * m3 == 4 * n3,
        ]
        assert all(assertions)
        checks += len(assertions)
        if n0 in {1, 2, 3, 10, 100, 1000, args.max_n}:
            rows.append({
                "source_n": n0,
                "source_m": m0,
                "dd_star_n": n1,
                "dd_star_m": m1,
                "proper_m22_n": n2,
                "proper_m22_m": m2,
                "c_star_n": n3,
                "c_star_m": m3,
            })

    t_box = Fraction(241, 200)
    s_box = Fraction(11642479, 23232400)
    scenarios = {
        "three_local_legs": transfer(
            Fraction(1), Fraction(0), Fraction(0), Fraction(0), t_box, s_box
        ),
        "raw_occurrence_scan": transfer(
            Fraction(1), Fraction(1), Fraction(0), Fraction(0), t_box, s_box
        ),
        "stored_linear_occurrence_index": transfer(
            Fraction(1), Fraction(0), Fraction(1), Fraction(1), t_box, s_box
        ),
    }
    assert scenarios["three_local_legs"] == (t_box, s_box)
    assert scenarios["raw_occurrence_scan"][0] == Fraction(441, 200)
    assert scenarios["stored_linear_occurrence_index"][1] == 1
    assert scenarios["raw_occurrence_scan"][0] > t_box
    assert scenarios["stored_linear_occurrence_index"][1] > s_box
    checks += 5

    # Two nested local virtual-access layers keep alpha=beta=0 at exponent
    # scale; two nested raw rank scans already add two full time exponents.
    two_local = transfer(
        Fraction(1), Fraction(0), Fraction(0), Fraction(0),
        *transfer(Fraction(1), Fraction(0), Fraction(0), Fraction(0),
                  t_box, s_box)
    )
    two_raw = transfer(
        Fraction(1), Fraction(1), Fraction(0), Fraction(0),
        *transfer(Fraction(1), Fraction(1), Fraction(0), Fraction(0),
                  t_box, s_box)
    )
    assert two_local == (t_box, s_box)
    assert two_raw[0] == t_box + 2
    checks += 2

    result = {
        "claim": "M22-LOCAL-CHAIN140",
        "status": {
            "size_and_incidence_arithmetic": "COMPUTATIONAL exact-integer audit",
            "gadget_semantics": "not inferred; imported only from cited proofs",
            "ordinary_sat_first_leg": "OPEN",
            "ARC_EDGE_90": "OPEN",
            "DIRECT_POST": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "max_source_variables": args.max_n,
        "checks": checks,
        "failures": 0,
        "sample_rows": rows,
        "flmv_box": {
            "t_strict": str(t_box),
            "s_strict": str(s_box),
            "s_decimal": float(s_box),
        },
        "mb3_scenarios": {
            key: {"time": str(val[0]), "space": str(val[1])}
            for key, val in scenarios.items()
        },
        "two_level_controls": {
            "local_time": str(two_local[0]),
            "local_space": str(two_local[1]),
            "raw_scan_time": str(two_raw[0]),
            "raw_scan_space": str(two_raw[1]),
        },
        "direct_potential_counterexample": {
            "candidate": "number of occurrence tags not copied into workspace",
            "terminal_source_still_contains_tags": True,
            "terminal_zero_without_artificial_output_reset": False,
            "if_reset_on_output": "one output transition can erase the entire candidate value",
            "verdict": "FALSIFIED/RETIRED as a post-acquisition universal potential",
        },
        "elapsed_seconds": time.perf_counter() - start,
    }
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"checks": checks, "failures": 0,
                      "elapsed_seconds": result["elapsed_seconds"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
