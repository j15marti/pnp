"""Exact minimum tree-like resolution refutation size (= min DPLL leaves) for
PHP_n^{n+1}, compared with an O(1) counting decider on the same family.
Hostile control for the 'free optimal sequence' bridge: a trivial fast
algorithm need not induce short derivations in a fixed weak R.
Runtime target < 30 s (n <= 3)."""
import json, sys, time
from functools import lru_cache

def php(n):
    m = n + 1
    v = lambda i, j: i * n + j          # pigeon i in hole j
    cls = [tuple((v(i, j), 1) for j in range(n)) for i in range(m)]
    for j in range(n):
        for a in range(m):
            for b in range(a + 1, m):
                cls.append(((v(a, j), 0), (v(b, j), 0)))
    return m * n, cls

def min_tree_leaves(nv, cls):
    @lru_cache(maxsize=None)
    def T(rho):  # rho: tuple of -1/0/1
        undecided = False
        for c in cls:
            sat = False; free = False
            for x, s in c:
                if rho[x] == s: sat = True; break
                if rho[x] == -1: free = True
            if not sat and not free:
                return 1            # leaf: clause falsified
            if not sat: undecided = True
        if not undecided:
            raise ValueError("satisfiable branch")
        best = None
        for x in range(nv):
            if rho[x] == -1:
                r = list(rho); r[x] = 0; a = T(tuple(r))
                if best is not None and a >= best: continue
                r[x] = 1; t = a + T(tuple(r))
                if best is None or t < best: best = t
        return best
    val = T(tuple([-1] * nv))
    return val, T.cache_info().currsize

out = {}
for n in range(1, 4):
    t0 = time.time(); nv, cls = php(n)
    leaves, states = min_tree_leaves(nv, cls)
    out[f"PHP_{n}^{n+1}"] = dict(vars=nv, clauses=len(cls), min_tree_leaves=leaves,
        min_tree_size=2 * leaves - 1, states=states, seconds=round(time.time() - t0, 2),
        counting_decider_ops=1)
    print(out[f"PHP_{n}^{n+1}"], flush=True)
json.dump(out, open("treeres_php_results.json", "w"), indent=1)
