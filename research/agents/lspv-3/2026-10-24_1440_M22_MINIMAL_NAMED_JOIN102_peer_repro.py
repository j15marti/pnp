#!/usr/bin/env python3
"""M22-MINIMAL-NAMED-JOIN102 independent standard-library peer reproducer.
Run: python 2026-10-24_1440_M22_MINIMAL_NAMED_JOIN102_peer_repro.py
Finite checks only; not an FLMV-machine time/space measurement.
"""
import itertools as I
import json
from collections import Counter
P=((1,2,4),(1,2,5),(3,4,6),(3,5,6))
Q=((1,2,4),(1,2,6),(3,4,5),(3,5,6))
YP=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
YQ=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
def mk(p,n):
    return tuple(p)+tuple(tuple(-u for u in c) for c in n)
def truth(cs,x):
    return all(any(((x>>(abs(v)-1))&1)==int(v>0) for v in c) for c in cs)
def sol(cs,k):
    return [x for x in range(1<<k) if truth(cs,x)]
def projection(x,ids):
    return tuple((x>>(i-1))&1 for i in ids)
def grammar(cs):
    if len(set(cs))!=len(cs):return False,False,0
    dp=Counter();dn=Counter();pp=set();qq=set()
    for c in cs:
        if len(c)!=3 or len({abs(v) for v in c})!=3 or not (all(v>0 for v in c) or all(v<0 for v in c)):
            return False,False,0
        support=tuple(sorted(map(abs,c)))
        (pp if c[0]>0 else qq).add(support)
        for v in c:(dp if v>0 else dn)[abs(v)]+=1
    names=set(dp)|set(dn)
    valid=all(dp[n]==dn[n]==2 for n in names)
    return valid,valid and pp!=qq,len(pp-qq)
base=mk(P,Q); assert grammar(base)==(True,True,2)
YY=mk(YP,YQ); assert grammar(YY)[1] and len(sol(YY,6))==20
bs=sol(base,6); assert len(bs)==24
T=set(I.product((0,1),repeat=3))-{(0,0,1),(1,1,0)}
assert {projection(x,(1,2,3)) for x in bs}==T
for a,b,c in I.product((0,1),repeat=3):
    prefix=a|(b<<1)|(c<<2)
    plus={h for h in range(8) if truth(mk(P,()),prefix|(h<<3))}
    minus={h for h in range(8) if truth(mk((),Q),prefix|(h<<3))}
    assert plus and minus and (bool(plus&minus)==((a,b,c) in T))
for pair in I.combinations((1,2,3),2):
    assert len({projection(x,pair) for x in bs})==4
tri=tuple(I.combinations(range(1,7),3))
fac=[f for f in I.combinations(tri,4) if all(sum(v in c for c in f)==2 for v in range(1,7))]
assert len(fac)==75
byq=Counter(); bymodels=Counter(); byboundary=Counter(); missing_pair=0
for p in fac:
    for n in fac:
        cs=mk(p,n);ok,target,q=grammar(cs)
        assert ok
        mm=sol(cs,6)
        assert mm
        byq[q]+=1; bymodels[len(mm)]+=1
        if target:byboundary[len({projection(x,(1,2,3)) for x in mm})]+=1
        for pair in I.combinations(range(1,7),2):
            missing_pair+=(len({projection(x,pair) for x in mm})<4)
assert dict(byq)=={0:75,2:1260,3:1680,4:2610}
assert dict(byboundary)=={6:456,7:1854,8:3240}
assert dict(bymodels)=={18:450,19:240,20:1080,21:1440,22:1650,24:720,26:45}
assert missing_pair==0
def tensor(r):
    return tuple(tuple((1 if v>0 else -1)*(abs(v)+6*j) for v in c)
                 for j in range(r) for c in base)
for r in (1,2,3):
    cc=tensor(r)
    assert grammar(cc)==(True,True,2*r)
    mm=sol(cc,6*r)
    assert len(mm)==24**r
    bb=tuple(6*j+i for j in range(r) for i in (1,2,3))
    assert len({projection(x,bb) for x in mm})==6**r
assert not truth(((1,),(-1,)),0) and not truth(((1,),(-1,)),1)
print(json.dumps({
    "status":"COMPUTATIONAL (finite); source theorem separate",
    "base":{"variables":6,"clauses":8,"q":2,"full_models":24,
            "allowed_boundary":["".join(map(str,x)) for x in sorted(T)]},
    "six_variable_complete_catalog":{"positive_factors":75,"negative_factors":75,
       "formulas":5625,"fully_paired_out_target":75,"in_target":5550,
       "q":dict(sorted(byq.items())),"models":dict(sorted(bymodels.items())),
       "three_boundary_size_in_target":dict(sorted(byboundary.items())),
       "pair_projection_failures":missing_pair},
    "tensor_exhaustive_r":[1,2,3],"outside_target_unsat_unit_control":True,
    "in_target_UNSAT_source":"Döcker 198x264; imported certificate, not re-solved here"
},indent=2,sort_keys=True))
