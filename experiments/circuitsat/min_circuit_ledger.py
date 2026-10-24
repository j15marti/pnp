"""Exact minimum fan-in-2 circuit size (basis B2, all 16 binary ops) for every
Boolean function on n<=3 inputs, by level-BFS over sets of computed truth tables.
Also reports, per function, number of essential inputs and size/formula data.
Runs in well under 30 s for n<=3 (n=4 deliberately NOT attempted: chunk needed)."""
import sys, json, itertools, time
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
inp = []
for i in range(n):
    t = 0
    for a in range(N):
        if (a >> i) & 1: t |= 1 << a
    inp.append(t)
# nondegenerate binary ops as functions on (x,y) truth tables
def ops(x, y):
    nx, ny = FULL ^ x, FULL ^ y
    return {x & y, x & ny, nx & y, nx & ny, x | y, x | ny, nx | y, nx | ny, x ^ y, FULL ^ (x ^ y)}
best = {0: 0, FULL: 0}
for t in inp: best[t] = 0; best[FULL ^ t] = 0
level = {frozenset(inp)}
t0 = time.time(); k = 0
seen = {frozenset(inp)}
while len(best) < (1 << N) and k < 8:
    k += 1; nxt = set()
    for S in level:
        L = list(S)
        for x, y in itertools.combinations(L, 2):
            for z in ops(x, y):
                if z in S or (FULL ^ z) in S: continue
                T = frozenset(S | {z})
                if T in seen: continue
                seen.add(T); nxt.add(T)
                for w in (z, FULL ^ z):
                    if w not in best: best[w] = k
    level = nxt
    print(f"size {k}: states={len(level)} functions_found={len(best)}/{1<<N} t={time.time()-t0:.1f}s", file=sys.stderr)
def essential(f):
    c = 0
    for i in range(n):
        if any(((f >> a) & 1) != ((f >> (a ^ (1 << i))) & 1) for a in range(N)): c += 1
    return c
rows = {}
for f, s in best.items():
    e = essential(f)
    rows.setdefault(e, {}).setdefault(s, 0); rows[e][s] += 1
summary = {"n": n, "max_size": max(best.values()),
           "by_essential_inputs": {str(e): {"count": sum(d.values()), "min_size": min(d), "max_size": max(d), "hist": {str(k): v for k, v in sorted(d.items())}} for e, d in sorted(rows.items())}}
print(json.dumps(summary, indent=1))
json.dump(summary, open(f"/home/user/pnp/experiments/circuitsat/ledger_n{n}.json", "w"), indent=1)
