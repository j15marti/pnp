"""Exact minimum B2 (all 2-input gates) circuit size for every n-variable
Boolean function, by BFS over sets of computed signals. Wires = 2*gates
(every gate has fan-in 2; output tap is free). Usage: min_gates.py n maxgates"""
import sys, time, json
n=int(sys.argv[1]); K=int(sys.argv[2]); N=1<<n; M=(1<<N)-1
inputs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
ops=[lambda x,y,t=t:((t&1 and ~x&~y)|(t&2 and ~x&y)|(t&4 and x&~y)|(t&8 and x&y))&M for t in range(16)]
def apply(t,x,y):
    r=0
    if t&1:r|=~x&~y
    if t&2:r|=~x&y
    if t&4:r|=x&~y
    if t&8:r|=x&y
    return r&M
best={0:0,M:0}
for x in inputs: best[x]=0; best[M^x]=0
level={frozenset(inputs)}
t0=time.time()
for g in range(1,K+1):
    nxt=set()
    for S in level:
        L=sorted(S)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for t in (1,2,4,7,8,6,9,11,13,14): # nontrivial; others are NOT/const/proj
                    f=apply(t,L[i],L[j])
                    if f in S: continue
                    for h in (f,M^f):
                        if h not in best: best[h]=g
                    nxt.add(S|{f})
    level=nxt
    print(f"n={n} g={g} states={len(level)} funcs_so_far={len(best)}/{1<<N} t={time.time()-t0:.1f}s",flush=True)
    if time.time()-t0>20: print("time-chunk stop"); break
from collections import Counter
print(json.dumps(sorted(Counter(best.values()).items())))
