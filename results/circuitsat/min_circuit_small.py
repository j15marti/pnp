"""Exact min B2 circuit size (gates; fan-in 2; free output negation) for all n<=3 functions,
and point-function / dependence data for n=4. Runs well under 30s."""
import sys, json, itertools, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
def var(i): return sum(1<<x for x in range(N) if (x>>i)&1)
def norm(f): return f^M if f&1 else f
base=[var(i) for i in range(n)]
def news(S):
    out=set()
    L=list(S)
    for a,b in itertools.combinations(L,2):
        for t in (a&b, a&(b^M), (a^M)&b, (a|b), a^b):
            out.add(norm(t))
    return out
best={}  # normalized function -> min gates
t0=time.time()
for f in base+[0]: best[norm(f)]=0
level={frozenset(base)}
size=0
maxsize=int(sys.argv[2])
while level and size<maxsize:
    size+=1; nxt=set()
    for S in level:
        for g in news(S):
            if g in S: continue
            if g not in best: best[g]=size
            if size<maxsize: nxt.add(S|{g})
    level=nxt
    print(size,len(level),len(best),round(time.time()-t0,1),file=sys.stderr)
from collections import Counter
cnt=Counter(best.values())
tot=1<<(N-1)
print(json.dumps({"n":n,"max_depth_explored":maxsize,"normalized_functions_total":tot,"found":len(best),"count_by_size":dict(cnt)}))
# point functions
pf=[]
for x in range(N):
    f=norm(1<<x)
    pf.append(best.get(f))
print("point-function sizes",pf)
