"""Exact minimum B2 circuit sizes for all n-variable functions (n<=3), normal form.
Gates: fan-in 2, any of the 16 binary ops; w.l.o.g. normal (g(0,0)=0) since
complementing is free. Cost = #gates; wires = 2*#gates. Runs <30 s for n<=3."""
import sys, json, itertools, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[lambda a,b:a&b, lambda a,b:a&~b&M, lambda a,b:~a&b&M, lambda a,b:a|b, lambda a,b:a^b]
best={0:0}
for v in inp: best[v]=0
start=frozenset(inp)
level={start}; seen={start}; g=0; t0=time.time()
while len(best)<(1<<(N-1)) and g<7:
    g+=1; nxt=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                c=op(a,b)
                if c in S or c==0: continue
                T=S|{c}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if c not in best: best[c]=g
    level=nxt
    print(f"n={n} gates={g} states={len(nxt)} covered={len(best)}/{1<<(N-1)} t={time.time()-t0:.1f}",file=sys.stderr)
# full table (f and complement have equal cost)
cost={}
for f in range(1<<N):
    nf=f if not f&1 else (~f)&M
    cost[f]=best.get(nf)
json.dump({"n":n,"cost":{str(k):v for k,v in cost.items()}},open(f"mincircuit_n{n}.json","w"))
from collections import defaultdict
by=defaultdict(lambda:[10**9,-1,0])
hist=defaultdict(int)
for f,c in cost.items():
    hist[c]+=1
    k=bin(f).count("1"); r=by[k]; r[0]=min(r[0],c); r[1]=max(r[1],c); r[2]+=1
print("histogram gates->#functions",dict(sorted(hist.items())))
print("by #satisfying assignments k: (min,max,count)",{k:tuple(v) for k,v in sorted(by.items())})
