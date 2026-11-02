"""Exact min #gates (fan-in 2, all 16 binary ops, free negation) for every n-input Boolean function, n<=3.
Method: BFS over sets of computed truth tables (normalised: f and ~f identified). Wires = 2*gates."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def norm(t): return min(t,t^M)
start=frozenset(norm(t) for t in inputs)
best={0:0,M:0}
for t in inputs: best[norm(t)]=0
ops=range(16)
def app(op,a,b):
    r=0
    for k,(x,y) in enumerate(((0,0),(0,1),(1,0),(1,1))):
        if (op>>k)&1: r|=(a if x else a^M)&(b if y else b^M)
    return r
frontier={start}; seen={start}; g=0
while frontier:
    g+=1; new=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                for A in (a,a^M):
                    for B in (b,b^M):
                        t=norm(app(op,A,B))
                        if t in S: continue
                        if t not in best: best[t]=g
                        T=S|{t}
                        if T not in seen: seen.add(T); new.add(T)
    frontier=new
    if len(best)>=(1<<(N-1))+1 or g>=6: break
hist={}
for t,v in best.items(): hist[v]=hist.get(v,0)+1
print(n,"classes(f~~f):",len(best),"max gates:",max(best.values()),"hist:",dict(sorted(hist.items())))
