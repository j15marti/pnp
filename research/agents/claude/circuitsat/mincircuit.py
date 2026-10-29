"""Exact minimum gate count C(f) over the full binary basis B2 (fan-in 2, inputs free,
negation free via B2) for all f on n<=3 variables, by BFS over sets of computed truth tables.
Wires = 2*gates (+1 output tap). Also counts SAT-relevant statistics. Runs < 30 s."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in range(16)]
    start=frozenset(inputs+[0,M])
    best={}  # function -> min gates
    seen={start:0}; frontier=[start]
    for f in start: best.setdefault(f,0)
    k=0
    while frontier and k<6:
        k+=1; nxt=[]
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                for op in ops:
                    g=op(a,b)
                    if g in S: continue
                    T=S|{g}
                    if T not in seen:
                        seen[T]=k; nxt.append(T); best.setdefault(g,k)
        frontier=nxt
        if len(best)==1<<N: break
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    hist={}
    for f,c in b.items(): hist[c]=hist.get(c,0)+1
    out[n]={"covered":len(b),"total":1<<N,"hist":hist,"maxC":max(b.values())}
    print(n,out[n])
json.dump(out,open("mincircuit_results.json","w"),indent=1)
