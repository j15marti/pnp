#!/usr/bin/env python3
"""Compact GATE289 exact M22 n=6 certificate. Standard library, no oracle."""
from itertools import combinations, product
from collections import Counter

triples = list(combinations(range(1, 7), 3))
patterns = [q for q in combinations(triples, 4)
            if all(sum(i in c for c in q) == 2 for i in range(1, 7))]
assert len(patterns) == 75

def fail(c, a):
    return not any(a[abs(v)-1] == (v > 0) for v in c)

def violations(f, a):
    return sum(fail(c, a) for c in f)

def conditional8(f, p):
    total = 0
    for c in f:
        if any(abs(v) in p and p[abs(v)] == (v > 0) for v in c):
            continue
        free = sum(abs(v) not in p for v in c)
        total += 1 << (3 - free)
    return total

def certificate(f):
    a, b = f[0][0], f[0][1]
    assert a > 0 and b > 0
    p = {a: 0, b: 1}
    v = conditional8(f, p)
    assert v < 8
    for i in range(1, 7):
        if i in p:
            continue
        t = []
        for bit in (0, 1):
            q = dict(p); q[i] = bit
            t.append((conditional8(f, q), q))
        assert sum(x[0] for x in t) == 2 * v
        v, p = min(t, key=lambda x: x[0])
    a = [p[i] for i in range(1, 7)]
    assert violations(f, a) == 0
    return a

hist = Counter()
for P in patterns:
    for N in patterns:
        f = [tuple(c) for c in P] + [tuple(-v for v in c) for c in N]
        witness = certificate(f)
        count = sum(violations(f, a) == 0 for a in product((0, 1), repeat=6))
        assert count >= 1 and violations(f, witness) == 0
        hist[count] += 1
assert sum(hist.values()) == 5625
assert sum(k * v for k, v in hist.items()) == 119250
print("PASS all 5625 complete valid n=6 sources, witness histogram", dict(sorted(hist.items())))
