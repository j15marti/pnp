"""Exact minimum B2-circuit size (fan-in-2 gates, all 16 binary ops, free output negation
via the 16 ops) of every n-input Boolean function, n<=3, by DP over gate counts.
Chunking: n=1,2,3 each run in well under 30 s. Output: JSON on stdout."""
import json, sys, itertools
def run(n):
    N=1<<n; mask=(1<<N)-1
    var=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    consts=[0,mask]
    # cost via Knuth-style: best[f]=min gates; iterate closure on formulas-with-sharing is hard;
    # use exact search over circuits as sets of computed functions (BFS on sets, n<=3 feasible)
    ops=[(lambda a,b,t=t:sum(1<<k for k in range(4) if (t>>k)&1 and False)) for t in range(0)]
    def combine(a,b,t):
        r=0
        # t bit (2*abit+bbit)
        for tt in range(4):
            if (t>>tt)&1:
                am = a if (tt>>1)&1 else ~a&mask
                bm = b if tt&1 else ~b&mask
                r |= am&bm
        return r
    start=frozenset(var+consts)
    best={f:0 for f in start}
    frontier={start}; seen={start}
    g=0
    while len(best)<(1<<N) and g<8:
        g+=1; nxt=set()
        for S in frontier:
            L=list(S)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    for t in range(1,15):
                        h=combine(L[i],L[j],t)
                        if h in S: continue
                        T=S|{h}
                        if T in seen: continue
                        seen.add(T); nxt.add(T)
                        if h not in best: best[h]=g
        frontier=nxt
    hist={}
    for f,c in best.items(): hist[c]=hist.get(c,0)+1
    return {"n":n,"functions":len(best),"hist":dict(sorted(hist.items())),"max":max(best.values())}
n=int(sys.argv[1]); print(json.dumps(run(n)))
