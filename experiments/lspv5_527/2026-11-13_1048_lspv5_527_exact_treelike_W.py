#!/usr/bin/env python3
"""LSPV-5/527: exact minimum tree-like resolution refutation size (free optimal
sequence, no search charge) for small UNSAT families.  Tree-like resolution
refutations of F with L leaves <-> decision trees for Search(F) with L leaves
(Beame-Pitassi / Krajicek), so min leaves = exact min_pi cost_R(pi) for R = tree-like
resolution.  Each instance is a separate stage (<=~30s), results appended to JSON.
Usage: python3 script.py <instance_name> <out.json>"""
import sys, json, time, itertools
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var p(i,j)
    v = lambda i, j: i * m + j + 1
    C = [tuple(v(i, j) for j in range(m)) for i in range(m + 1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m + 1), 2):
            C.append((-v(a, j), -v(b, j)))
    return C

def tseitin(edges, odd_vertex=0):
    verts = sorted({u for e in edges for u in e})
    C = []
    for x in verts:
        inc = [k + 1 for k, e in enumerate(edges) if x in e]
        charge = 1 if x == odd_vertex else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge:  # forbid assignments with wrong parity
                C.append(tuple(-l if s else l for l, s in zip(inc, signs)))
    return C

K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
K33 = [(a, b) for a in range(3) for b in range(3, 6)]
PRISM = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
CUBE = [(a, a ^ (1 << k)) for a in range(8) for k in range(3) if a < a ^ (1 << k)]
INST = {"PHP3_2": lambda: php(2), "PHP4_3": lambda: php(3),
        "TS_K4": lambda: tseitin(K4), "TS_K33": lambda: tseitin(K33),
        "TS_PRISM": lambda: tseitin(PRISM), "TS_CUBE": lambda: tseitin(CUBE),
        "FULL3": lambda: [tuple(s * (i + 1) for i, s in enumerate(sg)) for sg in itertools.product([1, -1], repeat=3)]}

def min_leaves(C):
    C = [frozenset(c) for c in C]
    @lru_cache(maxsize=None)
    def L(F):  # F: frozenset of residual clauses (frozensets)
        if frozenset() in F:
            return 1
        vs = {abs(l) for c in F for l in c}
        best = None
        for x in vs:
            tot = 0
            for lit in (x, -x):
                G = frozenset(c - {-lit} for c in F if lit not in c)
                tot += L(G)
                if best is not None and tot >= best: break
            if best is None or tot < best: best = tot
        return best
    r = L(frozenset(C)); return r, L.cache_info().currsize

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    C = INST[name](); t = time.time(); leaves, states = min_leaves(C)
    rec = {"instance": name, "vars": len({abs(l) for c in C for l in c}), "clauses": len(C),
           "width": max(map(len, C)), "min_treelike_leaves": leaves,
           "min_treelike_size": 2 * leaves - 1, "memo_states": states, "seconds": round(time.time() - t, 3)}
    try: data = json.load(open(out))
    except Exception: data = []
    data = [d for d in data if d["instance"] != name] + [rec]
    json.dump(data, open(out, "w"), indent=1, sort_keys=True); open(out, "a").write("\n")
    print(rec)
