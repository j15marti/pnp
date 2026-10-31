# Exact minimum B2 (all binary gates) circuit size for every n-input Boolean function, n<=3.
# Iterative deepening over sets of computed truth tables. Runtime < 30 s for n<=3.
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
ops=[lambda a,b,t=t:sum(((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x for x in range(N)) for t in range(16)]
# nontrivial gates only (depend on both inputs): 6 of 16
nontriv=[t for t in range(16) if len({(t>>0)&1,(t>>2)&1})==2 and len({(t>>0)&1,(t>>1)&1})==2]
best={}
for f in [0,M]+inp: best[f]=0
frontier={frozenset(inp)}; k=0
seen={frozenset(inp)}
while frontier and len(best)<(1<<N):
    k+=1; new=set()
    for S in frontier:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for t in nontriv:
                v=ops[t](a,b)
                if v in S: continue
                T=S|{v}
                if T in seen: continue
                seen.add(T); new.add(T)
                if v not in best: best[v]=k
    frontier=new
    print("k",k,"states",len(new),"known",len(best),flush=True)
from collections import Counter
c=Counter(best.values()); print(sorted(c.items()))
json.dump({"n":n,"hist":sorted(c.items()),"max_gates":max(best.values()),"max_wires":2*max(best.values())},open(f"minsize_n{n}.json","w"))
