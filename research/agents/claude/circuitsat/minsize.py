"""Exact minimum B2 circuit size (fan-in-2, all 16 gates, free output negation) of every n-variable
function, n<=3, by level-wise BFS over sets of computed truth tables. Stages: gate budget g per run (<30s)."""
import sys, json, itertools, time
n=int(sys.argv[1]); G=int(sys.argv[2])
M=(1<<(1<<n))-1
vars_=[sum(((i>>v)&1)<<i for i in range(1<<n)) for v in range(n)]
gates=[lambda a,b,t=t:sum(((t>>(2*((a>>i)&1)+((b>>i)&1)))&1)<<i for i in range(1<<n)) for t in range(16)]
def canon(f): return min(f,f^M)
start=frozenset(canon(v) for v in vars_)|{0}  # constants free
best={}   # canonical function -> min gates
for f in start: best[f]=0
level={frozenset(start)}
seen={frozenset(start)}
t0=time.time()
for g in range(1,G+1):
    nxt=set()
    for S in level:
        L=list(S)
        # S holds canonical reps; gate on f or ~f is covered by 16 gate types
        for a,b in itertools.combinations(L,2):
            for t in range(16):
                h=canon(gates[t](a,b))
                if h in S: continue
                if h not in best: best[h]=g
                T=S|{h}
                if T not in seen: seen.add(T); nxt.add(T)
    level=nxt
    print(f"g={g} states={len(nxt)} known={len(best)}/{(M+1)//2} t={time.time()-t0:.1f}",flush=True)
    if len(best)==(M+1)//2 or time.time()-t0>20: break
from collections import Counter
print(json.dumps({"n":n,"complete":len(best)==(M+1)//2,"hist":sorted(Counter(best.values()).items())}))
