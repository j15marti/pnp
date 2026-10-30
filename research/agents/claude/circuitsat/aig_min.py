# Exact min AIG size (AND gates, free negation) for all n-var functions, n<=3, and min formula leaf count.
import sys, itertools, json, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
vars_=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
def norm(t): return min(t, M^t)
best={}; t0=time.time()
start=frozenset(norm(v) for v in vars_)
for f in [0]+list(start): best[norm(f)]=0
level={start}; seen={start}; k=0
total=(1<<N)//2
while level and len(best)<total and time.time()-t0<25:
    k+=1; nxt=set()
    for S in level:
        lits=[x for s in S for x in (s,M^s)]+[0,M]
        for a,b in itertools.combinations(lits,2):
            g=a&b; ng=norm(g)
            if ng in S or ng in (0,): continue
            if ng not in best: best[ng]=k
            T=S|{ng}
            if T not in seen: seen.add(T); nxt.add(T)
    level=nxt
# formula leaf-count (fanout-1), AND with free negation
L={}
for v in vars_: L[v]=1; L[M^v]=1
L[0]=0; L[M]=0
ch=True
while ch:
    ch=False
    items=list(L.items())
    for (a,la),(b,lb) in itertools.product(items,items):
        for g in (a&b,): 
            for h in (g,M^g):
                c=la+lb
                if h not in L or L[h]>c: L[h]=c; ch=True
res={'n':n,'complete':len(best)==total,'num_classes':len(best),
 'aig_size_hist':{},'max_aig':max(best.values()),'formula_leaves_max':max(L.values()),
 'formula_hist':{}}
for v in best.values(): res['aig_size_hist'][v]=res['aig_size_hist'].get(v,0)+1
for v in L.values(): res['formula_hist'][v]=res['formula_hist'].get(v,0)+1
print(json.dumps(res))
