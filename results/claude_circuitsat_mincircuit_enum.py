import itertools,sys,json
def run(n,maxg):
    N=1<<n; M=(1<<N)-1
    inp=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    gates=[g for g in range(16) if g not in (0,3,5,10,12,15)]  # drop constants/projections/negated projections
    def ap(g,x,y):
        r=0
        for b in range(4):
            if (g>>b)&1:
                xm=x if b&1 else M^x
                ym=y if b&2 else M^y
                r|=xm&ym
        return r
    best={}
    for f in inp: best[f]=0; best[M^f]=0
    best[0]=0;best[M]=0
    # BFS over circuits (ordered gate lists), canonical: up to maxg gates
    seen={tuple(sorted(inp)):0}
    frontier=[tuple(inp)]
    for d in range(1,maxg+1):
        nxt=set()
        for S in frontier:
            for x,y in itertools.combinations(S,2):
                for g in gates:
                    z=ap(g,x,y)
                    if z in S: continue
                    nxt.add(tuple(sorted(S+(z,))))
                    for w in (z,M^z):
                        if w not in best: best[w]=d
        frontier=list(nxt); print(n,d,len(frontier),len(best),file=sys.stderr)
    return best,N
for n,mg in ((2,2),(3,4)):
    b,N=run(n,mg)
    from collections import Counter
    c=Counter(b.values()); print(n,sorted(c.items()),len(b),"of",1<<N)
# unique-sat family n=4, 3 gates
b,N=run(4,3)
mint=[f for f in b if bin(f).count('1')==1]
print("n=4 minterms",len(mint),set(b[f] for f in mint))
