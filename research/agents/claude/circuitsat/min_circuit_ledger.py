# Exact min #gates over full binary basis B2 (fan-in 2, free negation) for all n-var functions, n=2,3.
# Method: BFS over sets of computed truth tables (size-k circuits), runs <30s for n<=3.
import sys, json
from itertools import product
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>p)&1)+((b>>p)&1)))&1)<<p) for p in range(N)) for t in range(16)]
    best={0:0,M:0}
    for x in xs: best[x]=0; best[M^x]=0
    # frontier: states = frozenset of available tables; DFS iterative deepening per size
    seen_level={}
    level=[frozenset(xs)]
    size=0
    while len(best)<(1<<N) and size<8:
        size+=1; nxt=set()
        for S in level:
            L=list(S)
            for i in range(len(L)):
                for j in range(i,len(L)):
                    for op in ops:
                        f=op(L[i],L[j])
                        if f in S: continue
                        nxt.add(S|{f})
                        for g in (f,M^f):
                            if g not in best: best[g]=size
        level=list(nxt)
        print(n,size,len(level),len(best),file=sys.stderr)
    return best
out={}
for n in (2,3):
    b=run(n)
    dist={}
    for v in b.values(): dist[v]=dist.get(v,0)+1
    N=1<<n
    minterm=[b[1<<a] for a in range(N)]
    out[n]=dict(dist=dist,minterm_sizes=sorted(set(minterm)),covered=len(b))
print(json.dumps(out))
