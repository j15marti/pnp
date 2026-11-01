#!/usr/bin/env python3
"""ARC-SETUP-QUERY-SPLIT296: stand-alone exact-rational ledger, no SAT oracle."""
from fractions import Fraction as F
import json

A,G,LAM,SIG=F(11,10),F(3,5),F(1,2),F(1,2)
C=F(241,200)
def theorem57(c):
    f=F(1)
    vals=[]
    for k in range(1,13):
        f=c*f/(1+f)
        vals.append(min((1/f-c)/k,c**(-k)))
    assert vals[1]>max(v for i,v in enumerate(vals) if i!=1)
    assert c**(-4)<vals[1]
    return vals[1]
assert theorem57(F(6,5))==F(23,45)
assert theorem57(C)==F(11642479,23232400)
assert theorem57(C)>SIG
def fixed(delta,rho):
    return max(A,G+delta,(G+rho)/(1-LAM))
scenarios=[(F(0),F(0)),(F(1,2),F(0)),(F(3,5),F(0)),
           (F(121,200),F(0)),(F(1),F(0)),
           (F(0),F(1,1000)),(F(0),F(1,400)),(F(0),F(3,1000))]
for delta,rho in scenarios:
    print(f"setup={delta} per_guest_step={rho} fixed_time={fixed(delta,rho)} strict={fixed(delta,rho)<C}")
assert C-G==F(121,200)                 # additive per child boundary
assert C*(1-LAM)-G==F(1,400)           # per guest step multiplier boundary
assert fixed(F(3,5),F(0))==F(6,5)
assert fixed(F(1),F(0))==F(8,5)
for K0,L0 in [(2,1),(4,3),(10,8),(100,50)]:
    K,L=F(K0),F(L0)
    for j in range(25):
        if K<C and L<theorem57(C):
            print(f"initial={K0},{L0} first_strict_iteration={j}")
            break
        K=max(A,G+LAM*K)
        L=max(SIG,LAM*L)
    else:
        raise AssertionError("failed finite conditional recurrence")
print(json.dumps({"status":"CONDITIONAL ARITHMETIC ONLY","p_vs_np":"OPEN"},sort_keys=True))
