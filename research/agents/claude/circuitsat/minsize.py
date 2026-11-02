# Exact min #fan-in-2 gates (AND with free negations on wires => AND/OR/NAND/NOR/imp family, no XOR) 
# for all Boolean functions of n<=3 variables, by BFS over sets of computed functions.
import sys, json, itertools
n=int(sys.argv[1]); maxd=int(sys.argv[2])
N=1<<n; M=(1<<N)-1
def var(i): return sum(1<<a for a in range(N) if (a>>i)&1)
def canon(f): return min(f, M^f)
start=frozenset(canon(var(i)) for i in range(n))
best={0:0}
for v in start: best[v]=0
level={start}; seen={start}
for d in range(1,maxd+1):
    nxt=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for pa in (a,M^a):
                for pb in (b,M^b):
                    c=canon(pa&pb)
                    if c in S or c==0: continue
                    if c not in best: best[c]=d
                    T=S|{c}
                    if T not in seen: seen.add(T); nxt.add(T)
    level=nxt
    print(d,len(level),len(best),file=sys.stderr)
# report on all functions f (canonical), also include complement
res={}
for f in range(1<<N):
    c=canon(f)
    res[f]=best.get(c)
json.dump({"n":n,"maxd":maxd,"size":res},open(f"minsize_n{n}.json","w"))
from collections import Counter
print("n",n,"dist",sorted(Counter(res.values(),).items(),key=lambda x:(x[0] is None,x[0])))
# unique-sat functions (one satisfying assignment)
u=[res[1<<a] for a in range(N)]
print("unique-sat min sizes",set(u))
par=sum(1<<a for a in range(N) if bin(a).count('1')%2)
print("parity",res[par])
