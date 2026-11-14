"""Exact minimum tree-like resolution refutation size (= min falsified-clause decision tree size).
COMPUTATIONAL evidence only. Each invocation < ~30 s. Usage: python3 treelike_min.py
"""
import itertools, json, random, sys, time
from functools import lru_cache
sys.setrecursionlimit(100000)

def min_treelike(n, clauses):
    # clause: list of literals (+v/-v, v in 1..n). state: (a0,a1) bitmasks of vars set to 0/1.
    cl = [(sum(1<<(abs(l)-1) for l in c if l>0), sum(1<<(abs(l)-1) for l in c if l<0)) for c in clauses]
    full = (1<<n)-1
    @lru_cache(maxsize=None)
    def T(a0, a1):
        # clause falsified iff all positive lits set 0 and all negative lits set 1
        for p, q in cl:
            if p & ~a0 == 0 and q & ~a1 == 0:
                return 1
        free = full & ~(a0|a1)
        best = None
        v = free
        while v:
            b = v & -v; v ^= b
            s = 1 + T(a0|b, a1)
            if best is not None and s >= best: continue
            s += T(a0, a1|b)
            if best is None or s < best: best = s
        return best
    return T(0, 0)

def php(m):  # m+1 pigeons, m holes
    var = lambda i, j: i*m + j + 1
    C = [[var(i, j) for j in range(m)] for i in range(m+1)]
    for j in range(m):
        for i, k in itertools.combinations(range(m+1), 2):
            C.append([-var(i, j), -var(k, j)])
    return m*(m+1), C

def sat(n, C):
    for x in range(1<<n):
        if all(any((l>0) == bool(x>>(abs(l)-1)&1) for l in c) for c in C): return True
    return False

out = {"php": [], "random3cnf": []}
for m in (1, 2, 3):
    n, C = php(m); t = time.time()
    out["php"].append({"m": m, "vars": n, "clauses": len(C), "min_treelike_size": min_treelike(n, C), "sec": round(time.time()-t, 2)})
rng = random.Random(20261114)
for n in (6, 8, 10):
    worst = 0; cnt = 0
    while cnt < 12:
        C = [[v*rng.choice((1, -1)) for v in rng.sample(range(1, n+1), 3)] for _ in range(int(6*n))]
        if sat(n, C): continue
        cnt += 1; worst = max(worst, min_treelike(n, C))
    out["random3cnf"].append({"n": n, "m_clauses": 6*n, "samples": cnt, "max_min_treelike_size": worst})
print(json.dumps(out, indent=1))
