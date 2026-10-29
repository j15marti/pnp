"""Exact minimum B2 (all 2-input gates, free negation) circuit size for n-variable functions.
BFS over sets of computed truth tables; n=2,3. Runs in seconds."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
# nondegenerate gates up to negation of output: AND-type (and, with input/output negations) and XOR
def combos(f,g):
    r={f&g,f&~g&M,~f&g&M,~f&~g&M,f^g}
    out=set()
    for h in r: out.add(h); out.add(~h&M)
    return out
# size[h]=min gates; level sets: state=frozenset of computed functions (inputs implicit)
best={}
for f in [0,M]+xs+[~x&M for x in xs]: best[f]=0
frontier={frozenset()}
seen={frozenset()}
s=0
while len(best)<(1<<N):
    s+=1; new=set()
    for st in frontier:
        pool=list(st)+xs
        for a,b in itertools.combinations(pool,2):
            for h in combos(a,b):
                if h in st or h in xs: continue
                ns=st|{h}
                key=frozenset(ns)
                if key in seen: continue
                seen.add(key); new.add(key)
                if h not in best: best[h]=s
    frontier=new
    print("size",s,"states",len(new),"functions",len(best),flush=True)
from collections import Counter
print(json.dumps({"n":n,"hist":sorted(Counter(best.values()).items())}))
