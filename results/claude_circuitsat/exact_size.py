# Exact B2 circuit size (fan-in 2, all 16 binary gates, free negation) for all n-input functions.
# BFS over sets of computed functions (truth tables), level = #gates. Usage: python3 exact_size.py n maxdepth
import sys, json, itertools
n=int(sys.argv[1]); D=int(sys.argv[2]); N=1<<n; M=(1<<N)-1
inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
def norm(f): return min(f,M^f)          # free negation: identify f with ~f
ops=[lambda a,b:a&b, lambda a,b:a&(M^b), lambda a,b:(M^a)&b, lambda a,b:a^b]  # AND-type + XOR up to negation
def gates(a,b):
    r={a&b,a&(M^b),(M^a)&b,(M^a)&(M^b),a^b}
    return {norm(x) for x in r}
base=frozenset(norm(x) for x in inputs)
best={f:0 for f in base}; best[0]=0   # constants cost 0
level={base}; seen={base}
for k in range(1,D+1):
    new=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for g in gates(a,b):
                if g in S: continue
                T=S|{g}
                if T not in seen: seen.add(T); new.add(T)
                if g not in best: best[g]=k
    level=new
    print(k,len(level),len(best),file=sys.stderr)
    if len(best)>=(1<<(N-1)) : break
from collections import Counter
c=Counter(best.values())
print(json.dumps({"n":n,"classes_up_to_negation_total":1<<(N-1),"found":len(best),"count_by_size":dict(sorted(c.items()))}))
