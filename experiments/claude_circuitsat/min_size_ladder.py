"""Exact min fan-in-2 circuit size (full binary basis, free inputs) for all n-variable functions, n<=3.
Enumerates sets of computed functions by BFS over gate count (each gate = 2 wires in). Also counts
point functions (unique satisfying assignment). Runs in seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    inputs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[lambda x,y,t=t:sum(((t>>(2*((x>>a)&1)+((y>>a)&1)))&1)<<a for a in range(N)) for t in range(16)]
    best={}  # function -> min gates
    for f in [0,mask]+inputs: best[f]=0
    # state = frozenset of available functions; DFS iterative deepening is heavy; use level BFS on states
    start=frozenset([0,mask]+inputs)
    level={start}; k=0; seen=set(level)
    while level and len(best)<(1<<N) and k<8:
        k+=1; nxt=set()
        for S in level:
            L=sorted(S)
            for x,y in itertools.combinations(L,2):
                for op in ops:
                    g=op(x,y)
                    if g in S: continue
                    if g not in best: best[g]=k
                    T=S|{g}
                    if T not in seen: seen.add(T); nxt.add(T)
        level=nxt
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    pts=[f for f in b if bin(f).count('1')==1]
    dist={}
    for v in b.values(): dist[v]=dist.get(v,0)+1
    out[n]={"funcs_found":len(b),"of":1<<N,"size_distribution":dist,"point_function_min_size":sorted({b[f] for f in pts})}
    print(n,out[n]); sys.stdout.flush()
json.dump(out,open("results/raw/claude_circuitsat/min_size_ladder.json","w"),indent=1)
