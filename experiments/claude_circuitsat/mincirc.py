"""Exact minimum gate count (fan-in-2, full basis B2, free negation) for all n-input Boolean functions, n<=3.
Wires = 2*gates (each gate has 2 in-wires). Iterative-deepening search over straight-line programs."""
import json, sys, itertools
n = int(sys.argv[1]) if len(sys.argv)>1 else 3
N = 1<<n; MASK=(1<<N)-1
ins = []
for i in range(n):
    t=0
    for a in range(N):
        if (a>>i)&1: t|=1<<a
    ins.append(t)
# functions up to complement are equivalent (free negation); canonicalize by bit0==0
def canon(f): return f if not f&1 else f^MASK
ops=[lambda a,b:a&b, lambda a,b:a&(~b&MASK), lambda a,b:(~a&MASK)&b, lambda a,b:a^b, lambda a,b:a|b]
# BFS over sets of canonical functions available; cost = #gates
start=frozenset(canon(x) for x in ins)|frozenset([0])
best={}  # function -> min gates
best[0]=0
for x in ins: best[canon(x)]=0
frontier={start}
seen={start}
g=0
total=1<<(N-1)
while len(best)<total and g<8:
    g+=1; new=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                for A in (a,a^MASK):
                    for B in (b,b^MASK):
                        c=canon(op(A,B))
                        if c in S: continue
                        T=S|{c}
                        if T not in seen:
                            seen.add(T); new.add(T)
                        if c not in best: best[c]=g
    frontier=new
    print("gates",g,"states",len(new),"funcs found",len(best),flush=True)
from collections import Counter
cnt=Counter(best.values())
out={"n":n,"functions_up_to_negation":total,"count_by_min_gates":dict(sorted(cnt.items())),
     "max_gates":max(best.values()),"wires_max":2*max(best.values())}
print(out)
json.dump(out,open(f"mincirc_n{n}.json","w"),indent=1)
