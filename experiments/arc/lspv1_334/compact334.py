#!/usr/bin/env python3
"""Portable LSPV1-334 finite audit. Truth-table counts are OFFLINE checks."""
from itertools import combinations, product
from collections import defaultdict
from json import dumps

def edges(name):
    if name == 'K4':
        return list(combinations(range(4), 2)), 4
    E = [tuple(sorted((i, (i + 1) % 5))) for i in range(5)]
    E += [tuple(sorted((i, i + 5))) for i in range(5)]
    E += [tuple(sorted((i + 5, 5 + (i + 2) % 5))) for i in range(5)]
    assert len(set(E)) == 15
    return E, 10

def encode(E, h, odd):
    C, vertex_groups = [], []
    for v in range(h):
        inc = sorted(k + 1 for k, e in enumerate(E) if v in e)
        assert len(inc) == 3
        ids = []
        for a in product((0, 1), repeat=3):
            if sum(a) % 2 != (int(odd) if v == 0 else 0):
                ids.append(len(C) + 1)
                C.append(tuple(-x if b else x for x, b in zip(inc, a)))
        vertex_groups.append(ids)
    return C, vertex_groups

def evaluate(C, assignment):
    return all(any(((assignment >> (abs(lit) - 1)) & 1) == int(lit > 0)
                   for lit in clause) for clause in C)

def decode(C):
    B = defaultdict(list)
    for j, c in enumerate(C, 1):
        if len(c) != 3 or len({abs(v) for v in c}) != 3:
            return None
        key = tuple(sorted(abs(v) for v in c))
        B[key].append((j, c))
    rows = []
    for variables, entries in sorted(B.items()):
        if len(entries) != 4:
            return None
        forbidden = set()
        for _, c in entries:
            forbidden.add(sum((int(-x in c) << k) for k, x in enumerate(variables)))
        charge = next((b for b in (0, 1) if forbidden == {
            a for a in range(8) if (a.bit_count() % 2) != b}), None)
        if charge is None:
            return None
        rows.append((sum(1 << (x - 1) for x in variables), charge))
    return rows

def linear_unsat(rows):
    pivots = {}
    for mask, rhs in rows:
        while mask:
            p = (mask & -mask).bit_length() - 1
            if p not in pivots:
                pivots[p] = (mask, rhs)
                break
            mask ^= pivots[p][0]
            rhs ^= pivots[p][1]
        else:
            if rhs:
                return True
    return False

def run():
    out = {}
    for name in ('K4', 'Petersen'):
        E, h = edges(name)
        for odd in (False, True):
            C, ids = encode(E, h, odd)
            rows = decode(C)
            assert rows is not None and len(rows) == h
            assert len(C) == 4 * h
            n = len(E)
            models = sum(evaluate(C, z) for z in range(1 << n))
            assert (models == 0) == odd
            assert models == (0 if odd else 2 ** (n - h + 1))
            assert linear_unsat(rows) == odd
            for group in ids:
                for a in range(8):
                    vars_ = sorted({abs(l) for j in group for l in C[j - 1]})
                    z = sum(((a >> k) & 1) << (v - 1) for k, v in enumerate(vars_))
                    assert all(evaluate([C[j - 1]], z) for j in group) == (
                        a.bit_count() % 2 == (int(odd) if group == ids[0] else 0))
            assert sum(mask for mask, _ in rows) % 2 == 0
            assert all((sum(mask >> k & 1 for mask, _ in rows) == 2) for k in range(n))
            key = name + ('_UNSAT' if odd else '_SAT')
            out[key] = {'variables': n, 'clauses': len(C), 'models': models,
                        'parity_refutation_nodes': 2 * h if odd else None}
    print(dumps(out, indent=2))

if __name__ == '__main__':
    run()
