"""Exact minimum circuit size (B2, fan-in 2) and formula leaf-count for all n<=3 Boolean functions.
Wires = 2*gates (fan-in 2). Runs in a few seconds."""
import itertools, json, sys
from collections import Counter
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[]
    for i in range(n):
        t=0
        for x in range(N):
            if (x>>i)&1: t|=1<<x
        ins.append(t)
    ops=[lambda a,b,M=M:a&b,lambda a,b,M=M:a|b,lambda a,b,M=M:a^b,
         lambda a,b,M=M:(~a&M)&b,lambda a,b,M=M:a&(~b&M),
         lambda a,b,M=M:(~(a&b))&M,lambda a,b,M=M:(~(a|b))&M,lambda a,b,M=M:(~(a^b))&M,
         lambda a,b,M=M:(~a&M)|b,lambda a,b,M=M:a|(~b&M)]
    # circuit size: BFS on sets of available functions (normalise: allow free negation via B2 closure)
    best={}
    for t in ins+[0,M]: best[t]=0
    for t in list(best): best[(~t)&M]=0
    seen={frozenset(ins)}; frontier=[tuple(ins)]
    g=0
    while len(best)<(1<<N) and g<8:
        g+=1; nxt=[]
        for st in frontier:
            for a,b in itertools.combinations(st,2):
                for op in ops:
                    c=op(a,b)
                    if c in st: continue
                    ns=tuple(sorted(st+(c,)))
                    k=frozenset(ns)
                    if k in seen: continue
                    seen.add(k); nxt.append(ns)
                    for t in (c,(~c)&M):
                        if t not in best: best[t]=g
        frontier=nxt
    return best
def formula(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    L={}
    for t in ins+[0,M]: L[t]=1 if t in ins else 0
    for t in list(L): L[(~t)&M]=L[t]
    changed=True
    while changed:
        changed=False
        items=list(L.items())
        for a,la in items:
            for b,lb in items:
                for c in (a&b,a|b,a^b):
                    for d in (c,(~c)&M):
                        v=la+lb
                        if d not in L or L[d]>v: L[d]=v; changed=True
    return L
out={}
for n in (1,2,3):
    b=run(n); C=Counter(b.values())
    F=formula(n) if n<=3 else None
    out[n]={"funcs":1<<(1<<n),"circuit_size_hist":dict(sorted(C.items())),"max_gates":max(b.values()),
            "max_wires":2*max(b.values()),"formula_leaves_max":max(F.values()),
            "formula_hist":dict(sorted(Counter(F.values()).items()))}
print(json.dumps(out,indent=1))
json.dump(out,open("results/circuitsat_exact_small.json","w"),indent=1)
