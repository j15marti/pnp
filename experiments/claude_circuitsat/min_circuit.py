"""Exact minimum B2-circuit size (2-input gates, all 16 binary ops, free negation absorbed) for all
n-variable functions, n<=3, by iterative-deepening over gate sequences. Runs well under 30 s."""
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=range(16)
    def ap(op,u,v):
        r=0
        for a in range(N):
            r|=((op>>((((u>>a)&1)<<1)|((v>>a)&1)))&1)<<a
        return r
    # normalized: functions f and ~f equivalent cost; store up to complement
    best={}
    def norm(f): return min(f,f^M)
    level=[tuple(xs)]; seen={}
    # BFS over (sorted tuple of available funcs); cost = #gates
    from collections import deque
    start=frozenset(norm(x) for x in xs)|{0}
    for f in start: best[f]=0
    frontier=[start]; vis={start}
    d=0
    while frontier and d<8:
        d+=1; nxt=[]
        for S in frontier:
            L=list(S)
            for u,v in itertools.combinations(L,2):
                for op in range(1,15):
                    g=norm(ap(op,u,v))
                    if g in S: continue
                    S2=S|{g}
                    if g not in best: best[g]=d
                    if S2 not in vis and d<6:
                        vis.add(S2); nxt.append(S2)
        frontier=nxt
        if len(best)>=(1<<(N-1)): break
    return best,N
for n in (1,2,3):
    best,N=run(n)
    from collections import Counter
    c=Counter(best.values())
    print(n,"classes(up to compl.)",len(best),"of",1<<(N-1),dict(sorted(c.items())))
