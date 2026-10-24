#!/usr/bin/env python3
"""BLOCK-CLOSED-ORACLE85 compact independent standard-library auditor."""
from itertools import product

def edge(q, i, b):
    a, c = i + 1, ((i + 1) % q) + 1
    return ((-a, c), (a, -c)) if not b else ((a, c), (-a, -c))

def cnf(q, bs):
    f = []
    for i, b in enumerate(bs):
        for j, (a, c) in enumerate(edge(q, i, b)):
            u = q + 2*i + j + 1
            f += [(a, c, u), (a, c, -u)]
    return f

def count(q, f):
    ans = 0
    for a in range(1 << (3*q)):
        if all(any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in C) for C in f):
            ans += 1
    return ans

def xpaths(q, bs, mask):
    return sum(
        all(( ((x >> i) & 1) ^ ((x >> ((i+1) % q)) & 1) ) == bs[i]
            for i in range(q) if (mask >> i) & 1)
        for x in range(1 << q)
    )

tests = 0
for q in range(3, 7):
    for bs in product((0, 1), repeat=q):
        f = cnf(q, bs)
        parity = sum(bs) % 2
        assert len(f) == 4*q and len(set(f)) == 4*q
        tests += 1
        if q <= 4:
            assert count(q, f) == ((1 << (2*q+1)) if not parity else 0)
            tests += 1
        for mask in range(1, (1 << q)-1):
            assert xpaths(q, bs, mask) == 1 << (q - mask.bit_count())
            tests += 1
        if q <= 4:
            for miss in range(q):
                sub = [f[4*i+j] for i in range(q) if i != miss for j in range(4)]
                sub += f[4*miss:4*miss+2]
                assert count(q, sub) == ((1 << (2*q+1)) if not parity else (1 << (2*q)))
                tests += 1
print({"assertions": tests, "failures": 0})
