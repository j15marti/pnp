#!/usr/bin/env python3
"""Exact arithmetic audit for EXISTENTIAL-CLOSURE-ENDPOINT114.

This script checks only the finite contraction arithmetic and the FLMV
endpoint margin.  It does not test or assume the missing SAT closure theorem.
"""

from fractions import Fraction
import json


C_STAR = Fraction(241, 200)
TIME_FIXED_POINT = Fraction(6, 5)
TIME_FLOOR = Fraction(11, 10)
SPACE_FLOOR = Fraction(1, 2)


def d(c: Fraction) -> Fraction:
    return Fraction(1, 2) * ((c + 2) / (c * c) - c)


def f(t: Fraction) -> Fraction:
    return max(TIME_FLOOR, Fraction(3, 5) + t / 2)


def g(s: Fraction) -> Fraction:
    return max(SPACE_FLOOR, s / 2)


def contraction_bound(t0: Fraction, r: int) -> Fraction:
    return TIME_FIXED_POINT + max(Fraction(0), t0 - TIME_FIXED_POINT) / (2**r)


def sufficient_steps(t0: Fraction, s0: Fraction) -> int:
    r = 0
    while not (
        max(Fraction(0), t0 - TIME_FIXED_POINT) / (2**r) < Fraction(1, 200)
        and s0 / (2**r) <= SPACE_FLOOR
    ):
        r += 1
    return r


def iterate(t0: Fraction, s0: Fraction, r: int) -> tuple[Fraction, Fraction]:
    t, s = t0, s0
    for _ in range(r):
        t, s = f(t), g(s)
    return t, s


def main() -> None:
    d_star = d(C_STAR)
    assert d_star == Fraction(11642479, 23232400)
    assert d_star - SPACE_FLOOR == Fraction(26279, 23232400) > 0

    checked = 0
    max_steps = 0
    witnesses = []
    # Exact grid: deliberately includes exponents far larger than any plausible
    # present SAT upper bound.  This is a finite regression check, not a proof.
    for t_num in range(0, 1025):
        for s_num in range(0, 257, 8):
            t0, s0 = Fraction(t_num, 2), Fraction(s_num, 2)
            r = sufficient_steps(t0, s0)
            tr, sr = iterate(t0, s0, r)
            assert tr <= contraction_bound(t0, r)
            assert tr < C_STAR
            assert sr <= SPACE_FLOOR
            checked += 1
            max_steps = max(max_steps, r)
            if (t_num, s_num) in {(0, 0), (4, 8), (20, 32), (1024, 256)}:
                witnesses.append(
                    {
                        "initial": [str(t0), str(s0)],
                        "steps": r,
                        "terminal": [str(tr), str(sr)],
                    }
                )

    result = {
        "claim": "EXISTENTIAL-CLOSURE-ENDPOINT114 arithmetic only",
        "status": "PASS",
        "c_star": str(C_STAR),
        "d_c_star": str(d_star),
        "space_margin": str(d_star - SPACE_FLOOR),
        "grid_pairs_checked": checked,
        "maximum_sufficient_steps_on_grid": max_steps,
        "selected_trajectories": witnesses,
        "open_obligation": (
            "Prove all-input same-realization existential closure of the "
            "achievable SAT time-space exponent set in the matched FLMV model."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
