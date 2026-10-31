"""Exact minimum gate count (fan-in 2, AND-type gates with free negation on wires,
i.e. basis {AND,OR,NAND,NOR,and negated-input variants}; XOR counted separately)
for all Boolean functions on n<=3 inputs, by BFS on sets of computed functions.
Wires = 2*gates (fan-in 2).  Runs in a few seconds."""
import itertools, json, sys
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
vars_=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def ops(a,b,xor):
    r=set()
    for na in (a,a^M):
        for nb in (b,b^M):
            r.add(na&nb); r.add((na&nb)^M)
    if xor: r.add(a^b); r.add((a^b)^M)
    return r
def solve(xor,maxg=7):
    best={0:0,M:0}
    for v in vars_: best[v]=0; best[v^M]=0
    # iterative deepening over circuits as sets of available functions
    level={frozenset([v for v in vars_])}
    cost={}
    for f in list(best): cost[f]=0
    for g in range(1,maxg+1):
        nxt=set()
        for S in level:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for h in ops(a,b,xor):
                    hh=min(h,h^M)
                    if hh in S: continue
                    if h not in cost: cost[h]=g; cost[h^M]=g
                    nxt.add(S|{hh})
        level=nxt
        if len(cost)==N and False: break
        print(xor,g,len(level),len(cost),file=sys.stderr)
        if len(cost)>= (1<<N) : break
        if len(level)>300000: break
    return cost
for xor in (False,True):
    c=solve(xor)
    hist={}
    for f in range(1<<N):
        hist[c.get(f,None)]=hist.get(c.get(f,None),0)+1
    print("n",n,"xor",xor,"gate-count histogram",dict(sorted(hist.items(),key=lambda t:(t[0] is None,t[0]))))
