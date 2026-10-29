# Exact min number of 2-input gates (full binary basis B2) computing every n-var function, n<=3.
# BFS over sets of computed truth tables; layered by gate count. Runs in seconds.
import itertools, json, sys
def run(n, maxg=7):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    ops=range(16)
    def app(op,a,b):
        r=0
        for x in range(N):
            if (op>>(2*((a>>x)&1)+((b>>x)&1)))&1: r|=1<<x
        return r
    best={}  # tt -> min gates
    for t in [0,full]+inputs: best[t]=0
    frontier={tuple(sorted(inputs))}
    for g in range(1,maxg+1):
        nxt=set()
        for S in frontier:
            for a,b in itertools.combinations(S,2):
                for op in ops:
                    t=app(op,a,b)
                    if t not in S and t not in (0,full):
                        if t not in best: best[t]=g
                        nxt.add(tuple(sorted(S+(t,))))
        frontier=nxt
        if len(best)==(1<<N): break
    return best
out={}
for n in (2,3):
    b=run(n)
    mx=max(b.values()); out[n]={"functions":len(b),"max_min_gates":mx,
      "count_by_size":{k:sum(1 for v in b.values() if v==k) for k in range(mx+1)}}
print(json.dumps(out,indent=1))
json.dump(out,open("minsize_results.json","w"),indent=1)
