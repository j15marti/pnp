# Exact minimum B2-circuit size (fan-in 2, all 16 binary gates, inputs free fan-out) for all n-var functions, n<=3.
# Wires = 2*gates (+0; output is a node). Chunk: n=1,2,3 each runs in seconds.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
def var(i): return sum(1<<x for x in range(N) if (x>>i)&1)
ins=tuple(var(i) for i in range(n))
def gates(a,b):
    out=set()
    for op in range(16):
        v=0
        for k,(p,q) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            if (op>>k)&1:
                v|=( (a if p else a^M) & (b if q else b^M) )
        out.add(v)
    return out
best={}  # function -> min gates
consts={0,M}
for f in list(ins)+[0,M]: best[f]=0
for f in ins: best[f^M]=1 if False else best.get(f^M,None) or None
best={f:0 for f in set(ins)|{0,M}}
frontier={tuple(sorted(ins))}
size=0
states={frozenset(ins)}
while len(best)<(1<<N) and size<7:
    size+=1; new=set()
    for st in states:
        L=list(st)
        for a,b in itertools.combinations_with_replacement(L,2):
            for g in gates(a,b):
                if g in st: continue
                ns=st|{g}
                new.add(ns)
                if g not in best: best[g]=size
    states=new
    print("size",size,"states",len(states),"covered",len(best),flush=True)
    if len(states)>300000: break
from collections import Counter
print(n,sorted(Counter(best.values()).items()))
json.dump({"n":n,"dist":sorted(Counter(best.values()).items()),"covered":len(best)},open(f"minsize_n{n}.json","w"))
