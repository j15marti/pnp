import sys,itertools,time
n=int(sys.argv[1]);maxs=int(sys.argv[2])
N=1<<n;M=(1<<N)-1
base=[]
for i in range(n):
    t=0
    for x in range(N):
        if x>>i&1:t|=1<<x
    base.append(t)
ops=[lambda a,b,f=f:sum(((f>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x for x in range(N)) for f in range(16)]
# nontrivial ops only: those depending on both args
def dep(f): return (f&3!=(f>>2)&3) and (f&5!=(f>>1)&5) if False else True
best={}  # tt -> min gates
for t in base: best[t]=0
for c in [0,M]: best[c]=0
# circuits as tuples of tt lists; DFS with canonical increasing gate order dedupe by frozenset
seen=set();t0=time.time()
def rec(cur,k):
    key=frozenset(cur)
    if (key,k) in seen:return
    seen.add((key,k))
    if k==maxs:return
    L=list(cur)
    for a,b in itertools.combinations(L,2):
        for f in range(16):
            r=ops[f](a,b)
            if r in cur:continue
            if r not in best or best[r]>k+1:best[r]=k+1
            rec(cur|{r},k+1)
rec(frozenset(base),0)
from collections import Counter
print(n,maxs,Counter(best.values()),len(best),time.time()-t0)
# functions with exactly one satisfying assignment
one=[t for t in best if bin(t).count('1')==1]
print('unique-SAT funcs found',len(one),Counter(best[t] for t in one))
