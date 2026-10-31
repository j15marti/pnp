# Exact min #fan-in-2 gates (full binary basis) per n-input Boolean function, n=1..3.
# Layered BFS over DAG states (frozenset of truth tables); last gate handled without storing layer.
import sys, json, itertools
n=int(sys.argv[1]); maxd=int(sys.argv[2])
N=1<<n; M=(1<<N)-1
ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
lits=set(ins)|{M^x for x in ins}|{0,M}
cost={f:0 for f in lits}
def ops(a,b):
    for op in range(16):
        r=0
        for k,(x,y) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (op>>k)&1:
                r|=((a if x else M^a)&(b if y else M^b))
        yield r
layer={frozenset(ins)}
for d in range(1,maxd+1):
    new=set()
    for st in layer:
        L=list(st)
        for a,b in itertools.combinations(L,2):
            for r in ops(a,b):
                if r not in cost: cost[r]=d
                if d<maxd and r not in st: new.add(st|{r})
    layer=new
    print("layer",d,len(layer),file=sys.stderr)
tot=1<<N
dist={}
for f in range(tot):
    c=cost.get(f); dist[str(c)]=dist.get(str(c),0)+1
needle=max(cost[f] for f in cost if bin(f).count("1")==1) if n>0 else 0
json.dump({"n":n,"maxdepth":maxd,"dist":dist,"needle_cost":needle,
 "parity_cost":cost.get(sum(1<<a for a in range(N) if bin(a).count("1")%2)),
 "maj_cost":cost.get(sum(1<<a for a in range(N) if bin(a).count("1")*2>n))},open(f"mincost_n{n}.json","w"))
print(open(f"mincost_n{n}.json").read())
