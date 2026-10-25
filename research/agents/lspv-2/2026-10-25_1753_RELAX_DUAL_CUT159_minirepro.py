#!/usr/bin/env python3
"""RELAX-DUAL-CUT159: independent stdlib rational verifier.
Full SciPy-proposed/EXACTLY VERIFIED dual-ray pilot is in the attached ZIP.
"""
from itertools import product
from fractions import Fraction

def sat(F,a):
    return all(any(a[abs(v)-1]==(1 if v>0 else 0) for v in c) for c in F)

def clause_rows(F,n):
    out=[]
    for c in F:
        a=[0]*n;neg=0
        for v in c:
            if v>0:a[v-1]-=1
            else:a[-v-1]+=1;neg+=1
        out.append((a,neg-1))
    return out

def dual_ok(rows,w,n):
    assert all(z>=0 for z in w)
    co=[Fraction(0)]*n;rhs=Fraction(0)
    for (a,b),z in zip(rows,w):
        rhs+=z*b
        for j in range(n):co[j]+=z*a[j]
    return all(x==0 for x in co) and rhs<0

F=[tuple(i+1 if a[i]==0 else -(i+1) for i in range(3))
   for a in product((0,1),repeat=3)]
assert not any(sat(F,a) for a in product((0,1),repeat=3))
assert sum(sat(F[:-1],a) for a in product((0,1),repeat=3))==1
for x,y in product((0,1),repeat=2):
    idx=[i for i,c in enumerate(F) if int(c[0]>0)!=x and int(c[1]>0)!=y]
    assert len(idx)==2
    pinx=([1 if x==0 else -1,0,0],0 if x==0 else -1)
    piny=([0,1 if y==0 else -1,0],0 if y==0 else -1)
    assert dual_ok([clause_rows(F,3)[i] for i in idx]+[pinx,piny],
                   [Fraction(1),Fraction(1),Fraction(2),Fraction(2)],3)

Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
assert sum(sat(Y,a) for a in product((0,1),repeat=6))==20
assert sat(Y,(1,1,1,0,0,0))
for Q,n in [(F,3),(Y,6)]:
    for a,b in clause_rows(Q,n):
        assert b-sum(Fraction(t,2) for t in a)==Fraction(1,2)
print({"status":"PASS","certificates":4,"Y_models":20,
       "F8_UNSAT":True,"fractional_half_point":True})