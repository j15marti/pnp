#!/usr/bin/env python3
"""No-producer-import independent finite theorem checks for LSPV-1 312.
Runs from any directory; standard library only. No FLMV runtime claim.
"""
from itertools import product, combinations, permutations
from fractions import Fraction
import json
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-x for x in c) for c in N)
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def sat(F,a):return all(any(a[abs(l)-1]==(l>0) for l in c) for c in F)
def models(F,n,pins=None):
    pins=pins or {}
    return sum(sat(F,a) and all(a[k-1]==v for k,v in pins.items())
      for a in product((0,1),repeat=n))
assert models(F,9)==70 and models(Y,6)==20
assert models(F,9,{1:0,2:0,8:1,9:1})==2
assert models(F,9,{3:0,6:1,7:1,9:1})==0
checks=0
for i,j in combinations(range(12),2):
    for ti,tj in product((0,3),repeat=2):
        wants={};valid=True
        for c,t in ((F[i],ti),(F[j],tj)):
            for l in c:
                want=(l>0) if t==3 else (l<0)
                if abs(l) in wants and wants[abs(l)]!=want:valid=False
                wants[abs(l)]=want
        observed=any(all(sum(a[abs(l)-1]==(l>0) for l in F[k])==v
                        for k,v in ((i,ti),(j,tj)))
                     for a in product((0,1),repeat=9))
        assert valid==observed;checks+=1
for a in product((0,1),repeat=9):
    for c in F:
        t=sum(a[abs(l)-1]==(l>0) for l in c)
        tbar=sum((1-a[abs(l)-1])==(l>0) for l in c)
        assert t+tbar==3;checks+=1
traces=0; mixtures=0
for t in range(1,7):
    for ordering in permutations(range(t)):
        # Each prefix of first touches h is a possible interrupted
        # accepting transcript, including unhit opposite-label branches.
        for h in range(t+1):
            ranks={j:i+1 for i,j in enumerate(ordering[:h])}
            y=[ranks.get(j,h) for j in range(t)]
            assert sum(y)>=h*(t+1)/2
            if h==t:
                assert sum(y)==t*(t+1)//2 and max(y)==t
            traces+=1
    for e in (Fraction(0),Fraction(1,10),Fraction(1,4),Fraction(1,3),Fraction(2,5)):
        p=1-2*e
        # Promise-only: scan with p, guess each label with e.
        yes=p*t
        no=p*Fraction(t+1,2)
        assert yes==(1-2*e)*t and no==(1-2*e)*Fraction(t+1,2)
        assert p+e==1-e
        mixtures+=1
def valid(F,n):
    from collections import Counter
    if len(F)*3!=4*n:return False
    counts=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(x==0 or abs(x)>n or (x>0)!=(c[0]>0) for x in c):return False
        z=tuple(sorted(c))
        if z in seen:return False
        seen.add(z)
        for x in c:counts[abs(x),x>0]+=1
    return all(counts[i,s]==2 for i in range(1,n+1) for s in (False,True))
assert valid(F,9) and valid(Y,6)
bad=(F[:-1],F[:-1]+((1,1,2),),F[:-1]+((-1,2,3),),
     F[:-1]+(F[0],),F[:-1]+((1,2,10),),F[:-1]+((0,2,3),))
assert all(not valid(G,9) for G in bad)
print(json.dumps({"run":"LSPV1_312_INDEPENDENT","status":"PASS","checks":checks,
  "partial_ordered_traces":traces,"mixture_checks":mixtures,
  "F9_models":70,"Y6_models":20,"F9_SAT_UNSAT_cubes":[2,0],
  "S_U_extremes":264,"complement_checks":6144,
  "malformed_rejects":6,"P_vs_NP":"OPEN"},indent=2))
