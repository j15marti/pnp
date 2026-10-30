"""Exact minimum gate counts (fan-in 2, full binary basis B2) via BFS over sets of computed truth tables.
Wires = 2*gates (each gate has two in-wires; fan-out edges counted at the consumer). Usage: python3 mincircuit.py n gmax"""
import sys, json
n=int(sys.argv[1]); gmax=int(sys.argv[2]); N=1<<(1<<n); full=N-1
X=[]
for i in range(n):
    t=0
    for r in range(1<<n):
        if (r>>i)&1: t|=1<<r
    X.append(t)
# 16 binary ops as (a,b)->tt via 4-bit code
def ops(a,b):
    na,nb=full^a,full^b
    q=[na&nb,na&b,a&nb,a&b]
    res=set()
    for c in range(16):
        t=0
        for k in range(4):
            if (c>>k)&1: t|=q[k]
        res.add(t)
    return res
best={}  # function -> min gates
for t in X+[0,full]: best[t]=0
frontier={tuple(sorted(X))}
seen=set(frontier)
for g in range(1,gmax+1):
    new=set()
    for st in frontier:
        L=list(st)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for t in ops(L[i],L[j]):
                    if t in st: continue
                    s=tuple(sorted(st+(t,)))
                    if s in seen: continue
                    seen.add(s); new.add(s)
                    for u in (t,full^t):
                        if u not in best: best[u]=g
    frontier=new
    print("g",g,"states",len(new),"funcs",len(best),flush=True)
from collections import Counter
print(sorted(Counter(best.values()).items()), "of", N)
