"""Exact minimum tree-like resolution refutation size (nodes) for small CNFs.
Tree-like Res size = min decision-tree size for the falsified-clause search
problem (leaves=2L-1 nodes); this is a standard exact equivalence.
DP over partial assignments (3^n states). Each invocation < ~30 s.
Usage: python3 tree_res_exact.py [stage]   stage in {php, rand, xor}
"""
import sys, json, random, itertools
from functools import lru_cache

def min_tree(n, clauses):
    # clause: list of signed ints (1-based). state: tuple of -1/0/1 per var
    cl = [[(abs(l)-1, 1 if l > 0 else 0) for l in c] for c in clauses]
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def f(st):
        for c in cl:
            if all(st[v] != -1 and st[v] != s for v, s in c):
                return 1
        best = None
        for v in range(n):
            if st[v] == -1:
                a = list(st); a[v] = 0; x = f(tuple(a))
                if best is not None and x >= best: continue
                a[v] = 1; y = f(tuple(a))
                t = x + y + 1
                if best is None or t < best: best = t
        return best
    return f(tuple([-1]*n))

def php(m):  # m+1 pigeons, m holes
    var = lambda i, j: i*m + j + 1
    C = [[var(i, j) for j in range(m)] for i in range(m+1)]
    for j in range(m):
        for i, k in itertools.combinations(range(m+1), 2):
            C.append([-var(i, j), -var(k, j)])
    return (m+1)*m, C

def unsat(n, C):
    for a in itertools.product([0,1], repeat=n):
        if all(any((a[abs(l)-1] == 1) == (l > 0) for l in c) for c in C):
            return False
    return True

def rand3(n, m, rng):
    return [[v*rng.choice([1,-1]) for v in rng.sample(range(1, n+1), 3)] for _ in range(m)]

out = {}
stage = sys.argv[1] if len(sys.argv) > 1 else "php"
if stage == "php":
    for m in (1, 2, 3):
        n, C = php(m); out[f"PHP_{m+1}_{m}"] = {"n": n, "clauses": len(C), "min_tree_nodes": min_tree(n, C)}
elif stage == "rand":
    rng = random.Random(20261110)
    for n in (6, 7, 8):
        best, cnt = 0, 0
        while cnt < 40:
            C = rand3(n, int(6*n), rng)
            if unsat(n, C):
                cnt += 1; best = max(best, min_tree(n, C))
        out[f"rand3_n{n}_ratio6"] = {"samples_unsat": cnt, "max_min_tree_nodes": best, "trivial_upper": 2**(n+1)-1}
print(json.dumps(out, indent=1))
