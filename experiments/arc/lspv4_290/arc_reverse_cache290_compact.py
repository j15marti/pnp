#!/usr/bin/env python3
"""ARC-REVERSE-CACHE290 public compact exact arithmetic/stream audit.
Full independent original SAT/UNSAT certificates, producer and raw output
are in ARC_REVERSE_CACHE290_FULL_REPRO.zip; this checker does not claim
native FLMV timing or a general SAT lower bound.
"""
from fractions import Fraction as F

def lower(m, b):
    assert m > b >= 0
    half = m // 2
    return half * ((half + b) // (b + 1))

def grouped(m, b):
    assert m > b >= 0
    h = (m + b) // (b + 1)
    return h * m - (b + 1) * h * (h - 1) // 2

def bitwrites(m):
    """Index one-bits prepared for separate indexed reads at all 0..m-1."""
    return sum(i.bit_count() for i in range(m))

def flmv(c):
    f, vals = F(1), []
    for k in range(1, 5):
        f = c * f / (1 + f)
        vals.append(min((1 / f - c) / k, c ** (-k)))
    best = max(vals[:3])
    assert c ** (-4) < best
    assert vals.index(best) == 1
    return best, vals

def check():
    expected = {
        133: {0: 8911, 1: 4489, 4: 1836, 16: 588, 64: 204, 132: 133},
        7948: {0: 31589326, 1: 15796650, 4: 6321045,
               16: 1861938, 64: 489909, 256: 126883},
    }
    n = 0
    for m, cases in expected.items():
        for b, target in cases.items():
            assert grouped(m, b) == target
            assert grouped(m, b) >= lower(m, b)
            n += 2
    assert flmv(F(6, 5))[0] == F(23, 45)
    assert flmv(F(241, 200))[0] == F(11642479, 23232400)
    assert bitwrites(8) == 12
    assert grouped(7948, 0) == 7948 * 7949 // 2
    n += 4
    print("PASS", n, "compact exact checks")
    print("7948-bit indexed-address one-bits:", bitwrites(7948))
    print("Native complete physical FLMV tape XOR NOT MEASURED")
    print("P versus NP OPEN")

if __name__ == "__main__":
    check()
