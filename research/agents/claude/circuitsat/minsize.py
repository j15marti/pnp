# Exact min #gates (fan-in 2, all 16 binary gates, B2) for n-input functions via BFS over
# sets of computed truth tables. Wires = 2*gates (every gate has two incoming wires).
import sys, itertools, json
n=int(sys.argv[1]); maxg=int(sys.argv[2])
N=1<<n; FULL=(1<<N)-1
inputs=[sum(((i>>k)&1)<<i for i in range(N)) for k in range(n)]
def ops(a,b):
    na,nb=FULL^a,FULL^b
    return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,FULL^(a^b)}  # nontrivial gates (up to output neg handled by closure below)
best={}  # truth table -> min gates (functions incl. complements: B2 closed under negation of output)
def norm(f): return f
# DFS-free BFS: level k = set of frozensets of available tables (inputs + k gates)
level={frozenset(inputs)}
for t in inputs: best[t]=0; best[FULL^t]=0
best[0]=0; best[FULL]=0
for g in range(1,maxg+1):
    new=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for r in ops(a,b):
                if r in S: continue
                T=S|{r}
                new.add(T)
                if r not in best: best[r]=g
                if (FULL^r) not in best: best[FULL^r]=g
    level=new
    print(g,len(level),file=sys.stderr)
from collections import Counter
c=Counter(best.values())
print(json.dumps({"n":n,"maxg":maxg,"count_by_gates":dict(sorted(c.items())),"covered":len(best),"of":1<<N}))
