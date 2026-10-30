"""Min AIG gate counts (AND + free inversion) for all n-var functions, BFS over
computed-function sets.  n=2 complete; n=3 up to MAXG gates (chunked, <30s)."""
import sys, itertools, time
n=int(sys.argv[1]); MAXG=int(sys.argv[2])
N=1<<n; FULL=(1<<N)-1
var=[sum(1<<p for p in range(N) if (p>>i)&1) for i in range(n)]
best={}  # function(normalized by output inversion) -> min gates
for v in var: best[v]=0; best[FULL^v]=0
best[0]=0; best[FULL]=0
frontier={frozenset(var)}
seen=set(frontier)
t=time.time()
for g in range(1,MAXG+1):
    nxt=set()
    for S in frontier:
        L=[x for f in S for x in (f,FULL^f)]
        for a,b in itertools.combinations(L,2):
            h=a&b
            if h in S or (FULL^h) in S: continue
            if h not in best: best[h]=g; best[FULL^h]=g
            T=frozenset(S|{h})
            if T not in seen: seen.add(T); nxt.add(T)
    frontier=nxt
    print(f"g={g} states={len(frontier)} t={time.time()-t:.1f}s",flush=True)
    if time.time()-t>20: print("stopped (time)"); break
from collections import Counter
print("n",n,"funcs found",len(best),"of",1<<N,dict(sorted(Counter(best.values()).items())))
pt=var[0]
for v in var[1:]: pt&=v
print("AND_n min gates",best[pt],"expected",n-1)
