# Exact minimum B2 (all 2-input gates) circuit size of every n-input Boolean function, n<=3,
# by BFS over sets of computed truth tables (circuit = set of functions available).
# Wires counted: fan-in-2 => wires = 2*gates (each gate has two incoming wires). Runs in seconds.
import itertools, json, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[(lambda x,y,t=t:sum(1<<k for k in range(N)
          if (t>>(2*((x>>k)&1)+((y>>k)&1)))&1)) for t in range(16)]
    best={}   # function -> min gates
    for f in [0,full]+inputs+[full^i for i in inputs]: best[f]=0
    # frontier of states: frozenset of available functions (inputs + gates)
    start=frozenset(inputs); level={start}; seen={start}
    for g in range(1,12):
        nxt=set()
        for S in level:
            L=sorted(S)
            for a,b in itertools.combinations(L,2):
                for op in ops:
                    h=op(a,b)
                    if h in S: continue
                    for hh in (h,full^h):
                        if hh not in best: best[hh]=g
                    T=S|{h}
                    if T not in seen: seen.add(T); nxt.add(T)
        level=nxt
        if len(best)==1<<N: break
    return best
res={}
for n in (1,2,3):
    b=run(n); hist={}
    for f,g in b.items(): hist[g]=hist.get(g,0)+1
    res[n]={"gates_hist":dict(sorted(hist.items())),"max_gates":max(b.values()),"count":len(b)}
    print(n,res[n])
json.dump(res,open("minsize_results.json","w"),indent=1)
