"""Exact minimum circuit size over the full binary basis B2 (all 16 two-input gates),
fan-in 2, unbounded fan-out. Wires = 2*gates. Level-by-level set of reachable
(multi)sets of truth tables, deduplicated; n<=3 exhaustive, n=4 by chunked search.
Usage: python3 minsize.py n [maxsize]"""
import sys, itertools, json
n=int(sys.argv[1]); R=1<<n; M=(1<<R)-1
def var(i):
    t=0
    for x in range(R):
        if (x>>i)&1: t|=1<<x
    return t
inputs=tuple(sorted({var(i) for i in range(n)}))
def gates(a,b):
    for g in range(16):
        t=0
        for x in range(R):
            if (g>>(2*((a>>x)&1)+((b>>x)&1)))&1: t|=1<<x
        yield t
trivial={0,M}|set(inputs)|{M^v for v in inputs}
best={f:0 for f in trivial}   # constants/literals cost 0 (negation free in B2)
frontier={frozenset(inputs)}
size=0; maxs=int(sys.argv[2]) if len(sys.argv)>2 else 8
seen={frozenset(inputs)}
while frontier and size<maxs:
    size+=1; new=set()
    for S in frontier:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for t in gates(a,b):
                if t in S or t in trivial: continue
                S2=S|{t}
                if S2 in seen: continue
                seen.add(S2); new.add(S2)
                if t not in best: best[t]=size
    frontier=new
    print("size",size,"states",len(frontier),"fns",len(best),file=sys.stderr)
    if len(best)==(1<<R): break
hist={}
for f,s in best.items(): hist[s]=hist.get(s,0)+1
def name(f):
    return {"AND":(1<<(R-1)),"OR":M^1,"XOR":sum(1<<x for x in range(R) if bin(x).count("1")%2),
     "MAJ":sum(1<<x for x in range(R) if bin(x).count("1")*2>n)}
out={"n":n,"hist":hist,"covered":len(best),"total":1<<R,"named":{k:best.get(v) for k,v in name(0).items()}}
print(json.dumps(out))
