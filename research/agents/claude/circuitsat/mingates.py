"""Exact min #2-input-gates (basis B2, all 16 binary gates) for all n-input functions, n<=3.
BFS over circuits via DP on 'set of computed truth tables' (shortest circuit = min gates).
Wires counted = 2*gates (+ nothing for output). Runs in a few seconds."""
import itertools, json, sys
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[lambda a,b,t=t:sum(((t>>(2*((a>>k)&1)+((b>>k)&1)))&1)<<k for k in range(N)) for t in range(16)]
# iterative deepening on sets of computed functions (canonical frozenset)
best={}
start=frozenset(inputs)
level={start}; seen={start}; g=0
cost={f:0 for f in inputs}; cost[0]=0; cost[M]=0
while level:
    g+=1; nxt=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                f=op(a,b)
                if f in S: continue
                T=S|{f}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if f not in cost: cost[f]=g
    level=nxt
    if len(cost)>=N and g>=1 and len(cost)==1<<N: break
    if g>int(sys.argv[2]): break
from collections import Counter
c=Counter(cost.values())
print(n,len(cost),"of",1<<N,"functions; max gates",max(cost.values()),dict(sorted(c.items())))
json.dump({"n":n,"hist":dict(sorted(c.items()))},open(f"mingates_n{n}.json","w"))
