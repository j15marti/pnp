"""Exact minimum DPLL / tree-like Resolution leaf count L(F) for small UNSAT CNFs.
L(F) = min leaves of a decision tree whose every leaf falsifies a clause of F;
this equals the minimum number of leaves of a tree-like Resolution refutation
(standard correspondence; refutation size = 2L-1 clauses).  Runtime < 30 s."""
import itertools, json, sys, time
from functools import lru_cache

def php(m, n):  # m pigeons, n holes, var (i,j) -> i*n+j+1
    v = lambda i, j: i * n + j + 1
    C = [tuple(v(i, j) for j in range(n)) for i in range(m)]
    for j in range(n):
        for a, b in itertools.combinations(range(m), 2):
            C.append((-v(a, j), -v(b, j)))
    return m * n, C

def tseitin_k4_odd():  # K4, 6 edges, charge 1 on vertex 0 -> UNSAT
    E = list(itertools.combinations(range(4), 2)); C = []
    for x in range(4):
        inc = [k + 1 for k, e in enumerate(E) if x in e]
        ch = 1 if x == 0 else 0
        for s in itertools.product([0, 1], repeat=3):
            if sum(s) % 2 != ch:  # forbid assignment s
                C.append(tuple(-l if b else l for l, b in zip(inc, s)))
    return 6, C

def min_leaves(nv, C):
    @lru_cache(maxsize=None)
    def L(asg):  # asg: tuple of 0/1/None
        live = []
        for c in C:
            sat = False; undec = False
            for l in c:
                val = asg[abs(l) - 1]
                if val is None: undec = True
                elif (val == 1) == (l > 0): sat = True; break
            if sat: continue
            if not undec: return 1
            live.append(c)
        best = None
        vars_ = {abs(l) for c in live for l in c if asg[abs(l) - 1] is None}
        for x in vars_:
            a = list(asg)
            a[x - 1] = 0; t0 = L(tuple(a))
            if best is not None and t0 >= best: continue
            a[x - 1] = 1; t = t0 + L(tuple(a))
            if best is None or t < best: best = t
        return best
    return L(tuple([None] * nv))

if __name__ == "__main__":
    out = {}
    for name, (nv, C) in [("PHP(2,1)", php(2, 1)), ("PHP(3,2)", php(3, 2)),
                          ("PHP(4,3)", php(4, 3)), ("Tseitin-K4-odd", tseitin_k4_odd())]:
        t = time.time(); Lm = min_leaves(nv, C)
        out[name] = {"vars": nv, "clauses": len(C), "min_leaves": Lm,
                     "min_treeRes_clauses": 2 * Lm - 1, "seconds": round(time.time() - t, 2)}
        print(name, out[name], flush=True)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
