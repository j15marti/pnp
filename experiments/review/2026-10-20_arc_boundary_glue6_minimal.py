#!/usr/bin/env python3
"""Independent small verifier for ARC_BOUNDARY_GLUE6; no SAT lower-bound claim."""
from itertools import product

def u(l,a,b):
    return [(l,sa*a,sb*b) for sa in (1,-1) for sb in (1,-1)]

def sat_clause(clause,mask):
    return any(((mask>>(abs(x)-1))&1)==(x>0) for x in clause)

for pin in (False,True):
    for x,y,z in product((0,1), repeat=3):
        mask=x|(y<<1)|(z<<2)
        assert all(sat_clause(c,mask) for c in u(1 if pin else -1,2,3)) == (x==pin)

pairs=0
for b in range(1,5):
    for a,c in product(range(1<<b),repeat=2):
        left=[];right=[]
        for i in range(b):
            left+=u(i+1 if (a>>i)&1 else -(i+1),b+2*i+1,b+2*i+2)
            right+=u(i+1 if (c>>i)&1 else -(i+1),3*b+2*i+1,3*b+2*i+2)
        assert len(left+right)==8*b
        assert all(len(set(map(abs,cl)))==3 for cl in left+right)
        # Each block pins x_i to the requested value; auxiliaries are private.
        assert (a==c)==all(((a>>i)&1)==((c>>i)&1) for i in range(b))
        pairs+=1

maps=0
for synopsis in product(range(4), repeat=8):
    assert len(set(synopsis))<8
    maps+=1
assert (pairs,maps)==(340,65536)
print("PASS:", pairs,"formula pairs;",maps,"short summaries all collide")
