# Exact minimum fan-in-2 circuit size (full binary basis) over all n-var functions, n<=3 (n=3 via level-BFS over
# sets of computed tables, up to level LMAX). Reproducer for ClaudeCircuitSAT.tex Table 1.
import json, sys, time
def run(n,LMAX):
    N=1<<n; full=(1<<N)-1
    base=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    def ap(t,x,y): return sum((((t>>(2*((x>>a)&1)+((y>>a)&1)))&1)<<a) for a in range(N))
    ops=[t for t in range(16) if t not in (0,15,3,5,10,12)]  # nontrivial binary gates (10)
    best={f:0 for f in base+[0,full]}
    # n=1: NOT x = gate(x,x); treat negation of input as cost 1 here
    level={frozenset(base)}
    seen=set(level)
    for k in range(1,LMAX+1):
        new=set()
        for S in level:
            L=sorted(S)
            for i in range(len(L)):
                for j in range(i,len(L)):
                    for t in ops:
                        z=ap(t,L[i],L[j])
                        if z in S: continue
                        if z not in best: best[z]=k
                        T=S|{z}
                        if T not in seen: seen.add(T); new.add(T)
        level=new
        print(n,"level",k,"states",len(level),"funcs",len(best),flush=True)
        if len(best)==1<<N: break
    return best
res={}
for n,L in [(1,1),(2,2),(3,4)]:
    t0=time.time(); b=run(n,L); mx=max(b.values())
    from collections import Counter
    res[n]={"num_functions":1<<(1<<n),"found":len(b),"max_min_gates":mx,"histogram":dict(Counter(b.values())),"sec":round(time.time()-t0,1)}
    print(res[n])
json.dump(res,open('../../results/raw/claude_circuitsat_min_size.json','w'),indent=1)
