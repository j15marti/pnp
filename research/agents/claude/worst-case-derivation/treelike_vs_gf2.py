#!/usr/bin/env python3
"""COMPUTATIONAL control for the W_R(N) program (Claude worst-case-derivation log).

For tiny UNSAT CNFs F, compute EXACTLY
  T(F) = minimum tree-like resolution refutation size (number of nodes),
using the KNOWN equivalence: minimal tree-like refutations can be taken regular and
correspond one-to-one to decision trees whose every leaf falsifies an input clause;
size(tree refutation) = #nodes of decision tree.  T(F|rho) computed by memoised DP:
  T(G) = 1 if G contains an empty clause, else min_x T(G|x=0) + T(G|x=1) + 1.
Also reports the cost of Gaussian elimination (row operations) on the XOR form of
Tseitin formulas, the "algebraic switch" control.  Deterministic, no randomness.
Finite tests are not asymptotic proofs.
"""
import itertools, json, sys, time
from functools import lru_cache

def tseitin(edges, charge):
    # variables = edges; vertex v: XOR of incident edges = charge[v]
    nv = 1 + max(max(e) for e in edges)
    cls = []
    for v in range(nv):
        inc = [i + 1 for i, e in enumerate(edges) if v in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge[v]:  # forbid this assignment
                cls.append(tuple(-x if s else x for x, s in zip(inc, signs)))
    return len(edges), cls

def php(n):  # n+1 pigeons, n holes; var p(i,j)
    var = lambda i, j: i * n + j + 1
    cls = [tuple(var(i, j) for j in range(n)) for i in range(n + 1)]
    for j in range(n):
        for a in range(n + 1):
            for b in range(a + 1, n + 1):
                cls.append((-var(a, j), -var(b, j)))
    return (n + 1) * n, cls

def treelike_size(nvars, clauses):
    clauses = [frozenset(c) for c in clauses]
    @lru_cache(maxsize=None)
    def T(rho):  # rho: tuple of literals set true
        r = set(rho)
        live = []
        for c in clauses:
            if any(l in r for l in c):
                continue
            rest = frozenset(l for l in c if -l not in r)
            if not rest:
                return 1
            live.append(rest)
        assigned = {abs(l) for l in r}
        cand = sorted({abs(l) for c in live for l in c} - assigned)
        best = None
        for x in cand:
            s = T(tuple(sorted(r | {x}))) + T(tuple(sorted(r | {-x}))) + 1
            if best is None or s < best:
                best = s
        return best
    return T(())

def gf2_rowops(edges, charge):
    nv = 1 + max(max(e) for e in edges)
    rows = []
    for v in range(nv):
        m = 0
        for i, e in enumerate(edges):
            if v in e:
                m |= 1 << i
        rows.append([m, charge[v]])
    ops = 0
    piv_rows = []
    for r in rows:
        m, b = r
        for pm, pb in piv_rows:
            if m & (pm & -pm):
                m ^= pm; b ^= pb; ops += 1
        if m == 0:
            if b == 1:
                return ops, True  # derived 0 = 1
            continue
        piv_rows.append((m, b))
    return ops, False

def main():
    t0 = time.time()
    K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    K33 = [(a, b) for a in range(3) for b in range(3, 6)]
    Q3 = [(u, u ^ (1 << k)) for u in range(8) for k in range(3) if u < u ^ (1 << k)]
    cyc = lambda n: [(i, (i + 1) % n) for i in range(n)]
    out = {"script": "treelike_vs_gf2.py", "semantics": "exact min tree-like Res size via DT DP", "rows": []}
    fams = [("tseitin_C5", cyc(5)), ("tseitin_C8", cyc(8)), ("tseitin_K4", K4),
            ("tseitin_K33", K33), ("tseitin_Q3", Q3)]
    for name, E in fams:
        nv = 1 + max(max(e) for e in E)
        ch = [1] + [0] * (nv - 1)  # odd total charge => UNSAT
        n, cl = tseitin(E, ch)
        s = treelike_size(n, cl)
        ops, ok = gf2_rowops(E, ch)
        out["rows"].append({"name": name, "vars": n, "clauses": len(cl), "treelike_res_size": s,
                            "gf2_rowops": ops, "gf2_refutes": ok, "t": round(time.time() - t0, 2)})
    for k in (2, 3):
        n, cl = php(k)
        s = treelike_size(n, cl)
        out["rows"].append({"name": f"php_{k+1}_{k}", "vars": n, "clauses": len(cl), "treelike_res_size": s,
                            "gf2_rowops": None, "gf2_refutes": None, "t": round(time.time() - t0, 2)})
    out["elapsed_s"] = round(time.time() - t0, 2)
    json.dump(out, sys.stdout, indent=1)

if __name__ == "__main__":
    main()
