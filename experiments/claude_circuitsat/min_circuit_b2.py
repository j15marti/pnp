"""Exact minimum fan-in-2 circuit size (basis B2 = all 16 binary gates, inputs/constants free)
for every Boolean function on n<=3 variables. Level-by-level exhaustive search.
Runtime ~ a few seconds. Output: results/raw/claude_circuitsat/min_circuit_b2.json"""
import json, itertools, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    base=[0,mask]+xs   # constants and inputs cost 0
    # state = frozenset of computed functions (sets of available truth tables); BFS on gate count
    best={}  # function -> min gates
    for f in base: best[f]=0
    frontier={frozenset(base)}
    gates=0
    gate_ops=[lambda a,b,t=t:(((t&1)and(~a&~b))|((t>>1&1)and(~a&b))|((t>>2&1)and(a&~b))|((t>>3&1)and(a&b))) for t in range(16)]
    def ap(t,a,b):
        r=0
        if t&1: r|=~a&~b
        if t&2: r|=~a&b
        if t&4: r|=a&~b
        if t&8: r|=a&b
        return r&mask
    while len(best)<(1<<N):
        gates+=1; new=set()
        for S in frontier:
            L=sorted(S)
            for i,a in enumerate(L):
                for b in L[i+1:]:
                    for t in range(1,15):
                        c=ap(t,a,b)
                        if c in S: continue
                        if c not in best: best[c]=gates
                        new.add(S|{c})
        frontier=new
        print(n,gates,len(frontier),len(best),file=sys.stderr)
    return best
out={}
for n in (1,2,3):
    b=run(n)
    from collections import Counter
    out[n]=dict(Counter(b.values()))
    out[n]['max']=max(b.values())
json.dump(out,open('/home/user/pnp/results/raw/claude_circuitsat/min_circuit_b2.json','w'),indent=1)
print(out)
