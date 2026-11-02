# Exact min #gates (fan-in 2, all 16 binary gates, free fan-out) for every n-var function, n=2,3.
# BFS over sets of computed truth tables, depth-limited. Runs well under 30s for n<=3.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
ins=[]
for i in range(n):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    ins.append(t)
def ops(a,b):
    r=set()
    for g in range(16):
        t=0
        for k,(p,q) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (g>>k)&1:
                A=a if p else a^M; B=b if q else b^M
                t|=A&B
        r.add(t)
    return r
base=frozenset(ins)|{0,M}
best={f:0 for f in base}
frontier={base}; seen={base}; d=0
while frontier and len(best)<(1<<N):
    d+=1; nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for f in ops(a,b):
                if f in S: continue
                T=S|{f}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                if f not in best: best[f]=d
    frontier=nxt
    print("depth",d,"states",len(nxt),"covered",len(best),file=sys.stderr)
# stats: functions with exactly one satisfying assignment depending on all vars
uniq=[f for f in best if bin(f).count('1')==1]
print(json.dumps({"n":n,"max_gates":max(best.values()),
 "unique_sat_min_gates":sorted(set(best[f] for f in uniq)),
 "hist":{k:sum(1 for v in best.values() if v==k) for k in range(d+1)}}))
