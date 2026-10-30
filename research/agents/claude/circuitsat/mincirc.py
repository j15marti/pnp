"""Exact minimum B2 (all 2-input gates) circuit size for every n-variable function, n<=3.
State = frozenset of available truth tables; BFS by number of gates. Runs in a few seconds.
Also records min #wires = 2*gates (fan-in 2, gate inputs only) and the hardest function per n."""
import json, itertools, sys
def run(n, maxg):
    N = 1 << n; full = (1 << N) - 1
    ins = []
    for i in range(n):
        t = 0
        for a in range(N):
            if (a >> i) & 1: t |= 1 << a
        ins.append(t)
    # 2-input ops as 4-bit tables over (x,y); exclude constants & projections (useless)
    ops = [o for o in range(16) if o not in (0, 15, 3, 5, 10, 12)]
    def ap(o, x, y):
        r = 0
        nx, ny = full ^ x, full ^ y
        if o & 1: r |= nx & ny
        if o & 2: r |= x & ny
        if o & 4: r |= nx & y
        if o & 8: r |= x & y
        return r
    best = {}
    for t in ins + [0, full]: best[t] = 0
    for t in ins: best[full ^ t] = 0  # negation free as output
    start = frozenset(ins)
    layer = {start}; seen = {start}
    for g in range(1, maxg + 1):
        nxt = set()
        for S in layer:
            L = sorted(S)
            for x, y in itertools.combinations(L, 2):
                for o in ops:
                    z = ap(o, x, y)
                    if z in S: continue
                    T = S | {z}
                    if T in seen: continue
                    seen.add(T); nxt.add(T)
                    for w in (z, full ^ z):
                        if w not in best: best[w] = g
        layer = nxt
        print(f"n={n} gates={g} states={len(layer)} classified={len(best)}/{1<<N}", file=sys.stderr)
        if len(best) == (1 << N): break
    return best
out = {}
for n, mg in ((1, 1), (2, 2), (3, 4)):
    b = run(n, mg)
    hist = {}
    for v in b.values(): hist[v] = hist.get(v, 0) + 1
    out[n] = {"complete": len(b) == 1 << (1 << n), "hist": hist, "max_gates": max(b.values())}
    pt = [b[1 << a] for a in range(1 << n)]  # point functions
    out[n]["point_function_gates"] = pt[0]
json.dump(out, open("mincirc_results.json", "w"), indent=1)
print(out)
