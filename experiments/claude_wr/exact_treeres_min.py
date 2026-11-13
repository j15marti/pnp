"""Exact free-strategy minimum tree-like resolution size (min decision-tree leaves
for the false-clause search problem) on small UNSAT CNFs.  The minimum is taken
over ALL refutations, i.e. the optimal sequence is granted for free, matching the
W_R(N) directive.  Each instance is a separate stage; total runtime < 30 s."""
import itertools, json, sys, time
from functools import lru_cache

def php(n):  # n+1 pigeons, n holes
    v = lambda p, h: p * n + h + 1
    cls = [tuple(v(p, h) for h in range(n)) for p in range(n + 1)]
    for h in range(n):
        for p, q in itertools.combinations(range(n + 1), 2):
            cls.append((-v(p, h), -v(q, h)))
    return n * (n + 1), cls

def tseitin_k4():  # odd charge on K4, edges = variables
    E = list(itertools.combinations(range(4), 2)); cls = []
    for u in range(4):
        inc = [i + 1 for i, e in enumerate(E) if u in e]
        par = 1 if u == 0 else 0
        for s in itertools.product([0, 1], repeat=3):
            if sum(s) % 2 != par:  # forbid assignments with wrong parity
                cls.append(tuple(x if b == 0 else -x for x, b in zip(inc, s)))
    return len(E), cls

def min_leaves(nv, cls):
    cls = [frozenset(c) for c in cls]
    @lru_cache(maxsize=None)
    def S(rho):  # rho: frozenset of true literals
        for c in cls:
            if all(-l in rho for l in c):
                return 1
        best = None
        for x in range(1, nv + 1):
            if x in rho or -x in rho: continue
            a = S(rho | {x})
            if best is not None and a >= best: continue
            t = a + S(rho | {-x})
            if best is None or t < best: best = t
        return best
    return S(frozenset())

if __name__ == "__main__":
    out = []
    for name, (nv, cls) in [("PHP_2_1", php(1)), ("PHP_3_2", php(2)), ("TSEITIN_K4_odd", tseitin_k4()), ("PHP_4_3", php(3))]:
        t = time.time(); L = min_leaves(nv, cls)
        N = sum(len(c) for c in cls) + len(cls)
        out.append(dict(instance=name, vars=nv, clauses=len(cls), size_N=N,
                        min_tree_res_leaves=L, min_tree_res_nodes=2 * L - 1,
                        seconds=round(time.time() - t, 2)))
        print(out[-1], flush=True)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
