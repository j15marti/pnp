#!/usr/bin/env python3
"""Independent direct-clause no-producer-import GATE317 verifier; P vs NP OPEN."""
from itertools import product

def original(t):
    out=[]
    for j in range(2*t):
        a=6*j;b=6*((j+2*t-1)%(2*t))
        positives=[(b+1,a+2,a+3),(a+1,a+4,a+5),(a+2,a+4,a+6),(a+3,a+5,a+6)]
        out+=positives+[tuple(-z for z in c) for c in positives]
    return out

def models(F,p):
    n=max(abs(z) for c in F for z in c)
    free=[x for x in range(1,n+1) if x not in p]
    ans=0
    for bits in product((False,True),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        ans+=all(any(a[abs(z)]==(z>0) for z in c) for c in F)
    return ans

def valid(F):
    n=max(abs(z) for c in F for z in c)
    return len(F)*3==4*n and len(set(tuple(sorted(c)) for c in F))==len(F) and all(
        len(c)==3 and len(set(map(abs,c)))==3 and all((z>0)==(c[0]>0) for z in c)
        for c in F) and all(sum(x in c for c in F)==sum(-x in c for c in F)==2 for x in range(1,n+1))

checks=0
for t in (1,2):
    F=original(t)
    assert valid(F);checks+=1
    for w in product((0,1),repeat=t):
        p={6*j+1:False for j in range(2*t)}
        for i,v in enumerate(w):
            p[12*i+2]=bool(v); p[12*i+8]=not bool(v)
        assert models(F,p)==18**t;checks+=1
        for i in range(t):
            assert models(F,{**p,12*i+4:False})==(9*18**(t-1) if w[i] else 0)
            checks+=1
        allpins={**p,**{12*i+4:False for i in range(t)}}
        assert models(F,allpins)==(9**t if all(w) else 0)
        checks+=1
        if not any(w):
            assert not any(all(abs(z) in p and p[abs(z)]!=(z>0) for z in c) for c in F)
            checks+=1
print('GATE317 independent PASS:',checks,'assertions; no producer imports')
