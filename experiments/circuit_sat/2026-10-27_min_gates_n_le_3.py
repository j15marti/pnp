#!/usr/bin/env python3
"""Exact minimum fan-in-2 AND/OR circuits (free negation on wires) for all Boolean functions of n<=3 inputs.
Cost = #binary gates; wires into gates = 2*gates. Functions identified up to complement (free output negation).
Level-BFS over deduplicated node-sets; each run < 30s. Usage: python3 script.py n"""
import sys, itertools, json
n=int(sys.argv[1]); R=1<<n; M=(1<<R)-1
def cls(f): return min(f,f^M)
xs=[]
for i in range(n):
    t=0
    for a in range(R):
        if (a>>i)&1: t|=1<<a
    xs.append(t)
base=frozenset(cls(x) for x in xs)
best={cls(0):0}
for x in xs: best[cls(x)]=0
total=len({cls(f) for f in range(M+1)})
level={frozenset()}  # gate-class sets
seen={frozenset()}
k=0
while len(best)<total:
    k+=1; nxt=set()
    for S in level:
        nodes=list(base|S)
        for a,b in itertools.combinations(nodes,2):
            for pa in (0,M):
                for pb in (0,M):
                    g=cls((a^pa)&(b^pb))
                    if g in base or g in S: continue
                    T=S|{g}
                    if T not in nxt: nxt.add(T)
                    if g not in best: best[g]=k
    level=nxt
    print("level",k,"states",len(level),"classes found",len(best),"/",total,file=sys.stderr)
from collections import Counter
c=Counter(best.values())
print(json.dumps({"n":n,"classes":total,"histogram_by_gates":dict(sorted(c.items())),"max_gates":max(best.values())}))
