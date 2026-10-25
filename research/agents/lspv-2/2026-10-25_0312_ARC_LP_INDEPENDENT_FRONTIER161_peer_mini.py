#!/usr/bin/env python3
"""ARC-LP-INDEPENDENT-FRONTIER161: finite exact rational checks only."""
from itertools import product
from fractions import Fraction
from collections import defaultdict
def graph(F):
    g=defaultdict(set)
    for C in F:
        S={abs(z) for z in C}
        for v in S:g[v].update(S-{v})
    return dict(g)
def independent(g):
    I=[];blocked=set()
    for v in sorted(g):
        if v not in blocked:
            I.append(v);blocked.add(v);blocked.update(g[v])
    return I
def lp_witness(F,alpha):
    h=Fraction(1,2)
    for C in F:
        score=sum(((Fraction(alpha[abs(z)]) if abs(z) in alpha else h) if z>0
                  else 1-(Fraction(alpha[abs(z)]) if abs(z) in alpha else h))
                  for z in C)
        assert score>=1,(C,alpha,score)
def restrict(F,alpha):
    return tuple(tuple(z for z in C if abs(z) not in alpha) for C in F
                 if not any((z>0)==bool(alpha[abs(z)])
                            for z in C if abs(z) in alpha))
def sat(F,n):
    return any(all(any((z>0)==bool(bits[abs(z)-1]) for z in C) for C in F)
               for bits in product((0,1),repeat=n))
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Y2=Y+tuple(tuple((abs(z)+6)*(1 if z>0 else -1) for z in C) for C in Y)
F8=tuple(tuple((i+1) if a[i]==0 else -(i+1) for i in range(3))
         for a in product((0,1),repeat=3))
bridge=((3,4,5),(5,6,7),(7,8,9))
cases=[('Y6-Cstar-SAT',Y,6,True),('two-block-SAT',Y2,12,True),
       ('connected-SAT',F8[:-1]+bridge,9,True),
       ('connected-UNSAT',F8+bridge,9,False)]
calls=0
for name,F,n,label in cases:
    G=graph(F);I=independent(G)
    assert all(y not in G[x] for x in I for y in I if x!=y)
    for bits in product((0,1),repeat=len(I)):
        lp_witness(F,dict(zip(I,bits)))
    if len(I)>=2:
        x,y=I[:2];leaves=[]
        for a,b in product((0,1),repeat=2):
            C1=restrict(F,{x:a})
            C2=restrict(C1,{y:b})
            lp_witness(F,{x:a,y:b})
            leaves.append(sat(C2,n));calls+=1
        assert any(leaves)==label,(name,leaves)
    else:
        assert sat(F,n)==label
print({'status':'PASS','sources':len(cases),
       'real_two_level_exact_leaves':calls,
       'LP_feasible_all_independent_pins':True})
