"""Exact min #AND-gates (fan-in 2, free edge negation, free output negation) for all n-input
Boolean functions, n<=3, by BFS over sets of computed truth tables (canonical frozensets).
Wires = 2*gates (fan-in 2).  Usage: python mincirc.py [n]"""
import sys, itertools, json
n=int(sys.argv[1]) if len(sys.argv)>1 else 2
N=1<<n; FULL=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def norm(t): return min(t,FULL^t)   # negation free
start=frozenset(norm(t) for t in inputs)
best={}  # normalized fn -> min gates
for t in start: best[t]=0
level={start}; seen={start}; g=0
while level and len(best)<(1<<(N-1)):
    g+=1; nxt=set()
    for S in level:
        L=list(S)+[]
        full=[]
        for t in L: full+= [t,FULL^t]
        full+=[0]  # constant handled separately
        for a,b in itertools.combinations(full,2):
            c=norm(a&b)
            if c in S: continue
            T=S|{c}
            if T in seen: continue
            seen.add(T); nxt.add(T)
            if c not in best: best[c]=g
    level=nxt
    print(f"gates={g} states={len(level)} funcs_found={len(best)}/{1<<(N-1)}",flush=True)
from collections import Counter
cnt=Counter(best.values())
print(dict(sorted(cnt.items())))
json.dump({"n":n,"count_by_gates_up_to_negation":dict(cnt),"max_gates":max(best.values())},open(f"mincirc_n{n}.json","w"))
