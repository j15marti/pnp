#!/usr/bin/env python3
"""Exact finite audit of support recognition and Tutte incidence reduction.

Standard library only. The matching counter below is exponential and is an
independent small-instance oracle, NOT the polynomial Edmonds implementation.
Run from repo root; emits immutable JSON evidence to stdout.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, product
import hashlib
import json
from pathlib import Path


def source(q, edges, demands):
    incidence = [[] for _ in range(q)]
    for i, (u, v) in enumerate(edges, 1):
        assert u != v
        incidence[u].append(i)
        incidence[v].append(i)
    assert all(len(row) == 3 for row in incidence)
    assert len(set(map(tuple, incidence))) == q
    return [tuple(x if bit == 0 else -x for x, bit in zip(row, bits))
            for row, b in zip(incidence, demands)
            for bits in product((0, 1), repeat=3) if sum(bits) != b]


def recognise(clauses):
    groups = defaultdict(list)
    for clause in clauses:
        if len(clause) != 3 or 0 in clause:
            return None
        scope = tuple(sorted(map(abs, clause)))
        if len(set(scope)) != 3:
            return None
        groups[scope].append(clause)
    scopes = sorted(groups)
    demands = []
    occ = defaultdict(list)
    for v, scope in enumerate(scopes):
        table = set()
        for bits in product((0, 1), repeat=3):
            a = dict(zip(scope, bits))
            if all(any(a[abs(z)] == int(z > 0) for z in row)
                   for row in groups[scope]):
                table.add(bits)
        matches = [b for b in (1, 2) if table ==
                   {bits for bits in product((0, 1), repeat=3)
                    if sum(bits) == b}]
        if len(matches) != 1:
            return None
        demands.append(matches[0])
        for x in scope:
            occ[x].append(v)
    if not scopes or any(len(vs) != 2 for vs in occ.values()):
        return None
    return len(scopes), [tuple(occ[x]) for x in sorted(occ)], demands


def gadget(q, edges, demands):
    ports = [[] for _ in range(q)]
    pairs = []
    for i, (u, v) in enumerate(edges):
        ports[u].append(2*i)
        ports[v].append(2*i+1)
        pairs.append((2*i, 2*i+1))
    n = 2*len(edges)
    for v in range(q):
        for _ in range(3-demands[v]):
            pairs.extend((n, p) for p in ports[v])
            n += 1
    assert n == 6*q-sum(demands)
    assert len(pairs) == len(edges)+3*sum(3-b for b in demands)
    return n, pairs


def perfect_matching_count(n, edges):
    adj = [0]*n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    @lru_cache(None)
    def visit(mask):
        if not mask:
            return 1
        if mask.bit_count() % 2:
            return 0
        vertices = [v for v in range(n) if mask >> v & 1]
        u = min(vertices, key=lambda v: (adj[v] & mask).bit_count())
        rest = mask ^ (1 << u)
        nbrs = adj[u] & rest
        total = 0
        while nbrs:
            bit = nbrs & -nbrs
            nbrs -= bit
            total += visit(rest ^ bit)
        return total
    answer = visit((1 << n)-1)
    return answer, visit.cache_info().currsize


def degree_counts(q, edges):
    counts = Counter()
    for mask in range(1 << len(edges)):
        degrees = [0]*q
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                degrees[u] += 1
                degrees[v] += 1
        counts[tuple(degrees)] += 1
    return counts


def encoding(c, d):
    r = c+1 if c % 2 == 0 else c+2
    r = max(3, r)
    n0 = d+(10*c+1)*r+2
    m0 = (20*c+4)*r
    n, m = n0+m0+3, 2*m0+4
    w = n.bit_length()
    N = 3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w
    return dict(c=c, d=d, r=r, n=n, m=m, w=w, N=N)


def run():
    k4 = list(combinations(range(4), 2))
    prism = [(i, (i+1)%3) for i in range(3)]
    prism += [(3+i, 3+(i+1)%3) for i in range(3)]
    prism += [(i, i+3) for i in range(3)]
    parallel = [(0,1), (0,1), (2,3), (2,3), (0,2), (1,3)]
    k33 = [(i,j) for i in range(3) for j in range(3,6)]
    cases = []
    for name, q, edges in [('K4',4,k4), ('prism',6,prism),
                           ('parallel',4,parallel), ('K33',6,k33)]:
        counts = degree_counts(q, edges)
        for b in product((1,2), repeat=q):
            F = source(q, edges, b)
            rec = recognise(F)
            assert rec is not None
            nn, hh = gadget(*rec)
            pms, states = perfect_matching_count(nn, hh)
            expected = counts[b]
            assert pms == expected*(2**b.count(1))
            # Exact recognition survives clause reversal, literal permutation,
            # duplicates, and a bijective variable relabeling.
            names = len(edges)
            changed = [tuple((1 if z>0 else -1)*(names+1-abs(z))
                             for z in reversed(row)) for row in reversed(F)]
            changed.append(changed[0])
            assert recognise(changed) is not None
            bad = F+[tuple(-z for z in F[0])]
            # A mutation need not fail, so compare its admitted semantics.
            if (rr := recognise(bad)) is not None:
                n2, h2 = gadget(*rr)
                answer2, _ = perfect_matching_count(n2,h2)
                brute2 = sum(all(any(((mask>>(abs(z)-1))&1)==int(z>0)
                                    for z in row) for row in bad)
                             for mask in range(1 << names))
                assert bool(answer2) == bool(brute2)
            cases.append(dict(graph=name, demands=b, source_models=expected,
                              matching_models=pms, matching_vertices=nn,
                              matching_edges=len(hh), oracle_states=states))
    # Connected cubic graph with a bridge, built from two subdivided K4s.
    half = [e for e in k4 if e != (0,1)]+[(0,4),(1,4)]
    bridge = half+[(u+5,v+5) for u,v in half]+[(4,9)]
    counts = degree_counts(10,bridge)
    even_unsat = next((b for b in product((1,2),repeat=10)
                       if sum(b)%2==0 and counts[b]==0), None)
    bridge_check = {'even_sum_unsat_demands':even_unsat}
    if even_unsat is not None:
        F=source(10,bridge,even_unsat)
        nn, hh=gadget(*recognise(F))
        pms, states=perfect_matching_count(nn,hh)
        assert pms==0
        bridge_check.update(edges=bridge, matching_vertices=nn,
                            oracle_states=states, label='UNSAT')
    assert recognise([(1,2,3)]) is None
    assert recognise([(1,1,2)]) is None
    assert recognise(source(4,k4,(1,1,1,1))[:-1]) is None
    return dict(target='DYNAMIC-DEGREE-FACTOR-ADMISSION1',
                source_revision='98bad277e88aa3c096c4f857dc4323fb910e398a',
                mode='exhaustive deterministic; no seed',
                cases=cases, case_count=len(cases),
                sat=sum(c['source_models']>0 for c in cases),
                unsat=sum(c['source_models']==0 for c in cases),
                bridge_control=bridge_check,
                K4_encoding=encoding(20,6),
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                limitations='Finite exponential oracle, not TM timing or a blossom implementation; no compiled-input SAT rerun.')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
