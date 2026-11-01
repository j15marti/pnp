#!/usr/bin/env python3
"""Wire ledger: min #wires (sum of gate fan-ins) for every Boolean function of n<=3 inputs,
basis {AND,OR,NOT} fan-in<=2, inputs/constants free.  Tree (formula) cost by DP; DAG cost
by exact Dijkstra over sets of available functions (n<=2 fully, n=3 up to cost cap)."""
import sys, json, heapq, itertools
def run(n, dag_cap):
    N=1<<n; M=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    base={0:0,M:0}
    for v in ins: base[v]=0
    # tree cost: T[f]=min wires of formula
    T=dict(base)
    ch=True
    while ch:
        ch=False
        items=list(T.items())
        for f,c in items:
            g=M^f; 
            if T.get(g,99)>c+1: T[g]=c+1; ch=True
        for (f,c),(g,d) in itertools.product(items,items):
            for h in (f&g,f|g):
                if T.get(h,99)>c+d+2: T[h]=c+d+2; ch=True
    # DAG cost via Dijkstra on frozensets (inputs implicit)
    start=frozenset(base); best={start:0}; pq=[(0,0,start)]; D={}; cnt=0
    while pq:
        c,_,S=heapq.heappop(pq)
        if best.get(S,99)<c: continue
        for f in S:
            if f not in D or D[f]>c: D[f]=c
        if len(D)==(1<<N): break
        if c+1>dag_cap: continue
        L=list(S); new=[]
        for f in L: new.append((M^f,1))
        for i,f in enumerate(L):
            for g in L[i:]:
                new.append((f&g,2)); new.append((f|g,2))
        for h,w in new:
            if h in S or c+w>dag_cap: continue
            S2=S|{h}
            if best.get(S2,99)>c+w:
                best[S2]=c+w; cnt+=1; heapq.heappush(pq,(c+w,cnt,S2))
    return T,D
out={}
for n,cap in ((1,6),(2,10),(3,12)):
    T,D=run(n,cap)
    N=1<<n
    hist={}
    for f in range(1<<N):
        hist.setdefault(T[f],0); hist[T[f]]+=1
    dh={}
    for f,c in D.items(): dh[c]=dh.get(c,0)+1
    out[n]={"tree_hist":dict(sorted(hist.items())),"dag_hist_upto_cap":dict(sorted(dh.items())),"dag_found":len(D),"total":1<<N,"tree_max":max(T.values()),"cap":cap}
    print(n,out[n],flush=True)
json.dump(out,open("wire_ledger_results.json","w"),indent=1)
