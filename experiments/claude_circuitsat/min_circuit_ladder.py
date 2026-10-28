"""Exact minimum B2 circuit size (fan-in-2 gates, all 16 binary gates, free negation
via gate choice) for every n-input Boolean function, n<=3, by layered search over
sets of computed truth tables. Wires = 2*gates (fan-in 2). Runs in seconds."""
import itertools, json, sys
def run(n, maxg):
    rows = 1<<n; full=(1<<rows)-1
    ins=[sum(((r>>i)&1)<<r for r in range(rows)) for i in range(n)]
    best={}  # function -> min gates
    for f in [0,full]+ins+[full^x for x in ins]: best[f]=0
    # DFS over circuits as sequences of tables, iterative deepening; record min gates per function
    def gate_outs(a,b):
        for g in range(16):
            o=0
            for r in range(rows):
                x=(a>>r)&1;y=(b>>r)&1
                if (g>>(2*x+y))&1:o|=1<<r
            yield o
    visited=set()
    def dfs(tabs,g):
        key=frozenset(tabs)
        if key in visited: return
        visited.add(key)
        for t in tabs:
            if best.get(t,99)>g and t not in ():
                best[t]=min(best.get(t,99),g) if g>0 else 0
        if g==maxg: return
        seen=set(tabs)
        for a,b in itertools.combinations(range(len(tabs)),2):
            for o in set(gate_outs(tabs[a],tabs[b])):
                if o in seen: continue
                dfs(tabs+[o],g+1)
    dfs(list(ins),0)
    return best
res={}
for n,maxg in [(2,3),(3,4)]:
    b=run(n,maxg)
    hist={}
    for f in range(1<<(1<<n)):
        k=b.get(f)
        if f in (0,(1<<(1<<n))-1): k=0
        hist[str(k)]=hist.get(str(k),0)+1
    res[n]=hist
    print(n,hist)
json.dump(res,open("../../results/raw/claude_circuitsat_min_size.json","w"),indent=1)
