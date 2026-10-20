#!/usr/bin/env python3
"""Exact arithmetic controls for EXPONENT-EXTRACTOR-FIREWALL21.

This does not test the recursion-theorem proof.  It checks the two downstream
claims used for allocation: an arbitrary fixed solver exponent can be absorbed
by a cofinal fixed-k MMW composition, and arbitrary fixed starting exponents
enter the stated conditional ARC comparison box after finitely many iterations.
"""

from fractions import Fraction
import json


def main():
    counts = {
        "delay_domination_checks": 0,
        "mmw_cofinal_checks": 0,
        "arc_finite_entry_checks": 0,
        "failures": 0,
    }

    # Finite shadows of the diagonal delay n^(E(e)+1) versus n^E(e).
    for exponent in range(65):
        for n in range(2, 257):
            assert n ** (exponent + 1) > n**exponent
            assert n ** (exponent + 1) // n**exponent == n
            counts["delay_domination_checks"] += 2

    # MMW composition at target length M=N^(6/5+o(1)).  For every fixed
    # ordinary-query solver exponents C,D, one fixed sufficiently large k
    # enters the strict comparison box t<241/200, s<1/2.
    a = Fraction(6, 5)
    tau = Fraction(241, 200)
    for C in range(257):
        for D in range(257):
            # Time requires k>240(C+1).  Space requires
            # k>(12/5)max(1,D).  Add one after integer flooring.
            k_time = 240 * (C + 1) + 1
            k_space = (12 * max(1, D)) // 5 + 1
            k = max(k_time, k_space)
            t = a * (1 + Fraction(C + 1, k))
            s = a * Fraction(max(1, D), k)
            assert k > 240 * (C + 1)
            assert Fraction(5 * k, 12) > max(1, D)
            assert t < tau
            assert s < Fraction(1, 2)
            counts["mmw_cofinal_checks"] += 4

    # Conditional ARC recurrence.  No exponent extractor is used: each fixed
    # starting pair merely has some finite hardwirable iteration count.
    max_entry_round = 0
    for t0 in range(1, 65):
        for s0 in range(1, 65):
            t = Fraction(t0, 1)
            s = Fraction(s0, 1)
            entered = False
            for r in range(1, 65):
                t = max(Fraction(11, 10), Fraction(3, 5) + t / 2)
                s = max(Fraction(1, 2), s / 2)
                if t < tau and s <= Fraction(1, 2):
                    entered = True
                    max_entry_round = max(max_entry_round, r)
                    break
            assert entered
            counts["arc_finite_entry_checks"] += 1

    counts["max_arc_entry_round"] = max_entry_round
    counts["assertions_total"] = (
        counts["delay_domination_checks"]
        + counts["mmw_cofinal_checks"]
        + counts["arc_finite_entry_checks"]
    )
    print(json.dumps(counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
