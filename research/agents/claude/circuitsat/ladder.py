# Exact min gate count (fan-in-2, all 16 binary gates, free inputs/constants) for all n<=3 functions.
# Iterative deepening over sets of computed truth tables. Runs in seconds.
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    base=ins+[0,M]
    allf=range(1<<N)
    best={}
    def gates(a,b):
        for g in range(16):
            r=0
            for k in range(4):
                if (g>>k)&1:
                    r|=(a if k&2 else a^M)&(b if k&1 else b^M)
            yield r
    # BFS by number of gates over frozenset states (small n only)
    level={frozenset(base)}; seen={frozenset(base)}
    cost={f:0 for f in base}
    c=0
    while len(cost)<(1<<N):
        c+=1; nxt=set()
        for S in level:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for r in set(gates(a,b)):
                    if r in S: continue
                    T=S|{r}
                    if T not in seen: seen.add(T); nxt.add(T)
                    if r not in cost: cost[r]=c
        level=nxt
    return cost
out={}
for n in (1,2,3):
    cost=run(n); N=1<<n
    byk={}
    for f,c in cost.items():
        k=bin(f).count('1'); byk.setdefault(k,[]).append(c)
    out[n]={'maxcost':max(cost.values()),'by_k':{k:{'min':min(v),'max':max(v),'count':len(v)} for k,v in sorted(byk.items())}}
print(json.dumps(out,indent=1))
json.dump(out,open('ladder_results.json','w'),indent=1)
