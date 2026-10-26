"""Exact minimum B2 (fan-in-2, all 16 gates) circuit size for n<=3 functions.
Iterative deepening over gate sequences; truth tables as ints. Runs in seconds."""
import itertools, json, sys
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    xs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[(lambda x,y,t=t:sum(((t>>(2*((x>>a)&1)+((y>>a)&1)))&1)<<a for a in range(N))) for t in range(16)]
    # precompute gate tables lazily via dict
    best={}
    def dfs(funcs,left,depth):
        for f in funcs: 
            if f not in best or best[f]>depth: best[f]=depth
        if left==0: return
        seen=set(funcs)
        for i in range(len(funcs)):
            for j in range(i+1,len(funcs)):
                for t in range(1,15):
                    h=ops[t](funcs[i],funcs[j])
                    if h in seen: continue
                    dfs(funcs+[h],left-1,depth+1)
    dfs(xs,maxg,0)
    return best,full
out={}
for n,mg in ((1,1),(2,3)):
    best,full=run(n,mg)
    dist={}
    for f,c in best.items(): dist[c]=dist.get(c,0)+1
    # functions depending on all n vars
    N=1<<n
    def dep(f,i): return any(((f>>a)&1)!=((f>>(a^(1<<i)))&1) for a in range(N))
    full_dep=[c for f,c in best.items() if all(dep(f,i) for i in range(n))]
    out[n]={"reached":len(best),"total_functions":1<<N,"dist_by_gates":dist,
            "min_gates_all_vars_dependent":min(full_dep) if full_dep else None,
            "max_gates_reached":max(best.values())}
    print(n,out[n],flush=True)
json.dump(out,open(sys.argv[1],"w"),indent=1)
