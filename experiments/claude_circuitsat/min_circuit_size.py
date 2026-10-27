"""Exact minimum B2 (all 2-input gates) circuit size for all n-variable functions, n<=3,
by breadth-first closure over sets of computed truth tables (gates reuse = fan-out allowed).
Runtime ~ few seconds. Output: results/raw/claude_circuitsat/min_size_n{2,3}.json"""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(((i>>v)&1)<<i for i in range(N)) for v in range(n)]
    ops=[lambda a,b,t=t:sum((((t>>(2*((a>>i)&1)+((b>>i)&1)))&1)<<i) for i in range(N)) for t in range(16)]
    # nontrivial gates: depend on both args
    def nontriv(t): return t not in (0,15,3,12,5,10)
    ops=[o for t,o in enumerate(ops) if nontriv(t)]
    best={}
    for f in [0,M]+inputs+[M^x for x in inputs]: best[f]=0   # free: constants, inputs, negated inputs (NOT free)
    # DFS iterative deepening on circuits (as sets of available functions)
    start=frozenset([0,M]+inputs)
    cost={f:0 for f in start}
    for f in inputs: cost[M^f]=0
    seen={start:0}
    frontier=[start]
    k=0
    while len(cost)<(1<<N) and k<12:
        k+=1; nxt=set()
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for o in ops:
                    g=o(a,b)
                    if g in S: continue
                    T=S|{g}
                    # allow free negation closure
                    T=T|{M^g}
                    if T in seen: continue
                    seen[T]=k; nxt.add(T)
                    for h in (g,M^g):
                        if h not in cost: cost[h]=k
        frontier=list(nxt)
        print(n,k,len(frontier),len(cost),file=sys.stderr)
    return cost
for n in (2,3):
    c=run(n)
    hist={}
    for v in c.values(): hist[v]=hist.get(v,0)+1
    N=1<<n
    names={}
    if n==3:
        def tt(fn): return sum(fn(i&1,(i>>1)&1,(i>>2)&1)<<i for i in range(8))
        names={"AND3":tt(lambda a,b,c:a&b&c),"OR3":tt(lambda a,b,c:a|b|c),"XOR3":tt(lambda a,b,c:a^b^c),
               "MAJ3":tt(lambda a,b,c:int(a+b+c>=2)),"MUX":tt(lambda a,b,c:b if a else c),"EXACT1":tt(lambda a,b,c:int(a+b+c==1))}
    json.dump({"n":n,"num_functions":len(c),"histogram_size":hist,"named":{k:c[v] for k,v in names.items()}},
      open(f"results/raw/claude_circuitsat/min_size_n{n}.json","w"),indent=1)
    print(n,len(c),hist,{k:c[v] for k,v in names.items()})
