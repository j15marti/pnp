#!/usr/bin/env python3
"""Exact minimum tree-like Resolution refutation size (= decision-tree nodes,
Prover-Delayer correspondence) for small UNSAT CNFs, versus the work of a
poly-time non-Resolution algorithm (Gaussian elimination over GF(2) for Tseitin).
Exhaustive DP over partial assignments; each instance < ~20 s."""
import itertools, json, sys, time
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var p(i,j)
    v = lambda i, j: i*m + j + 1
    C = [[v(i, j) for j in range(m)] for i in range(m+1)]
    for j in range(m):
        for i, k in itertools.combinations(range(m+1), 2):
            C.append([-v(i, j), -v(k, j)])
    return m*(m+1), C

def tseitin(edges, nverts, odd_vertex=0):
    nv = len(edges); C = []; rows = []
    for u in range(nverts):
        inc = [e+1 for e, (a, b) in enumerate(edges) if u in (a, b)]
        ch = 1 if u == odd_vertex else 0
        rows.append((inc, ch))
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != ch:  # forbid assignments with wrong parity
                C.append([(-x if s else x) for x, s in zip(inc, signs)])
    return nv, C, rows

def min_tree_res(n, C):
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def f(state):  # state: tuple in {0,1,2}^n, 2 = unassigned
        for c in C:
            if all(state[abs(l)-1] == (0 if l > 0 else 1) for l in c):
                return 1
        best = None
        for x in range(n):
            if state[x] == 2:
                s0 = state[:x]+(0,)+state[x+1:]; s1 = state[:x]+(1,)+state[x+1:]
                a = f(s0)
                if best is not None and 1+a+1 >= best: continue
                b = 1+a+f(s1)
                if best is None or b < best: best = b
        return best
    return f(tuple([2]*n)), f.cache_info().currsize

def gauss_ops(rows, nv):
    M = []
    for inc, ch in rows:
        r = 0
        for x in inc: r |= 1 << (x-1)
        M.append([r, ch])
    ops = 0; piv = 0
    for col in range(nv):
        p = next((i for i in range(piv, len(M)) if M[i][0] >> col & 1), None)
        if p is None: continue
        M[piv], M[p] = M[p], M[piv]
        for i in range(len(M)):
            if i != piv and M[i][0] >> col & 1:
                M[i][0] ^= M[piv][0]; M[i][1] ^= M[piv][1]; ops += 1
        piv += 1
    inconsistent = any(r == 0 and c == 1 for r, c in M)
    return ops, inconsistent

out = []
which = sys.argv[1] if len(sys.argv) > 1 else "all"
insts = []
if which in ("all", "php"):
    for m in (1, 2, 3):
        n, C = php(m); insts.append((f"PHP_{m+1}->{m}", n, C, None))
if which in ("all", "tseitin"):
    K4 = [(a, b) for a, b in itertools.combinations(range(4), 2)]
    Q3 = [(a, b) for a in range(8) for b in range(8) if a < b and bin(a ^ b).count("1") == 1]
    K33 = [(a, b) for a in range(3) for b in range(3, 6)]
    for name, E, nvx in (("Tseitin_K4", K4, 4), ("Tseitin_K33", K33, 6), ("Tseitin_Q3cube", Q3, 8)):
        n, C, rows = tseitin(E, nvx); insts.append((name, n, C, rows))
for name, n, C, rows in insts:
    t = time.time(); size, states = min_tree_res(n, C)
    rec = dict(instance=name, vars=n, clauses=len(C), min_tree_res_size=size,
               dp_states=states, seconds=round(time.time()-t, 2))
    if rows is not None:
        ops, inc = gauss_ops(rows, n); rec.update(gauss_xor_row_ops=ops, gauss_detects_unsat=inc)
    out.append(rec); print(json.dumps(rec), flush=True)
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "/dev/null", "w"), indent=1)
