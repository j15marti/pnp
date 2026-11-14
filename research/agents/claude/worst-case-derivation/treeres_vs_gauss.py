"""Exact minimum tree-like resolution refutation size vs. Gaussian-elimination cost
on Tseitin formulas (and PHP).  Each graph is one independent stage (<30 s each);
results are appended to treeres_vs_gauss_results.json so completed stages are reused.
Usage: python3 treeres_vs_gauss.py [stage_name ...]"""
import itertools, json, sys, time, os
from functools import lru_cache

def tseitin(edges, nverts):
    # charge 1 on vertex 0, 0 elsewhere -> odd total charge -> UNSAT
    inc = {v: [] for v in range(nverts)}
    for i, (a, b) in enumerate(edges):
        inc[a].append(i); inc[b].append(i)
    clauses = []
    for v in range(nverts):
        es = inc[v]; c = 1 if v == 0 else 0
        for bits in itertools.product([0, 1], repeat=len(es)):
            if sum(bits) % 2 != c:  # forbid this assignment
                clauses.append(tuple((e, 1 - b) for e, b in zip(es, bits)))  # literal (var, sign) true if var==sign
    return len(edges), clauses, inc

def php(n):  # n+1 pigeons, n holes; var p*n+h
    cl = [tuple((p*n+h, 1) for h in range(n)) for p in range(n+1)]
    for h in range(n):
        for p, q in itertools.combinations(range(n+1), 2):
            cl.append(((p*n+h, 0), (q*n+h, 0)))
    return n*(n+1), cl

def min_tree_res(nvars, clauses, budget=25.0):
    """Min #leaves of a decision tree whose every leaf falsifies a clause.
    Min tree-like resolution refutation size (#clauses) = 2*leaves - 1."""
    t0 = time.time()
    cmask = [(sum(1 << v for v, s in c if s == 1), sum(1 << v for v, s in c if s == 0)) for c in clauses]
    # clause falsified iff all pos-literal vars set 0 and all neg-literal vars set 1
    memo = {}
    def f(z, o):  # z: vars set 0, o: vars set 1
        key = (z, o)
        if key in memo: return memo[key]
        if time.time() - t0 > budget: raise TimeoutError
        best = None; cand = 0
        for p, n in cmask:
            if (p & o) or (n & z):  # satisfied
                continue
            if (p & ~z) == 0 and (n & ~o) == 0:
                memo[key] = 1; return 1
            cand |= (p | n) & ~(z | o)
        # branch only on variables of live clauses (sufficient for optimality: a tree
        # querying only live-clause variables exists of no larger size -- standard)
        v = 0
        while cand:
            if cand & 1:
                b = 1 << v
                l = f(z | b, o)
                if best is None or l < best:
                    r = f(z, o | b)
                    if best is None or l + r < best: best = l + r
            cand >>= 1; v += 1
        memo[key] = best; return best
    leaves = f(0, 0)
    return leaves, 2 * leaves - 1, len(memo), time.time() - t0

def gauss_ops(nvars, inc, nverts):
    # row ops over GF(2) on the vertex-parity system: rows = vertices, cols = edges
    rows = [sum(1 << e for e in inc[v]) | ((1 if v == 0 else 0) << nvars) for v in range(nverts)]
    ops = 0; r = 0
    for col in range(nvars):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> col & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> col & 1:
                rows[i] ^= rows[r]; ops += 1
        r += 1
    inconsistent = any(row == (1 << nvars) for row in rows)
    return ops, inconsistent

GRAPHS = {
 "cycle6": (6, [(i, (i+1) % 6) for i in range(6)]),
 "cycle10": (10, [(i, (i+1) % 10) for i in range(10)]),
 "K4": (4, list(itertools.combinations(range(4), 2))),
 "K33": (6, [(a, b) for a in range(3) for b in range(3, 6)]),
 "prism": (6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),
 "cube": (8, [(a, a ^ (1 << k)) for a in range(8) for k in range(3) if a < a ^ (1 << k)]),
 "petersen": (10, [(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+2)%5) for i in range(5)] + [(i,5+i) for i in range(5)]),
}

def main():
    out = "treeres_vs_gauss_results.json"
    res = json.load(open(out)) if os.path.exists(out) else {}
    stages = sys.argv[1:] or list(GRAPHS) + ["php2", "php3", "php4"]
    for s in stages:
        if s in res and res[s].get("status") == "done": continue
        try:
            if s.startswith("php"):
                n = int(s[3:]); nv, cl = php(n)
                lv, sz, st, dt = min_tree_res(nv, cl)
                res[s] = dict(family="PHP", n=n, vars=nv, clauses=len(cl), min_tree_leaves=lv,
                              min_tree_res_size=sz, states=st, secs=round(dt, 2), status="done")
            else:
                nverts, edges = GRAPHS[s]; nv, cl, inc = tseitin(edges, nverts)
                lv, sz, st, dt = min_tree_res(nv, cl)
                ops, inc_ok = gauss_ops(nv, inc, nverts)
                res[s] = dict(family="Tseitin", vertices=nverts, vars=nv, clauses=len(cl),
                              min_tree_leaves=lv, min_tree_res_size=sz, gauss_row_xors=ops,
                              gauss_detects_unsat=inc_ok, states=st, secs=round(dt, 2), status="done")
        except TimeoutError:
            res[s] = dict(status="timeout_25s")
        print(s, res[s], flush=True)
        json.dump(res, open(out, "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    main()
