# Exact minimum fan-in-2 circuit size (AND gates, free negation on every wire/output)
# for ALL boolean functions on n<=3 variables.  Layered BFS over sets of computed
# normalized functions (f(0)=0 normal form, since output negation is free).
import sys, itertools, json, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
def norm(f): return f^M if f&1 else f
lits=[]
for i in range(n):
    f=sum(1<<a for a in range(N) if (a>>i)&1); lits.append(norm(f))
allf=sorted({norm(f) for f in range(1<<N)})
def gates(avail):
    out=set()
    for a,b in itertools.combinations(avail,2):
        for ea in (0,M):
            for eb in (0,M):
                g=norm((a^ea)&(b^eb))
                if g not in avail: out.add(g)
    return out
best={}  # function -> min gates
for f in lits+[0]: best[f]=0
layer={frozenset(lits+[0])}  # 0 = constant (free)
k=0; t0=time.time()
while len(best)<len(allf):
    k+=1; nxt=set()
    for S in layer:
        for g in gates(sorted(S)):
            T=S|{g}; nxt.add(T)
            if g not in best: best[g]=k
    layer=nxt
    print(f"n={n} gates={k} states={len(layer)} known={len(best)}/{len(allf)} t={time.time()-t0:.1f}s",flush=True)
mx=max(best.values()); hard=[f for f,v in best.items() if v==mx]
print(json.dumps({"n":n,"max_gates":mx,"max_wires":2*mx,"num_hardest_normalized":len(hard),
 "hist":{v:sum(1 for x in best.values() if x==v) for v in sorted(set(best.values()))}}))
