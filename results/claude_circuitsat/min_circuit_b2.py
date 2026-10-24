"""Exact minimum B2 circuit size (fan-in-2 gates, all 10 nondegenerate binary ops) for all
Boolean functions on n<=3 inputs, via BFS over sets of computed truth tables.
Runtime budget ~30s. Usage: python3 min_circuit_b2.py n"""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[]
for t in range(16):
    # t: truth table of op over (a,b) bits
    f=lambda a,b,t=t:(((t>>0)&1)*(~a&~b)|((t>>1)&1)*(a&~b)|((t>>2)&1)*(~a&b)|((t>>3)&1)*(a&b))&M
    # degenerate: depends on <2 args
    vals=[(t>>k)&1 for k in range(4)]
    dep_a=vals[0]!=vals[1] or vals[2]!=vals[3]
    dep_b=vals[0]!=vals[2] or vals[1]!=vals[3]
    if dep_a and dep_b: ops.append(f)
start=frozenset(inputs|{0,M} if False else inputs)
best={}  # function -> min gates
for f in list(inputs)+[0,M]: best[f]=0; best[M^f]=0
frontier={start}; seen={start}; d=0
total=1<<N
while frontier and len(best)<total:
    d+=1; nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                g=op(a,b)
                if g in S: continue
                T=S|{g}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                for h in (g,M^g):
                    if h not in best: best[h]=d
    frontier=nxt
    print("depth",d,"states",len(nxt),"covered",len(best),"/",total,flush=True)
from collections import Counter
print(json.dumps({"n":n,"hist":sorted(Counter(best.values()).items()),"max":max(best.values())}))
