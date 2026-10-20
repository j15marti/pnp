#!/usr/bin/env python3
"""Exact controls for FIXED-PARAMETER-HARDWIRING22.

Checks the exponent gaps, finite absorption thresholds for explosive fixed-k
constants, the variable-k counterexample, and finite-depth ARC entry.  This is
an arithmetic audit, not a construction of R_k or the ARC contractor.
"""

from fractions import Fraction
import json


def ceil_fraction(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def main():
    a = Fraction(6, 5)
    tau = Fraction(241, 200)
    sigma = Fraction(1, 2)
    counts = {
        "fixed_k_gap_checks": 0,
        "fixed_constant_absorption_checks": 0,
        "variable_k_counterexample_checks": 0,
        "arc_finite_depth_checks": 0,
        "failures": 0,
    }
    max_log2_N0 = 0

    # For every fixed solver exponent pair, choose a fixed k.  Even the
    # deliberately explosive constant A_k=2^(2^k) has a finite absorption
    # threshold because k is held constant as N tends to infinity.
    for C in range(129):
        for D in range(129):
            k = max(240 * (C + 1) + 1, (12 * max(1, D)) // 5 + 1)
            et = a * (1 + Fraction(C + 1, k))
            es = a * Fraction(max(1, D), k)
            assert et < tau
            assert es < sigma
            counts["fixed_k_gap_checks"] += 2

            # Allocate half the exponent gap to absorb A_k.  Since
            # log2(A_k)=2^k, it suffices that log2 N >= 2^(k+1)/gap.
            dt = tau - et
            ds = sigma - es
            log2_N0_t = ceil_fraction(Fraction(2 ** (k + 1), 1) / dt)
            log2_N0_s = ceil_fraction(Fraction(2 ** (k + 1), 1) / ds)
            assert Fraction(2**k, log2_N0_t) <= dt / 2
            assert Fraction(2**k, log2_N0_s) <= ds / 2
            max_log2_N0 = max(max_log2_N0, log2_N0_t.bit_length(), log2_N0_s.bit_length())
            counts["fixed_constant_absorption_checks"] += 2

    # Variable k(N) is different.  On log2 N=q^2 and k=q,
    # log_N 2^(2^k)=2^q/q^2 -> infinity.
    previous = None
    for q in range(16, 81):
        overhead_exponent = Fraction(2**q, q * q)
        assert overhead_exponent > q
        if previous is not None:
            assert overhead_exponent > previous
            counts["variable_k_counterexample_checks"] += 1
        previous = overhead_exponent
        counts["variable_k_counterexample_checks"] += 1

    # Finite ARC depth after the starting exponents are fixed.  No r(N) and no
    # exponent extractor are used.
    max_arc_depth = 0
    for t0 in range(1, 65):
        for s0 in range(1, 65):
            t = Fraction(t0)
            s = Fraction(s0)
            entered = False
            for depth in range(1, 65):
                t = max(Fraction(11, 10), Fraction(3, 5) + t / 2)
                s = max(Fraction(1, 2), s / 2)
                if t < tau and s <= sigma:
                    entered = True
                    max_arc_depth = max(max_arc_depth, depth)
                    break
            assert entered
            counts["arc_finite_depth_checks"] += 1

    counts["max_arc_depth"] = max_arc_depth
    counts["max_absorption_threshold_bit_length"] = max_log2_N0
    counts["assertions_total"] = sum(
        counts[k]
        for k in (
            "fixed_k_gap_checks",
            "fixed_constant_absorption_checks",
            "variable_k_counterexample_checks",
            "arc_finite_depth_checks",
        )
    )
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
