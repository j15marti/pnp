"""Exact minimum B2-circuit size (2-input gates, free negation) for all n-variable functions, n<=3.
Gate = AND with optional negation of each input and output, or XOR/XNOR.  Wires = 2*gates (fan-in 2).
Usage: python3 mincircuit.py N   (N in 1,2,3)   Runtime well under 30 s for N<=3."""
import sys, json, itertools
n = int(sys.argv[1]); M = 1 << n; FULL = (1 << M) - 1
X = []
for i in range(n):
    t = 0
    for a in range(M):
        if (a >> i) & 1: t |= 1 << a
    X.append(t)
def gates(a, b):
    na, nb = a ^ FULL, b ^ FULL
    return {a & b, a & nb, na & b, na & nb, a ^ b}   # output negation handled by complement-closure
base = frozenset(X)
cost = {}
def norm(f): return f
for f in list(X) + [f ^ FULL for f in X] + [0, FULL]: cost[f] = 0
level = {base}
k = 0
seen_states = {base}
while len(cost) < (1 << M):
    k += 1
    nxt = set()
    for st in level:
        L = list(st)
        for a, b in itertools.combinations(L, 2):
            for g in gates(a, b):
                for h in (g, g ^ FULL):
                    if h not in cost: cost[h] = k
                ns = st | {g}
                if len(ns) > len(st): nxt.add(ns)
    nxt -= seen_states; seen_states |= nxt; level = nxt
hist = {}
for f, c in cost.items(): hist[c] = hist.get(c, 0) + 1
out = {"n": n, "histogram_gates": hist, "max_gates": max(hist), "max_wires": 2 * max(hist)}
# parity and AND_n costs
par = 0
for a in range(M):
    if bin(a).count("1") % 2: par |= 1 << a
andn = 1 << (M - 1)
out["cost_parity"] = cost[par]; out["cost_AND"] = cost[andn]
print(json.dumps(out))
