"""Exact minimum fan-in-2 circuit size over the full binary basis B2 (inputs and
negations free) for ALL n-variable Boolean functions, n=1..3.  BFS over sets of
computed truth tables.  Runs in well under 30s for n<=3.
Usage: python3 min_circuit.py [n]"""
import sys, json, itertools
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = 1 << n; FULL = (1 << M) - 1
def var(i):
    return sum(1 << x for x in range(M) if (x >> i) & 1)
inputs = [var(i) for i in range(n)]
# 'free negation': closed under complement, so store canonical rep min(t, ~t)
canon = lambda t: min(t, FULL ^ t)
def combos(a, b):
    out = set()
    for A in (a, FULL ^ a):
        for B in (b, FULL ^ b):
            out.add(canon(A & B))          # AND/OR/NAND/... all reduce to AND up to negations
            out.add(canon(A ^ B))          # XOR/XNOR
    return out
start = frozenset(canon(v) for v in inputs)
best = {}                                   # function (canon) -> min gates
for t in range(1 << M): pass
for t in start: best[t] = 0
best[0] = 0                                 # constants cost 0
layer = {start}; seen = {start}; k = 0
while layer and len(best) < (1 << (M - 1)):
    k += 1; nxt = set()
    for S in layer:
        L = list(S)
        for a, b in itertools.combinations(L, 2):
            for t in combos(a, b):
                if t in S: continue
                T = S | {t}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if t not in best: best[t] = k
    layer = nxt
hist = {}
for f, c in best.items(): hist[c] = hist.get(c, 0) + 2
print(json.dumps({"n": n, "functions_total": 1 << M, "classes_up_to_negation": len(best),
                  "histogram_gates_to_functions": dict(sorted(hist.items())),
                  "max_gates": max(best.values())}))
