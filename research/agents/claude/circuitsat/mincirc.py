# Exact min #fan-in-2 gates (all 16 binary gates) for every n-input Boolean function, n<=3, by BFS over sets of computed functions.
import itertools, sys, json
n=int(sys.argv[1]); M=1<<n; FULL=(1<<M)-1
inputs=[sum(((x>>i)&1)<<x for x in range(M)) for i in range(n)]
def gates(a,b):
    for g in range(16):
        r=0
        for k,(p,q) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            if (g>>k)&1:
                A=a if p else FULL^a; B=b if q else FULL^b
                r|=A&B
        yield r
best={}  # function -> min gates ; BFS over frozenset of wires, depth limited
from collections import deque
start=frozenset(inputs+[0,FULL])
seen={start:0}; q=deque([start]); best={f:0 for f in start}
maxd=int(sys.argv[2])
while q:
    s=q.popleft(); d=seen[s]
    if d==maxd: continue
    for a,b in itertools.combinations(sorted(s),2):
        for r in set(gates(a,b)):
            if r in s: continue
            t=s|{r}
            if t not in seen:
                seen[t]=d+1; q.append(t)
                if r not in best or best[r]>d+1: best[r]=d+1
from collections import Counter
print(n,len(best),FULL+1,sorted(Counter(best.values()).items()))
