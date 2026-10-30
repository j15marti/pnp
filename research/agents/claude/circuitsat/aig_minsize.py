"""Exact minimum AIG size (2-input AND gates, free inverters) for all n-variable functions, n<=3.
Method: iterative deepening over circuits as sets of available truth tables (<=30s for n<=3)."""
import sys, json, itertools
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
inputs = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    inputs.append(t)
best = {}  # function (up to nothing) -> min gates; function and its complement share cost
def lits(sig):
    out = set()
    for t in sig: out.add(t); out.add(FULL ^ t)
    return out
def canon(t): return min(t, FULL ^ t)
best[0] = 0
for t in inputs: best[canon(t)] = 0
MAXG = int(sys.argv[2]) if len(sys.argv) > 2 else 6
seen = set()
def dfs(sig, g, limit):
    # sig: tuple of tables (inputs + gates), g gates used
    key = (frozenset(canon(t) for t in sig))
    if key in seen: return
    seen.add(key)
    c = canon(sig[-1]) if g else None
    if g:
        if c not in best or best[c] > g: best[c] = g
    if g == limit: return
    L = list(lits(sig))
    for a, b in itertools.combinations(L, 2):
        t = a & b
        if canon(t) in key: continue
        dfs(sig + (t,), g + 1, limit)
for limit in range(1, MAXG + 1):
    seen.clear()
    dfs(tuple(inputs), 0, limit)
    print("limit", limit, "functions(up to compl)", len(best), file=sys.stderr)
    if len(best) == (1 << (N - 1)): break
res = {}
for f in range(1 << N):
    c = canon(f); res[f] = best.get(c)
pt = {}
for f, g in res.items():
    pc = bin(f).count("1")
    if g is not None: pt.setdefault(pc, []).append(g)
summary = {k: {"min": min(v), "max": max(v)} for k, v in sorted(pt.items())}
print(json.dumps({"n": n, "max_gates": max(g for g in res.values() if g is not None),
                  "unresolved": sum(g is None for g in res.values()), "by_popcount": summary}))
