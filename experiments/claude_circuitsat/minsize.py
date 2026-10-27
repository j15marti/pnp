# Exact minimum B2-circuit size (fan-in 2, all 16 binary gates, free negation) for all n-var functions, n<=3.
# Level-set BFS over sets of computed truth tables (state = frozenset of functions available), size<=S.
import json, itertools, sys
n=int(sys.argv[1]); N=1<<(1<<n); M=N-1
inputs=[sum(((r>>i)&1)<<r for r in range(1<<n)) for i in range(n)]
ops=[]
def comb(a,b):
    out=set()
    for t in range(16):
        v=0
        for r in range(1<<n):
            x=(a>>r)&1; y=(b>>r)&1
            if (t>>(2*x+y))&1: v|=1<<r
        out.add(v)
    return out
best={}
start=frozenset(inputs+[0,M])
best[start]=0
frontier={start}
mins={f:0 for f in start}
for s in range(1,8):
    nxt=set()
    for st in frontier:
        L=sorted(st)
        for a,b in itertools.combinations(L,2):
            for v in comb(a,b):
                if v not in st:
                    ns=st|{v}
                    if ns not in best:
                        best[ns]=s; nxt.add(ns)
                        if v not in mins: mins[v]=s
    frontier=nxt
    if len(mins)==N or not nxt or len(frontier)>400000: break
hist={}
for f,s in mins.items(): hist[s]=hist.get(s,0)+1
print(json.dumps({"n":n,"covered":len(mins),"of":N,"hist":dict(sorted(hist.items())),"lastlevel":s}))
