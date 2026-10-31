# Exact min AND-inverter-graph size (free negation, free constants/inputs) for all n-input functions, n<=3.
# Iterative-deepening over sets of available functions (bitmask truth tables).
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
base=[0,M]+inputs+[M^x for x in inputs]
best={}
def closure_add(s,f): return s|{f,M^f}
def search(avail,k,depth,maxd):
    # avail: frozenset closed under negation
    for f in avail:
        if f not in best or best[f]>depth: best[f]=depth
    if depth==maxd: return
    L=sorted(avail); seen=set()
    for i,a in enumerate(L):
        for b in L[i:]:
            g=a&b
            if g in avail or g in seen: continue
            seen.add(g)
            search(avail|{g,M^g},k,depth+1,maxd)
maxd=int(sys.argv[2])
search(frozenset(base),0,0,maxd)
from collections import Counter
c=Counter(best.values()); print(n,maxd,len(best),"of",1<<N,dict(sorted(c.items())))
