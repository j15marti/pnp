"""Exact B2 circuit size (fan-in-2 gates, all 16 binary ops, free output negation) for all n-var functions, n<=3.
Wires = 2*gates (every gate has 2 in-edges). Level-wise BFS over sets of computed truth tables, deduplicated. Runs in seconds."""
import itertools, json, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
inputs = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    inputs.append(t)
def ops(a, b):
    na, nb = FULL ^ a, FULL ^ b
    return {a & b, a & nb, na & b, na & nb, a ^ b} | {FULL ^ v for v in (a & b, a & nb, na & b, na & nb, a ^ b)}
canon = lambda t: min(t, FULL ^ t)   # output negation is free
best = {canon(0): 0}
for t in inputs: best.setdefault(canon(t), 0)
level = {frozenset(inputs)}
g = 0
while len(best) < (FULL + 2) // 2 and g < 8:
    g += 1; nxt = set()
    for S in level:
        for a, b in itertools.combinations(sorted(S), 2):
            for t in ops(a, b):
                if t in S: continue
                nxt.add(S | {t})
                best.setdefault(canon(t), g)
    level = nxt
    print("gates", g, "states", len(level), "functions solved", len(best), flush=True)
from collections import Counter
dist = Counter(best.values())
print(json.dumps({"n": n, "max_gates": max(best.values()), "max_wires": 2 * max(best.values()), "dist_up_to_negation": dict(sorted(dist.items()))}))
