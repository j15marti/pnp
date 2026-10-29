"""Exact minimum B2 circuit size (fan-in-2 gates) for all n-input Boolean functions, n<=3.
Iterative-deepening DFS over gate sequences; truth tables as ints. Runs in a few seconds."""
import json, sys, itertools
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
def var(i): return sum(1 << x for x in range(N) if (x >> i) & 1)
ins = [var(i) for i in range(n)]
OPS = [lambda a, b, m=m: sum(1 << k for k in range(4) if (m >> k) & 1 and 0) for m in range(0)]
def apply(m, a, b, mask=FULL):  # m: 4-bit table over (a,b)
    r = 0
    if m & 1: r |= ~a & ~b
    if m & 2: r |= a & ~b
    if m & 4: r |= ~a & b
    if m & 8: r |= a & b
    return r & mask
MS = [m for m in range(1, 15) if m not in (3, 5, 10, 12)]  # genuinely 2-ary
best = {}
def reach(depth):
    seen = set()
    def rec(tabs, d):
        key = (tuple(sorted(tabs)), d)
        for t in tabs[n:]:
            if t not in best or best[t] > len(tabs) - n: best[t] = len(tabs) - n
        if d == 0: return
        if key in seen: return
        seen.add(key)
        L = len(tabs)
        for i in range(L):
            for j in range(i + 1, L):
                for m in MS:
                    t = apply(m, tabs[i], tabs[j])
                    if t in tabs: continue
                    rec(tabs + [t], d - 1)
    rec(list(ins), depth)
rec_depth = {2: 1, 3: 4}[n]
reach(rec_depth)
for t in [0, FULL] + ins + [FULL ^ v for v in ins]: best[t] = 0
res = {}
for f in range(1 << N):
    res[f] = best.get(f)
from collections import Counter
dist = Counter(v for v in res.values())
print(n, "distribution (gates:count):", dict(sorted(dist.items(), key=lambda kv: (kv[0] is None, kv[0]))))
json.dump({"n": n, "dist": {str(k): v for k, v in dist.items()}}, open(f"exact_min_n{n}.json", "w"), indent=1)
