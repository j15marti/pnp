"""CLAUDE WBAR-0001 experiment: exact minimum tree-like resolution refutation size
of Tseitin formulas (odd total charge) on small 3-regular graphs, versus the exact
number of F2 row operations Gaussian elimination uses to refute the same system.
Tree-like resolution size (with weakening) = 2L-1, L = min leaves of a decision tree
for the falsified-clause search problem (exact correspondence, e.g. Beame-Pitassi 1996).
Deterministic: no randomness. Each graph runs in one stage (<30 s).
Usage: python3 -I tseitin_treeres.py [graph names...]"""
import sys, json, time, itertools
from functools import lru_cache

GRAPHS = {
  "K4": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
  "K33": [(a,b) for a in range(3) for b in range(3,6)],
  "prism": [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
  "petersen": [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)],
  "cube": [(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)],
}

def tseitin(edges):
    V = sorted({v for e in edges for v in e})
    charge = {v: (1 if v == V[0] else 0) for v in V}   # odd total charge -> UNSAT
    clauses = []
    for v in V:
        inc = [i for i,e in enumerate(edges) if v in e]
        for bits in itertools.product([0,1], repeat=len(inc)):
            if sum(bits) % 2 != charge[v]:   # forbidden local assignment -> clause
                pos = sum(1<<x for x,b in zip(inc,bits) if b == 0)
                neg = sum(1<<x for x,b in zip(inc,bits) if b == 1)
                clauses.append((pos,neg))
    return V, charge, clauses

def min_tree_res(nvars, clauses):
    full = (1<<nvars)-1
    @lru_cache(maxsize=None)
    def L(mask, val):
        for pos,neg in clauses:
            if (pos|neg) & ~mask == 0 and (val & pos) == 0 and (val & neg) == neg:
                return 1
        best = None
        free = full & ~mask
        while free:
            b = free & -free; free ^= b
            a = L(mask|b, val); 
            if best is not None and a >= best: continue
            c = L(mask|b, val|b)
            if best is None or a+c < best: best = a+c
        return best
    leaves = L(0,0)
    return leaves, 2*leaves-1, L.cache_info().currsize

def gauss_ops(V, charge, edges):
    rows = []
    for v in V:
        r = sum(1<<i for i,e in enumerate(edges) if v in e)
        rows.append([r, charge[v]])
    ops = 0; piv = 0
    for col in range(len(edges)):
        p = next((i for i in range(piv,len(rows)) if rows[i][0]>>col & 1), None)
        if p is None: continue
        rows[piv], rows[p] = rows[p], rows[piv]
        for i in range(len(rows)):
            if i != piv and rows[i][0]>>col & 1:
                rows[i][0] ^= rows[piv][0]; rows[i][1] ^= rows[piv][1]; ops += 1
        piv += 1
    contradiction = any(r[0]==0 and r[1]==1 for r in rows)
    return ops, contradiction

if __name__ == "__main__":
    names = sys.argv[1:] or ["K4","K33","prism","cube"]
    out = {}
    for g in names:
        E = GRAPHS[g]; t0 = time.time()
        V, ch, C = tseitin(E)
        leaves, size, states = min_tree_res(len(E), C)
        ops, contra = gauss_ops(V, ch, E)
        out[g] = dict(vertices=len(V), edge_vars=len(E), clauses=len(C),
                      min_treeres_leaves=leaves, min_treeres_size=size,
                      dp_states=states, gauss_row_ops=ops, gauss_refutes=contra,
                      seconds=round(time.time()-t0,2))
        print(g, out[g], flush=True)
    json.dump(out, open("tseitin_treeres_results.json" if not sys.argv[1:] else
                        "tseitin_treeres_results_%s.json" % "_".join(names),"w"), indent=1)
