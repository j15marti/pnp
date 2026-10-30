"""Exact minimum AND/OR circuit size (NOT free, fan-in 2) for all n-variable functions.
Layered BFS over sets of computed signals (mod complement). Usage: python minsize.py n maxdepth"""
import sys, json, itertools
n=int(sys.argv[1]); D=int(sys.argv[2]); N=1<<n; M=(1<<N)-1
def canon(f): return min(f, f^M)
inp=[]
for i in range(n):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    inp.append(canon(t))
const=canon(0)
best={const:0}; 
for f in inp: best[f]=0
start=frozenset(inp)
layer={start}; seen={start}
for k in range(1,D+1):
    new=set()
    for S in layer:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for pa in (0,M):
                for pb in (0,M):
                    g=canon((a^pa)&(b^pb))
                    if g in S: continue
                    T=S|{g}
                    if T not in seen:
                        seen.add(T); new.add(T)
                    if g not in best: best[g]=k
    layer=new
    print(k,len(layer),len(best),flush=True)
    if len(best)==(1<<(N-1)): break
res={str(f):s for f,s in best.items()}
hist={}
for s in best.values(): hist[s]=hist.get(s,0)+1
print(json.dumps({"n":n,"classes_found":len(best),"total_classes":1<<(N-1),"hist":hist}))
json.dump({"n":n,"hist":hist,"complete":len(best)==(1<<(N-1))},open(f"minsize_n{n}.json","w"))
