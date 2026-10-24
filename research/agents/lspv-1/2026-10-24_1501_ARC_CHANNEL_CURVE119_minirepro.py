#!/usr/bin/env python3
"""ARC-CHANNEL-CURVE119 compact exact-rational regression.
The full 237-assertion finite audit also contains adaptive SAT/UNSAT controls.
No experiment proves all-input contraction or P != NP.
"""
from fractions import Fraction as F
import itertools, json

def beta2(c):
    return ((c+2)/(c*c)-c)/2

def beta_k(c,k):
    f=F(1)
    for _ in range(k):
        f=c*f/(1+f)
    return min((1/f-c)/k, c**(-k))

def profile(r,eta,theta,sigma):
    assert 0<=theta<1
    C=max(r,eta/(1-theta))
    rho=max(sigma,theta)
    return C,rho

assert beta2(F(6,5))==F(23,45)
assert beta2(F(241,200))==F(11642479,23232400)
assert beta_k(F(151,100),4)==F(13827784249,207954240400)
assert all(beta_k(c,2)==beta2(c) for c in [F(241,200),F(13,10),F(151,100)])

cases=[
  ("ARC-0",F(11,10),F(3,5),F(1,2),F(1,2)),
  ("ARC-space-bypass",F(11,10),F(3,5),F(1,2),F(11,20)),
  ("CURVE-13",F(13,10),F(39,40),F(1,4),F(3,10)),
  ("CURVE-space-bypass",F(13,10),F(39,40),F(1,4),F(7,20)),
  ("CURVE-105",F(21,20),F(1,5),F(2,5),F(2,5)),
  ("INDEXED-4",F(59,40),F(57,40),F(1,20),F(1,20)),
]
out=[]
for name,*args in cases:
    C,rho=profile(*args)
    two=rho<beta2(C)
    indexed=any(rho<beta_k(C+F(j,100),ell)
                for j in range(1,11) for ell in range(1,9))
    out.append(dict(name=name,C=str(C),rho=str(rho),
                    excluded_by_2=two,excluded_by_sampled_indexed=indexed))
assert out[0]["excluded_by_2"] and not out[1]["excluded_by_2"]
assert out[2]["excluded_by_2"] and not out[3]["excluded_by_2"]
assert not out[-1]["excluded_by_2"] and out[-1]["excluded_by_sampled_indexed"]
# Opposite-label SAT controls, independent exhaustive CNF truth evaluation.
def sat(clauses,n):
    for values in itertools.product((0,1),repeat=n):
        if all(any(values[abs(lit)-1] == (lit>0) for lit in clause)
               for clause in clauses):
            return True
    return False
def xor3(p):
    return [tuple(-sign*(j+1) for j,sign in enumerate(
            tuple(1 if x else -1 for x in values)))
            for values in itertools.product((0,1),repeat=3)
            if sum(values)%2 != p]
assert sat([(1,2),(-1,2)],2)
assert not sat([(1,),(-1,)],1)
assert sat(xor3(0),3)
assert not sat(xor3(0)+xor3(1),3)
full=[tuple((j+1)*sg for j,sg in enumerate(v))
      for v in itertools.product((-1,1),repeat=3)]
assert not sat(full,3)
print(json.dumps(dict(profiles=out,sat_unsat_controls=5,
      status="COMPUTATIONAL only; ARC-EDGE-90 OPEN"),indent=2))
