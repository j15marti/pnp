#!/usr/bin/env python3
"""LSPV-4 STREAM-CUT285 compact self-contained grammar/equality check (no U198 fixture).
Full producer, 75,713-assertion independent verifier, and source fixtures are in the ZIP.
Python 3.9+, standard library. The source code is a finite test, not a SAT lower bound."""
import itertools, collections
from fractions import Fraction
def build(t,p,q):
    bas,aa,bb,neg=[],[],[],[]
    for i in range(t):
        a,b,c,d,e,f=range(6*i+1,6*i+7)
        bas.extend([(a,b,d),(c,e,f)])
        A=(a,b,c); B=(d,e,f)
        aa.append(A if ((p>>i)&1)==0 else B)
        bb.append(B if ((q>>i)&1)==0 else A)
        neg.extend([(-a,-b,-c),(-a,-d,-e),(-b,-d,-f),(-c,-e,-f)])
    return bas+aa+bb+neg
def valid(F,n):
    if not F or 3*len(F)!=4*n: return False
    if len(set(tuple(sorted(c)) for c in F))!=len(F): return False
    d=collections.Counter()
    for c in F:
        if len(c)!=3 or len(set(abs(z) for z in c))!=3: return False
        if any(abs(z)>n or z==0 for z in c): return False
        if not (all(z>0 for z in c) or all(z<0 for z in c)): return False
        d.update(c)
    return all(d[i]==d[-i]==2 for i in range(1,n+1))
def flmv(c):
    f=Fraction(1); vv=[]
    for k in range(1,4):
        f=c*f/(1+f);vv.append(min((1/f-c)/k,c**(-k)))
    assert vv[1]>vv[0] and vv[1]>vv[2] and vv[1]>c**(-4)
    return vv[1]
count=0;valid_count=0
for t in range(1,7):
    for p in range(1<<t):
        for q in range(1<<t):
            assert valid(build(t,p,q),6*t)==(p==q)
            count+=1;valid_count+=(p==q)
G=build(1,0,0)
models=sum(all(any((bool(bits[abs(z)-1]) == (z>0)) for z in C) for C in G)
           for bits in itertools.product((0,1),repeat=6))
assert models==22
assert flmv(Fraction(6,5))==Fraction(23,45)
assert flmv(Fraction(241,200))==Fraction(11642479,23232400)
for t in (6,8):
    for p in (0,(1<<t)-1):
        d_phys=2*p.bit_count()
        assert (d_phys==0 if p==0 else d_phys==2*t)
print({'PASS':True,'pairs':count,'valid':valid_count,'malformed':count-valid_count,
       'small_gadget_models':models,'FLMV':['23/45','11642479/23232400'],
       'status':'COMPUTATIONAL; ARBITRARY-A->PHI(A) AND P vs NP OPEN'})
