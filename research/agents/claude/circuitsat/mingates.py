# Exact min #AND-gates (free negation on wires, so OR is included) for all n-var functions.
# BFS over sets of computed functions; wires = 2*gates. Runs < 30s for n<=3.
import sys, itertools
n=int(sys.argv[1]); N=1<<(1<<n); M=N-1
X=[sum(1<<a for a in range(1<<n) if (a>>i)&1) for i in range(n)]
best={}
def lits(S): return [f for g in S for f in (g,M^g)]
start=frozenset(X)
for f in X: best[f]=best[M^f]=0
best[0]=best[M]=0
layer={start}; seen={start}; d=0
while layer and d<7:
    d+=1; nxt=set()
    for S in layer:
        L=lits(S)
        for a,b in itertools.combinations(L,2):
            g=a&b
            if g in S or (M^g) in S: continue
            T=S|{g}
            if T in seen: continue
            seen.add(T); nxt.add(T)
            for h in (g,M^g):
                if h not in best: best[h]=d
    layer=nxt
from collections import Counter
print("n",n,"funcs",N,"resolved",len(best),"max gates",max(best.values()))
print(sorted(Counter(best.values()).items()))
