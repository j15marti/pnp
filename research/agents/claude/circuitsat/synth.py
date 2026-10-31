"""Exact B2 (all 2-input gates) minimum gate counts C(f) for all f on n<=3 inputs.
Layered search over sets of computed functions; each gate has exactly 2 input wires, so wires=2*gates.
Usage: python3 synth.py N  -> writes synth_nN.json"""
import sys, json, itertools
n=int(sys.argv[1]); R=1<<n; M=(1<<R)-1
# truth tables as ints; variable i table
V=[sum(1<<x for x in range(R) if (x>>i)&1) for i in range(n)]
# nonconstant 2-input ops (as 4-bit tables) that depend on both args
OPS=[o for o in range(16) if o not in (0,15,3,12,5,10)]
def ap(o,a,b):
    r=0
    for k,(x,y) in enumerate([(0,0),(1,0),(0,1),(1,1)]):  # (a,b) bits
        if (o>>k)&1:
            ma=a if x else (~a&M); mb=b if y else (~b&M); r|=ma&mb
    return r
best={}
for f in range(1<<R): best[f]=None
for f in [0,M]+V+[~v&M for v in V]: best[f]=0
frontier={frozenset(V)}
seen={frozenset(V)}
g=0
while any(v is None for v in best.values()):
    g+=1; new=set()
    for S in frontier:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for o in OPS:
                r=ap(o,a,b)
                if r in S: continue
                T=S|{r}
                if T in seen: continue
                seen.add(T); new.add(T)
                for h in (r,~r&M):
                    if best[h] is None: best[h]=g
    frontier=new
    print(n,"gates",g,"states",len(new),flush=True)
from collections import Counter
cnt=Counter(best.values())
json.dump({"n":n,"hist":{str(k):v for k,v in sorted(cnt.items())},"max":max(best.values()),
 "and_n":best[(1<<(R-1))]},open(f"synth_n{n}.json","w"))
print(sorted(cnt.items()))
