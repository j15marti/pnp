"""Exact minimum circuit size (fan-in-2, all 16 binary gates, free negation) of n-input
Boolean functions by BFS over sets of computed functions. Wires = 2*gates (+1 output tap)."""
import json, sys, itertools, time
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[lambda x,y,t=t:sum((1<<k) for k in range(4) if (t>>k)&1 and False) for t in range(0)]
    def gates(x,y):
        # all 16 binary ops on (x,y) bitvectors
        nx,ny=full^x,full^y
        return {(x&y),(x&ny),(nx&y),(nx&ny),(x|y)^0,(x^y),(full^(x^y)),(full^(x&y)),(full^(x|y)),(x|ny),(nx|y),(nx|ny)}
    best={}
    for f in ins+[0,full]+[full^i for i in ins]: best[f]=0
    # states: frozenset of non-trivial computed functions beyond inputs
    frontier={frozenset(ins)}
    for g in range(1,maxg+1):
        new=set()
        for S in frontier:
            L=list(S)|{0}.__class__() if False else list(S)
            for x,y in itertools.combinations(L,2):
                for h in gates(x,y):
                    if h in S or h in (0,full): continue
                    if h not in best and (full^h) not in best:
                        best[h]=g; best[full^h]=g
                    new.add(S|{h})
        frontier=new
        print(n,g,len(frontier),len(best),file=sys.stderr)
    return best
res={}
t=time.time()
b=run(2,3); res['n2']={'funcs_total':16,'reached':len(b)}
from collections import Counter
b=run(3,4); res['n3']={'funcs_total':256,'reached':len(b),'size_hist':dict(Counter(b.values()))}
res['n3']['wires_max']=2*max(b.values())
b=run(4,3); res['n4_le3']={'funcs_total':65536,'reached':len(b),'size_hist':dict(Counter(b.values()))}
res['seconds']=round(time.time()-t,1)
json.dump(res,open('ladder_results.json','w'),indent=1); print(res)
