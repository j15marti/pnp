"""Exact minimum B2 (all 2-input gates) circuit size, n<=3 inputs, by layered BFS over
gate-sets. Wires = 2*gates (fan-in 2). Also tracks min size of the SAT-instance 'f != 0'
(trivial) and of functions with unique satisfying assignment (point functions)."""
import itertools, json, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    ops=list(range(16))
    def app(o,a,b):
        r=0
        for k,(p,q) in enumerate(((0,0),(0,1),(1,0),(1,1))):
            if (o>>k)&1:
                r|=(a if p else ~a&mask)&(b if q else ~b&mask)
        return r
    best={}  # truth table -> min gates
    for t in [0,mask]+inputs+[~i&mask for i in inputs]: best[t]=0
    # frontier: sets of computed functions (inputs+gates); iterative deepening on gate count
    level={frozenset(inputs)}
    for g in range(1,8):
        nxt=set()
        for S in level:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for o in ops:
                    r=app(o,a,b)
                    if r in S: continue
                    for t in (r,~r&mask):
                        if t not in best: best[t]=g
                    nxt.add(S|{r})
        level=nxt
        if len(best)>=1<<N: break
        if len(level)>400000: return best,g,False
    return best,g,True
out={}
for n in (1,2,3):
    best,g,done=run(n)
    N=1<<n
    out[n]={"gates_max":max(best.values()),"functions_resolved":len(best),"of":1<<N,"complete":done and len(best)==1<<N,
      "point_fn_gates":best.get(1,None),"parity_gates":best.get(sum(1<<x for x in range(N) if bin(x).count('1')%2),None)}
    print(n,out[n],flush=True)
json.dump(out,open("results/raw/claude_circuitsat/exact_min_circuits.json","w"),indent=1)
