"""Exact min DPLL decision-tree leaf count (= min tree-like resolution refutation
leaf count under the standard correspondence) for tiny UNSAT CNFs.
Each instance is a separate invocation (python3 script.py NAME) to keep each run < ~30 s.
Free choice of the branching sequence is granted (minimum over all trees)."""
import sys, json, time, itertools, random
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var p(i,j)
    v = lambda i, j: i * m + j + 1
    C = [[v(i, j) for j in range(m)] for i in range(m + 1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m + 1), 2):
            C.append([-v(a, j), -v(b, j)])
    return (m + 1) * m, C

def tseitin(edges, charge):
    n = len(edges); C = []
    verts = sorted({x for e in edges for x in e})
    for u in verts:
        inc = [k + 1 for k, e in enumerate(edges) if u in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge[u]:  # forbid assignments with wrong parity
                C.append([(-x if s else x) for x, s in zip(inc, signs)])
    return n, C

def rand3(n, m, seed):
    rnd = random.Random(seed)
    while True:
        C = [[x * rnd.choice([1, -1]) for x in rnd.sample(range(1, n + 1), 3)] for _ in range(m)]
        # keep the first sampled formula that brute force certifies UNSAT
        if not any(all(any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in C) for a in range(1 << n)):
            return n, C

def min_tree(n, C):
    cl = [(sum(1 << (abs(l) - 1) for l in c if l > 0), sum(1 << (abs(l) - 1) for l in c if l < 0)) for c in C]
    full = (1 << n) - 1
    @lru_cache(maxsize=None)
    def f(set_mask, val):  # val bits valid where set_mask
        for pos, neg in cl:
            if (pos | neg) & ~set_mask == 0 and (pos & val) == 0 and (neg & val) == neg:
                return 1
        best = None
        for x in range(n):
            b = 1 << x
            if set_mask & b: continue
            s = f(set_mask | b, val) 
            if best is not None and s >= best: continue
            s += f(set_mask | b, val | b)
            if best is None or s < best: best = s
        return best
    return f(0, 0), f.cache_info().currsize

INST = {
    'PHP_2_1': lambda: php(1), 'PHP_3_2': lambda: php(2), 'PHP_4_3': lambda: php(3),
    'TSEITIN_K4_odd': lambda: tseitin([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)], {0:1,1:0,2:0,3:0}),
    'TSEITIN_K33_odd': lambda: tseitin([(a,b) for a in range(3) for b in range(3,6)], {0:1,1:0,2:0,3:0,4:0,5:0}),
    'RAND3_n8_m48_s1': lambda: rand3(8, 48, 1), 'RAND3_n10_m60_s1': lambda: rand3(10, 60, 1),
}
if __name__ == '__main__':
    name = sys.argv[1]; t = time.time(); n, C = INST[name]()
    leaves, states = min_tree(n, C)
    print(json.dumps({'instance': name, 'vars': n, 'clauses': len(C), 'min_leaves': leaves,
                      'memo_states': states, 'seconds': round(time.time() - t, 2)}))
