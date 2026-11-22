"""Verify packed selected-anchor semantics and cache ambiguity for finite controls."""
from itertools import product
from collections import defaultdict
from fractions import Fraction
import json


def formula(bits, index, complement):
    rows = []
    for j, bit in enumerate(bits):
        block = [(0,1,2)]*3 + [(0,3,4), (2 if bit else 1,3,4)]
        rows.extend(tuple(5*j+a for a in row) for row in block)
    u = 5*index + (2 if complement else 1)
    a, b, c = range(5*len(bits), 5*len(bits)+3)
    return rows + [(u,a,b), (u,b,c), (u,c,a)]


def audit():
    decisions = 0
    for k in (1, 2):
        for bits in product((0,1), repeat=k):
            for i in range(k):
                for c in (0,1):
                    masks = [sum(1 << x for x in r) for r in formula(bits,i,c)]
                    sat = any(all((a & m).bit_count() == 1 for m in masks)
                              for a in range(1 << (5*k+3)))
                    assert sat == (bits[i] ^ c)
                    decisions += 1
    results = {}
    for k in range(1, 9):
        rates = {}
        for label, cache in [('first', lambda x:x[0]), ('parity', lambda x:sum(x)%2)]:
            fibers = defaultdict(list)
            for x in product((0,1), repeat=k):
                fibers[cache(x)].append(x)
            ambiguous = sum(len(xs) for xs in fibers.values() for i in range(k)
                            if len({x[i] for x in xs})==2)
            rate = Fraction(ambiguous,k*2**k)
            assert rate >= Fraction(k-1,k)
            rates[label] = str(rate)
        results[k] = rates
    return dict(decisions=decisions, ambiguous_rates=results, seed=None,
                scope="semantic and cache-fiber checks, no native tape run")


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
