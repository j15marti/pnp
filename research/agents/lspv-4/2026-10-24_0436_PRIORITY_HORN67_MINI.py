#!/usr/bin/env python3
"""Independent minimal check for PRIORITY-HORN-PARSIMONY67. Python stdlib."""
from itertools import product
from itertools import combinations
def ok_clause(C,assignment):
    return any((assignment[abs(x)-1] if x > 0 else not assignment[abs(x)-1]) for x in C)
def count(C,n):
    return sum(all(ok_clause(c,a) for c in C) for a in product((False,True),repeat=n))
def lift(C,n):
    out=[]
    for j,(a,b,c) in enumerate(C):
        s,t,u=[n+3*j+i for i in (1,2,3)]
        out.extend(((s,t,u),(-s,a),(-t,b),(-u,c),(-t,-a),(-u,-a),(-u,-b)))
    return out,n+3*len(C)
def local_count(truth,guards):
    return sum(bool(any(s)) and all(not s[i] or truth[i] for i in range(3))
       and all(not s[i] or not truth[j] for i,j in guards)
       for s in product((False,True),repeat=3))
universe=[(i,j) for i in range(3) for j in range(3) if i!=j]
good=[]
for bits in product((0,1),repeat=6):
    guards=[universe[i] for i in range(6) if bits[i]]
    if all(local_count(t,guards)==int(any(t)) for t in product((False,True),repeat=3)):
        good.append(guards)
assert len(good)==6
assert all(len(g)==3 for g in good)
assert [(1,0),(2,0),(2,1)] in good
for C in [[(1,2,3)],[(1,-2,3)],[(-1,-2,-3)],[(1,2,3),(-1,-2,-3)],[(1,-2,3),(-2,1,-3)]]:
    G,n=lift(C,3)
    assert count(G,n)==count(C,3)
    assert all(sum(z>0 for z in clause)<=1 for clause in G if len(clause)==2)
def baseline(q,bits):
    u,v=q+2,q+3
    C=[(1,u),(1,-u),(-(q+1),v),(-(q+1),-v)]
    C.extend((-i,i+1 if bits[i-1] else -(i+1)) for i in range(1,q+1))
    return C
def anchor(C,q):
    t,a,b=q+4,q+5,q+6
    Z=[tuple((-var if bit else var) for var,bit in zip((t,a,b),s))
        for s in product((False,True),repeat=3) if any(s)]
    return Z+[(x,y,t) for x,y in C]
for q in range(1,8):
    for bits in product((0,1),repeat=q):
        C=baseline(q,bits)
        assert (count(C,q+3)==0)==all(bits)
        G=anchor(C,q)
        assert count(G,q+6)==count(C,q+3)
print("PRIORITY-HORN-PARSIMONY67 VERIFIED: six schemes, unique local lift, 254 baseline cases")
