"""Exact min #gates (fan-in 2, basis B2 = all 16 binary gates) for every Boolean function on n<=3 inputs.
Level-by-level closure over sets of computed truth tables (circuit = DAG, sharing allowed).
Also reports min wires = 2*gates (+1 output wire) for formulas? -> here: wires counted as 2*gates."""
import json, itertools, sys
def run(n, maxg):
    N=1<<n; M=(1<<N)-1
    ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    best={0:0,M:0}
    for t in ins: best[t]=0
    # state: frozenset of computed tables; BFS on gate count with canonical sets
    start=frozenset(set(ins)|{0,M})
    frontier={start}; seen={start}
    for g in range(1,maxg+1):
        nxt=set()
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for op in range(16):
                    v=0
                    for ai in (0,1):
                        for bi in (0,1):
                            if (op>>(2*ai+bi))&1:
                                v|=(a if ai else a^M)&(b if bi else b^M)
                    if v in S: continue
                    T=S|{v}
                    if T not in seen:
                        seen.add(T); nxt.add(T)
                    if v not in best: best[v]=g
        frontier=nxt
        if len(best)==1<<N: break
    return best,g
res={}
for n,mg in ((1,1),(2,3),(3,7)):
    b,g=run(n,mg)
    from collections import Counter
    c=Counter(b.values())
    res[n]={"functions":1<<(1<<n),"covered":len(b),"gates_hist":dict(sorted(c.items())),"max_gates":max(b.values())}
    print(n,res[n],flush=True)
json.dump(res,open("minsize_results.json","w"),indent=1)
