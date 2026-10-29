"""Exact minimum B2-circuit size (2-input gates, all 16 binary ops) for all n-var
functions, n=1..3, by BFS over sets of computed truth tables. Wires = 2*gates."""
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[(lambda x,y,o=o:sum(1<<k for k in range(4) if (o>>k)&1 and False)) for o in range(0)]
    def app(o,x,y):
        r=0
        for k in range(4):
            if (o>>k)&1:
                a,b=k&1,(k>>1)&1
                m=(x if a else ~x&M)&(y if b else ~y&M)
                r|=m
        return r
    best={f:0 for f in [0,M]+inputs}   # constants/inputs free
    # iterative deepening on gate count: states = frozenset of available functions
    from collections import deque
    start=frozenset([0,M]+inputs)
    seen={start:0}; q=deque([start]); mn={}
    for f in start: mn[f]=0
    while q:
        s=q.popleft(); d=seen[s]
        if d>=int(sys.argv[2]): continue
        L=sorted(s)
        for x,y in itertools.combinations_with_replacement(L,2):
            for o in range(1,15):
                g=app(o,x,y)
                if g in s: continue
                t=s|{g}
                if t not in seen:
                    seen[t]=d+1; q.append(t)
                    if g not in mn: mn[g]=d+1
    return mn,N
n=int(sys.argv[1]); mn,N=run(n)
from collections import Counter
c=Counter(mn.values())
print(n,"funcs found",len(mn),"of",1<<(1<<n),dict(sorted(c.items())))
json.dump({"n":n,"count_by_gates":dict(sorted(c.items()))},open(f"mincircuit_n{n}.json","w"))
