"""Exact minimum AIG size (2-input AND, free negation of any wire) for all n-var functions, n<=3.
Wires counted: 2 per gate. Output may be negated. Iterative-deepening DFS over gate sequences."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; FULL=(1<<N)-1
inp=[sum(1<<m for m in range(N) if (m>>i)&1) for i in range(n)]
best={0:0,FULL:0}
for t in inp: best[t]=0; best[FULL^t]=0
def dfs(sigs,k,limit):
    # record all functions reachable with k gates
    for s in sigs[-1:] if False else []: pass
def run():
    seen={}  # frozenset of signal sets at depth -> avoid dup
    level=[tuple(sorted(inp))]
    k=0
    while len(best)<(1<<N):
        k+=1; nxt=set()
        for sigs in level:
            lits=[x for s in sigs for x in (s,FULL^s)]
            for a,b in itertools.combinations(lits,2):
                g=a&b
                if g in sigs or (FULL^g) in sigs or g in (0,FULL): continue
                ns=tuple(sorted(sigs+(min(g,FULL^g),)))
                nxt.add(ns)
                for f in (g,FULL^g):
                    if f not in best: best[f]=k
        level=list(nxt)
    return k
K=run()
from collections import Counter
print(json.dumps({"n":n,"max_gates":K,"max_wires":2*K,"distribution":dict(sorted(Counter(best.values()).items()))}))
