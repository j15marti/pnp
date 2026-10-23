# Exact min #gates (fan-in 2, full basis B2, shared gates allowed) for every n-var function, n<=3.
# BFS over sets of computed truth tables; wires = 2*gates (every gate has two in-wires; fan-out free).
import sys, json, itertools
n=int(sys.argv[1]); R=1<<n; M=(1<<R)-1
inputs=[sum(((x>>i)&1)<<x for x in range(R)) for i in range(n)]
ops=[lambda a,b,t=t:sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(R)) for t in range(16)]
# restrict to non-degenerate ops (depend on both args)
good=[t for t in range(16) if any(((t>>k)&1)!=((t>>(k^1))&1) for k in range(4)) and any(((t>>k)&1)!=((t>>(k^2))&1) for k in range(4))]
best={}
for f in (0,M)+tuple(inputs): best[f]=0; best[M^f]=0
level={frozenset(inputs)}; seen=set(level); g=0
while True:
    g+=1; new=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for t in good:
                h=ops[t](a,b)
                if h in S: continue
                T=S|{h}
                if T in seen: continue
                seen.add(T); new.add(T)
                for hh in (h,M^h):
                    if hh not in best: best[hh]=g
    print(g,len(new),len(best),flush=True)
    if len(best)==1<<R or not new: break
    level=new
from collections import Counter
c=Counter(best.values()); print(sorted(c.items()))
json.dump({'n':n,'hist':sorted(c.items()),'max_gates':max(best.values())},open(f'results/circuitsat/mincirc_n{n}.json','w'))
