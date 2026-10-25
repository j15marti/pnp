"""Exact minimum B2 (all 2-input gates) circuit size for every n-variable function, n<=3.
Wires counted = 2 per gate (fan-in) ; also records min size of functions that are SAT-hard-ish
(e.g. parity, AND, majority). Runs in well under 30s."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[]
    for i in range(n):
        v=0
        for x in range(N):
            if (x>>i)&1: v|=1<<x
        ins.append(v)
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in range(16)]
    # BFS over frozensets of computed funcs, canonical by sorted tuple; best[f]=min gates
    best={}
    for v in ins+[0,M]: best[v]=0
    frontier={frozenset(ins)}
    seen={frozenset(ins)}
    k=0
    while len(best)<(1<<N) and k<8:
        k+=1; nxt=set()
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for t in range(1,15):
                    c=ops[t](a,b)
                    if c in S: continue
                    T=S|{c}
                    if T in seen: continue
                    seen.add(T); nxt.add(T)
                    for f in (c,M^c):
                        if f not in best: best[f]=k
        frontier=nxt
    return best,N
out={}
for n in (1,2,3):
    best,N=run(n)
    hist={}
    for f,s in best.items(): hist[s]=hist.get(s,0)+1
    M=(1<<N)-1
    par=0
    for x in range(N):
        if bin(x).count('1')%2: par|=1<<x
    andf=1<<(N-1)
    maj=sum(1<<x for x in range(N) if bin(x).count('1')*2>n)
    out[n]={"num_functions":len(best),"size_histogram":hist,"max_size":max(best.values()),
            "AND":best[andf],"PARITY":best[par],"MAJ":best[maj]}
    print(n,out[n])
json.dump(out,open('/home/user/pnp/results/raw/claude_circuitsat/min_circuit_n123.json','w'),indent=1)
