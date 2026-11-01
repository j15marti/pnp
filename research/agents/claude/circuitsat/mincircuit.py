# Exact min B2 gate counts for all n-input functions (n<=3) by BFS over sets of computed functions.
# Fan-in-2 gates, any of the 16 binary ops (constants/projections harmless). Wires = 2*gates (edges into gates).
import sys, json, time
n=int(sys.argv[1]); LIM=float(sys.argv[2]) if len(sys.argv)>2 else 25
R=1<<n; M=(1<<R)-1
ins=[sum(((p>>i)&1)<<p for p in range(R)) for i in range(n)]
def ops(a,b):
    na,nb=M^a,M^b
    for x in (a,na):
        for y in (b,nb):
            yield x&y; yield M^(x&y)
    yield a^b; yield M^(a^b)
best={}
for f in ins: best[f]=0
best[0]=0; best[M]=0   # constants free
for f in ins: best[M^f]=0  # negation absorbed by B2 gates only if used as input; count as 0 for inputs
start=frozenset(ins); level={start}; seen={start}; k=0; t0=time.time(); done=True
while level and len(best)<(1<<R):
    k+=1; new=set()
    for S in level:
        L=list(S)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for g in set(ops(L[i],L[j])):
                    if g in S or g in (0,M): continue
                    T=S|{g}
                    if T in seen: continue
                    seen.add(T); new.add(T)
                    for h in (g,M^g):
                        if h not in best: best[h]=k
        if time.time()-t0>LIM: done=False;break
    if not done: break
    level=new
    print("gates",k,"states",len(new),"functions found",len(best),file=sys.stderr)
cnt={}
for f,v in best.items(): cnt[v]=cnt.get(v,0)+1
print(json.dumps({"n":n,"complete":done and len(best)==(1<<R),"max_gates":max(best.values()),"hist":cnt,"found":len(best),"of":1<<R}))
