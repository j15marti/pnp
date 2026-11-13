#!/usr/bin/env python3
"""Exact minimum tree-like Resolution refutation size vs Gaussian-elimination work
on small odd-charge Tseitin 3-CNFs (3-regular graphs).

Tree-like Resolution refutation of F with L leaves <-> decision tree whose leaves each
falsify a clause of F (standard equivalence); minimum size = 2*Lmin - 1.  Lmin is computed
exactly by DP over partial assignments: f(rho)=1 if rho falsifies a clause, else
min_x f(rho,x=0)+f(rho,x=1).  One graph per invocation (chunking rule: each run < 30 s).
Usage: python3 tseitin_tree_vs_gauss.py GRAPHNAME OUT.json
"""
import sys, json, time, itertools
from functools import lru_cache

GRAPHS = {
    "K4":   [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
    "K33":  [(a,b) for a in range(3) for b in range(3,6)],
    "PRISM":[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
    "Q3":   [(a,b) for a in range(8) for b in range(a+1,8) if bin(a^b).count("1")==1],
}

def tseitin(edges, charge):
    nv = 1+max(max(e) for e in edges)
    inc = {v:[i for i,e in enumerate(edges) if v in e] for v in range(nv)}
    clauses = []  # (mask, falsifying values bits) : clause falsified iff vars in mask take bits
    for v in range(nv):
        vs = inc[v]
        for bits in itertools.product((0,1), repeat=len(vs)):
            if sum(bits)%2 != charge[v]:          # assignment violates parity -> forbid it
                m = 0; val = 0
                for x,b in zip(vs,bits):
                    m |= 1<<x; val |= b<<x
                clauses.append((m,val))
    return clauses

def min_tree_leaves(n, clauses):
    @lru_cache(maxsize=None)
    def f(mask, val):
        for m,cv in clauses:
            if mask & m == m and val & m == cv:
                return 1
        best = None
        for x in range(n):
            if not mask>>x & 1:
                a = f(mask|1<<x, val)
                if best is not None and a >= best: continue
                b = f(mask|1<<x, val|1<<x)
                if best is None or a+b < best: best = a+b
        return best
    r = f(0,0); info = f.cache_info()
    return r, info.currsize

def gauss_ops(edges, charge):
    """Row-XOR count of Gaussian elimination on the incidence parity system over GF(2)."""
    nv = 1+max(max(e) for e in edges); n=len(edges)
    rows = []
    for v in range(nv):
        r = 0
        for i,e in enumerate(edges):
            if v in e: r |= 1<<i
        rows.append([r, charge[v]])
    ops = 0; piv_row = 0
    for c in range(n):
        p = next((i for i in range(piv_row,len(rows)) if rows[i][0]>>c &1), None)
        if p is None: continue
        rows[piv_row],rows[p] = rows[p],rows[piv_row]
        for i in range(len(rows)):
            if i!=piv_row and rows[i][0]>>c &1:
                rows[i][0]^=rows[piv_row][0]; rows[i][1]^=rows[piv_row][1]; ops+=1
        piv_row += 1
    unsat = any(r[0]==0 and r[1]==1 for r in rows)
    return ops, unsat

def brute_unsat(n, clauses):
    for a in range(1<<n):
        if not any(a & m == cv for m,cv in clauses): return False
    return True

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    edges = GRAPHS[name]; nv = 1+max(max(e) for e in edges)
    charge = [1]+[0]*(nv-1)                      # odd total charge -> UNSAT
    cl = tseitin(edges, charge); n = len(edges)
    t0=time.time()
    assert brute_unsat(n, cl)
    L, states = min_tree_leaves(n, cl)
    ops, unsat = gauss_ops(edges, charge); assert unsat
    res = dict(graph=name, vertices=nv, variables=n, clauses=len(cl),
               cnf_literal_occurrences=3*len(cl), min_tree_leaves=L,
               min_treelike_resolution_size=2*L-1, dp_states=states,
               gauss_row_xors=ops, seconds=round(time.time()-t0,2))
    json.dump(res, open(out,"w"), indent=1); print(json.dumps(res))
