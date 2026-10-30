"""Exact minimum AIG size (AND gates, free edge negation) for all Boolean functions
of n<=3 inputs, by iterative-deepening over gate sets via BFS on function-sets.
Wires = 2*gates (fan-in 2). Runtime ~ seconds."""
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    var=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    base=frozenset([0,M]+var+[M^v for v in var])
    # best[f]=min gates; DFS over circuits as sets of available functions (with negations)
    best={f:0 for f in base}
    frontier=[(base,0)]
    seen={base:0}
    k=0
    while len(best)<(1<<N) and k<12:
        k+=1; nxt=[]
        for S,_ in frontier:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                g=a&b
                if g in S: continue
                T=S|{g,M^g}
                if T in seen: continue
                seen[T]=k; nxt.append((T,k))
                for f in (g,M^g):
                    best.setdefault(f,k)
        frontier=nxt
    return best,N
out={}
for n in (1,2,3):
    best,N=run(n); M=(1<<N)-1
    hist={}
    for f,c in best.items(): hist[c]=hist.get(c,0)+1
    var=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    par=0
    for v in var: par^=v
    andall=M
    for v in var: andall&=v
    out[n]={"functions":len(best),"hist_gates":dict(sorted(hist.items())),
            "max_gates":max(best.values()),"parity":best[par],"and_all":best[andall]}
    print(n,out[n])
json.dump(out,open("aig_min_results.json","w"),indent=1)
