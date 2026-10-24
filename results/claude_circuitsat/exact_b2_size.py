"""Exact min #gates (fan-in 2, full basis B2, negation free) with sharing, via BFS over
states = frozenset of computed (complement-normalised) truth tables.
Usage: python3 exact_b2_size.py n maxdepth   (n<=4). Each run < ~30s for n<=3; n=4 uses depth cap."""
import sys, json, itertools, time
n=int(sys.argv[1]); D=int(sys.argv[2]); M=(1<<(1<<n))-1
def norm(t): return t^M if t&1 else t
vs=[]
for i in range(n):
    t=0
    for x in range(1<<n):
        if (x>>i)&1: t|=1<<x
    vs.append(t)
start=frozenset(vs)
best={}          # normalised function -> min gates
for v in vs: best[v]=0
best[0]=0        # constants
level={start}; seen={start}; t0=time.time()
for d in range(1,D+1):
    new=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for r in (a&b,a&(b^M),(a^M)&b,(a^M)&(b^M),a^b):
                r=norm(r)
                if r in S: continue
                if r not in best: best[r]=d
                T=S|{r}
                if T not in seen: seen.add(T); new.add(T)
    level=new
    print(f"depth {d}: states {len(level)} funcs {len(best)}/{1<<((1<<n)-1)} t={time.time()-t0:.1f}s",flush=True)
    if len(best)==1<<((1<<n)-1): break
    if time.time()-t0>20: print("time cap");break
from collections import Counter
print(sorted(Counter(best.values()).items()))
json.dump({"table":{str(k):v for k,v in best.items()}},open(f"/home/user/pnp/results/claude_circuitsat/exact_b2_table_n{n}.json","w"))
json.dump({"n":n,"depth_reached":d,"covered":len(best),"total":1<<((1<<n)-1),"dist":sorted(Counter(best.values()).items())},open(f"/home/user/pnp/results/claude_circuitsat/exact_b2_n{n}.json","w"))
