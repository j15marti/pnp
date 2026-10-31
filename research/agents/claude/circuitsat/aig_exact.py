"""Exact minimum AIG size (2-input AND gates, free negation) for all n<=3 functions.
Iterative-deepening over circuits with sharing. Runs < 30 s."""
import sys, json, itertools
n = int(sys.argv[1]) if len(sys.argv)>1 else 3
N = 1<<n; FULL=(1<<N)-1
inputs=[]
for i in range(n):
    t=0
    for a in range(N):
        if (a>>i)&1: t|=1<<a
    inputs.append(t)
best={0:0,FULL:0}
for t in inputs: best[t]=0; best[FULL^t]=0
def norm(t): return min(t,FULL^t)
# DFS: signals list; extend by AND of two literals; record min gates for every reached function
LIMIT=int(sys.argv[2]) if len(sys.argv)>2 else 6
seen=set()
def rec(sigs,k):
    key=(frozenset(norm(s) for s in sigs))
    if (key,k) in seen: return
    seen.add((key,k))
    if k==LIMIT: return
    lits=[]
    for s in sigs: lits += [s,FULL^s]
    new=set()
    for a,b in itertools.combinations(lits,2):
        g=a&b
        if norm(g) in key: continue
        new.add(norm(g))
    for g in new:
        for v in (g,FULL^g):
            if v not in best or best[v]>k+1: best[v]=k+1
        rec(sigs+[g],k+1)
rec(list(inputs),0)
cls={}
for t in range(1<<N):
    if t in best: cls[t]=best[t]
miss=(1<<N)-len(cls)
byk={}
for t,k in cls.items(): byk.setdefault(k,[]).append(t)
print("n",n,"limit",LIMIT,"functions found",len(cls),"of",1<<N)
for k in sorted(byk): print(k,len(byk[k]))
# unique-SAT (exactly one satisfying assignment) minimum
us=[k for t,k in cls.items() if bin(t).count("1")==1]
print("unique-sat min gates",min(us),"max",max(us))
