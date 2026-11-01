# Exact minimum #gates (fan-in 2, all 16 binary gates) for every n-var function, n<=3, by BFS over sets of computed truth tables.
import itertools,json,sys
def run(n):
    N=1<<n; M=(1<<N)-1
    vars_=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    base=frozenset([0,M]+vars_)  # constants & inputs free
    gates=[lambda a,b,t=t:sum(1<<k for k in range(0,0) ) for t in []]
    def ops(a,b):
        r=set()
        for t in range(16):
            v=0
            for (x,y,bit) in ((a,b,0),(~a&M,b,0)): pass
            out=0
            # evaluate gate t pointwise
            for p in range(N):
                xa=(a>>p)&1; yb=(b>>p)&1
                if (t>>(2*xa+yb))&1: out|=1<<p
            r.add(out)
        return r
    best={f:None for f in range(M+1)}
    for f in base: best[f]=0
    frontier=[base]; k=0
    seen={base}
    while any(v is None for v in best.values()) and k<8:
        k+=1; nxt=[]
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for o in ops(a,b):
                    if o in S: continue
                    T=S|{o}
                    if T in seen: continue
                    seen.add(T); nxt.append(T)
                    if best[o] is None: best[o]=k
        frontier=nxt
    from collections import Counter
    return dict(sorted(Counter(best.values()).items()))
for n in (1,2,3): print(n,run(n)); sys.stdout.flush()
