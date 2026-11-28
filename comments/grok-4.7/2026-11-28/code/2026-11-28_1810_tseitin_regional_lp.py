#!/usr/bin/env python3
"""EB-REGLP-T1: exact feasibility certificates for the C04-36 blind regional
transfer LP on Tseitin (odd-charge) formulas over random cubic graphs.

For each instance:
  * graph G: random simple connected 3-regular graph (networkx, fixed seed);
  * Tseitin system: vertex v has x_e1+x_e2+x_e3 = c_v (mod 2), sum c = 1 (UNSAT);
    CNF companion = 4 width-3 clauses per vertex (same exact factor supports);
  * blind C04-36 cover: every factor scope, plus union of every overlapping
    pair of factor scopes with |union| <= 5 (deduplicated);
  * R_U = words on U satisfying every vertex factor whose scope is inside U;
  * construction: for region U pick reference vertex r(U) at maximal BFS
    distance from U, and let p_U = marginal on U of the uniform distribution on
    the solutions of all vertex equations except r(U);
  * exact checks (Fractions): sum p_U = 1, p_U >= 0, support(p_U) subset R_U,
    and for every pair of regions with nonempty intersection T the two
    marginals on T coincide (this implies all C04-36 subset equalities);
  * GF(2) check that the full system is inconsistent (sum of rows: 0 = 1);
  * condition check of Lemma: B(U) != V computed by enumerating all cuts D
    inside U (2^|U| subsets) and their small sides.
Optionally (--lp) also builds the LP explicitly and solves it with HiGHS as a
floating cross-check (not part of the exact certificate).
"""
import sys, json, random, itertools, hashlib, argparse
from fractions import Fraction
from collections import defaultdict, deque
import networkx as nx

def gf2_solve(rows, rhs, nvar):
    """rows: list of int bitmasks; returns (consistent, x0, nullbasis)."""
    piv = {}  # pivot col -> (row, rhs)
    order = []
    for r, b in zip(rows, rhs):
        for c, (pr, pb) in piv.items():
            if r >> c & 1:
                r ^= pr; b ^= pb
        if r == 0:
            if b: return False, None, None
            continue
        c = r.bit_length() - 1
        # reduce existing pivots by new row
        for c2 in list(piv):
            pr, pb = piv[c2]
            if pr >> c & 1:
                piv[c2] = (pr ^ r, pb ^ b)
        piv[c] = (r, b)
    x0 = 0
    for c, (r, b) in piv.items():
        if b: x0 |= 1 << c
    free = [c for c in range(nvar) if c not in piv]
    basis = []
    for f in free:
        v = 1 << f
        for c, (r, b) in piv.items():
            if r >> f & 1: v |= 1 << c
        basis.append(v)
    return True, x0, basis

def build(n, seed):
    g = nx.random_regular_graph(3, n, seed=seed)
    tries = 0
    while not nx.is_connected(g):
        tries += 1; g = nx.random_regular_graph(3, n, seed=seed + 1000 * tries)
    edges = sorted(tuple(sorted(e)) for e in g.edges())
    eid = {e: i for i, e in enumerate(edges)}
    inc = {v: sorted(eid[tuple(sorted((v, u)))] for u in g[v]) for v in g}
    charge = {v: 0 for v in g}; charge[0] = 1
    return g, edges, eid, inc, charge

def cover(inc):
    scopes = sorted({tuple(s) for s in inc.values()})
    regs = set(scopes)
    for a, b in itertools.combinations(scopes, 2):
        if set(a) & set(b):
            u = tuple(sorted(set(a) | set(b)))
            if len(u) <= 5: regs.add(u)
    return sorted(regs, key=lambda r: (len(r), r))


