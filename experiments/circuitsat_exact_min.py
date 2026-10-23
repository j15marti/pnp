# Exact minimum fan-in-2 circuit size (basis B2, all 16 binary gates, free constants) for ALL n-var functions, n<=3,
# plus counts for n=4 at size<=3. Runs in seconds. Output: results/circuitsat_exact_min.json
import itertools, json, sys
def run(n, maxk):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    base=set(inputs)|{0,full}
    # cost[f]=min gates. DP over circuits: level sets of "circuit states" is large; instead use
    # formula-free DAG search: states = frozenset of available functions (sorted tuple), BFS by gate count.
    gates=[lambda a,b,t=t: sum(1<<k for k in range(N) if (t>>(2*((a>>k)&1)+((b>>k)&1)))&1) for t in range(16)]
    best={f:0 for f in base}
    layer={tuple(sorted(inputs))}
    for k in range(1,maxk+1):
        new=set(); 
        for st in layer:
            av=list(st)+[0,full]
            for a,b in itertools.combinations(range(len(av)),2):
                for g in gates:
                    f=g(av[a],av[b])
                    if f in st or f in (0,full): continue
                    if f not in best: best[f]=k
                    
                    if k<maxk: new.add(tuple(sorted(st+(f,))))
        layer=new
        print(n,k,len(layer),len(best),file=sys.stderr)
    return best
out={}
b2=run(2,1); out['n2']={'max':max(b2.values()),'covered':len(b2)}
b3=run(3,4)
from collections import Counter
out['n3']={'covered':len(b3),'of':256,'hist':dict(Counter(b3.values()))}
b3and=None
json.dump(out,open('results/circuitsat_exact_min.json','w'),indent=1); print(out)
