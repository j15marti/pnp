"""Exact minimum AIG size (2-input AND, free negation on wires) for all
n-input Boolean functions, n<=3, by level-wise BFS over sets of computed
functions (stored up to complement).  Wires = 2*gates (fan-in 2).
Chunked: each n and depth cap run separately; well under 30 s."""
import sys, json, itertools
n = int(sys.argv[1]); cap = int(sys.argv[2])
N = 1 << n; FULL = (1 << N) - 1
def var(i):
    return sum(1 << x for x in range(N) if (x >> i) & 1)
def norm(t): return min(t, FULL ^ t)
start = frozenset(norm(var(i)) for i in range(n))
best = {norm(0): 0}
for s in start: best[s] = 0
level = {start}
for g in range(1, cap + 1):
    nxt = set()
    for st in level:
        fs = list(st)
        lits = fs + [FULL ^ f for f in fs]
        for a, b in itertools.combinations(lits, 2):
            t = norm(a & b)
            if t in st or t == 0: continue
            if t not in best: best[t] = g
            nxt.add(st | {t})
    level = nxt
    print(g, len(level), len(best), file=sys.stderr)
    if len(best) == (1 << N) // 2: break
cnt = {}
for t, g in best.items(): cnt[g] = cnt.get(g, 0) + 1
print(json.dumps({"n": n, "classes_by_complement": len(best), "of": (1 << N)//2,
                  "count_by_gates": cnt, "max_gates": max(best.values())}))
