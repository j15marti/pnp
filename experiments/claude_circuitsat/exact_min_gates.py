# Exact minimum fan-in-2 gate count (basis: all 16 binary gates, free NOT absorbed) for n-input functions, n<=3.
# Level-by-level BFS over sets of computed truth tables (circuits as sets of tables). Runs in seconds.
import json, itertools
def run(n):
    N=1<<n; full=(1<<N)-1
    ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    gates=[lambda a,b,t=t:sum(((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x for x in range(N)) for t in range(16)]
    best={}  # function -> min gates
    start=frozenset(ins+[0,full]); seen={start}; frontier=[start]
    for f in start: best.setdefault(f,0)
    for k in range(1,8):
        nxt=[]
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for g in gates:
                    v=g(a,b)
                    if v not in S:
                        T=S|{v}
                        if T not in seen: seen.add(T); nxt.append(T); best.setdefault(v,k)
        frontier=nxt
        if len(best)==1<<N: break
    dep=lambda f:[i for i in range(n) if any(((f>>x)&1)!=((f>>(x^(1<<i)))&1) for x in range(N))]
    rows={}
    for f,c in best.items():
        d=len(dep(f)); rows.setdefault(d,[]).append(c)
    return {d:{"count":len(v),"min":min(v),"max":max(v)} for d,v in sorted(rows.items())}
out={n:run(n) for n in (1,2,3)}
print(json.dumps(out,indent=1))
json.dump(out,open("results/raw/claude_circuitsat/exact_min_gates.json","w"),indent=1)
