"""Exact minimum gate counts over B2 (all 2-input gates) for n<=3 variables.
Method: dynamic programming over *sets of computed truth tables* is exponential; instead
BFS over circuits by gate count using frozenset of (non-constant) computed tables, canonical under
nothing. n=3 has 256 tables; max optimum is small, so exhaustive search is fast."""
import itertools, json, sys
def run(n, maxg=8):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((i>>j)&1)<<i for i in range(N)) for j in range(n)]
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>i)&1)+((b>>i)&1)))&1)<<i) for i in range(N)) for t in range(16)]
    best={}  # table -> min gates
    start=frozenset(xs)
    for x in xs: best[x]=0
    best[0]=0; best[M]=0  # constants free (B2 contains them via gates; count 0 conv.)
    frontier={start}; seen={start}
    for g in range(1,maxg+1):
        new=set()
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for op in ops:
                    r=op(a,b)
                    if r in S: continue
                    T=S|{r}
                    if T in seen: continue
                    seen.add(T); new.add(T)
                    if r not in best: best[r]=g
        frontier=new
        if len(best)>=1<<N: break
    return best
out={}
for n in (1,2,3):
    b=run(n)
    hist={}
    for v in b.values(): hist[v]=hist.get(v,0)+1
    out[n]={"funcs":len(b),"hist":dict(sorted(hist.items())),"max":max(b.values())}
    print(n,out[n],flush=True)
json.dump(out,open("mincircuit_results.json","w"),indent=1)
