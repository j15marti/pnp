# Exact min B2 gate count (fan-in 2, all 16 binary gates; wires=2*gates) for all n-variable functions, n<=3.
# Also: sat-instance count ladder. Runs in seconds.
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    ops=[(lambda a,b,t=t: sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N))) for t in range(16)]
    best={0:0,M:0}
    for v in ins: best[v]=0
    # BFS by size: frontier of circuits as frozensets of computed functions
    level={frozenset(ins)}
    size=0
    seen_all=set(best)
    while len(best)<(1<<N):
        size+=1; nxt=set()
        for S in level:
            L=list(S)|[] if False else list(S)+[0,M]
            for a,b in itertools.combinations(L,2):
                for op in ops:
                    c=op(a,b)
                    if c not in S and c not in (0,M):
                        nxt.add(S|{c})
                        if c not in best: best[c]=size
        level=nxt
        if size>12: break
    hist={}
    for f,s in best.items(): hist[s]=hist.get(s,0)+1
    return dict(sorted(hist.items())), max(best.values())
out={}
for n in (1,2,3):
    out[n]=run(n); print(n,out[n])
json.dump({str(k):v for k,v in out.items()},open('ladder_results.json','w'))
