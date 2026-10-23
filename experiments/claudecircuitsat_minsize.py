import itertools,sys,time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
# B2 gates: 16 binary ops minus degenerate; use nondegenerate 10
ops=[lambda a,b:a&b,lambda a,b:a|b,lambda a,b:a^b,lambda a,b:~(a&b)&M,lambda a,b:~(a|b)&M,lambda a,b:~(a^b)&M,
 lambda a,b:a&~b&M,lambda a,b:~a&b&M,lambda a,b:(a|~b)&M,lambda a,b:(~a|b)&M]
base=frozenset(xs)
best={}  # function -> min gates
for f in list(xs)+[0,M]: best[f]=0
for x in xs: best[~x&M]=1
# level sets: frozenset of computed functions; BFS dedupe
level={base}
t=time.time()
for g in range(1,int(sys.argv[2])+1):
    nxt=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for o in ops:
                f=o(a,b)
                if f in S: continue
                nxt.add(S|{f})
                if f not in best: best[f]=g
    level=nxt
    print(g,len(level),len(best),time.time()-t,flush=True)
    if time.time()-t>20: break
from collections import Counter
print(Counter(best.values()), "of", 1<<N)
