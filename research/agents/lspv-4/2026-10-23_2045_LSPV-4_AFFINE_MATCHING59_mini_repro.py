#!/usr/bin/env python3
"""Self-contained exact mini-auditor for AFFINE-MATCHING59. Python 3 stdlib."""
from itertools import product
from random import Random

def sat(clauses,x):
    return all(any(bool(x & (1 << (abs(z)-1))) == (z>0) for z in c) for c in clauses)

def count(n,clauses):
    return sum(sat(clauses,x) for x in range(1<<n))

def ypos(l):
    return 2*abs(l)-1 if l>0 else 2*abs(l)

def match(n0,phi):
    cs=[]
    for i in range(1,n0+1):
        cs += [(2*i-1,2*i),(-(2*i-1),-2*i)]
    return (2*n0,cs+[tuple(ypos(l) for l in c) for c in phi])

def chain(q,b):
    u,v=q+2,q+3
    cs=[(1,u),(1,-u),(-q-1,v),(-q-1,-v)]
    cs += [(-i,i+1 if b[i-1] else -(i+1)) for i in range(1,q+1)]
    return q+3,cs

def lift(q,b):
    n0,cs=chain(q,b)
    t,a,c=n0+1,n0+2,n0+3
    pairs=[]
    for i in range(1,n0+4):
        pairs += [(2*i-1,2*i),(-(2*i-1),-2*i)]
    tern=[(ypos(x),ypos(y),ypos(t)) for x,y in cs]
    guards=[(ypos(-t),ypos(sa*a),ypos(sb*c))
            for sa in (1,-1) for sb in (1,-1)]
    return 2*(n0+3),pairs+tern+guards

def records(n,cs):
    return (n,len(cs))+tuple(z for c in cs for z in (len(c),*c,*([0]*(3-len(c)))))

def projection(n0,x):
    mask=0
    for i in range(n0):
        bit=(x>>i)&1
        mask |= 1 << (2*i if bit else 2*i+1)
    return mask

def audit():
    checks=0
    for q in range(1,6):
        for bits in product((0,1),repeat=q):
            n,cs=chain(q,bits)
            assert (count(n,cs)==0)==all(bits)
            checks += 1
    for q in (1,2):
        for b in product((0,1),repeat=q):
            n0,source=chain(q,b)
            n,output=lift(q,b)
            assert n==2*q+12 and len(output)==3*q+20
            assert count(n,output)==4*count(n0,source)
            checks += 2
    for q in (1,3,8,30):
        n,cs=lift(q,(1,)*q)
        original=records(n,cs)
        touched=set()
        for i in range(q):
            bits=[1]*q;bits[i]=0
            nx,cx=lift(q,tuple(bits))
            changed={j for j,(x,y) in enumerate(zip(original,records(nx,cx))) if x!=y}
            assert len(changed)==1 and changed.isdisjoint(touched)
            touched |= changed
            checks += 1
    rnd=Random(2026102359)
    for n0 in (3,4,5):
        triples=[tuple(s*(i+1) for i,s in zip(ids,signs))
                 for ids in __import__('itertools').combinations(range(n0),3)
                 for signs in product((-1,1),repeat=3)]
        for _ in range(30):
            phi=[rnd.choice(triples) for j in range(rnd.randrange(10))]
            n,new=match(n0,phi)
            assert len(new)==2*n0+len(phi)
            assert count(n0,phi)==count(n,new)
            assert all(sat(phi,x)==sat(new,projection(n0,x)) for x in range(1<<n0))
            checks += 3
    return checks

if __name__=='__main__':
    print('AFFINE-MATCHING59 mini-audit assertions passed:',audit())
