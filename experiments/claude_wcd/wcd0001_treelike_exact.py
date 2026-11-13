#!/usr/bin/env python3
"""CLAUDE WCD-0001: exact minimum tree-like resolution refutation size vs. a
polynomial-time GF(2) algorithm on small Tseitin and PHP instances.

Exactness: a tree-like resolution refutation of F with L leaves corresponds
(Lovasz-Naor-Newman-Wigderson / standard) to a decision tree for the
falsified-clause search problem with L leaves, and vice versa, so
  minTreeRes(F) [nodes] = 2*minDT_leaves(F) - 1.
We compute minDT_leaves exactly by memoised recursion over partial
assignments:  D(rho) = 1 if rho falsifies a clause, else
  min_x D(rho,x=0) + D(rho,x=1).
Each instance is a separate invocation (chunking per AGENTS.md 30s rule):
  python3 wcd0001_treelike_exact.py <instance> <out.json>
"""
import sys, json, time, itertools
from functools import lru_cache

def tseitin(edges, nverts, charge_vertex=0):
    # variable per edge; vertex v parity = 1 iff v == charge_vertex (odd total => UNSAT)
    clauses = []
    for v in range(nverts):
        inc = [i for i, e in enumerate(edges) if v in e]
        target = 1 if v == charge_vertex else 0
        for bits in itertools.product([0, 1], repeat=len(inc)):
            if sum(bits) % 2 != target:   # forbid this local assignment
                clauses.append([(inc[j], 1 - bits[j]) for j in range(len(inc))])  # literal (var, required value)
    return len(edges), clauses

def php(m):  # m+1 pigeons, m holes
    var = lambda p, h: p * m + h
    cl = [[(var(p, h), 1) for h in range(m)] for p in range(m + 1)]
    for h in range(m):
        for p, q in itertools.combinations(range(m + 1), 2):
            cl.append([(var(p, h), 0), (var(q, h), 0)])
    return (m + 1) * m, cl

GRAPHS = {
    "K4": ([(a, b) for a, b in itertools.combinations(range(4), 2)], 4),
    "K33": ([(a, b) for a in range(3) for b in range(3, 6)], 6),
    "Q3": ([(a, a ^ (1 << i)) for a in range(8) for i in range(3) if a < a ^ (1 << i)], 8),
    "C6": ([(i, (i + 1) % 6) for i in range(6)], 6),
}

def build(name):
    if name in GRAPHS:
        e, nv = GRAPHS[name]; n, cl = tseitin(e, nv); return n, cl, ("tseitin", e, nv)
    if name.startswith("PHP"):
        m = int(name[3:]); n, cl = php(m); return n, cl, ("php", m)
    raise SystemExit("unknown instance")

def min_dt(n, clauses):
    # clause as (mask, valmask): falsified by rho=(assigned, values) iff all its vars assigned with value != required
    cm = []
    for c in clauses:
        mask = 0; req = 0
        for v, r in c:
            mask |= 1 << v; req |= r << v
        cm.append((mask, req))
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def D(asg, val):
        for mask, req in cm:
            if asg & mask == mask and ((val ^ req) & mask) == mask:
                return 1
        best = None
        for x in range(n):
            b = 1 << x
            if asg & b: continue
            s = D(asg | b, val)
            if best is not None and s >= best: continue
            s += D(asg | b, val | b)
            if best is None or s < best: best = s
        return best
    r = D(0, 0)
    return r, D.cache_info().currsize

def gf2_ops(edges, nv):
    # Gaussian elimination on vertex parity equations; count row XORs (poly algorithm)
    rows = []
    for v in range(nv):
        m = 0
        for i, e in enumerate(edges):
            if v in e: m |= 1 << i
        rows.append([m, 1 if v == 0 else 0])
    ops = 0; r = 0
    for col in range(len(edges)):
        piv = next((i for i in range(r, len(rows)) if rows[i][0] >> col & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][0] >> col & 1:
                rows[i][0] ^= rows[r][0]; rows[i][1] ^= rows[r][1]; ops += 1
        r += 1
    unsat = any(m == 0 and b == 1 for m, b in rows)
    return ops, unsat

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    t = time.time()
    n, cl, meta = build(name)
    leaves, states = min_dt(n, cl)
    rec = {"instance": name, "vars": n, "clauses": len(cl), "min_dt_leaves": leaves,
           "min_treelike_res_nodes": 2 * leaves - 1, "memo_states": states}
    if meta[0] == "tseitin":
        ops, unsat = gf2_ops(meta[1], meta[2]); rec.update(gf2_row_xors=ops, gf2_detects_unsat=unsat)
    rec["seconds"] = round(time.time() - t, 2)
    json.dump(rec, open(out, "w"), indent=1); print(json.dumps(rec))
