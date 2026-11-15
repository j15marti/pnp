#!/usr/bin/env python3
"""Exact minimum TREE-like Resolution length for proper (n-1)-CNF MUS on n vars (edge covers of Q_n).
Tree-like refutation <-> decision tree whose leaves are subcubes each inside one falsified edge.
DP over the 3^n subcubes. length = leaves - 1."""
import sys, json, time
from functools import lru_cache
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import qcube_min_resolution as q

def tree_len(edges, n):
    E = [frozenset(e) for e in edges]
    @lru_cache(maxsize=None)
    def leaves(fixmask, fixval):
        free = [i for i in range(n) if not fixmask >> i & 1]
        pts = set()
        for k in range(1 << len(free)):
            v = fixval
            for j, i in enumerate(free):
                if k >> j & 1: v |= 1 << i
            pts.add(v)
        if any(pts <= e for e in E): return 1
        return min(leaves(fixmask | 1 << i, fixval) + leaves(fixmask | 1 << i, fixval | 1 << i) for i in free)
    return leaves(0, 0) - 1

if __name__ == '__main__':
    n = int(sys.argv[1]); t0 = time.time()
    autos = q.automorphisms(n); vm = [[f(v) for v in range(1 << n)] for f in autos]
    covers = q.minimal_covers(n); seen = set(); rows = []
    for c in covers:
        if c in seen: continue
        orb = {frozenset(tuple(sorted((m[a], m[b]))) for a, b in c) for m in vm}; seen |= orb
        k = min(tuple(sorted(o)) for o in orb)
        rows.append({"mu": len(k), "tree": tree_len(k, n), "orbit": len(orb), "edges": [list(e) for e in k]})
    print(json.dumps({"n": n, "covers": len(covers), "classes": len(rows), "rows": rows, "sec": round(time.time() - t0, 2)}))
