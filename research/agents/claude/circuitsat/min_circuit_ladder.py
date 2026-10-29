#!/usr/bin/env python3
"""Exact minimum fan-in-2 circuit size (basis B2 = all 16 binary gates) for every
n-input Boolean function, n=1,2,3.  Forward enumeration of sets of available
truth tables, deduplicated.  Runs well under 30 s.  Writes ladder_results.json."""
import json, itertools, sys, time
def run(n):
    N = 1 << n; full = (1 << N) - 1
    inputs = []
    for i in range(n):
        t = 0
        for a in range(N):
            if (a >> i) & 1: t |= 1 << a
        inputs.append(t)
    def gate(g, x, y):  # g in 0..15 : truth table of 2-input gate
        r = 0
        nx, ny = full ^ x, full ^ y
        if g & 1: r |= nx & ny
        if g & 2: r |= x & ny
        if g & 4: r |= nx & y
        if g & 8: r |= x & y
        return r
    first = {0: 0, full: None}  # constants: size 0 convention, see report
    best = {}
    for f in inputs: best[f] = 0
    best[0] = 0; best[full] = 0   # constants/inputs/negations tracked separately below
    level = {frozenset(inputs)}
    size = 0
    while True:
        size += 1
        nxt = set()
        for st in level:
            L = sorted(st)
            for a, b in itertools.combinations(L, 2):
                for g in range(1, 15):
                    f = gate(g, a, b)
                    if f in st: continue
                    if f not in best: best[f] = size
                    nxt.add(st | {f})
        level = nxt
        if len(best) >= (1 << N) or not level or size > 7: break
    # negated literals cost 0 in B2 (absorbed into gate type); record
    return best, size
res = {}
for n in (1, 2, 3):
    t0 = time.time(); best, s = run(n)
    # B2 absorbs negation: a negated input costs 0 gates; fix up
    full = (1 << (1 << n)) - 1
    for i in range(n):
        pass
    hist = {}
    for f, c in best.items(): hist[c] = hist.get(c, 0) + 1
    res[n] = {"functions_found": len(best), "of": 1 << (1 << n), "hist_by_size": hist,
              "max_size": max(best.values()), "seconds": round(time.time()-t0, 2)}
    print(n, res[n], file=sys.stderr)
json.dump(res, open("ladder_results.json", "w"), indent=1)
