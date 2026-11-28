#!/usr/bin/env python3
"""EB-REGLP-R1: scaling of the C04-36 blind width-5 pair-union regional LP on
random 3-CNF at clause density 4.6 (= 184/40, density of CNF-RANDOM-3CNF-40).
Instances: uniform random 3-CNF (distinct vars per clause, random signs),
seed-fixed; only certified-UNSAT instances (pysat CaDiCaL/Glucose) are kept.
Cover: all clause scopes (grouped by scope; R_U = words satisfying every clause
whose scope is inside U) + union of each overlapping pair with |union|<=5.
LP: normalization + for every proper subset T contained in >=2 regions,
marginal of each region on T equals that of the first region.
Solved by HiGHS (floating). FEASIBLE/INFEASIBLE are COMPUTATIONAL (floating),
not exact rational certificates."""
import itertools, random, json, sys, time, hashlib
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from pysat.solvers import Glucose4

def inst(n, m, seed):
    rng = random.Random(seed)
    cl = []
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        cl.append(tuple((v, rng.random() < 0.5) for v in vs))  # (var, negated?)
    return cl

def unsat(n, cl):
    with Glucose4(bootstrap_with=[[(-(v+1) if neg else v+1) for v, neg in c] for c in cl]) as s:
        return not s.solve()

def lp(n, cl):
    scopes = sorted({tuple(sorted(v for v, _ in c)) for c in cl})
    regs = set(scopes)
    byvar = defaultdict(list)
    for s in scopes:
        for v in s: byvar[v].append(s)
    for v, L in byvar.items():
        for a, b in itertools.combinations(L, 2):
            u = tuple(sorted(set(a) | set(b)))
            if len(u) <= 5: regs.add(u)
    regs = sorted(regs, key=lambda r: (len(r), r))
    R = {}; col = {}
    for U in regs:
        Us = set(U); pos = {v: k for k, v in enumerate(U)}
        ins = [c for c in cl if all(v in Us for v, _ in c)]
        R[U] = [w for w in itertools.product((0, 1), repeat=len(U))
                if all(any(w[pos[v]] != neg for v, neg in c) for c in ins)]
        if not R[U]: return 'INFEASIBLE(empty region)', len(regs), 0, 0
        for w in R[U]: col[(U, w)] = len(col)
    rows, cols, vals, b = [], [], [], []; r = 0
    for U in regs:
        for w in R[U]: rows.append(r); cols.append(col[(U, w)]); vals.append(1.0)
        b.append(1.0); r += 1
    sub = defaultdict(list)
    for U in regs:
        for k in range(1, len(U)):
            for T in itertools.combinations(U, k): sub[T].append(U)
    for T, L in sub.items():
        if len(L) < 2: continue
        A0 = L[0]
        idx0 = [A0.index(v) for v in T]
        for U in L[1:]:
            idx = [U.index(v) for v in T]
            base = {}
            for w in R[U]:
                key = tuple(w[i] for i in idx)
                rr = base.setdefault(key, None)
            keyrow = {}
            for bw in itertools.product((0, 1), repeat=len(T)):
                keyrow[bw] = r; b.append(0.0); r += 1
            for w in R[U]:
                rows.append(keyrow[tuple(w[i] for i in idx)]); cols.append(col[(U, w)]); vals.append(1.0)
            for w in R[A0]:
                rows.append(keyrow[tuple(w[i] for i in idx0)]); cols.append(col[(A0, w)]); vals.append(-1.0)
    A = coo_matrix((vals, (rows, cols)), shape=(r, len(col))).tocsr()
    res = linprog(np.zeros(len(col)), A_eq=A, b_eq=np.array(b), bounds=(0, None), method='highs')
    st = {0: 'FEASIBLE', 2: 'INFEASIBLE'}.get(res.status, 'STATUS%d' % res.status)
    return st, len(regs), len(col), r

def main():
    sizes = [int(x) for x in sys.argv[1].split(',')]; per = int(sys.argv[2])
    out = []
    for n in sizes:
        m = round(4.6 * n); got = 0; seed = 9100000 + 1000 * n
        while got < per:
            seed += 1; cl = inst(n, m, seed)
            if not unsat(n, cl): continue
            got += 1; t = time.time()
            st, nr, nc, ne = lp(n, cl)
            rec = dict(n=n, m=m, seed=seed, unsat=True, lp=st, regions=nr, columns=nc, eq_rows=ne, secs=round(time.time()-t, 2))
            out.append(rec); print(json.dumps(rec), flush=True)
    js = json.dumps(out, indent=1) + '\n'
    open('2026-11-28_1810_random3cnf_results_partial.json', 'w').write(js)
    print('sha256', hashlib.sha256(js.encode()).hexdigest())
main()
