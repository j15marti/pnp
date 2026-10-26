"""Exact min gate counts (B2 basis: all 16 binary gates, fan-in 2) for all n-input functions, n<=3.
Iterative-deepening DFS over gate sequences (each gate = (op,i,j) over earlier signals)."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[]
for o in range(16):
    ops.append(lambda a,b,o=o: sum(((o>>(2*((a>>k)&1)+((b>>k)&1)))&1)<<k for k in range(N)))
# precompute op tables lazily with memo
from functools import lru_cache
@lru_cache(None)
def app(o,a,b): return ops[o](a,b)
best={}
def dfs(sigs,depth,maxd):
    # record
    f=sigs[-1]
    g=len(sigs)-n
    if f not in best or best[f]>g: best[f]=g
    if depth==maxd: return
    L=len(sigs)
    seen=set(sigs)
    for i in range(L):
        for j in range(i+1,L):
            for o in range(16):
                v=app(o,sigs[i],sigs[j])
                if v in seen: continue
                sigs.append(v); dfs(sigs,depth+1,maxd); sigs.pop()
# all functions realized: need every signal not just last; record every new signal
def run(maxd):
    def rec(sigs,depth):
        g=depth
        for f in sigs[n:]:
            pass
        v=sigs[-1]
        if v not in best or best[v]>g: best[v]=g
        if depth==maxd: return
        L=len(sigs); seen=set(sigs)
        for i in range(L):
            for j in range(i+1,L):
                for o in range(16):
                    w=app(o,sigs[i],sigs[j])
                    if w in seen: continue
                    sigs.append(w); rec(sigs,depth+1); sigs.pop()
    for f in inputs+[0,M]: best[f]=0
    rec(list(inputs),0)
run(int(sys.argv[2]))
hist={}
for f in range(M+1):
    if f in best: hist[best[f]]=hist.get(best[f],0)+1
print(json.dumps({"n":n,"maxd":int(sys.argv[2]),"found":len(best),"of":M+1,"hist":hist}))
