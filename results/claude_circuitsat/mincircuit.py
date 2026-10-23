# Exact minimum gate count (fan-in-2, all 16 binary gates, sharing allowed) for all n-variable Boolean functions, n<=3.
# Level-BFS over sets of computed truth tables; runtime budget well under 30 s per n.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<(1<<n); M=N-1
inputs=[]
for i in range(n):
    t=0
    for x in range(1<<n):
        if (x>>i)&1: t|=1<<x
    inputs.append(t)
full=(1<<(1<<n))-1
def gates(a,b):
    out=set()
    for g in range(16):
        t=0
        for k,(u,v) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            if (g>>k)&1:
                ma = a if u else full^a
                mb = b if v else full^b
                t|=ma&mb
        out.add(t)
    return out
best={}   # function -> min gates
for f in [0,full]+inputs+[full^i for i in inputs]: best[f]=0
frontier={frozenset(inputs)}
seen=set(frontier)
for s in range(1,8):
    nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for t in gates(a,b):
                if t in S: continue
                T=S|{t}
                # canonicalise up to nothing (cheap); dedupe
                if T not in seen:
                    seen.add(T); nxt.add(T)
                    # t costs s gates; also complement is free in B2 (negation absorbed)
                    for u in (t,full^t):
                        if u not in best: best[u]=s
    frontier=nxt
    print(n,"level",s,"states",len(frontier),"known",len(best),file=sys.stderr)
    if len(best)>=N: break
    if len(seen)>400000: break
from collections import Counter
print(json.dumps({"n":n,"covered":len(best),"of":N,"hist":dict(Counter(best.values()))}))
