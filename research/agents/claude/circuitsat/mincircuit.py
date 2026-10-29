"""Exact minimum B2 circuit size (gates; wires = 2*gates) for all n-input
functions, n<=3, by iterative-deepening DFS over sets of computed truth tables.
Runtime budget: < 30 s per n."""
import json, sys, itertools
n = int(sys.argv[1]); N = 1 << n; FULL = (1 << N) - 1
def var(i): return sum(1 << x for x in range(N) if (x >> i) & 1)
inputs = [var(i) for i in range(n)]
def gates(a, b):
    out = set()
    for g in range(16):  # all 2-input gates on truth tables
        t = 0
        for (u, v, bit) in ((~a & FULL, ~b & FULL, 0), (~a & FULL, b, 1), (a, ~b & FULL, 2), (a, b, 3)):
            if (g >> bit) & 1: t |= u & v
        out.add(t)
    return out
cost = {}
for f in (0, FULL, *inputs, *(~v & FULL for v in inputs)): cost[f] = 0
level = {tuple(sorted(inputs))}
seen = {tuple(sorted(inputs))}
k = 0
while len(cost) < (1 << N) and k < 8:
    k += 1; nxt = set()
    for st in level:
        for a, b in itertools.combinations(st, 2):
            for t in gates(a, b):
                if t in st: continue
                ns = tuple(sorted(st + (t,)))
                if ns not in seen: seen.add(ns); nxt.add(ns)
                for c in (t, ~t & FULL):
                    if c not in cost: cost[c] = k
    level = nxt
    print(n, "k", k, "states", len(level), "classified", len(cost), file=sys.stderr)
hist = {}
for f, c in cost.items(): hist[c] = hist.get(c, 0) + 1
res = {"n": n, "functions": len(cost), "max_gates": max(cost.values()), "histogram": hist,
       "AND_n": cost[inputs[0] if n == 1 else __import__('functools').reduce(lambda x, y: x & y, inputs)],
       "XOR_n": cost[__import__('functools').reduce(lambda x, y: x ^ y, inputs)]}
print(json.dumps(res))
