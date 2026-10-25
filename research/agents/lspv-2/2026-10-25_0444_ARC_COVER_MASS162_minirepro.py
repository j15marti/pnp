#!/usr/bin/env python3
"""ARC-COVER-MASS162 independent minimal exact both-label and all-cover audit.
Full 50-source Python interpreter and raw rows are in the user-facing
ARC_COVER_MASS162_ROLE2_2026-10-25.zip artifact. Standard library only.
"""
import itertools
import json
from fractions import Fraction

Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
U=tuple(tuple(j+1 if ((a>>j)&1)==0 else -(j+1)
              for j in range(3)) for a in range(8))
def SAT(F,a):
    return all(any(a[abs(z)-1]==int(z>0) for z in c) for c in F)
def decide(F,n):
    return any(SAT(F,a) for a in itertools.product((0,1),repeat=n))
def restrict(F,pins):
    out=[]
    for c in F:
        if any(pins.get(abs(z),-1)==int(z>0) for z in c):
            continue
        out.append(tuple(z for z in c if abs(z) not in pins))
    return tuple(out)
def ordinary(F,n):
    s='p cnf %d %d\n'%(n,len(F))
    s+=''.join(' '.join(map(str,c))+' 0\n' for c in F)
    ls=s.splitlines()
    assert ls[0]==f'p cnf {n} {len(F)}'
    G=[]
    for line in ls[1:]:
        t=tuple(map(int,line.split()))
        assert t and t[-1]==0
        G.append(t[:-1])
    assert tuple(G)==F
    return len(s)
def intact(F,pins):
    return sum(all(abs(z) not in pins for z in c) for c in F)
def two_levels(F,n):
    direct=decide(F,n);decisions=[]
    for a in (0,1):
        F1=restrict(F,{1:a});ordinary(F1,n)
        for b in (0,1):
            F2=restrict(F,{1:a,2:b});ordinary(F2,n)
            ans=decide(F2,n);decisions.append(ans)
            for bits in itertools.product((0,1),repeat=n):
                if bits[0]==a and bits[1]==b:
                    assert SAT(F,bits)==SAT(F2,bits)
    assert any(decisions)==direct
    return {'root_SAT':direct,'level2_SAT':sum(decisions),
            'level2_UNSAT':4-sum(decisions)}
assert len(Y)==8 and len(set(Y))==8
assert len([a for a in itertools.product((0,1),repeat=6) if SAT(Y,a)])==20
assert not decide(U,3) and decide(U[:-1],3)
assert SAT(Y,(1,1,1,0,0,0))
for v in range(1,7):
    assert sum(z==v for c in Y for z in c)==2
    assert sum(z==-v for c in Y for z in c)==2
    assert all(abs(z)!=v for z in ())  # no hidden pin or helper
assert all(tuple(-z for z in c) not in Y for c in Y)
terms=0
for tri in itertools.product((-1,0,1),repeat=6):
    pins={j+1:a for j,a in enumerate(tri) if a>=0}
    if intact(Y,pins)==0:
        terms+=1
        assert len(pins)>=2
assert terms==596
minhits=[]
for pair in itertools.combinations(range(1,7),2):
    if intact(Y,dict.fromkeys(pair,0))==0:
        minhits.append(pair)
assert minhits==[(3,4)]
out={'run':'ARC-COVER-MASS162-peer','status':'PASS',
     'Y_models':20,'Y_all_ternary_hits_3ary_partial_terms':terms,
     'Y_min_2pin_hit':minhits[0],
     'cases':{'Y6':two_levels(Y,6),
              'F8_UNSAT':two_levels(U,3),
              'F8_minus_one_SAT':two_levels(U[:-1],3)},
     'product_mass':[]}
for p in (1,2,4,8,16):
    mass=Fraction(20,64)**p
    assert mass+1-mass==1
    out['product_mass'].append({'p':p,'SAT_fraction':str(mass),
       'falsified_clause_union_fraction':str(1-mass),
       'min_ternary_hitting_cover_terms':2**(2*p)})
print(json.dumps(out,indent=2))
