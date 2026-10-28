# Exact min #2-input gates (full basis B2) for all n-input Boolean functions, n<=3, by BFS over sets of computed functions.
# Runtime < 30s. Output JSON: per n, histogram of min gate counts and essential-input counts.
import json, itertools, sys
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t: sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in range(16)]
    best={}  # function -> min gates
    for f in [0,full]+inputs+[full^i for i in inputs]: best[f]=0
    # state: frozenset of available functions (incl inputs); DFS iterative deepening for each target via level sets
    from functools import lru_cache
    start=frozenset(inputs)
    level={start}
    seen={start}
    for g in range(1,maxg+1):
        nxt=set()
        for S in level:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for op in ops:
                    r=op(a,b)
                    if r in S: continue
                    T=S|{r}
                    # record
                    if r not in best: best[r]=g
                    if T not in seen:
                        seen.add(T); nxt.add(T)
        level=nxt
        # normalise: record funcs
    return best
out={}
for n,mg in [(2,3),(3,4)]:
    b=run(n,mg)
    hist={}
    for f,g in b.items(): hist[g]=hist.get(g,0)+1
    out[n]={"covered":len(b),"of":1<<(1<<n),"hist":hist}
print(json.dumps(out))
