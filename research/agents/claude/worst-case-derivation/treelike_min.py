"""Exact minimum tree-like resolution refutation size for small UNSAT CNFs.

Uses the exact correspondence: a minimal tree-like resolution refutation of F
with L leaves (axiom/weakened leaves) corresponds to a minimal decision tree
for the falsified-clause search problem Search(F) with L leaves; refutation
size (number of clause occurrences) is 2L-1.  The optimal derivation is chosen
freely (min over all trees) -- strategy search is not charged.
Usage: python treelike_min.py php N | tseitin_k4 | out.json
Each invocation is one instance and finishes well under 30 s for the sizes used.
"""
import sys, json, time
from functools import lru_cache

def php(n):  # n+1 pigeons, n holes; var p(i,j)
    v = lambda i, j: i * n + j
    cls = [[(v(i, j), 1) for j in range(n)] for i in range(n + 1)]
    for j in range(n):
        for a in range(n + 1):
            for b in range(a + 1, n + 1):
                cls.append([(v(a, j), 0), (v(b, j), 0)])
    return (n + 1) * n, cls

def tseitin_k4():  # K4, odd total charge (vertex 0 charged 1)
    edges = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    cls = []
    for u in range(4):
        inc = [k for k, e in enumerate(edges) if u in e]
        ch = 1 if u == 0 else 0
        for m in range(8):
            bits = [(m >> t) & 1 for t in range(3)]
            if sum(bits) % 2 != ch:  # forbid this assignment
                cls.append([(inc[t], 1 - bits[t]) for t in range(3)])
    return len(edges), cls

def solve(nv, cls):
    # clause falsified by (setmask,valmask) iff all its literals set and false
    C = []
    for c in cls:
        m = 0; val_false = 0
        for x, pos in c:
            m |= 1 << x
            if not pos: val_false |= 1 << x  # literal ~x false when x=1
        C.append((m, val_false))
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def f(sm, vm):
        for m, vf in C:
            if sm & m == m and (vm & m) == vf:
                return 1
        best = None
        for x in range(nv):
            b = 1 << x
            if sm & b: continue
            l = f(sm | b, vm)
            if best is not None and l >= best: continue
            r = f(sm | b, vm | b)
            if best is None or l + r < best: best = l + r
        return best
    L = f(0, 0)
    return L, f.cache_info().currsize

if __name__ == "__main__":
    t = time.time()
    if sys.argv[1] == "php":
        n = int(sys.argv[2]); nv, cls = php(n); name = f"PHP^{n+1}_{n}"
    else:
        nv, cls = tseitin_k4(); name = "Tseitin(K4,odd)"
    L, states = solve(nv, cls)
    out = dict(instance=name, vars=nv, clauses=len(cls), min_leaves=L,
               min_treelike_size=2 * L - 1, memo_states=states,
               seconds=round(time.time() - t, 2))
    print(json.dumps(out))
    if len(sys.argv) > 3 or (sys.argv[1] != "php" and len(sys.argv) > 2):
        with open(sys.argv[-1], "a") as fh: fh.write(json.dumps(out) + "\n")
