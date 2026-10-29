"""Exact minimum B2 (all 2-input gates) circuit size for every n-input function, n<=3.
Wires counted = 2*gates (fan-in 2). Layered DP: S_k = set of frozensets of computed
truth tables reachable with k gates (state = set of available functions)."""
import itertools, json, sys
n=int(sys.argv[1]); N=1<<(1<<n); M=N-1
vars_=[sum(((a>>i)&1)<<a for a in range(1<<n)) for i in range(n)]
gates=range(16)
def ap(g,x,y):
    r=0
    for b in range(4):
        if (g>>b)&1:
            r|=( (x if (b>>1)&1 else ~x) & (y if b&1 else ~y) )
    return r&M
start=frozenset(vars_)
best={}   # function -> min gates
for f in range(N):
    if f in (0,M) or f in vars_ or (M^f) in vars_: best[f]=0
level={start}; seen={start}; k=0
while len(best)<N and k<8:
    k+=1; nxt=set()
    for S in level:
        L=sorted(S)
        for x,y in itertools.combinations(L,2):
            for g in gates:
                h=ap(g,x,y)
                if h in S: continue
                T=S|{h}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                for z in (h,M^h):
                    if z not in best: best[z]=k
    level=nxt
    print("k",k,"states",len(level),"covered",len(best),file=sys.stderr)
from collections import Counter
c=Counter(best.values())
tab={}
for f,k in best.items():
    key=(bin(f).count("1"),k); tab[key]=tab.get(key,0)+1
print(json.dumps({"n":n,"count_by_gates":dict(sorted(c.items())),"max":max(best.values()),
 "minsize_by_satcount":{str(j):min(k for (jj,k) in tab if jj==j) for j in sorted({a for a,_ in tab})}}))
