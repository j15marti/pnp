import itertools,sys,json
n=int(sys.argv[1]); K=int(sys.argv[2]); N=1<<n; M=(1<<N)-1
xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
ops=[lambda a,b:a&b,lambda a,b:a|b,lambda a,b:a^b,lambda a,b:~(a&b)&M,lambda a,b:~(a|b)&M,lambda a,b:~(a^b)&M,
 lambda a,b:a&~b&M,lambda a,b:~a&b&M,lambda a,b:(~a|b)&M,lambda a,b:(a|~b)&M]
best={}
for x in xs: best[x]=0
best[0]=0;best[M]=0  # constants free (trivial)
for x in list(xs): best[~x&M]=best.get(~x&M,0)  # negations free in B2 (absorbed)
front={tuple(sorted(xs))}
for k in range(1,K+1):
    nf=set()
    for st in front:
        for a,b in itertools.combinations(st,2):
            for o in ops:
                f=o(a,b)
                if f in st: continue
                ns=tuple(sorted(st+(f,)))
                nf.add(ns)
                for g in (f,~f&M):
                    if g not in best: best[g]=k
    front=nf
    print(k,len(front),len(best),file=sys.stderr)
from collections import Counter
print(json.dumps(sorted(Counter(best.values()).items())), len(best), "of", 1<<N)
