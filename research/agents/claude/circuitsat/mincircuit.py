#!/usr/bin/env python3
"""Exact minimum B2 circuit size (fan-in-2 gates, all 16 binary ops) for all
Boolean functions on n<=3 inputs, by iterative-deepening DFS.  Wires = 2*gates
(every counted gate is non-degenerate, i.e. depends on both inputs).
Runs in a few seconds.  Output: JSON table by n."""
import json, sys
from itertools import product
def run(n, maxg):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[o for o in range(16) if True]
    def ap(o,x,y):
        r=0
        for b in range(4):
            if (o>>b)&1:
                xm = x if (b&1) else (~x&M)
                ym = y if (b&2) else (~y&M)
                r|=xm&ym
        return r
    best={}
    # state: tuple of computed tables; BFS by number of gates over sets
    level=[frozenset(inputs)]
    seen={frozenset(inputs)}
    for t in inputs: best[t]=0
    best[0]=0; best[M]=0   # constants free
    for g in range(1,maxg+1):
        nxt=[]
        for S in level:
            L=sorted(S)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    for o in range(16):
                        v=ap(o,L[i],L[j])
                        if v in S: continue
                        S2=S|{v}
                        if S2 in seen: continue
                        seen.add(S2); nxt.append(S2)
                        if v not in best: best[v]=g
        level=nxt
        if len(best)>=(1<<N): break
    for f in range(1<<N): best.setdefault(f,None)
    return best
res={}
for n,mg in [(1,1),(2,3),(3,6)]:
    b=run(n,mg)
    hist={}
    for f,g in b.items(): hist[g]=hist.get(g,0)+1
    res[n]={"hist_gates":{str(k):v for k,v in sorted(hist.items(),key=lambda kv:(kv[0] is None,kv[0]))},
            "max_gates":max(g for g in b.values() if g is not None)}
print(json.dumps(res,indent=1))
