"""Exact AIG (2-input AND, free wire negation) gate-count ladder for n<=3 inputs.
Wires in a circuit with g gates: 2g internal fan-in wires + 1 output marker.
Iterative-deepening DFS over gate sequences; truth tables as ints."""
import json, sys, itertools, time
def run(n, maxg):
    N=1<<n; M=(1<<N)-1
    xs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    best={}  # function -> min gates
    for f in [0,M]+xs+[M^x for x in xs]: best[f]=0
    def dfs(funcs, g, limit):
        # funcs: list of available function tables (no negation duplicates)
        if g==limit: return
        L=len(funcs)
        seen=set()
        for i in range(L):
            for j in range(i+1,L):
                for ni in (0,1):
                    for nj in (0,1):
                        a=funcs[i]^(M if ni else 0); b=funcs[j]^(M if nj else 0)
                        h=a&b
                        if h in seen: continue
                        seen.add(h)
                        for t in (h,h^M):
                            if t not in best or best[t]>g+1: best[t]=g+1
                        if h in funcs or (h^M) in funcs: continue
                        dfs(funcs+[h], g+1, limit)
    for lim in range(1,maxg+1):
        dfs(xs[:],0,lim)
    return best
out={}
for n,maxg in ((1,1),(2,3),(3,6)):
    t=time.time(); b=run(n,maxg)
    N=1<<n; tot=1<<N
    hist={}
    for f in range(tot):
        hist[b.get(f,-1)]=hist.get(b.get(f,-1),0)+1
    out[n]={"max_gates_found":max(b.values()),"covered":len(b),"total":tot,"hist":hist,"sec":round(time.time()-t,2)}
    print(n,out[n],flush=True)
json.dump(out,open("../../results/raw/claude_circuitsat_aig_ladder.json","w"),indent=1)
