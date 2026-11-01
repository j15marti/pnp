"""Exact minimum AND-gate count (AIG: 2-input AND, free edge negation) for all
Boolean functions on n=1..3 inputs, plus wires = 2*gates (+ output). Iterative
deepening over sets of available truth tables. Runs well under 30 s for n<=3."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inp=[]
    for i in range(n):
        t=0
        for x in range(N):
            if (x>>i)&1: t|=1<<x
        inp.append(t)
    best={}  # function -> min gates
    # BFS over frontier: state = frozenset of available (non-neg-normalised) tables
    def lits(S):
        out=set()
        for t in S: out.add(t); out.add(M^t)
        out.add(0); out.add(M)
        return out
    start=frozenset(inp)
    for f in list(lits(start)): best[f]=0
    level={start}; k=0; seen={start}
    while level and k<7:
        k+=1; nxt=set()
        for S in level:
            L=sorted(lits(S))
            for a,b in itertools.combinations_with_replacement(L,2):
                g=a&b
                if g in lits(S): continue
                S2=frozenset(S|{g})
                if S2 in seen: continue
                seen.add(S2); nxt.add(S2)
                for f in (g,M^g):
                    if f not in best: best[f]=k
        level=nxt
        if len(best)==1<<N: break
    return best,k
res={}
for n in (1,2,3):
    best,k=run(n)
    N=1<<n; M=(1<<N)-1
    from collections import Counter
    c=Counter(best.values())
    # minterms: unique-SAT functions
    mint=[best.get(1<<x) for x in range(N)]
    res[n]={"functions_covered":len(best),"of":1<<N,"hist":dict(c),"minterm_gates":sorted(set(mint)),"maxgates":max(best.values())}
    print(n,res[n])
json.dump(res,open("min_aig_results.json","w"),indent=1)