def bset(g, edge_end, U, n):
    """B(U) = union of sides W with |W|<=n/2, W nonempty, delta(W) subset U."""
    Bs = set()
    for k in range(1, len(U) + 1):
        for D in itertools.combinations(U, k):
            H = g.copy(); H.remove_edges_from(edge_end[e] for e in D)
            comps = list(nx.connected_components(H))
            cid = {x: i for i, c in enumerate(comps) for x in c}
            col = {0: 0}; Q = deque([0]); adj = defaultdict(list); okb = True
            for e in D:
                a, b = (cid[x] for x in edge_end[e])
                if a == b: okb = False; break
                adj[a].append(b); adj[b].append(a)
            if not okb: continue
            while Q:
                a = Q.popleft()
                for b in adj[a]:
                    if b not in col: col[b] = 1 - col[a]; Q.append(b)
                    elif col[b] == col[a]: okb = False
            if not okb or len(col) != len(comps): continue
            W = set().union(*(comps[i] for i in col if col[i] == 0))
            Wc = set(g) - W
            # verify delta(W) == D exactly
            dW = {i for i, (x, y) in edge_end.items() if (x in W) != (y in W)}
            assert dW == set(D)
            if len(W) <= n / 2: Bs |= W
            if len(Wc) <= n / 2: Bs |= Wc
    return Bs

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--sizes', default='8,12,16,24,32,48,64,96,128,200')
    ap.add_argument('--seeds', type=int, default=3); ap.add_argument('--lp', action='store_true')
    a = ap.parse_args()
    out = []
    for n in map(int, a.sizes.split(',')):
        for s in range(a.seeds):
            seed = 271128 + 97 * n + s
            g, edges, eid, inc, charge = build(n, seed)
            m = len(edges)
            V = sorted(g)
            rowmask = {v: sum(1 << e for e in inc[v]) for v in V}
            # global inconsistency (GF2): sum of all rows is 0, rhs 1
            ok, _, _ = gf2_solve([rowmask[v] for v in V], [charge[v] for v in V], m)
            assert not ok
            regs = cover(inc)
            dist_cache = {}
            # per-reference solution spaces
            sol = {}
            def space(r):
                if r not in sol:
                    vs = [v for v in V if v != r]
                    ok, x0, B = gf2_solve([rowmask[v] for v in vs], [charge[v] for v in vs], m)
                    assert ok
                    sol[r] = (x0, B)
                return sol[r]
            edge_end = {i: e for i, e in enumerate(edges)}
            P = {}
            refs = {}
            Bsets = {U: bset(g, edge_end, U, n) for U in regs}
            for U in regs:
                ends = {x for e in U for x in edge_end[e]}
                d = nx.multi_source_dijkstra_path_length(g, ends)
                cand = [v for v in V if v not in Bsets[U]]
                assert cand, ('B(U)=V', n, s, U)
                r = max(cand, key=lambda v: (d[v], -v))
                refs[U] = r
                x0, B = space(r)
                proj = lambda x: tuple((x >> e) & 1 for e in U)
                base = proj(x0); gens = [proj(b) for b in B]
                span = {tuple([0]*len(U))}
                for gv in gens:
                    span |= {tuple(p ^ q for p, q in zip(w, gv)) for w in span}
                words = {tuple(p ^ q for p, q in zip(base, w)) for w in span}
                P[U] = {w: Fraction(1, len(words)) for w in words}
            # exact checks
            inside = {U: [v for v in V if set(inc[v]) <= set(U)] for U in regs}
            supp_checks = 0
            for U in regs:
                assert sum(P[U].values()) == 1 and all(p > 0 for p in P[U].values())
                pos = {e: k for k, e in enumerate(U)}
                for w in P[U]:
                    for v in inside[U]:
                        supp_checks += 1
                        assert sum(w[pos[e]] for e in inc[v]) % 2 == charge[v]
            def marg(U, T):
                idx = [U.index(e) for e in T]; mm = defaultdict(Fraction)
                for w, p in P[U].items(): mm[tuple(w[i] for i in idx)] += p
                return dict(mm)
            byedge = defaultdict(list)
            for i, U in enumerate(regs):
                for e in U: byedge[e].append(i)
            pairs = set()
            for e, L in byedge.items():
                for i, j in itertools.combinations(L, 2): pairs.add((i, j))
            for i, j in pairs:
                T = tuple(sorted(set(regs[i]) & set(regs[j])))
                assert marg(regs[i], T) == marg(regs[j], T), (n, s, regs[i], regs[j])
            maxB = max(len(Bsets[U]) for U in regs)
            rec = dict(n=n, seed=seed, edges=m, regions=len(regs), columns=sum(len(P[U]) for U in regs),
                       Rsupport_cols=None, pair_checks=len(pairs), support_checks=supp_checks,
                       max_B=maxB, exact_feasible=True, gf2_unsat=True)
            if a.lp and n <= 64:
                rec['highs'] = highs_check(regs, inside, inc, charge)
            rec['Rsupport_cols'] = sum(2 ** (len(U) - len(inside[U])) for U in regs)
            out.append(rec); print(json.dumps(rec), flush=True)
    js = json.dumps(out, indent=1)
    open('2026-11-28_1810_tseitin_results.json', 'w').write(js + '\n')
    print('sha256', hashlib.sha256((js + '\n').encode()).hexdigest())

def highs_check(regs, inside, inc, charge):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    col = {}; R = {}
    for U in regs:
        pos = {e: k for k, e in enumerate(U)}; R[U] = []
        for w in itertools.product((0, 1), repeat=len(U)):
            if all(sum(w[pos[e]] for e in inc[v]) % 2 == charge[v] for v in inside[U]):
                col[(U, w)] = len(col); R[U].append(w)
    rows, cols, vals, b = [], [], [], []
    r = 0
    for U in regs:
        for w in R[U]: rows.append(r); cols.append(col[(U, w)]); vals.append(1)
        b.append(1); r += 1
    first = {}
    sub_regs = defaultdict(list)
    for U in regs:
        for k in range(1, len(U)):
            for T in itertools.combinations(U, k): sub_regs[T].append(U)
    for T, L in sub_regs.items():
        if len(L) < 2: continue
        A0 = L[0]
        for U in L[1:]:
            for bw in itertools.product((0, 1), repeat=len(T)):
                for (UU, sign) in ((U, 1), (A0, -1)):
                    idx = [UU.index(e) for e in T]
                    for w in R[UU]:
                        if tuple(w[i] for i in idx) == bw:
                            rows.append(r); cols.append(col[(UU, w)]); vals.append(sign)
                b.append(0); r += 1
    A = coo_matrix((vals, (rows, cols)), shape=(r, len(col))).tocsr()
    res = linprog(np.zeros(len(col)), A_eq=A, b_eq=np.array(b, float), bounds=(0, None), method='highs')
    return dict(status=int(res.status), message=res.message, cols=len(col), eq_rows=r)

if __name__ == '__main__':
    main()
