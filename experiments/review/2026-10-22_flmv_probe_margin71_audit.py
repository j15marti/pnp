#!/usr/bin/env python3
"""Exact/finite audit for FLMV-PROBE-MARGIN71."""

from fractions import Fraction
from math import ceil, log2
import random


def d(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def iterate(c0: Fraction, s0: Fraction, base: Fraction, steps: int):
    c, s = c0, s0
    for _ in range(steps):
        c = max(base, Fraction(3, 5) + c / 2)
        s = max(Fraction(1, 2), s / 2)
    return c, s


def first_entry(c0: Fraction, s0: Fraction, base: Fraction, safe: Fraction):
    c, s = c0, s0
    for j in range(10_000):
        if c <= safe and s <= Fraction(1, 2):
            return j, c, s
        c = max(base, Fraction(3, 5) + c / 2)
        s = max(Fraction(1, 2), s / 2)
    raise AssertionError("no finite entry")


def bisect_root(iterations=200):
    lo, hi = 1.2, 1.21
    for _ in range(iterations):
        mid = (lo + hi) / 2
        poly = mid**3 + mid**2 - mid - 2
        if poly < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    c_limit = Fraction(6, 5)
    c_safe = Fraction(241, 200)
    eta_safe = Fraction(121, 200)
    b_safe = Fraction(79, 200)
    rho_safe = Fraction(41, 200)

    assert d(c_limit) == Fraction(23, 45)
    assert d(c_limit) - Fraction(1, 2) == Fraction(1, 90)
    assert d(c_safe) == Fraction(11642479, 23232400)
    assert d(c_safe) - Fraction(1, 2) == Fraction(26279, 23232400)
    assert Fraction(3, 5) + eta_safe == c_safe
    assert 1 + Fraction(3, 5) - b_safe == c_safe
    assert 1 + rho_safe == c_safe

    root = bisect_root()
    assert abs(root - 1.2055694304005902) < 1e-14
    assert abs((root - 0.6) - 0.6055694304005902) < 1e-14

    checks = 9
    rng = random.Random(71)
    for _ in range(100_000):
        c0 = Fraction(rng.randrange(0, 40001), 1000)
        s0 = Fraction(rng.randrange(0, 40001), 1000)
        base = Fraction(rng.randrange(1100, 1206), 1000)
        if base > c_safe:
            base = c_safe
        j, c, s = first_entry(c0, s0, base, c_safe)
        assert c <= c_safe and s <= Fraction(1, 2)
        assert d(c) >= d(c_safe) > Fraction(1, 2)
        c2, s2 = iterate(c0, s0, base, j)
        assert (c2, s2) == (c, s)
        checks += 4

    print({
        "checks": checks,
        "failures": 0,
        "d_6_5": str(d(c_limit)),
        "margin_6_5": str(d(c_limit) - Fraction(1, 2)),
        "d_241_200": str(d(c_safe)),
        "margin_241_200": str(d(c_safe) - Fraction(1, 2)),
        "root_d_eq_half": root,
        "eta_root": root - 0.6,
        "eta_safe": str(eta_safe),
        "b_safe": str(b_safe),
        "rho_safe": str(rho_safe),
    })


if __name__ == "__main__":
    main()
