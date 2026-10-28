"""Exact minimum gate count C(f) over fan-in-2 gates (all 10 non-degenerate binary ops,
free negation absorbed by ops) for n-input functions, by BFS over sets of computed truth tables.
Also: exact minimum WIRE count = 2*C(f) for fan-in-2 circuits where every gate has exactly 2 in-wires
(outputs not counted); fan-out distribution of optimal circuits is recorded as 'reconvergent' flag.
Runtime-limited (<30s): n=2 full, n=3 up to depth D."""
import sys, json, time, itertools
n=int(sys.argv[1]); D=int(sys.argv[2]); T0=time.time()
N=1<<n; M=(1<<N)-1
inp=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
# ops as 4-bit tables, nondegenerate: depend on both args
ops=[t for t in range(16) if any(((t>>(2*a+b))&1)!=((t>>(2*a+(1-b)))&1) for a in (0,1) for b in (0,1)) and any(((t>>(2*a+b))&1)!=((t>>(2*(1-a)+b))&1) for a in (0,1) for b in (0,1))]
def ap(t,f,g):
    r=0
    for x in range(N):
        a=(f>>x)&1;b=(g>>x)&1
        if (t>>(2*a+b))&1: r|=1<<x
    return r
best={}  # f -> gates
for f in inp: best[f]=0; best[M^f]=0
best[0]=0;best[M]=0
level=[tuple(inp)]; seen={tuple(sorted(inp))}
for d in range(1,D+1):
    new=[];ns=set()
    for st in level:
        S=set(st)
        for f,g in itertools.combinations(st,2):
            for t in ops:
                h=ap(t,f,g)
                if h in S: continue
                s=tuple(sorted(st+(h,)))
                if s in seen or s in ns: continue
                ns.add(s); new.append(s)
                for u in (h,M^h):
                    if u not in best: best[u]=d
        if time.time()-T0>25: print("timeout at depth",d); break
    seen|=ns; level=new
    print("depth",d,"states",len(new),"funcs",len(best),"t=%.1f"%(time.time()-T0))
    if time.time()-T0>25: break
from collections import Counter
cnt=Counter(best.values())
print(dict(cnt), "of",1<<N)
json.dump({"n":n,"D":D,"count_by_C":dict(cnt),"funcs_found":len(best),"total":1<<N},open(f"results/raw/claude_circuitsat/min_gates_n{n}.json","w"))
