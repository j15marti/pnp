#!/usr/bin/env python3
"""Independent, no producer import: source original-clause SAT/UNSAT spot checks."""
from itertools import product
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def models(C,p):
    n=max(abs(x) for row in C for x in row)
    free=[x for x in range(1,n+1) if x not in p]
    ans=0
    for z in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,z))}
        ans+=all(any(a[abs(x)]==int(x>0) for x in row) for row in C)
    return ans
assert models(Y,{})==20
assert models(F9,{})==70
assert models(F9,{8:0,3:0,7:0,6:0,1:1,5:1})==0
assert models(F9,{1:0,3:0,5:1,6:0,7:0,8:0})==2
assert models(Y,{2:0,3:1,5:0})==3
assert models(Y,{2:0,3:1,5:0,1:0})==2
assert models(Y,{2:0,3:1,5:0,1:1,6:1})==0
assert models(Y,{3:0,4:1})==4
for C in (Y,F9):
    n=max(abs(x) for row in C for x in row)
    for bits in range(1<<n):
        a={i:(bits>>(i-1))&1 for i in range(1,n+1)}
        b={i:1-a[i] for i in a}
        assert all(sum(a[abs(x)]==int(x>0) for x in row)+
                   sum(b[abs(x)]==int(x>0) for x in row)==3 for row in C)
print("GATE315 no-import spot verifier PASS. P versus NP OPEN.")