#!/usr/bin/env python3
"""Exact minimum DAG-Resolution refutation length for proper (n-1)-CNF MUS on n variables.

Correspondence (PROVED in report): a width-(n-1) clause on n variables omits one variable y
and is falsified by exactly the two assignments differing in y, i.e. it is an EDGE of Q_n.
A set of such clauses is UNSAT iff its edges cover all 2^n vertices; it is minimally UNSAT
iff the edge cover is minimal (every component is a star).

Clause encoding: (pos_mask, neg_mask). Resolution length = number of resolution inferences
(distinct derived clauses), weakening allowed (it never shortens minimum DAG length).
Exact search: f(P) over antichains P of pending requirement clauses (a requirement r is met by
any axiom or earlier-derived clause c with c subset of r). Each step chooses the clause e placed
latest among not-yet-placed proof lines; see report for the exactness argument.
Usage: qcube_min_resolution.py N [chunk_index chunk_count]
"""
import sys, json, itertools, time
from functools import lru_cache

def subset(a, b):  # clause a subset of clause b
    return (a[0] & ~b[0]) == 0 and (a[1] & ~b[1]) == 0

def minimal_covers(n):
    V = 1 << n
    edges = [(v, v ^ (1 << i)) for v in range(V) for i in range(n) if v < v ^ (1 << i)]
    # enumerate partitions of vertices into stars (>=2 vertices) -> minimal edge covers
    res = []
    def rec(uncov, chosen):
        if not uncov:
            res.append(frozenset(chosen)); return
        v = min(uncov)
        # v is a leaf of a star centred at neighbour c, or v is a centre with leaves L
        nb = [v ^ (1 << i) for i in range(n)]
        # option A: v centre with nonempty leaf set L subset of uncovered nbrs
        un = [u for u in nb if u in uncov]
        for k in range(1, len(un) + 1):
            for L in itertools.combinations(un, k):
                if k == 1:
                    # star of size 2: centre ambiguity; canonical: v (smaller) is centre
                    pass
                rec(uncov - {v} - set(L), chosen + [tuple(sorted((v, u))) for u in L])
        # option B: v leaf of a star centred at c with >=2 leaves, c uncovered, others leaves > v
        for c in un:
            others = [u for u in (c ^ (1 << i) for i in range(n)) if u != v and u in uncov and u > v]
            for k in range(1, len(others) + 1):
                for L in itertools.combinations(others, k):
                    rec(uncov - {v, c} - set(L), chosen + [tuple(sorted((c, u))) for u in (v,) + L])
    rec(frozenset(range(V)), [])
    return list(set(res))

def edge_to_clause(e, n):
    a, b = e
    y = (a ^ b).bit_length() - 1
    pos = neg = 0
    for i in range(n):
        if i == y: continue
        if (a >> i) & 1: neg |= 1 << i   # clause falsified when x_i = a_i
        else: pos |= 1 << i
    return (pos, neg)

def automorphisms(n):
    out = []
    for perm in itertools.permutations(range(n)):
        for flip in range(1 << n):
            def f(v, perm=perm, flip=flip):
                w = 0
                for i in range(n):
                    if (v >> i) & 1: w |= 1 << perm[i]
                return w ^ flip
            out.append(f)
    return out

def canon(cover, autos):
    return min(tuple(sorted(tuple(sorted((f(a), f(b)))) for a, b in cover)) for f in autos)

def min_refutation(axioms, n, budget=64):
    ax = list(axioms)
    allc = [(p, q) for p in range(1 << n) for q in range(1 << n) if p & q == 0]
    def covered(r):
        return any(subset(a, r) for a in ax)
    def antichain(S):
        S = set(S)
        return frozenset(r for r in S if not any(s != r and subset(s, r) for s in S))
    fail = {}
    def cands_of(P):
        cands = set()
        for r in P:
            pm, nm = r
            bits = [(0, i) for i in range(n) if pm >> i & 1] + [(1, i) for i in range(n) if nm >> i & 1]
            for k in range(len(bits) + 1):
                for sub in itertools.combinations(bits, k):
                    p = sum(1 << i for s, i in sub if s == 0); q = sum(1 << i for s, i in sub if s == 1)
                    cands.add((p, q))
        return cands
    L = len(ax)
    def users(r):
        return frozenset(i for i, a in enumerate(ax) if subset(a, r))
    def g(P, U, d):
        # True iff pending antichain P can be discharged with <= d further resolution lines.
        # U = axioms not yet used.  Admissible bound (report Lemma 3): need >= |U| - |P| new lines,
        # and >= 1 line if P is nonempty.
        if not P: return not U
        lb = max(1, len(U) - len(P))
        if d < lb: return False
        key = (P, U)
        if fail.get(key, -1) >= d: return False
        for e in cands_of(P):
            if covered(e):
                continue
            rest = [r for r in P if not subset(e, r)]
            used = e[0] | e[1]
            for x in range(n):
                if used >> x & 1: continue
                new = [(e[0] | 1 << x, e[1]), (e[0], e[1] | 1 << x)]
                U2 = U
                keep = []
                for r in new:
                    if covered(r): U2 = U2 - users(r)
                    else: keep.append(r)
                if g(antichain(rest + keep), U2, d - 1):
                    return True
        fail[key] = max(fail.get(key, -1), d)
        return False
    start0 = frozenset([(0, 0)])
    for d in range(max(1, len(ax) - 1), budget + 1):  # I >= L-1 for any DAG refutation using all L axioms of an MUS
        if g(start0, frozenset(range(L)), d):
            return d
    return None


def main():
    n = int(sys.argv[1]); ci = int(sys.argv[2]) if len(sys.argv) > 2 else 0; cc = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    t0 = time.time()
    autos = automorphisms(n)
    vmaps = [[f(v) for v in range(1 << n)] for f in autos]
    covers = minimal_covers(n)
    seen = set(); classes = {}
    for c in covers:
        if c in seen: continue
        orbit = {frozenset(tuple(sorted((m[a], m[b]))) for a, b in c) for m in vmaps}
        seen |= orbit
        classes[min(tuple(sorted(o)) for o in orbit)] = len(orbit)
    assert sum(classes.values()) == len(covers)
    keys = sorted(classes, key=lambda k: (len(k), k))
    rows = []
    for idx, k in enumerate(keys):
        if idx % cc != ci: continue
        clauses = [edge_to_clause(e, n) for e in k]
        w = min_refutation(clauses, n)
        stars = len({v for e in k for v in e}) and None
        rows.append({"class": idx, "orbit_size": classes[k], "mu": len(k), "W_res": w, "edges": [list(e) for e in k]})
    out = {"n": n, "num_minimal_covers": len(covers), "num_classes": len(keys), "chunk": [ci, cc],
           "rows": rows, "seconds": round(time.time() - t0, 2)}
    print(json.dumps(out))

if __name__ == "__main__":
    main()
