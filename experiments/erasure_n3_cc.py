import itertools,sys,time
n=3;N=8;M=(1<<N)-1
def norm(t): return min(t,M^t)
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
inputs=[norm(t) for t in inputs]
def gates(a,b):
    r=set()
    for na in (0,M):
        for nb in (0,M):
            v=(a^na)&(b^nb); r.add(norm(v)); r.add(norm(v^M))
    r.add(norm(a^b)); return r
# BFS over sets of computed (normalized) functions, size = #gates
best={}
for t in [0]+inputs: best[t]=0
cur={frozenset(inputs)}
seen=set(cur)
size=0
t0=time.time()
while len(best)<129 and size<4:
    size+=1; nxt=set()
    for S in cur:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for g in gates(a,b):
                if g in S: continue
                S2=S|{g}
                if S2 in seen: continue
                seen.add(S2); nxt.add(S2)
                if g not in best: best[g]=size
    cur=nxt; print(size,len(cur),len(best),flush=True)
import json
cc={}
for f in range(256):
    cc[f]=best.get(norm(f))
print("missing",sum(v is None for v in cc.values()),"max",max(v for v in cc.values() if v is not None))
json.dump(cc,open("cc3.json","w"))
