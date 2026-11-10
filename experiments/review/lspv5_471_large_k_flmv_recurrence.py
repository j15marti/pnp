#!/usr/bin/env python3
"""Exact controls for the conditional FLMV contraction recurrence.

This does not implement a SAT solver or the missing compiler.  It verifies the
arithmetic implication that would follow if the fully charged same-machine
compiler in [P2-A2] existed and were recursively applicable.
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def boundary_poly(c: Fraction) -> Fraction:
    """beta(c) > 1/2 iff this is negative, for c>0."""
    return c**3 + c**2 - c - 2


def step(t: Fraction, s: Fraction) -> tuple[Fraction, Fraction]:
    return max(Fraction(11, 10), Fraction(3, 5) + t / 2), max(Fraction(1, 2), s / 2)


def iterate(t0: Fraction, s0: Fraction, rounds: int) -> tuple[Fraction, Fraction]:
    t, s = t0, s0
    for _ in range(rounds):
        t, s = step(t, s)
    return t, s


def minimal_forbidden_round(t0: Fraction, s0: Fraction, cap: int = 10000) -> int:
    for r in range(cap + 1):
        t, s = iterate(t0, s0, r)
        if s <= Fraction(1, 2) and beta(t) > Fraction(1, 2):
            return r
    raise ValueError("round cap exceeded")


def root_decimal() -> Decimal:
    lo, hi = Decimal("1.2"), Decimal("1.21")
    for _ in range(250):
        mid = (lo + hi) / 2
        val = mid**3 + mid**2 - mid - 2
        if val < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def dfrac(x: Fraction) -> str:
    return str(Decimal(x.numerator) / Decimal(x.denominator))


def main() -> None:
    checks = 0
    # Exact published checkpoint.
    assert beta(Fraction(6, 5)) == Fraction(23, 45); checks += 1
    assert beta(Fraction(6, 5)) - Fraction(1, 2) == Fraction(1, 90); checks += 1

    # Closed form above the fixed point.
    for t0 in [Fraction(6, 5), Fraction(2), Fraction(10), Fraction(1000)]:
        for r in range(31):
            t, _ = iterate(t0, Fraction(1, 2), r)
            expected = Fraction(6, 5) + (t0 - Fraction(6, 5)) / (2**r)
            assert t == expected; checks += 1

    # No uniform finite number of rounds over unbounded initial exponents:
    # for each fixed r, choose t0 so the r-th iterate is exactly 121/100,
    # safely above the true beta(t)=1/2 boundary.
    for r in range(41):
        t0 = Fraction(6, 5) + (2**r) * Fraction(1, 100)
        t, _ = iterate(t0, Fraction(1, 2), r)
        assert t == Fraction(121, 100); checks += 1
        assert beta(t) < Fraction(1, 2); checks += 1

    cases = []
    for k in [2, 10, 100, 1000, 10**6]:
        r = minimal_forbidden_round(Fraction(k), Fraction(k))
        t, s = iterate(Fraction(k), Fraction(k), r)
        assert s == Fraction(1, 2); checks += 1
        assert boundary_poly(t) < 0; checks += 1
        if r:
            pt, ps = iterate(Fraction(k), Fraction(k), r - 1)
            assert ps > Fraction(1, 2) or boundary_poly(pt) >= 0; checks += 1
        cases.append({
            "initial_t_equals_s": k,
            "minimal_round": r,
            "t_r": dfrac(t),
            "s_r": dfrac(s),
            "beta_t_r": dfrac(beta(t)),
        })

    # Illustrative exponent-only magnitudes; not bytes and not measured space.
    scaling = []
    for d in [6, 12, 24, 60]:
        n = Decimal(10) ** d
        half = n ** (Decimal(1) / Decimal(2))
        threshold = n ** (Decimal(23) / Decimal(45))
        scaling.append({
            "N": f"1e{d}",
            "N_to_half": str(half),
            "N_to_23_over_45": str(threshold),
            "ratio_N_to_1_over_90": str(threshold / half),
        })

    result = {
        "status": "conditional_arithmetic_only",
        "boundary_beta_equals_half": str(root_decimal()),
        "exact_boundary_polynomial": "c^3+c^2-c-2=0",
        "cases_t0_s0_equal_k": cases,
        "illustrative_scaling": scaling,
        "assertions": checks,
        "limitations": [
            "No SAT solver or contraction compiler was constructed.",
            "No FLMV machine execution or model conversion was performed.",
            "Numerical powers omit constants and polylogarithmic factors and are not bytes.",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
