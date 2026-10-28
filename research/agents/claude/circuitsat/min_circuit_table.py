"""Exact minimum fan-in-2 circuit size (full binary basis B2, free negation) for
all Boolean functions on n<=3 variables, by iterative-deepening DFS.
Wires = 2*gates (every gate has fan-in 2; output wire not counted).
Runtime well under 30 s for n<=3. Usage: python3 min_circuit_table.py [n]"""
import sys, json, itertools
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
def var(i):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    return t
base = [var(i) for i in range(n)]
# B2 up to output negation: AND-type gates with input/output negations + XOR/XNOR
def ops(a, b):
    na, nb = FULL ^ a, FULL ^ b
    r = {a & b, a & nb, na & b, na & nb, a ^ b}
    r |= {FULL ^ v for v in r}
    return r
best = {}                       # function -> min size
best[0] = 0; best[FULL] = 0
for b in base: best[b] = 0; best[FULL ^ b] = 0
def dfs(sigs, depth_left, size):
    # record every signal (and its complement) at this size
    for s in sigs[n:]:
        for t in (s, FULL ^ s):
            if t not in best or best[t] > size: best[t] = size
    if depth_left == 0: return
    m = len(sigs)
    for i in range(m):
        for j in range(i + 1, m):
            for r in ops(sigs[i], sigs[j]):
                if r in sigs or (FULL ^ r) in sigs: continue
                dfs(sigs + [r], depth_left - 1, size + 1)
D = 0
total = 1 << N
while len(best) < total:
    D += 1
    dfs(list(base), D, 0)
# dfs above records size at the time of generation; exhaustive up to depth D
hist = {}
for f, s in best.items(): hist[s] = hist.get(s, 0) + 1
out = {"n": n, "num_functions": total, "max_size": max(best.values()),
       "histogram_size_to_count": dict(sorted(hist.items())),
       "max_wires_2x": 2 * max(best.values())}
print(json.dumps(out))
