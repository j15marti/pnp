"""Exact minimum tree-like resolution refutation size (= 2*leaves-1 of an optimal
falsified-clause decision tree) for small UNSAT CNFs. Each family/size is one
independent chunk (<30 s each); results appended to JSON.  Usage:
  python -I treelike_min.py php 3      (PHP^{m+1}_m, m=3)
  python -I treelike_min.py tseitin 4  (Tseitin on odd-charged cycle C_n... K_n below)
"""
import sys, json, time, itertools, os
from functools import lru_cache

def php(m):
    P = m + 1
    v = lambda i, j: i * m + j
    cls = [[(v(i, j), 1) for j in range(m)] for i in range(P)]
    for j in range(m):
        for a, b in itertools.combinations(range(P), 2):
            cls.append([(v(a, j), 0), (v(b, j), 0)])
    return P * m, cls

def tseitin_complete(n):
    # Tseitin on K_n with odd total charge (vertex 0 charge 1): UNSAT
    edges = list(itertools.combinations(range(n), 2))
    eid = {e: k for k, e in enumerate(edges)}
    cls = []
    for u in range(n):
        inc = [eid[tuple(sorted((u, w)))] for w in range(n) if w != u]
        ch = 1 if u == 0 else 0
        for bits in itertools.product((0, 1), repeat=len(inc)):
            if sum(bits) % 2 != ch:  # forbid this assignment
                cls.append([(e, 1 - b) for e, b in zip(inc, bits)])
    return len(edges), cls

def solve(nv, cls):
    masks = []
    for c in cls:
        pos = neg = 0
        for x, s in c:
            if s: pos |= 1 << x
            else: neg |= 1 << x
        masks.append((pos, neg))
    # partial assignment: set S (assigned vars), T (vars true)
    @lru_cache(maxsize=None)
    def leaves(S, T):
        F = S & ~T
        for pos, neg in masks:  # falsified: all pos vars false, all neg vars true
            if (pos & F) == pos and (neg & T) == neg:
                return 1
        best = None
        for x in range(nv):
            b = 1 << x
            if S & b: continue
            # only branch on vars of some not-yet-satisfied clause
            l0 = leaves(S | b, T)
            if best is not None and l0 >= best: continue
            l1 = leaves(S | b, T | b)
            t = l0 + l1
            if best is None or t < best: best = t
        return best
    t0 = time.time(); L = leaves(0, 0)
    return L, 2 * L - 1, time.time() - t0, leaves.cache_info().currsize

if __name__ == "__main__":
    fam, k = sys.argv[1], int(sys.argv[2])
    nv, cls = php(k) if fam == "php" else tseitin_complete(k)
    L, size, dt, states = solve(nv, cls)
    rec = dict(family=fam, param=k, vars=nv, clauses=len(cls), min_leaves=L,
               min_treelike_size=size, seconds=round(dt, 2), memo_states=states)
    print(json.dumps(rec))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "treelike_min_results.jsonl")
    with open(out, "a") as f: f.write(json.dumps(rec) + "\n")
