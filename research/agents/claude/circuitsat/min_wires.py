# Minimal 2-input-gate (AND/OR, free negations) circuit size and wire count
# for all Boolean functions on n inputs, n<=3. Runs in a few seconds.
import sys, itertools, json
def run(n):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    lits=set()
    for t in inputs: lits|={t,full^t}
    lits|={0,full}
    # best[f] = min gates; BFS over sets of available literal-closed functions
    best={}
    for f in lits: best[f]=0
    # state: frozenset of computed (positive) functions; iterative deepening on gate count
    def close(S): return S|{full^t for t in S}
    start=frozenset(lits)
    frontier={start}; g=0; seen={start}
    while frontier and len(best)<=full:
        g+=1; new=set()
        for S in frontier:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for h in (a&b,a|b):
                    if h not in S:
                        T=frozenset(close(S|{h}))
                        for f in (h,full^h):
                            if f not in best: best[f]=g
                        if T not in seen: seen.add(T); new.add(T)
        frontier=new
        if g>=5: break
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n; full=(1<<N)-1
    mx=max(b.values()); cnt=len(b)
    out[n]={"functions_found":cnt,"of":1<<N,"max_gates":mx,"max_wires":2*mx}
    print(n,out[n])
json.dump(out,open("min_wires_results.json","w"),indent=1)
