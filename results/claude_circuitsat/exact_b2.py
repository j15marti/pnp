"""Exact minimum B2 circuit size (fan-in-2 gates, free negation) for all n-var Boolean fns, n<=3.
BFS over sets of computed (negation-normalised) functions, level = #gates. Wires = 2*gates (fan-in 2) counted separately.
Per-level checkpoint in JSON. Each run is chunked by n and stops at LIMIT seconds."""
import sys, json, time, itertools
n=int(sys.argv[1]); LIMIT=float(sys.argv[2]) if len(sys.argv)>2 else 25
N=1<<n; M=(1<<N)-1
def var(i):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    return t
def norm(t): return t if not (t&1) else t^M   # f(0)=0 representative
ops=[lambda a,b:a&b, lambda a,b:a&~b&M, lambda a,b:~a&b&M, lambda a,b:a|b, lambda a,b:a^b]
inputs=[var(i) for i in range(n)]
best={0:0}; 
for v in inputs: best[norm(v)]=0
best[0]=0
# level states: frozenset of gate-outputs (normalised, excluding inputs/const)
t0=time.time()
level={frozenset()}
k=0
total=1<<N
seen_funcs=set(best)   # normalised funcs reachable
while len(seen_funcs)<(total//2) and k<9:
    k+=1; nxt=set()
    for S in level:
        base=list(S)+inputs
        for a,b in itertools.combinations(base,2):
            for op in ops:
                r=norm(op(a,b))
                if r==0 or r in S or r in inputs or norm(r) in map(norm,inputs): continue
                nxt.add(S|{r})
        if time.time()-t0>LIMIT: print("TIMEOUT at level",k,len(nxt)); sys.exit(1)
    level=nxt
    for S in level:
        for r in S:
            if r not in seen_funcs: seen_funcs.add(r); best[r]=k
    print("level",k,"states",len(level),"funcs",len(seen_funcs),"/",total//2,flush=True)
from collections import Counter
c=Counter(best.values())
# full function count (both polarities)
print(json.dumps({"n":n,"gates_histogram_norm_classes":dict(c),"max_gates":max(best.values())}))
json.dump({"n":n,"hist":{str(k):v for k,v in c.items()},"max_gates":max(best.values())},open(f"exact_b2_n{n}.json","w"))
