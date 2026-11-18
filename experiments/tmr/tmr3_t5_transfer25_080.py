#!/usr/bin/env python3
"""Independent exact 25-orbit and 125-state T5 K5-chain transfer solvers.

The graph consists of r complete K5 triple-sink atoms, each exposing a
three-hub interface; the next atom shares exactly those three hubs.
Each sink has its own T5 color, counted by the local factor w3.
"""
import itertools
import sys

D = range(5)
TRIPLES = tuple(itertools.combinations(range(5), 3))

def beats(a, z):
    return (z - a) % 5 in (1, 3)

def sink_count(a, b, c):
    return sum(beats(a, z) and beats(b, z) and beats(c, z) for z in D)

def atom_weight(a, b, c, d, e):
    colors = (a, b, c, d, e)
    result = 1
    for i, j, k in TRIPLES:
        result *= sink_count(colors[i], colors[j], colors[k])
        if not result:
            break
    return result

def count_orbits(r):
    """25-state quotient of the 125-state transfer under Z5 translation."""
    if not isinstance(r, int) or r < 0:
        raise ValueError('r must be a nonnegative integer')
    weights = {(a, b, d, e): atom_weight(a, b, 0, d, e)
               for a, b, d, e in itertools.product(D, repeat=4)}
    state = {(a, b): 1 for a, b in itertools.product(D, repeat=2)}
    for _ in range(r):
        state = {(d, e): sum(state[(b - a) % 5, (-a) % 5] * weights[a, b, d, e]
                             for a, b in itertools.product(D, repeat=2))
                 for d, e in itertools.product(D, repeat=2)}
    return 5 * sum(state.values())

def count_full(r):
    """Independent 125-state transfer recurrence, useful as an audit oracle."""
    if not isinstance(r, int) or r < 0:
        raise ValueError('r must be a nonnegative integer')
    state = {(a, b, c): 1 for a, b, c in itertools.product(D, repeat=3)}
    for _ in range(r):
        new = {}
        for c, d, e in itertools.product(D, repeat=3):
            new[c, d, e] = sum(state[a, b, c] * atom_weight(a, b, c, d, e)
                                for a, b in itertools.product(D, repeat=2))
        state = new
    return sum(state.values())

def selftest():
    expected = {0: 125, 1: 6120, 2: 5976840,
                10: 7258928966547540816707358627840}
    for r in (0, 1, 2, 3, 4, 5, 10, 20, 40, 80):
        x, y = count_orbits(r), count_full(r)
        assert x == y, (r, x, y)
        if r in expected:
            assert x == expected[r], (r, x)
    print('PASS 25-orbit and 125-state exact transfer, 10 chain lengths')

if __name__ == '__main__':
    selftest()
    if len(sys.argv) > 1:
        r = int(sys.argv[1]); print('r:', r, 'original T5 colorings:', count_orbits(r))
