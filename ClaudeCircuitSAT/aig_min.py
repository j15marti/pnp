# Exact minimum AND-inverter-graph (fan-in 2, free negation) size for all n<=3 functions.
# Cost = #AND gates g; wires = 2g (+1 output edge). Level-by-level exact search by DP over
# function SETS reachable with g gates (BFS on sets of available tables), canonical-ordered.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
best={0:0,M:0}
for t in inputs: best[t]=0; best[M^t]=0
GSEEN=set()
def rec(avail,g,maxg):
    if g==maxg: return
    seen=set()
    lits=[]
    for t in avail: lits+= [t,M^t]
    lits=sorted(set(lits))
    for a,b in itertools.combinations_with_replacement(lits,2):
        r=a&b
        for f in (r,M^r):
            if f in avail: continue
            if f not in best or best[f]>g+1: best[f]=g+1
            key=(tuple(sorted(avail|{f})))
            if key in seen or key in GSEEN: continue
            seen.add(key); GSEEN.add(key)
            rec(avail|{f},g+1,maxg)
rec(frozenset(inputs),0,int(sys.argv[2]))
from collections import Counter
print(n,len(best),N and 1<<N,Counter(best.values()))
json.dump({str(k):v for k,v in best.items()},open(f"aig_n{n}.json","w"))
# functions needing all n inputs
def dep(f,i): return any(((f>>x)&1)!=((f>>(x^(1<<i)))&1) for x in range(N))
full=[f for f in best if all(dep(f,i) for i in range(n))]
print("depends-on-all:",len(full),Counter(best[f] for f in full))
