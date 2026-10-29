"""Exact minimum B2 (fan-in 2, all 16 binary gates) circuit size C(f) for all f on n<=3 inputs.
Level-by-level BFS over sets of computed nodes (inputs + gates). Runtime well under 30 s for n<=3 (cap k<=6).
Usage: python3 mincircuit.py N KMAX"""
import sys, json, itertools
n=int(sys.argv[1]); KMAX=int(sys.argv[2]); R=1<<n; FULL=(1<<R)-1
def var(i): return sum(1<<x for x in range(R) if (x>>i)&1)
inputs=tuple(sorted(var(i) for i in range(n)))
ops=range(16)
def g(op,a,b):
    r=0
    for k,(p,q) in enumerate(((0,0),(0,1),(1,0),(1,1))):
        if (op>>k)&1:
            r|=(a if p else FULL^a)&(b if q else FULL^b)
    return r
# nondegenerate: result depends on both args => skip constants/projections/negated projections
nd=[o for o in ops if o not in (0,15,3,12,5,10)]
best={}  # function -> min gates (f and ~f identified)
def norm(f): return min(f,FULL^f)
for v in inputs: best[norm(v)]=0
best[0]=0
level={frozenset(inputs)}
for k in range(1,KMAX+1):
    nxt=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for o in nd:
                h=g(o,a,b)
                if h in S or (FULL^h) in S: continue
                nxt.add(S|{h})
                nf=norm(h)
                if nf not in best: best[nf]=k
    level=nxt
    print(k,len(level),len(best),file=sys.stderr)
    if len(best)==(1<<(R-1)): break
out={}
for f,c in best.items():
    for ff in (f,FULL^f): out[ff]=c
json.dump({"n":n,"complete":len(out)==(1<<R),"C":{str(f):c for f,c in out.items()}},open(f"mincircuit_n{n}.json","w"))
from collections import Counter
print("n",n,"complete",len(out)==(1<<R),"hist C:",sorted(Counter(out.values()).items()))
# SAT-count vs min size
by={}
for f,c in out.items():
    w=bin(f).count("1"); by.setdefault(w,[]).append(c)
for w in sorted(by): print("sat=",w,"minC",min(by[w]),"maxC",max(by[w]),"count",len(by[w]))
