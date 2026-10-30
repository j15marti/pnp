"""Exact min #gates (fan-in-2, all 16 binary gates, free inputs/constants) per Boolean function, n<=3.
BFS over sets of computed truth tables. Runs in seconds for n<=3."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
base=frozenset(inp+[0,M])
def binops(a,b):
    for g in range(16):
        r=0
        for k,(x,y) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (g>>k)&1:
                r|=(a if x else a^M)&(b if y else b^M)
        yield r
best={}  # function -> min gates
frontier={base}; seen={base}
for f in base: best[f]=0
d=0
while frontier and len(best)<=M:
    d+=1; nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for r in set(binops(a,b)):
                if r in S: continue
                T=S|{r}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if r not in best: best[r]=d
    frontier=nxt
    if len(best)==M+1: break
from collections import Counter
print(n,"max gates",max(best.values()),"dist",sorted(Counter(best.values()).items()))
