#!/usr/bin/env python3
"""Finite audit for BLACKBOX-FORK-SCALE-TRILEMMA1.

Finite controls only: delay-wrapper arithmetic, vanishing query-scale
arithmetic, and a toy replacement-covariance enumeration.
"""
from fractions import Fraction
import json

def delay_wrapper_checks():
    rows = []
    for denominator in range(2, 17):
        epsilon = Fraction(1, denominator)
        for common_exponent in range(1, 17):
            delay_exponent = common_exponent * denominator + 1
            charged = epsilon * delay_exponent
            assert charged > common_exponent
            rows.append({"epsilon": str(epsilon),
                         "common_exponent": common_exponent,
                         "chosen_delay_exponent": delay_exponent,
                         "induced_source_exponent": str(charged)})
    return rows

def vanishing_scale_checks():
    rows = []
    for solver_exponent in (1, 2, 4, 8, 16, 32):
        previous = None
        for j in (8, 16, 32, 64, 128):
            overhead = Fraction(solver_exponent, j)
            if previous is not None:
                assert overhead < previous
            previous = overhead
            rows.append({"fixed_solver_exponent": solver_exponent,
                         "scale": f"1/{j}",
                         "source_exponent_overhead": str(overhead)})
    return rows

def covariance_checks():
    invariant = []
    rejected = 0
    for table in range(1 << 9):
        rows = []
        for source in range(3):
            row = tuple((table >> (3 * source + impl)) & 1
                        for impl in range(3))
            rows.append(row)
        if all(len(set(row)) == 1 for row in rows):
            invariant.append(table)
        else:
            rejected += 1
    assert len(invariant) == 1 << 3
    assert rejected == (1 << 9) - (1 << 3)
    return {"maps": 1 << 9, "source_factor_maps": len(invariant),
            "rejected": rejected}

def main():
    delay = delay_wrapper_checks()
    vanishing = vanishing_scale_checks()
    out = {
        "claim": "BLACKBOX-FORK-SCALE-TRILEMMA1",
        "status": "COMPUTATIONAL",
        "scope_warning": "Finite arithmetic and toy covariance checks only; no asymptotic inference.",
        "delay_wrapper": {"checks": len(delay), "failures": 0,
                          "sample": delay[:4]},
        "vanishing_scale": {"checks": len(vanishing), "failures": 0,
                            "sample": vanishing[-5:]},
        "replacement_covariance": covariance_checks(),
    }
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
