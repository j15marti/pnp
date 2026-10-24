"""Exact min #gates (fan-in-2, all 16 binary ops = B2, free fan-out) for all
n-variable Boolean functions, n=1..3, by BFS over circuits (sets of truth tables).
Runs in well under 30 s. Wires = 2*gates (each gate has two incoming wires)."""
import json, itertools, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in (1,2,4,6,7,8,9,11,13,14)]
    best={0:0,mask:0}
    for v in inputs: best[v]=0; best[v^mask]=0
    # IDDFS over circuits; state = tuple of available tables
    maxg=7 if n<3 else 5
    seen=set()
    def dfs(avail,g,limit):
        key=frozenset(avail)
        if (key,g) in seen: return
        seen.add((key,g))
        for i in range(len(avail)):
            for j in range(i+1,len(avail)):
                for op in ops:
                    r=op(avail[i],avail[j])
                    if r in avail: continue
                    if r not in best or best[r]>g+1: best[r]=g+1
                    if g+1<limit: dfs(avail+[r],g+1,limit)
    dfs(list(inputs),0,maxg if n<3 else 4)
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    vals=[b.get(f) for f in range(1<<N)]
    missing=sum(v is None for v in vals)
    hist={}
    for v in vals:
        hist[str(v)]=hist.get(str(v),0)+1
    pts=[b[1<<x] for x in range(N)]
    out[n]=dict(max_gates=max(v for v in vals if v is not None),hist=hist,missing=missing,point_fn_gates=sorted(set(pts)))
print(json.dumps(out,indent=1))
json.dump(out,open(sys.argv[1],'w'),indent=1)
