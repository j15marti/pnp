"""Exact minimum tree-like Resolution refutation size (free optimal strategy).

Min tree-like Resolution refutation of F has L leaves iff the falsified-clause
search problem Search(F) has a decision tree with L leaves (Lovasz-Naor-Newman-
Wigderson correspondence); refutation size (clauses) = 2L-1.  We compute
  W_tree(F) = min over all decision trees of #leaves
by exact DP over partial assignments.  This is the user's quantity
min_pi cost(pi) with the optimal derivation chosen for free.
Each family member runs in well under 30 s (AGENTS.md runtime rule); stages are
separate CLI invocations: python wcd_treeres_exact.py <family> <param>.
"""
import itertools, json, sys, time
from functools import lru_cache

def solve(n, clauses):
    cl = [(p, q) for p, q in clauses]
    full = (1 << n) - 1
    @lru_cache(maxsize=None)
    def f(mask, val):
        for p, q in cl:  # p: positive-literal vars, q: negative-literal vars
            s = p | q
            if s & mask == s and (val & p) == 0 and (val & q) == q:
                return 1
        best = None
        free = full & ~mask
        x = free
        while x:
            b = x & -x; x ^= b
            c = f(mask | b, val) + f(mask | b, val | b)
            if best is None or c < best:
                best = c
        if best is None:
            raise ValueError("satisfiable")
        return best
    return f(0, 0), f.cache_info().currsize

def php(m):  # m pigeons, m-1 holes
    h = m - 1; var = lambda i, j: i * h + j; cls = []
    for i in range(m):
        cls.append((sum(1 << var(i, j) for j in range(h)), 0))
    for j in range(h):
        for i, k in itertools.combinations(range(m), 2):
            cls.append((0, (1 << var(i, j)) | (1 << var(k, j))))
    return m * h, cls

def tseitin(edges, nv, odd_vertex=0):
    cls = []
    for v in range(nv):
        inc = [e for e, (a, b) in enumerate(edges) if v in (a, b)]
        charge = 1 if v == odd_vertex else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge:  # forbid this assignment
                p = sum(1 << e for e, s in zip(inc, signs) if s == 0)
                q = sum(1 << e for e, s in zip(inc, signs) if s == 1)
                cls.append((p, q))
    return len(edges), cls

GRAPHS = {
 "K4": ([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)], 4),
 "K33": ([(a,b) for a in range(3) for b in range(3,6)], 6),
 "Prism": ([(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)], 6),
 "Q3": ([(a, a ^ (1 << k)) for a in range(8) for k in range(3) if a < a ^ (1 << k)], 8),
}

if __name__ == "__main__":
    fam, par = sys.argv[1], sys.argv[2]
    n, cls = php(int(par)) if fam == "php" else tseitin(*GRAPHS[par])
    t = time.time(); L, states = solve(n, cls)
    enc = sum(bin(p | q).count("1") for p, q in cls)  # literal occurrences
    print(json.dumps({"family": fam, "param": par, "vars": n, "clauses": len(cls),
        "literal_occurrences": enc, "min_leaves": L, "min_treeres_size": 2 * L - 1,
        "memo_states": states, "seconds": round(time.time() - t, 2)}))
