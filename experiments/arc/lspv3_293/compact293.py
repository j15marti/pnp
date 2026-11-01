#!/usr/bin/env python3
"""GATE293 compact, exact-integer audit. Python 3.10+; no dependencies.
The full 240-source producer and independent verifier are in the archive.
"""
from collections import Counter
from itertools import combinations
from math import comb
from random import Random
import json


def source(n, rng):
    def side():
        for _ in range(30000):
            slots = list(range(1, n + 1)) * 2
            rng.shuffle(slots)
            t = [tuple(sorted(slots[j:j + 3])) for j in range(0, 2*n, 3)]
            if len(set(t)) == len(t) and all(len(set(c)) == 3 for c in t):
                return t
        raise RuntimeError('failed to generate regular 3-uniform hypergraph')
    pos, neg = side(), side()
    f = [tuple(x for x in t) for t in pos] + [tuple(-x for x in t) for t in neg]
    ct = Counter(l for c in f for l in c)
    assert len(f) == 4*n//3 and len(set(f)) == len(f)
    assert all(ct[i] == ct[-i] == 2 for i in range(1, n+1))
    return f


def violations(f, mask):
    return sum(all(((mask >> (abs(l)-1)) & 1) != (l > 0) for l in c) for c in f)


def audit(f, n=9):
    hist = {k: Counter() for k in (4, 5)}
    for x in range(1 << n):
        if x.bit_count() in (4, 5):
            hist[x.bit_count()][violations(f, x)] += 1
    p = [set(c) for c in f if c[0] > 0]
    a1 = sum(len(x & y) == 1 for x, y in combinations(p, 2))
    a2 = sum(len(x & y) == 2 for x, y in combinations(p, 2))
    assert a1 + 2*a2 == n
    assert all(sum(v*freq for v, freq in hist[k].items()) == comb(n, k)
               for k in (4, 5))
    assert hist[4][0] >= 6 + 2*a2 and hist[5][0] >= 6
    return {'weight4_models': hist[4][0], 'weight5_models': hist[5][0],
            'positive_pair_intersections_one': a1,
            'positive_pair_intersections_two': a2,
            'proved_weight4_lower_bound': 6 + 2*a2}


def main():
    rng = Random(202611010024)
    res = [audit(source(9, rng)) for _ in range(240)]
    print(json.dumps({'target': 'proper duplicate-free monotone 3-SAT-(2,2)',
                      'n': 9, 'samples': len(res), 'seed': 202611010024,
                      'minimum_weight4_models': min(x['weight4_models'] for x in res),
                      'minimum_weight5_models': min(x['weight5_models'] for x in res),
                      'total_weight4_models': sum(x['weight4_models'] for x in res),
                      'total_weight5_models': sum(x['weight5_models'] for x in res),
                      'claim': 'Every valid nine-variable target has >=6 models at each of weights 4 and 5',
                      'status': 'restricted exact theorem; P versus NP OPEN'}, sort_keys=True))


if __name__ == '__main__':
    main()
