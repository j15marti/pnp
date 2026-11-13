"""Stage 2 (independent of stage 1): exact free-strategy minimum of three cost
measures on the same small UNSAT families, to test whether a cost measure can
even support a superpolynomial W_R(N) lower bound.

  leaves(F) = min over decision trees for the false-clause search problem
              (= min tree-like resolution refutation leaf count)
  depth(F)  = min over the same trees of the tree DEPTH
  space(F)  <= depth(F) + 2   (clause space of the DPLL run realizing the tree)

depth(F) <= #vars(F) <= N always, so any cost measure dominated by depth or by
clause space is poly(N)-bounded for free-strategy minima: no superpolynomial
worst-case lower bound is possible for it. Runtime < 30 s."""
import itertools, json, sys, time
from functools import lru_cache
sys.path.insert(0, "")
from exact_treeres_min import php, tseitin_k4

def minima(nv, cls):
    cls = [frozenset(c) for c in cls]
    def falsified(rho):
        return any(all(-l in rho for l in c) for c in cls)
    @lru_cache(maxsize=None)
    def D(rho):  # min depth
        if falsified(rho): return 0
        best = None
        for x in range(1, nv + 1):
            if x in rho or -x in rho: continue
            d = 1 + max(D(rho | {x}), D(rho | {-x}))
            if best is None or d < best: best = d
        return best
    return D(frozenset())

if __name__ == "__main__":
    out = []
    for name, (nv, cls) in [("PHP_2_1", php(1)), ("PHP_3_2", php(2)),
                            ("TSEITIN_K4_odd", tseitin_k4()), ("PHP_4_3", php(3))]:
        t = time.time(); d = minima(nv, cls)
        N = sum(len(c) for c in cls) + len(cls)
        out.append(dict(instance=name, vars=nv, size_N=N, min_tree_depth=d,
                        clause_space_upper=d + 2, depth_le_vars=d <= nv,
                        seconds=round(time.time() - t, 2)))
        print(out[-1], flush=True)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
