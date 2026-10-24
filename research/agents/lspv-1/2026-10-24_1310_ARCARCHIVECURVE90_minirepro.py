#!/usr/bin/env python3
"""Exact-rational regression audit for conditional ARC/FLMV arithmetic.

PROVED/EXACT results are proved in the companion LaTeX report.
The code verifies arithmetic only; it does not implement SAT contraction.
Python standard library only.
"""
import json
from fractions import Fraction as F

STAR=F(241,200)
def beta(c):
    c=F(c)
    return ((c+2)/(c*c)-c)/2
def f(t): return max(F(11,10),F(3,5)+t/2)
def g(s): return max(F(1,2),s/2)
def box(t,s): return t<STAR and s<=F(1,2)
def cert(t,s,c): return c>max(F(1),t) and s<beta(c)

assert beta(STAR)==F(11642479,23232400)
assert beta(STAR)-F(1,2)==F(26279,23232400)
assert beta(F(6,5))==F(23,45)
examples=[(F(121,100),F(9,20),F(61,50)),
          (F(13,10),F(3,10),F(131,100)),
          (F(6,5),F(1,2),STAR)]
assert all(cert(*x) for x in examples)
assert not box(*examples[0][:2]) and not box(*examples[1][:2])
assert all(beta(F(c,1000))>beta(F(c+1,1000))
           for c in range(1001,1520))

def first_hit(K):
    t=s=F(K)
    for j in range(300):
        if box(t,s): return j,str(t),str(s)
        t,s=f(t),g(s)
    raise AssertionError("no hit in 300 stages")

hits={str(k):first_hit(k) for k in (2,3,5,10,100,1000,10000)}
assert [v[0] for v in hits.values()]==[8,9,10,11,15,18,21]
checks=0
for k in range(1,1001):
    t=s=F(k)
    for j in range(10):
        assert t <= F(6,5)+max(F(0),F(k)-F(6,5))/2**j
        assert s <= max(F(1,2),F(k)/2**j)
        checks+=1
        t,s=f(t),g(s)
result={"run":"ARCARCHIVECURVE90","status":"COMPUTATIONAL on exact rational arithmetic",
        "scope":"conditional map only, no all-input SAT successor proved",
        "beta_reference":str(beta(STAR)),"margin_above_half":str(beta(STAR)-F(1,2)),
        "curve_examples":[{"t":str(t),"s":str(s),"c":str(c),
                           "beta_c":str(beta(c))}
                          for t,s,c in examples],
        "finite_hits":{k:{"steps":v[0],"t":v[1],"s":v[2]}
                       for k,v in hits.items()},
        "envelope_checks":checks}
print(json.dumps(result,indent=2))
