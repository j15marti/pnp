"""Exact minimum gate count (basis B2 = all 2-input gates, fan-in 2, wires=2*gates)
for every n-input Boolean function, n=1..3, by BFS over sets of computed truth tables.
Runs in a few seconds. Output: JSON histogram."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    ops=range(16)
    def ap(op,a,b):
        r=0
        for k,(p,q) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (op>>k)&1:
                r|=(a if p else a^M)&(b if q else b^M)
        return r
    # best[f]=min gates; DFS iterative deepening on circuits (sets of tables)
    best={0:0,M:0}
    for t in ins: best[t]=0; best[t^M]=0   # negation free in B2 (absorbed into gate)
    frontier={frozenset(ins)}
    g=0
    while len(best)<(1<<N):
        g+=1; nxt=set()
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                for op in ops:
                    c=ap(op,a,b)
                    if c in S: continue
                    nxt.add(S|{c})
                    if c not in best: best[c]=g
        frontier=nxt
    hist={}
    for f,v in best.items(): hist[v]=hist.get(v,0)+1
    return hist
out={n:run(n) for n in (1,2,3)}
print(json.dumps(out)); json.dump(out,open('min_circuit_b2_results.json','w'))
