# Exact minimum B2 (all 2-input gates) circuit size for all n-input functions, n<=3.
# Wires = 2*gates (fan-in 2) ; also tracks min number of gates needed for SAT-relevant classes.
import itertools, json, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    inputs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t: sum((((t>>((((a>>k)&1)<<1)|((b>>k)&1)))&1)<<k) for k in range(N)) for t in range(16)]
    best={}  # function -> min gates
    for f in [0,mask]+inputs: best[f]=0
    # BFS over circuits as frozenset of computed funcs (gates incl inputs); iterative deepening by gate count
    frontier={frozenset(inputs)}
    for g in range(1,8):
        new=set()
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for t in range(16):
                    f=ops[t](a,b)
                    if f in S: continue
                    best.setdefault(f,g)
                    new.add(S|{f})
        frontier=new
        if len(best)==1<<N: break
    return best
out={}
for n in (1,2,3):
    b=run(n); cnt={}
    for f,g in b.items(): cnt[g]=cnt.get(g,0)+1
    out[n]={"functions":len(b),"by_gates":dict(sorted(cnt.items())),"max_gates":max(b.values())}
    print(n,out[n]); sys.stdout.flush()
json.dump(out,open("mincirc_results.json","w"),indent=1)
