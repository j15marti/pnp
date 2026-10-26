"""Exact minimum B2 circuit size (2-input gates, all 16 ops, fan-out free) for all
n-variable functions, n=1..3, by BFS over sets of computed functions.
Wires = 2*gates (every gate has two incoming wires; inputs/constants free)."""
import json, itertools, sys, time
def run(n, tlimit=25):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[lambda x,y,t=t:(  (M&~x&~y if t&1 else 0)|(M&~x&y if t&2 else 0)|(M&x&~y if t&4 else 0)|(x&y if t&8 else 0)) for t in range(16)]
    best={0:0,M:0}
    for f in inputs: best[f]=0
    start=frozenset(inputs); frontier={start}; seen={start}; d=0; t0=time.time()
    while frontier and time.time()-t0<tlimit and len(best)<1<<N:
        d+=1; nxt=set()
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                for t in range(1,15):
                    h=ops[t](a,b)
                    if h in S or h==0 or h==M: continue
                    if h not in best: best[h]=d
                    T=S|{h}
                    if T not in seen: seen.add(T); nxt.add(T)
        frontier=nxt
    complete=len(best)==1<<N
    hist={}
    for v in best.values(): hist[v]=hist.get(v,0)+1
    return dict(n=n,complete=complete,depth_reached=d,hist=dict(sorted(hist.items())),
                maxgates=max(best.values()) if complete else None, funcs=len(best))
out=[run(n) for n in (1,2,3)]
json.dump(out,open('ladder_results.json','w'),indent=1); print(out)
