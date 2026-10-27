"""Exact min number of fan-in-2 B2 gates (all 16 binary gates) for every n-input function, n<=3.
Iterative deepening over circuits as sets of computed truth tables. Runs < 30s."""
import itertools, json, sys
n=3; N=1<<n; FULL=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def gates(a,b):
    out=set()
    for g in range(16):
        r=0
        for x in range(N):
            va=(a>>x)&1; vb=(b>>x)&1
            if (g>>(va*2+vb))&1: r|=1<<x
        out.add(r)
    return out
G={}
def gt(a,b):
    k=(a,b)
    if k not in G: G[k]=gates(a,b)
    return G[k]
# level sets: frontier of circuits (frozenset of tables) by gate count
best={}  # function -> min gates
for f in [0,FULL]+inputs+[FULL^i for i in inputs]: best[f]=0
level=[frozenset(inputs)]
seen={frozenset(inputs)}
for s in range(1,6):
    nxt=[]
    for c in level:
        L=sorted(c)
        for a,b in itertools.combinations(L,2):
            for r in gt(a,b):
                if r in c: continue
                if r not in best: best[r]=s
                nc=c|{r}
                if nc not in seen: seen.add(nc); nxt.append(nc)
    level=nxt
    print(s,len(level),len(best),file=sys.stderr)
    if len(best)==256: break
from collections import Counter
cnt=Counter(best.values())
print(json.dumps({"n":3,"count_by_min_gates":dict(sorted(cnt.items())),"total":len(best)}))
