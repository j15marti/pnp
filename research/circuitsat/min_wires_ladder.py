"""Exact minimum fan-in-2 gate count (B2 basis, free negation/constants) for all
n-variable Boolean functions, n=1..3, by exhaustive DAG enumeration.
wires = 2*gates (gate input pins). Also tabulates by number of satisfying assignments.
Runtime well under 30 s for n<=3."""
import itertools, json, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[lambda a,b,t=t:sum((( t>>(2*((a>>k)&1)+((b>>k)&1)))&1)<<k for k in range(N)) for t in range(16)]
    best={}  # function -> min gates
    seen=set()
    base=tuple(xs)
    for f in [0,mask]+xs: best[f]=0
    def dfs(nodes,g,limit):
        for f in nodes[-1:]:
            if f not in best or best[f]>g: best[f]=g if f not in best else min(best[f],g)
        if g==limit: return
        L=len(nodes)
        for i in range(L):
            for j in range(i,L):
                for op in ops:
                    v=op(nodes[i],nodes[j])
                    if v in nodes or v in (0,mask): continue
                    key=frozenset(nodes+[v])
                    if (key,g+1) in seen: continue
                    seen.add((key,g+1))
                    dfs(nodes+[v],g+1,limit)
    maxg={1:1,2:3,3:4}[n]
    # iterative deepening so best[] is minimal
    dfs(list(base),0,maxg)
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    missing=[f for f in range(1<<N) if f not in b]
    tab={}
    for f,g in b.items():
        k=bin(f).count('1')
        tab.setdefault(k,{}); tab[k][g]=tab[k].get(g,0)+1
    out[n]={'covered':len(b),'missing':len(missing),'max_gates':max(b.values()),'by_sat_count':{k:dict(sorted(v.items())) for k,v in sorted(tab.items())}}
    print(n,out[n]['covered'],'/',1<<N,'max gates',out[n]['max_gates'])
json.dump(out,open('research/circuitsat/min_wires_ladder_results.json','w'),indent=1)
