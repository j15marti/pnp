"""Exact minimum B2 circuit size (gates; wires = 2*gates) for all n-variable functions, n<=3.
Level-wise BFS over sets of computed truth tables (deduplicated). Runs in a few seconds."""
import itertools, json, sys
def run(n, kmax):
    N = 1 << n; full = (1 << N) - 1
    inputs = []
    for i in range(n):
        t = 0
        for a in range(N):
            if (a >> i) & 1: t |= 1 << a
        inputs.append(t)
    ops = [lambda x,y:x&y, lambda x,y:x|y, lambda x,y:x^y, lambda x,y:(~x)&y&full,
           lambda x,y:x&(~y)&full, lambda x,y:(~(x&y))&full, lambda x,y:(~(x|y))&full,
           lambda x,y:(~(x^y))&full, lambda x,y:(~x|y)&full, lambda x,y:(x|~y)&full]
    best = {0:0, full:0}
    for t in inputs: best[t]=0; best[~t&full]=0   # free: inputs, negations, constants
    base = tuple(sorted(set(inputs)))
    level = {frozenset(base)}
    for k in range(1, kmax+1):
        nxt = set()
        for S in level:
            L = list(S)
            for x,y in itertools.combinations(L,2):
                for op in ops:
                    v = op(x,y)
                    if v in S: continue
                    nxt.add(S | {v})
                    for w in (v, ~v & full):
                        if w not in best: best[w]=k
        level = nxt
        print(f"n={n} k={k} states={len(level)} functions_reached={len(best)}", file=sys.stderr)
    return best, 1<<N
out={}
for n,kmax in ((2,2),(3,4)):
    best,tot = run(n,kmax)
    hist={}
    for v in best.values(): hist[v]=hist.get(v,0)+1
    out[n]={"total":tot,"reached":len(best),"gate_histogram":hist}
print(json.dumps(out))
