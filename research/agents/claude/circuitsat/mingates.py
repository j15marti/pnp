# Exact min gate count (fan-in 2, AND/OR, free negation on wires) per Boolean function, n<=3.
# Level-by-level closure: size[f] = min over decompositions. Standard DP over sets of reachable truth tables.
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    base={0,M}|set(xs)|{M^x for x in xs}
    best={f:0 for f in base}
    # size k functions = f op g with cost(f)+cost(g)+1 under tree-cost (formula-ish upper bound) -> use circuit via sharing search instead
    # exact circuit size: BFS over sets of computed functions (n<=3 feasible for small k)
    from collections import deque
    start=frozenset(xs)
    seen={start:0}; res={}
    def lits(S): return set(S)|{M^s for s in S}|{0,M}
    frontier=[start]
    for k in range(0,8):
        for S in frontier:
            for f in lits(S):
                if f not in res or res[f]>k: res[f]=k
        if k==7: break
        nxt=set()
        for S in frontier:
            L=sorted(lits(S))
            for a,b in itertools.combinations(L,2):
                for g in (a&b,a|b):
                    if g not in lits(S): nxt.add(frozenset(S|{g}))
        nxt={S for S in nxt if S not in seen}
        for S in nxt: seen[S]=k+1
        frontier=list(nxt)
        if len(frontier)>400000: print("cap at k",k+1,file=sys.stderr); break
    return res
for n in (1,2,3):
    r=run(n); N=1<<n
    pt=[a for a in range(N)]
    # point functions (exactly one satisfying assignment)
    pts=sorted({r.get(1<<a,None) for a in range(N)}, key=str)
    mx=max(r.values()); print(n,"funcs resolved",len(r),"of",1<<N,"max size",mx,"point fn size",pts)
