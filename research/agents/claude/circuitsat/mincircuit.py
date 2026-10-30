"""Exact minimum AND-gate count (free negation on wires/outputs) for all n-input
Boolean functions, n<=3, by BFS over sets of computed truth tables.
Wires counted = 2*gates (each gate has fan-in 2). Runs in a few seconds."""
import sys, json, itertools
n = int(sys.argv[1]); N = 1 << n; FULL = (1 << N) - 1
inputs = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    inputs.append(t)
canon = lambda t: min(t, FULL ^ t)
start = frozenset(canon(t) for t in inputs) | {0}   # const 0 free
best = {}                      # canon function -> min gates
level = {start}; seen = {start}
for f in start: best[f] = 0
g = 0
while level and len(best) < (1 << (N - 1)) + 0 or level and g < 0:
    g += 1; nxt = set()
    for S in level:
        L = list(S)
        for a, b in itertools.combinations_with_replacement(L, 2):
            for pa in (a, FULL ^ a):
                for pb in (b, FULL ^ b):
                    c = canon(pa & pb)
                    if c in S: continue
                    T = S | {c}
                    if T not in seen: seen.add(T); nxt.add(T)
                    if c not in best: best[c] = g
    level = nxt
    if len(best) == (1 << (N - 1)): break
hist = {}
for f, v in best.items(): hist[v] = hist.get(v, 0) + 2   # x2 for negations of f
print(json.dumps({"n": n, "max_gates": max(best.values()), "count_by_gates": hist,
                  "total_functions": sum(hist.values())}))
for name, tt in [("AND", 1 << (N-1)), ]:
    pass
xor = 0
for x in range(N):
    if bin(x).count("1") & 1: xor |= 1 << x
print("PARITY gates:", best[canon(xor)], "AND_n gates:", best[canon(1 << (N-1))])
