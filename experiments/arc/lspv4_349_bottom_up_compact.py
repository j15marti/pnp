#!/usr/bin/env python3
"""Python 3 standard library only. Run: python lspv4_349_bottom_up_compact.py out.json
Exact census and ordinary-resolution minima. The full producer, independent
JavaScript verifier, growth certificates, malformed-input tests and resource
ledgers are in the accompanying BOTTOM_UP_SPLIT_VS_OVERLAP349 run archive.
Sources cost zero; each distinct derived resolvent costs one; reuse is free.
"""
from itertools import product, permutations
from collections import defaultdict
import json
import sys

clauses = []
for states in product((0, 1, -1), repeat=3):
    C = tuple((i+1)*s for i, s in enumerate(states) if s)
    if C:
        clauses.append(C)
clauses.sort(key=lambda C: (len(C), C))
covers = []
for C in clauses:
    mask = 0
    for a in range(8):
        if all(bool(a & (1 << (abs(l)-1))) != (l > 0) for l in C):
            mask |= 1 << a
    covers.append(mask)
seen_build = set()
minimal = set()

def build(ids, covered):
    key = sum(1 << i for i in ids)
    if key in seen_build:
        return
    seen_build.add(key)
    if covered == 255:
        minimal.add(tuple(sorted(ids)))
        return
    remaining = (~covered) & 255
    bit = remaining & -remaining
    for i, c in enumerate(covers):
        if not c & bit:
            continue
        new = ids + (i,)
        valid = True
        for j in new:
            other = 0
            for k in new:
                if k != j:
                    other |= covers[k]
            if not covers[j] & ~other:
                valid = False
                break
        if valid:
            build(new, covered | c)

build((), 0)
lookup = {frozenset(c): i for i, c in enumerate(clauses)}
transforms = []
for p in permutations(range(1, 4)):
    for sg in product((1, -1), repeat=3):
        transforms.append([lookup[frozenset(
            (1 if l > 0 else -1)*p[abs(l)-1]*sg[abs(l)-1] for l in C
        )] for C in clauses])
orbits = defaultdict(list)
for ids in minimal:
    key = min(tuple(sorted(tr[i] for i in ids)) for tr in transforms)
    orbits[key].append(ids)

universe = [frozenset()] + [frozenset(c) for c in clauses]
index = {c: i for i, c in enumerate(universe)}
rules = []
for i, A in enumerate(universe):
    for j in range(i+1, len(universe)):
        B = universe[j]
        opposite = [l for l in A if -l in B]
        if len(opposite) != 1:
            continue
        p = opposite[0]
        R = (A - {p}) | (B - {-p})
        rules.append((i, j, abs(p), index[R]))

def shortest(ids):
    initial = sum(1 << (i+1) for i in ids)
    level = {initial}
    seen = {initial}
    parents = {}
    layers = [1]
    for depth in range(1, 28):
        next_level = set()
        for state in sorted(level):
            for a, b, pivot, r in rules:
                if not ((state >> a) & 1 and (state >> b) & 1):
                    continue
                if (state >> r) & 1:
                    continue
                out = state | (1 << r)
                if out in seen:
                    continue
                parents[out] = (state, a, b, pivot, r)
                if r == 0:
                    path = []
                    while out != initial:
                        old, a, b, pivot, r = parents[out]
                        path.append({'left': sorted(universe[a]),
                                     'right': sorted(universe[b]),
                                     'pivot': pivot,
                                     'resolvent': sorted(universe[r])})
                        out = old
                    return depth, list(reversed(path)), layers
                seen.add(out)
                next_level.add(out)
        level = next_level
        layers.append(len(level))
        if not level:
            raise RuntimeError('UNSAT input unexpectedly lacks a refutation')
    raise RuntimeError('finite clause universe exhausted')

rows = []
for ids, members in sorted(orbits.items(), key=lambda kv: (len(kv[0]), kv[0])):
    cost, proof, layers = shortest(ids)
    rows.append({'formula': [clauses[i] for i in ids], 'm': len(ids),
                 'orbit_size': len(members), 'minimum_resolution': cost,
                 'minimum_mix341_by_AND3_and_source_arity': len(ids)-1,
                 'proof': proof, 'completed_shorter_layers': layers})
assert len(minimal) == 869
assert len(rows) == 43
assert sum(r['orbit_size'] for r in rows if r['minimum_resolution'] > r['m']-1) == 8
result = {'minimal_unsat_count': len(minimal), 'symmetry_classes': len(rows),
          'empty_clause_singleton': {'minimum': 0, 'excluded_from_census': True},
          'rows': rows,
          'limits': 'No superpolynomial mixed lower bound, B3 bridge, or machine-time lower bound.'}
path = sys.argv[1] if len(sys.argv) > 1 else 'bottom_up349_compact_results.json'
with open(path, 'w', encoding='utf8') as f:
    json.dump(result, f, indent=2)
print(json.dumps({'minimal_unsat_count': len(minimal), 'classes': len(rows),
                  'output': path}, indent=2))
