#!/usr/bin/env python3
"""GATE315 compact connected canonical source and pin-closed counts.
The full generic GF(2)/matroid compiler and no-import verifier are in the
GATE315 research archive. Restricted result, P versus NP OPEN."""
from itertools import product
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def original(t):
    C=[];p={}
    for k in range(t):
        C.extend(tuple((1 if v>0 else -1)*(abs(v)+6*k) for v in row) for row in Y)
        p.update({6*k+2:0,6*k+3:1,6*k+5:0})
    for k in range(t-1):
        i,j=8*k+6,8*(k+1)+6
        a,b=list(C[i]),list(C[j])
        a[0],b[2]=b[2],a[0]
        C[i],C[j]=tuple(a),tuple(b)
    return C,p
def count(C,p):
    n=max(abs(v) for row in C for v in row)
    free=[x for x in range(1,n+1) if x not in p]
    out=0
    for w in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,w))}
        out+=all(any(a[abs(lit)]==int(lit>0) for lit in row) for row in C)
    return out
for t in (1,2,3,4,8,16):
    F,p=original(t)
    assert len(F)==8*t and len({tuple(sorted(row)) for row in F})==8*t
    assert all(sum(v in row for row in F)==sum(-v in row for row in F)==2
               for v in range(1,6*t+1))
    for row in F:
        if len({(abs(v)-1)//6 for v in row})>1:
            assert any(abs(v) in p and p[abs(v)]==int(v>0) for v in row)
    if t<=3:
        assert count(F,p)==3**t
        assert count(F,{**p,1:0})==2*3**(t-1)
        assert count(F,{**p,1:1})==3**(t-1)
        assert count(F,{**p,1:1,6:1})==0
    print("t",t,"n",6*t,"nominal_tickets",3**t,
          "component_rows",4*t,"exact_models",3**t)
print("GATE315 restricted only, P versus NP OPEN.")