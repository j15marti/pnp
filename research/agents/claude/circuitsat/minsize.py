# Exact min #gates (fan-in-2, all 16 binary ops) per n-var Boolean function, n<=3.
# Level-by-level search over straight-line programs; state = tuple of truth tables (sorted set of available wires).
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
ins=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
def ops(a,b):
    r=set()
    for t in range(16):
        v=0
        for (x,y,bit) in ((0,0,0),(0,1,1),(1,0,2),(1,1,3)):
            if (t>>bit)&1:
                v|=(a if x else a^M)&(b if y else b^M)
        r.add(v)
    return r
best={0:0,M:0}
for a in ins: best[a]=0; best[a^M]=0
seen={frozenset(ins)}
frontier=[tuple(ins)]
depth=0
while len(best)<(1<<N) and depth<8:
    depth+=1; new=[]
    for st in frontier:
        s=set(st)
        for a,b in itertools.combinations(st,2):
            for v in ops(a,b):
                if v in s or v in (0,M): continue
                if v not in best:
                    best[v]=depth
                    if v^M not in best: best[v^M]=depth
                ns=frozenset(s|{v})
                if ns not in seen:
                    seen.add(ns); new.append(tuple(sorted(ns)))
    frontier=new
    print("depth",depth,"found",len(best),"states",len(frontier),file=sys.stderr)
from collections import Counter
c=Counter(best.values())
print(json.dumps({"n":n,"hist":dict(sorted(c.items())),"total":len(best)}))
