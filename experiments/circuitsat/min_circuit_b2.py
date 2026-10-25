"""Exact minimum fan-in-2 circuit size (basis B2 = all 16 binary gates) for all
Boolean functions on n<=3 inputs. Wires = 2*gates (each gate has fan-in 2).
Iterative-deepening DFS over gate sequences with canonical ordering; <30 s."""
import sys, json, itertools
n = int(sys.argv[1]); N = 1 << n; M = (1 << N) - 1
inputs = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    inputs.append(t)
def gates(a, b):
    out = set()
    for g in range(16):
        r = 0
        for k, (u, v) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (g >> k) & 1:
                r |= (a if u else a ^ M) & (b if v else b ^ M)
        out.add(r)
    return out
# BFS over frozenset-of-computed-functions states, level = #gates
best = {}  # function -> min gates
for t in [0, M] + inputs + [i ^ M for i in inputs]: best[t] = 0
frontier = {frozenset(inputs)}
seen = {frozenset(inputs)}
for s in range(1, 8):
    nxt = set()
    for st in frontier:
        lst = list(st)
        for a, b in itertools.combinations(lst, 2):
            for r in gates(a, b):
                if r in st: continue
                for f in (r, r ^ M):
                    if f not in best: best[f] = s
                ns = st | {r}
                if ns not in seen:
                    seen.add(ns); nxt.add(ns)
    frontier = nxt
    print(s, len(frontier), len(best), file=sys.stderr)
    if len(best) == 1 << N: break
from collections import Counter
c = Counter(best.values())
print(json.dumps({"n": n, "gates_histogram": dict(sorted(c.items())),
                  "max_gates": max(best.values()), "max_wires": 2*max(best.values())}))
