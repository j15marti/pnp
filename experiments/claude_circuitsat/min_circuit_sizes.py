"""Exact minimum fan-in-2 circuit size over the full basis B2 (all 16 binary gates)
for every Boolean function on n<=3 inputs; plus unique-satisfier classes.
Wires = 2*gates (each gate has two in-wires; fan-out edges are the same wires counted at their sink).
Runs in a few seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    inputs=[]
    for i in range(n):
        t=0
        for x in range(N):
            if (x>>i)&1: t|=1<<x
        inputs.append(t)
    ops=[lambda a,b,k=k: sum(((k>>(2*((a>>0)&1)+0))&0) for _ in [0]) for k in range(0)]  # placeholder
    def gate(k,a,b):  # k in 0..15 truth table of g(u,v) indexed 2u+v
        r=0
        # bitwise: g(u,v)=OR over (u,v) with bit set
        for u in (0,1):
            for v in (0,1):
                if (k>>(2*u+v))&1:
                    r|= (a if u else ~a&mask) & (b if v else ~b&mask)
        return r&mask
    best={}  # function -> min gates
    consts=[0,mask]
    start=frozenset(inputs)
    for f in list(inputs)+consts: best[f]=0
    # BFS over states (sets of computed functions), depth-limited, dedup states
    frontier={start}; seen={start}
    depth=0
    while len(best)<(1<<N) and depth<8:
        depth+=1; new=set()
        for st in frontier:
            L=list(st)
            for a,b in itertools.combinations_with_replacement(L,2):
                for k in range(16):
                    g=gate(k,a,b)
                    if g in st: continue
                    ns=st|{g}
                    if ns in seen: continue
                    seen.add(ns); new.add(ns)
                    if g not in best: best[g]=depth
        frontier=new
    return best
out={}
for n in (1,2,3):
    b=run(n); N=1<<n
    hist={}
    for f,c in b.items(): hist[c]=hist.get(c,0)+1
    # unique-satisfier functions (exactly one satisfying assignment)
    uniq=[c for f,c in b.items() if bin(f).count('1')==1]
    par=0
    for x in range(N):
        if bin(x).count('1')%2: par|=1<<x
    maj=0
    for x in range(N):
        if bin(x).count('1')*2>n: maj|=1<<x
    out[n]=dict(num_functions=len(b),hist={str(k):v for k,v in sorted(hist.items())},
        max_gates=max(b.values()),unique_sat_min=min(uniq),unique_sat_max=max(uniq),
        parity=b[par],majority=b[maj])
    print(n,out[n],flush=True)
json.dump(out,open('../../results/raw/claude_circuitsat_min_sizes.json','w'),indent=1)
