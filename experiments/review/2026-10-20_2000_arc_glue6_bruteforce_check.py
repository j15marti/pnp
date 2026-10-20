#!/usr/bin/env python3
"""Independent brute-force check of the ARC_BOUNDARY_GLUE6 gadget claim.
Claim: left/right pin blocks are each satisfiable, and their conjunction is
satisfiable iff the b-bit vectors agree. Exhaustive SAT over all 5b variables.
Runtime: well under 30 s for b<=3 (chunked by b)."""
from itertools import product
import sys

def u(l, a, b):
    return [(l, sa*a, sb*b) for sa in (1, -1) for sb in (1, -1)]

def formula(vec, b, off):
    cls = []
    for i in range(b):
        cls += u(i+1 if (vec >> i) & 1 else -(i+1), off+2*i+1, off+2*i+2)
    return cls

def sat(cls, n):
    for m in range(1 << n):
        if all(any(((m >> (abs(x)-1)) & 1) == (x > 0) for x in c) for c in cls):
            return True
    return False

fails = 0; checks = 0
for b in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 3):
    n = 5*b
    for a, c in product(range(1 << b), repeat=2):
        L, R = formula(a, b, b), formula(c, b, 3*b)
        ok = sat(L, n) and sat(R, n) and (sat(L+R, n) == (a == c))
        checks += 1; fails += (not ok)
    print(f"b={b} pairs={4**b} cumulative_checks={checks} failures={fails}")
