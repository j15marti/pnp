"""Exact minimum AND-gate (AIG, free inverters) size of every n-input Boolean function, n<=3.
Wires = 2 per AND gate (fan-in 2); output is a literal (complement free).
State = frozenset of normalised node functions (bit 0 of truth table = 0). Depth-limited BFS.
Runs in a few seconds for n<=3."""
import json, sys, time
n = int(sys.argv[1]); N = 1 << n; FULL = (1 << N) - 1
def norm(f): return f ^ FULL if f & 1 else f
inputs = []
for i in range(n):
    t = 0
    for a in range(N):
        if (a >> i) & 1: t |= 1 << a
    inputs.append(t)
base = frozenset(norm(t) for t in inputs)
best = {0: 0}                       # constants
for t in inputs: best[norm(t)] = 0
level = {base}; seen = {base}; d = 0; t0 = time.time()
while len(best) < (1 << (N - 1)) and d < 8:
    d += 1; nxt = set()
    for S in level:
        L = list(S)
        for i in range(len(L)):
            for j in range(i, len(L)):
                for pa in (0, 1):
                    for pb in (0, 1):
                        a = L[i] ^ (FULL if pa else 0); b = L[j] ^ (FULL if pb else 0)
                        g = norm(a & b)
                        if g in S: continue
                        S2 = S | {g}
                        if S2 in seen: continue
                        seen.add(S2); nxt.add(S2)
                        if g not in best: best[g] = d
    level = nxt
    print(f"depth {d}: states {len(level)}, functions resolved {len(best)}/{1<<(N-1)}, {time.time()-t0:.1f}s", flush=True)
hist = {}
for f, k in best.items(): hist[k] = hist.get(k, 0) + 1
print("histogram gates->#functions (up to complement):", dict(sorted(hist.items())))
json.dump({"n": n, "max_gates": max(best.values()), "max_wires": 2 * max(best.values()),
           "hist_up_to_complement": dict(sorted(hist.items()))}, open(f"aig_n{n}.json", "w"), indent=1)
