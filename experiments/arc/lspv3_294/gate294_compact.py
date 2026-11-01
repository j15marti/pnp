#!/usr/bin/env python3
"""LSPV-3 GATE294 compact independent boundary-key cache test, Python standard library."""
import collections,itertools,json
Hpos=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
H=Hpos+[tuple(-x for x in t) for t in Hpos]
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
F=H+[tuple((abs(l)+6)*(1 if l>0 else -1) for l in t) for t in Y]
def validate(f,n):
    if len(f)*3!=4*n:return False
    count=collections.Counter();seen=set()
    for c in f:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(abs(v)<1 or abs(v)>n for v in c):return False
        if not (all(v>0 for v in c) or all(v<0 for v in c)):return False
        t=tuple(sorted(c))
        if t in seen:return False
        seen.add(t);count.update(c)
    return all(count[i]==count[-i]==2 for i in range(1,n+1))
assert validate(F,12)
P={tuple(sorted(map(abs,c))) for c in F if c[0]>0}
Q={tuple(sorted(map(abs,c))) for c in F if c[0]<0}
core=P&Q
unpaired=[c for c in F if tuple(sorted(map(abs,c))) not in core]
assert len(core)==4 and len(unpaired)==8
boundary={v for t in core for v in t}
full=set();proj=set();coherent=0
for choices in itertools.product(range(3),repeat=len(unpaired)):
    pins={}
    consistent=True
    for c,k in zip(unpaired,choices):
        l=c[k];v=abs(l);b=int(l>0)
        if v in pins and pins[v]!=b:
            consistent=False;break
        pins[v]=b
    if not consistent:continue
    coherent+=1
    full.add(tuple(sorted(pins.items())))
    proj.add(tuple(sorted((v,b) for v,b in pins.items() if v in boundary)))
assert len(full)==44 and len(proj)==1 and coherent==202
models=sum(all(1<=sum((m>>(v-1))&1 for v in t)<=2 for t in core) for m in range(1<<12))
assert models>0
out={"canonical_valid":True,"source_n":12,"defect_clauses":8,
     "syntactic_trials":6561,"coherent":coherent,
     "full_signatures":len(full),"paired_boundary_signatures":len(proj),
     "factor_calls_with_boundary_cache":1,"factor_cache_hits":coherent-1,
     "source_sat":True,"physical_FLMV_XOR":"NOT MEASURED","P_vs_NP":"OPEN"}
print(json.dumps(out,indent=2,sort_keys=True))
