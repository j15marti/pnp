"""Exact minimum B2 (all 2-input gates, free negation) circuit size for all n<=3 functions,
and for selected n=4 targets (iterative deepening). Wires = 2*gates (fan-in 2 edges, gate->gate/output edges counted separately)."""
import json, sys, itertools, time
def run(n, limit_s=20):
    M=1<<n; FULL=(1<<M)-1
    ins=[]
    for i in range(n):
        t=0
        for x in range(M):
            if (x>>i)&1: t|=1<<x
        ins.append(t)
    # normalize: f ~ ~f (free negation) -> canonical min(f,~f)
    canon=lambda f:min(f,FULL^f)
    # all 2-input gates up to negation: AND-type with input/output negations -> a&b, a&~b, ~a&b, a|b ~ via neg..., xor
    def combos(a,b):
        na,nb=FULL^a,FULL^b
        return {a&b,a&nb,na&b,na&nb,a^b}  # outputs up to output-negation
    best={}  # canon(f)->min gates
    base={canon(t) for t in ins}|{0}
    for f in base: best[f]=0
    # BFS over circuits as sets of available functions (canonical), by gate count
    start=frozenset(base)
    layer={start}; seen={start}; g=0; t0=time.time()
    while layer and len(best)< (1<<(M-1)):
        g+=1; nxt=set()
        for S in layer:
            L=list(S)
            for a,b in itertools.combinations(L,2) if False else itertools.combinations_with_replacement(L,2):
                for h in combos(a,b):
                    c=canon(h)
                    if c in S: continue
                    if c not in best: best[c]=g
                    T=S|{c}
                    if T not in seen: seen.add(T); nxt.add(T)
            if time.time()-t0>limit_s: return best,g,False
        layer=nxt
    return best,g,True
out={}
for n in (1,2,3):
    best,g,done=run(n)
    hist={}
    for f,v in best.items(): hist[v]=hist.get(v,0)+1
    out[n]={"max_gates":max(best.values()),"hist_up_to_negation":dict(sorted(hist.items())),"complete":done,"classes":len(best)}
    print(n,out[n],flush=True)
json.dump(out,open("../../results/raw/claude_circuitsat/minsize_B2_n123.json","w") if __import__("os").makedirs("../../results/raw/claude_circuitsat",exist_ok=True) is None else None,indent=1)
