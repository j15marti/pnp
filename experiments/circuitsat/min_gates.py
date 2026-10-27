"""Exact minimum 2-input-gate (full B2 basis) circuit size for n-input functions, small n.
Level-wise BFS over sets of computed truth tables (states deduped). Each run < 30s."""
import sys, json, itertools
n=int(sys.argv[1]); maxd=int(sys.argv[2]); N=1<<n; M=(1<<N)-1
inputs=[]
for i in range(n):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    inputs.append(t)
const=[0,M]
def gates(a,b):
    out=set()
    for g in range(16):
        r=0
        for ba in (0,1):
            for bb in (0,1):
                if (g>>(2*ba+bb))&1:
                    r|=(a if ba else a^M)&(b if bb else b^M)
        out.add(r)
    return out
base=frozenset(inputs+const)
trivial=set(base)|{t^M for t in inputs}
best={f:0 for f in trivial}
level={base}
for d in range(1,maxd+1):
    nxt=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for r in gates(a,b):
                if r not in S: nxt.add(S|{r})
    for S in nxt:
        for f in S:
            if f not in best: best[f]=d
    level=nxt
    print(f"n={n} depth {d}: states {len(level)}, functions reached {len(best)}/{1<<N}",flush=True)
# unique-SAT (single minterm) functions
mint=[1<<x for x in range(N)]
res={"n":n,"maxd":maxd,"minterm_gates":sorted({best.get(m,None) or -1 for m in mint}),
     "count_by_gates":{k:sum(1 for v in best.values() if v==k) for k in range(maxd+1)}}
print(json.dumps(res))
json.dump(res,open(f"results/raw/circuitsat_min_gates_n{n}.json","w"))
