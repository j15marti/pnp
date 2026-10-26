"""Exact min #gates (fan-in-2, full basis B2) for every Boolean function of n<=3 inputs.
BFS over sets of computed truth tables (circuit states); runtime ~ seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    xs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[lambda p,q,t=t:sum(1<<k for k in range(N) if (t>>(2*((p>>k)&1)+((q>>k)&1)))&1) for t in range(16)]
    best={}
    start=frozenset(xs+[0,full])
    for f in start: best[f]=0
    layer={start}; seen={start}; g=0
    while layer and len(best)<(1<<N):
        g+=1; nxt=set()
        for S in layer:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for t in range(1,15):
                    h=ops[t](a,b)
                    if h in S: continue
                    T=S|{h}
                    if T in seen: continue
                    seen.add(T); nxt.add(T)
                    if h not in best: best[h]=g
        layer=nxt
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    hist={}
    for f,g in b.items(): hist[g]=hist.get(g,0)+1
    out[n]={"hist_gates_count":hist,"max_gates":max(b.values()),
            "AND":b[sum(1 for _ in [0]) and sum(1<<a for a in range(N) if a==N-1)],
            "XOR":b[sum(1<<a for a in range(N) if bin(a).count('1')%2)]}
    print(n,out[n])
json.dump(out,open("results/raw/claude_circuitsat/min_gates_b2_n123.json","w"),indent=1)
