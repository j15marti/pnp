"""Exact minimum B2-circuit size for n-input Boolean functions (n=2,3), plus chosen n=4 targets.
Level-set BFS over sets of computed truth tables (inputs + gates), dedup by frozenset.
Wires = 2*gates (fan-in 2). Runs <30s per invocation: parameters n, maxg."""
import sys, json, itertools
n=int(sys.argv[1]); maxg=int(sys.argv[2])
N=1<<n; FULL=(1<<N)-1
ins=[]
for i in range(n):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    ins.append(t)
OPS=[lambda a,b,c=c:0 for c in range(0)]
def gates(a,b):
    na,nb=FULL^a,FULL^b
    return {a&b,a&nb,na&b,na&nb&FULL,a|b,a|nb,na|b,na|nb,a^b,FULL^(a^b)}
best={}  # tt -> min gates
for t in ins: best[t]=0
for t in (0,FULL): best[t]=0
frontier={frozenset(ins)}
seen={frozenset(ins)}
for g in range(1,maxg+1):
    new=set()
    for S in frontier:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for t in gates(a,b):
                if t in S or t in(0,FULL): continue
                T=S|{t}
                if T not in seen:
                    seen.add(T); new.add(T)
                if t not in best: best[t]=g
    frontier=new
    print("g",g,"sets",len(new),"functions found",len(best),file=sys.stderr)
    if len(best)==FULL+2 or len(best)>=(1<<N)  : break
json.dump({"n":n,"maxg":maxg,"best":{str(k):v for k,v in best.items()}},open(f"exact_n{n}.json","w"))
from collections import Counter
print(n,sorted(Counter(best.values()).items()), "complete" if len(best)==(1<<N) else "partial")
