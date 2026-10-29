"""Exact min #gates (fan-in 2, all 16 binary gates, so negation free) for all
n-input Boolean functions, n<=3, via BFS over sets of computed truth tables.
Wires = 2*gates (fan-in 2, no unary gates). Runs in a few seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    gates=range(16)
    def ap(g,a,b):
        r=0
        for k,(x,y) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            if (g>>k)&1:
                r|=(a if x else a^full)&(b if y else b^full)
        return r
    best={}  # function -> min gates
    for f in [0,full]+ins+[i^full for i in ins]: best[f]=0
    seen={frozenset(ins)}; frontier=[frozenset(ins)]; k=0
    while frontier and k<8:
        k+=1; nxt=[]
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for g in range(16):
                    h=ap(g,a,b)
                    if h in S: continue
                    T=S|{h}
                    if T in seen: continue
                    seen.add(T); nxt.append(T)
                    for v in (h,h^full):
                        if v not in best: best[v]=k
        frontier=nxt
        if len(best)==1<<N: break
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    assert len(b)==1<<N, (n,len(b))
    dist={}
    for f,c in b.items(): dist[c]=dist.get(c,0)+1
    uniq=[c for f,c in b.items() if bin(f).count("1")==1]
    out[n]={"gates_distribution":dict(sorted(dist.items())),"max_gates":max(b.values()),
      "unique_sat_min_gates":sorted(set(uniq)),"max_gates_among_functions_with_2_sat_points":max(c for f,c in b.items() if bin(f).count("1")==2)}
    print(n,out[n])
json.dump(out,open("mincirc_results.json","w"),indent=1)
