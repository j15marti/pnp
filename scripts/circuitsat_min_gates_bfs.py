import sys, itertools, json, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
ops=[lambda x,y,t=t:sum(1<<k for k in range(4) if (t>>k)&1 and False) for t in range(0)]
def comb(x,y,t,M=M):
    # t: 4-bit table over (x,y); bit (2*xv+yv)
    r=0
    for xv in (0,1):
        for yv in (0,1):
            if (t>>(2*xv+yv))&1:
                r|=(x if xv else ~x&M)&(y if yv else ~y&M)
    return r
best={}
for v in ins+[0,M]: best[v]=0
start=tuple(sorted(set(ins)))
level={start}; seen={start}; g=0
for v in start: best.setdefault(v,0)
t0=time.time()
while level and time.time()-t0<25:
    g+=1; nxt=set()
    for st in level:
        for x,y in itertools.combinations(st,2):
            for t in range(16):
                z=comb(x,y,t)
                if z in st: continue
                ns=tuple(sorted(st+(z,)))
                if ns in seen: continue
                seen.add(ns); nxt.add(ns)
                if z not in best: best[z]=g
    level=nxt
    print(n,"gates",g,"states",len(level),"funcs",len(best),file=sys.stderr)
mx=max(best.values())
from collections import Counter
print(json.dumps({"n":n,"complete":len(best)==1<<N,"funcs":len(best),"max_gates":mx,"hist":sorted(Counter(best.values()).items())}))
# unique-sat functions
u=[v for v in best if bin(v).count("1")==1]
print("unique-SAT funcs",len(u),"gates hist",sorted(Counter(best[v] for v in u).items()))
