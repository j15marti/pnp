"""Exact minimum B2 (fan-in-2, all binary gates, free negation) circuit size C(f)
for all Boolean functions on n<=3 inputs, by exhaustive level-wise search.
Wires = 2*gates (every gate has fan-in 2; fan-out is free). Runs in <30 s."""
import json, sys, itertools
def run(n):
    M=1<<n; full=(1<<M)-1
    inputs=[sum(1<<x for x in range(M) if (x>>i)&1) for i in range(n)]
    # 10 nondegenerate binary ops as truth-table lambdas on (a,b) bitmasks
    def ops(a,b):
        na,nb=full^a,full^b
        return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,full^(a^b)}
    best={}  # f -> min gates
    for f in [0,full]+inputs+[full^i for i in inputs]: best[f]=0
    level={tuple(sorted(inputs))}
    k=0
    while len(best)<(1<<M):
        k+=1; nxt=set()
        for S in level:
            L=list(S)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    for g in ops(L[i],L[j]):
                        if g not in S:
                            if g not in best and g^full not in best: pass
                            for h in (g,g^full):
                                if h not in best: best[h]=k
                            nxt.add(tuple(sorted(S+(g,))) if False else tuple(sorted(set(S)|{g})))
        level=nxt
        if k>=6: break
    return best
out={}
for n in (1,2,3):
    b=run(n)
    dist={}
    for f,c in b.items(): dist[c]=dist.get(c,0)+1
    out[n]=dict(sorted(dist.items()))
    print(n,out[n],"functions",len(b))
json.dump(out,open("exact_small_results.json","w"),indent=1)
