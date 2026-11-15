"""Exact minimum tree-like Resolution refutation size (= nodes of an optimal
falsified-clause decision tree) for small UNSAT CNFs, plus a GF(2) elimination
control for Tseitin.  COMPUTATIONAL illustration only; each instance < 30 s."""
import itertools, json, sys, time
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes
    v = lambda p, h: p * m + h + 1
    cls = [[v(p, h) for h in range(m)] for p in range(m + 1)]
    for h in range(m):
        for p, q in itertools.combinations(range(m + 1), 2):
            cls.append([-v(p, h), -v(q, h)])
    return m * (m + 1), cls

def tseitin(edges, charge):
    nv = len(edges); cls = []; xor_rows = []
    verts = sorted({u for e in edges for u in e})
    for w in verts:
        inc = [i + 1 for i, e in enumerate(edges) if w in e]
        c = charge.get(w, 0)
        xor_rows.append((inc, c))
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != c:  # forbid this assignment
                cls.append([x if s == 0 else -x for x, s in zip(inc, signs)])
    return nv, cls, xor_rows

def min_tree_res(nv, cls):
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def size(rho):  # rho: tuple of 0/1/2 (2 = unset)
        for c in cls:
            if all(rho[abs(l) - 1] == (0 if l > 0 else 1) for l in c):
                return 1
        best = None
        for x in range(nv):
            if rho[x] == 2:
                a = list(rho); a[x] = 0; s0 = size(tuple(a))
                if best is not None and 1 + s0 >= best: continue
                a[x] = 1; s = 1 + s0 + size(tuple(a))
                if best is None or s < best: best = s
        return best
    return size(tuple([2] * nv))

def gf2_steps(nv, rows):
    M = [(set(r), c) for r, c in rows]; ops = 0
    for x in range(1, nv + 1):
        piv = next((i for i, (r, _) in enumerate(M) if x in r), None)
        if piv is None: continue
        pr, pc = M.pop(piv)
        for i, (r, c) in enumerate(M):
            if x in r: M[i] = (r ^ pr, c ^ pc); ops += len(pr)
    return ops, any(not r and c for r, c in M)

out = {}
for m in (1, 2, 3):
    t = time.time(); nv, cls = php(m)
    out[f"PHP_{m+1}_{m}"] = {"vars": nv, "clauses": len(cls), "min_tree_res_nodes": min_tree_res(nv, cls), "sec": round(time.time() - t, 2)}
graphs = {"K4": list(itertools.combinations(range(4), 2)),
          "C6": [(i, (i + 1) % 6) for i in range(6)],
          "K33": [(a, b) for a in range(3) for b in range(3, 6)]}
for name, E in graphs.items():
    t = time.time(); nv, cls, rows = tseitin(E, {0: 1})
    ops, contra = gf2_steps(nv, rows)
    out[f"Tseitin_{name}_odd"] = {"vars": nv, "clauses": len(cls), "min_tree_res_nodes": min_tree_res(nv, cls),
                                  "gf2_xor_ops": ops, "gf2_refutes": contra, "sec": round(time.time() - t, 2)}
print(json.dumps(out, indent=1))
json.dump(out, open(__file__.replace(".py", "_results.json"), "w"), indent=1)
