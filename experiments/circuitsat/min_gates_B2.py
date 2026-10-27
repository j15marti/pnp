"""Exact minimum number of fan-in-2 gates (full basis B2, free negation of wires via gate choice)
for every Boolean function on n=1..3 inputs. BFS over sets of available truth tables.
Runs in a few seconds. Output: JSON on stdout."""
import json, itertools, sys
def run(n, maxg):
    N = 1 << n; M = (1 << N) - 1
    ins = []
    for i in range(n):
        t = 0
        for x in range(N):
            if (x >> i) & 1: t |= 1 << x
        ins.append(t)
    ops = [lambda a, b, k=k: sum((((k >> (2*((a>>x)&1) + ((b>>x)&1))) & 1) << x) for x in range(N)) for k in range(16)]
    # only nonconstant, non-projection ops matter: keep ops depending on both args
    def dep_both(k):
        b=lambda i:(k>>i)&1
        return (b(0)!=b(2) or b(1)!=b(3)) and (b(0)!=b(1) or b(2)!=b(3))
    ks = [k for k in range(16) if dep_both(k)]
    best = {}  # truth table -> min gates (functions incl. complements)
    start = frozenset(ins)
    for t in ins: best[t] = 0
    layer = {start}; seen = {start}
    for g in range(1, maxg + 1):
        nxt = set()
        for S in layer:
            L = sorted(S)
            for a, b in itertools.combinations(L, 2):
                for k in ks:
                    t = ops[k](a, b)
                    if t in S: continue
                    S2 = S | {t}
                    if S2 in seen: continue
                    seen.add(S2); nxt.add(S2)
                    if t not in best: best[t] = g
        layer = nxt
    return best
out = {}
for n, mg in [(1, 1), (2, 3), (3, 4)]:
    N = 1 << n; M = (1 << N) - 1
    best = run(n, mg)
    # functions: include constants (0 gates conceptually: cost 0, trivial), and complements of inputs cost 0
    cost = {}
    for t in range(1 << N):
        if t == 0 or t == M: cost[t] = 0
        else:
            c = [best[u] for u in (t, M ^ t) if u in best]
            cost[t] = min(c) if c else None
    hist = {}
    for c in cost.values(): hist[str(c)] = hist.get(str(c), 0) + 1
    out[str(n)] = hist
print(json.dumps(out, indent=1))
