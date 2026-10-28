"""Exact min #fan-in-2 gates (full basis B2, free inputs/consts) for all n-var functions, n<=3.
Level-by-level closure of straight-line programs; also counts min wires (2/gate + 1 output) trivial."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    base=frozenset([0,M]+inputs)
    # best[f]=min gates; BFS over sets of computed functions (straight-line programs) via iterative deepening
    best={}
    for f in base: best[f]=0
    # DFS bounded depth k on program states
    gates16=range(16)
    def ap(g,a,b):
        r=0
        for x in range(2):
            for y in range(2):
                if (g>>(2*x+y))&1:
                    r|=(a if x else a^M)&(b if y else b^M)
        return r
    k=0
    while len(best)<(1<<N) and k<8:
        k+=1
        seen=set()
        def dfs(S,d):
            if d==0: return
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for g in range(16):
                    f=ap(g,a,b)
                    if f in S: continue
                    if f not in best: best[f]=k-d+1
                    S2=S|{f}
                    key=(S2,d-1)
                    if key in seen: continue
                    seen.add(key)
                    dfs(S2,d-1)
        dfs(base,k)
    return best,N
out={}
for n in (1,2,3):
    best,N=run(n)
    from collections import Counter
    out[n]={"funcs_found":len(best),"total":1<<N,"hist":dict(Counter(best.values()))}
    # point functions (unique satisfying assignment)
    pts=[1<<a for a in range(N)]
    out[n]["point_fn_gates"]=sorted(set(best.get(p,-1) for p in pts))
    print(n,out[n],flush=True)
json.dump(out,open("results/raw/claude_circuitsat/min_gates.json","w"),indent=1)
