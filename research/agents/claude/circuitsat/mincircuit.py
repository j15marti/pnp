# Min #gates (fan-in-2 AND/OR gates, free negation on wires) for all n-input functions, n<=3, by BFS over sets of computed truth tables.
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
base=frozenset([0,M]+inputs+[M^v for v in inputs])
def close(s): return s|{M^v for v in s}
best={}  # function -> min gates
level={base:0}; frontier=[base]; seen={base}
for v in base: best.setdefault(v,0)
g=0
while len(best)<(1<<N) and g<10:
    g+=1; nxt=[]
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for v in (a&b,a|b):
                if v in S: continue
                T=frozenset(S|{v,M^v})
                if T in seen: continue
                seen.add(T); nxt.append(T)
                for w in (v,M^v): best.setdefault(w,g)
    frontier=nxt
from collections import Counter
print(n,sorted(Counter(best.values()).items()),"max",max(best.values()))
