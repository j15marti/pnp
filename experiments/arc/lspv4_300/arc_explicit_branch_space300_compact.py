#!/usr/bin/env python3
"""LSPV-4 300 compact exact finite controls. Restricted output-transducer lemma.
This is NOT native FLMV timing, arbitrary SAT hardness, or a P-vs-NP proof.
Full independent verifier, archived source certificates and raw are in run archive.
"""
from fractions import Fraction
from itertools import product
from collections import Counter
from math import comb, ceil, log2
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
pins={8:0,3:0,7:0,6:0,1:1,5:1}
def good(F,n):
    occ=Counter((abs(x),x>0) for c in F for x in c)
    return len(F)==4*n//3 and len(set(tuple(sorted(c)) for c in F))==len(F) and all(
        len(c)==3 and len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F
    ) and all(occ[v,True]==occ[v,False]==2 for v in range(1,n+1))
def sat(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def count(F,n,p):
    free=[v for v in range(1,n+1) if v not in p]
    return sum(sat(F,{**p,**dict(zip(free,b))}) for b in product((0,1),repeat=len(free)))
assert good(F9,9) and good(Y6,6)
assert count(Y6,6,{})==20 and count(F9,9,{})==70 and count(F9,9,pins)==0
assert not good(F9[:-1],9) and not good(F9+F9[:1],9)
# Outside-cycle signed preferred bits plus parity leave just 111, yet every
# selected cycle-edge assignment violates a source-original cycle clause.
cycle=(3,4,10); free=(2,4,9)
outside=[]
for bits in product((0,1),repeat=3):
    a={**pins,**dict(zip(free,bits))}
    t=[sum(a[abs(x)]==int(x>0) for x in c) for c in F9]
    if bits==(1,1,1) and t[1]==t[5]==1:outside.append(bits)
assert outside==[(1,1,1)]
for pick in cycle:
    assert not any(all(
        sum({**pins,**dict(zip(free,bits))}[abs(x)]==int(x>0) for x in F9[j])
           ==(2 if j==pick else 1) for j in cycle)
        and bits==(1,1,1) for bits in product((0,1),repeat=3))
def shape(t):
    n=9*t;m=12*t;B=ceil(log2(n+1));H=ceil(log2(m+1))
    N=2*H+36*t*(B+1);w=N.bit_length()
    return dict(t=t,n=n,m=m,N=N,B=B,H=H,choices=3**t,
        full_scan_primitive=3*w*N,
        naive_triple_primitive=3*w*9*(B+1)*comb(m,3),
        index_content_xor=2*sum(v.bit_count() for v in range(N)),
        dense_GF2_bits=9*t*(3*t+1))
for t in (1,2,4,8,16,32,64,128):
    z=shape(t)
    C=[tuple((abs(x)+9*j)*(1 if x>0 else -1) for x in c)
        for j in range(t) for c in F9]
    assert good(C,9*t)
    assert z['N']==2*z['H']+36*t*(z['B']+1)
    print(z)
for c,expect in ((Fraction(6,5),Fraction(23,45)),(Fraction(241,200),Fraction(11642479,23232400))):
    f=Fraction(1);d=[]
    for k in range(1,5):
        f=c*f/(1+f);d.append(min((1/f-c)/k,c**(-k)))
    assert d[1]==expect and d[1]>d[0] and d[1]>d[2] and d[1]>c**(-4)
print('P versus NP OPEN: no universal ARC transformer, no numeric FLMV transfer')
