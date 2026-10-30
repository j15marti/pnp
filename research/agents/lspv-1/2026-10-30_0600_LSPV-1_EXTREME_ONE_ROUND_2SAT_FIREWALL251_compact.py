#!/usr/bin/env python3
"""LSPV-1 EXTREME251 standalone strict22 source-indexed certificate; Python 3 stdlib."""
from itertools import product
F=[(6,2,-4),(3,2,-6),(4,-5,-1),(5,4,3),
   (-3,-6,-1),(1,5,-2),(-4,6,-5),(-2,-3,1)]
n=6
def truth(C,a):return sum(a[abs(l)]==(l>0) for l in C)
def target(C,s):return {abs(l):int((l>0)==(s=='S')) for l in C}
def mode(C,D,ss):
    p,q=target(C,ss[0]),target(D,ss[1])
    return all(k not in q or v==q[k] for k,v in p.items())
def resolvent(C,D,x):
    p,q=set(C),set(D)
    if x not in p:p,q=q,p
    assert x in p and -x in q
    out=(p-{x})|(q-{-x})
    assert not any(-z in out for z in out)
    return tuple(sorted(out,key=lambda z:(abs(z),z)))
def all_a():
    return [{i:b[i-1] for i in range(1,n+1)}
            for b in product((0,1),repeat=n)]
def original_up(p):
    p=dict(p)
    while True:
        change=False
        for C in F:
            if any((l>0)==p[abs(l)] for l in C if abs(l) in p):continue
            R=tuple(l for l in C if abs(l) not in p)
            if not R:return None
            if len(R)==1:
                l=R[0];v=abs(l);val=int(l>0)
                if v in p and p[v]!=val:return None
                if v not in p:p[v]=val;change=True
        if not change:return p
def first_gen():
    out=[]
    for v in range(1,n+1):
        for j,C in enumerate(F):
            if v not in C:continue
            for k,D in enumerate(F):
                if -v not in D:continue
                overlap=set(map(abs,C))&set(map(abs,D))
                if not any(u!=v and (u in C)==(u in D) for u in overlap):continue
                try:R=resolvent(C,D,v)
                except AssertionError:continue
                out.append((j,k,v,R))
    assert len(out)<=4*n
    return out
def binary_closure(p):
    p=dict(p)
    while True:
        p=original_up(p)
        if p is None:return None
        B=[]
        for C in F:
            if any((l>0)==p[abs(l)] for l in C if abs(l) in p):continue
            R=tuple(l for l in C if abs(l) not in p)
            if len(R)<=2:B.append(R)
        free=[v for v in range(1,n+1) if v not in p]
        models=[]
        for bits in product((0,1),repeat=len(free)):
            a=dict(p);a.update(dict(zip(free,bits)))
            if all(truth(C,a)>0 for C in B):models.append(a)
        if not models:return None
        forced={v:models[0][v] for v in free
                if all(a[v]==models[0][v] for a in models)}
        if not forced:return p
        p.update(forced)
