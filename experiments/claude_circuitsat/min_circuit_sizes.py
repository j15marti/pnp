"""Exact minimum B2-circuit size (fan-in 2 gates, all 16 binary ops) for all n-variable
functions, n=1..3, by iterative-deepening search. Also records min wire count = 2*gates
(fan-in-2 convention; unary/constant gates not needed except via B2).
Runtime << 30 s."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=range(16)
    def ap(op,u,v):
        r=0
        for b in range(4):
            if (op>>b)&1:
                uu = M^u if not (b&1) else u
                vv = M^v if not (b>>1)&1 else v
                r|=uu&vv
        return r&M
    best={f:None for f in range(M+1)}
    for f in list(xs)+[0,M]: best[f]=0
    def dfs(avail,depth):
        for f in avail:
            if best[f] is None or best[f]>len(avail)-n: pass
        g=len(avail)-n
        for f in avail:
            if best[f] is None or best[f]>g: best[f]=g
        if g==depth: return
        for i in range(len(avail)):
            for j in range(i+1,len(avail)):
                for op in ops:
                    h=ap(op,avail[i],avail[j])
                    if h in avail: continue
                    dfs(avail+[h],depth)
    for d in range(1,6):
        dfs(list(xs),d)
        if all(v is not None for v in best.values()): break
    hist={}
    for v in best.values(): hist[v]=hist.get(v,0)+1
    return hist
out={}
for n in (1,2,3):
    out[n]=run(n)
    print(n,out[n]); sys.stdout.flush()
json.dump(out,open('min_circuit_sizes_results.json','w'),indent=1)
