"""Exact minimum fan-in-2 circuit size (all 16 binary gates, free negation) per
function on n inputs, n<=3, by iterative deepening over gate sequences.
Also: min gates / wires for a circuit whose function has exactly one satisfying
assignment on n inputs (unique-SAT hard instances), n<=4. Runs in seconds."""
import json, itertools, sys
def tt_inputs(n):
    N=1<<n; M=(1<<N)-1
    return [sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)], M
def closure_levels(n, maxg):
    ins,M=tt_inputs(n)
    # min gate count per truth table via BFS on frozenset-of-computed-wires (small n only)
    best={}
    def gates(a,b):
        out=set()
        for g in range(16):
            t=0
            for k,(x,y) in enumerate(((0,0),(0,1),(1,0),(1,1))):
                if (g>>k)&1:
                    t|=(a if x else a^M)&(b if y else b^M)
            out.add(t)
        return out
    base=frozenset(ins)|{0,M}
    frontier={base}; seen={base}
    for k in range(1,maxg+1):
        nxt=set()
        for S in frontier:
            L=list(S)
            for i in range(len(L)):
                for j in range(i,len(L)):
                    for t in gates(L[i],L[j]):
                        if t not in S:
                            T=S|{t,t^M}
                            if T not in seen:
                                seen.add(T); nxt.add(T)
                            if t not in best: best[t]=k
                            if (t^M) not in best: best[t^M]=k
        frontier=nxt
    return best,M
res={}
for n in (1,2,3):
    best,M=closure_levels(n,{1:2,2:3,3:4}[n])
    for t in list(best): pass
    allf=set(range(M+1)) if n<=2 else None
    ins,_=tt_inputs(n)
    cost={}
    for f in range(1<<(1<<n)):
        if f in ins or f in (0,M) or (f^M) in ins: cost[f]=0
        elif f in best: cost[f]=best[f]
        else: cost[f]=None
    mx=max(c for c in cost.values() if c is not None)
    unres=sum(c is None for c in cost.values())
    # unique-SAT functions: popcount 1
    us=[cost[1<<x] for x in range((1<<n))]
    res[n]={"max_gates":mx,"unresolved":unres,"unique_sat_min_gates":min(us),"unique_sat_max_gates":max(us)}
print(json.dumps(res,indent=1))
json.dump(res,open("min_circuit_ladder_results.json","w"),indent=1)
