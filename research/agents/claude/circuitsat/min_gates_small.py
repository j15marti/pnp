"""Exact minimum B2 fan-in-2 gate counts (wires = 2*gates) for all n<=3 input functions.
BFS over sets of available truth tables; runs in a few seconds."""
import json, itertools, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
inputs = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    inputs.append(t)
ops = [lambda a, b, k=k: sum((((k >> (2*((a>>x)&1)+((b>>x)&1))) & 1) << x) for x in range(N)) for k in range(16)]
best = {}
for t in inputs + [0, FULL]: best[t] = 0
frontier = {frozenset(inputs)}
g = 0
while frontier and len(best) < (1 << N):
    g += 1; nxt = set()
    for S in frontier:
        L = sorted(S)
        for a, b in itertools.combinations(L, 2):
            for k in range(16):
                t = ops[k](a, b)
                if t not in S:
                    if t not in best: best[t] = g
                    nxt.add(S | {t})
    frontier = nxt
    print("gates", g, "functions found", len(best), "states", len(frontier), file=sys.stderr)
    if g >= 5 or len(frontier) > 400000: break
hist = {}
for t, c in best.items(): hist[c] = hist.get(c, 0) + 1
print(json.dumps({"n": n, "found": len(best), "of": 1 << N, "histogram_gates": hist}))
