#!/usr/bin/env python3
"""SINGLE-PARITY-SCC76 compact independent exact-model audit, standard library."""
from itertools import product

def xor2(a,b,t):
    return [(-a,b),(a,-b)] if t==0 else [(a,b),(-a,-b)]

def xor3(a,b,c,t):
    return [tuple(v if z==0 else -v for v,z in zip((a,b,c),bits))
            for bits in product((0,1),repeat=3)
            if (bits[0]^bits[1]^bits[2]) != t]

def build(q,c,b):
    assert q>=4 and q%2==0 and len(c)==q//2
    B=[]; T=[]
    for j,bit in enumerate(c):
        B.extend(xor2(2*j+1,2*j+2,bit))
    for j in range(1,q-1):
        T.extend(xor3(1,2,q+1,0) if j==1 else xor3(q+j-1,j+1,q+j,0))
    B.extend(xor2(2*q-2,q,b))
    return 2*q-2,B,T

def satisfies(C,a):
    return all(any(a[abs(l)-1] == int(l>0) for l in cl) for cl in C)

def test():
    count=0; samples=[]
    for q in (4,6,8):
        for c in product((0,1),repeat=q//2):
            for b in (0,1):
                n,B,T=build(q,c,b)
                assert len(B)==q+2 and len(T)==4*q-8 and n==2*q-2
                models=sum(satisfies(B+T,a) for a in product((0,1),repeat=n))
                predicted=(1<<(q//2)) if ((sum(c)&1)==b) else 0
                assert models==predicted,(q,c,b,models,predicted)
                count+=4
                if len(samples)<5: samples.append((q,c,b,models))
    return {'checks':count,'failures':0,'samples':samples}

if __name__=='__main__':
    print(test())
