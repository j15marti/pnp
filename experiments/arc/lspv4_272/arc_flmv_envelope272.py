#!/usr/bin/env python3
"""Exact FLMV 2005 Theorem 5.7 envelope, no finite-k truncation assumption."""
from fractions import Fraction
from math import isqrt

def envelope(c):
    assert isinstance(c, Fraction) and c > 1
    f = Fraction(1)
    best = Fraction(0)
    argmax = []
    rows = []
    for k in range(1, 100000):
        f = c * f / (1 + f)
        arithmetic = (1 / f - c) / k
        tail_cap = c ** (-k)
        d = min(arithmetic, tail_cap)
        rows.append((k, f, arithmetic, tail_cap, d))
        if d > best:
            best = d
            argmax = [k]
        elif d == best:
            argmax.append(k)
        # Each later index j>=k+1 obeys d_j(c) <= c^(-j) <= c^(-(k+1)).
        if best > 0 and c ** (-(k + 1)) < best:
            return best, argmax, rows, c ** (-(k + 1))
    raise RuntimeError("no certified positive envelope within limit")

def main():
    for c in (Fraction(6,5), Fraction(241,200), Fraction(7,5),
              Fraction(3,2), Fraction(8,5)):
        d, ks, rows, excluded_tail = envelope(c)
        print(f"c={c} d*={d} approximately {float(d):.12f}, maximizing k={ks}")
        print(f"explicit k 1..{rows[-1][0]}; tail bound={excluded_tail}, strict={excluded_tail < d}")
        for k, f, a, cap, val in rows:
            print(f"  k={k}: f={f}, arithmetic={a}, cap={cap}, d={val}")
    a = envelope(Fraction(6,5))[0]
    b = envelope(Fraction(241,200))[0]
    assert a == Fraction(23,45)
    assert b == Fraction(11642479,23232400)
    assert b - Fraction(1,2) == Fraction(26279,23232400)
    print("EXACT FLMV ASSERTIONS PASS")
if __name__ == "__main__":
    main()
