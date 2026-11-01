#!/usr/bin/env python3
"""Public compact source-independent reproduction of restricted ARC-CUBIC300."""
from itertools import product,combinations
from collections import Counter
from fractions import Fraction
from math import comb,ceil,log2
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=P+[tuple(-x for x in c) for c in N]
PS={1:0,2:0,8:1,9:1}
PU={3:0,6:1,7:1,9:1}
def sat(F,a):
    return all(any(a[abs(x)]==(x>0) for x in c) for c in F)
def valid(F):
    h=Counter((abs(x),x>0) for c in F for x in c)
    return len(F)==12 and len({tuple(sorted(c)) for c in F})==12 and all(len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F) and all(h[i,True]==h[i,False]==2 for i in range(1,10))
def extensions(p):
    free=[x for x in range(1,10) if x not in p]
    return sum(sat(F,{**p,**dict(zip(free,bits))}) for bits in product((0,1),repeat=len(free)))
def gate(p):
    free=[x for x in range(1,10) if x not in p]
    active=[];covered=[]
    for j,c in enumerate(F):
        (covered if any(abs(x) in p and p[abs(x)]==(x>0) for x in c) else active).append(j)
    spill=Counter((abs(x),x>0) for j in covered for x in F[j] if abs(x) not in p)
    eta=sum(min(spill[x,True],spill[x,False]) for x in free)
    edges=[(j,*[abs(x) for x in F[j] if abs(x) not in p]) for j in active if len([x for x in F[j] if abs(x) not in p])==2]
    tris=0
    for T in combinations(edges,3):
        degrees=Counter(v for e in T for v in e[1:])
        tris+=len(degrees)==3 and set(degrees.values())=={2}
    assert tris==0
    return len(free),len(active),eta,len(edges),comb(len(edges),3)
assert valid(F)
assert sum(sat(F,dict(zip(range(1,10),a))) for a in product((0,1),repeat=9))==70
for p,expected,E in [(PS,2,6),(PU,0,4)]:
    assert extensions(p)==expected
    f,u,eta,e,q=gate(p)
    assert (f,u,eta,e,q)==(5,6,4,E,comb(E,3))
    print("cube",p,"models",expected,"f,u,eta,nu,delta",f,u,eta,0,2*f-u-eta,"triple_scans",q)
for t in (1,2,4,8,16,32,64):
    B=ceil(log2(9*t+1)); H=ceil(log2(12*t+1))
    src=2*H+36*t*(B+1)
    print("copies",t,"source_bits",src,"sat_candidates",comb(6*t,3),"unsat_candidates",comb(4*t,3),"sat_materialized_edge_bits",6*t*(2*B+H))
def env(c):
    f=Fraction(1);ds=[]
    for k in (1,2,3):
        f=c*f/(1+f)
        ds.append(min((1/f-c)/k,c**(-k)))
    assert ds[1]>ds[0] and ds[1]>ds[2] and c**(-4)<ds[1]
    return ds[1]
assert env(Fraction(6,5))==Fraction(23,45)
assert env(Fraction(241,200))==Fraction(11642479,23232400)
print("FLMV exact",env(Fraction(6,5)),env(Fraction(241,200)),"P vs NP OPEN")
