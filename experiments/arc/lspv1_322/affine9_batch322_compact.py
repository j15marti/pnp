#!/usr/bin/env python3
"""Compact independent-source AFFINE9-BATCH-SHARPNESS322 reproducer."""
from itertools import combinations, product
from collections import Counter
P=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9)]
M=[(1,5,9),(2,6,7),(3,4,8),(1,6,8),(2,4,9),(3,5,7)]
F=[(1,c) for c in P]+[(-1,c) for c in M]
def sat(f,a):
    return all(any((((a>>(v-1))&1)==(s==1)) for v in t) for s,t in f)
def block(t):
    return [(s,tuple(v+9*k for v in tri)) for k in range(t) for s,tri in F]
def project(f,I):
    untouched=[];out=[]
    for j,(s,t) in enumerate(f):
        if not any(x in t for x in I):
            untouched.append(frozenset(s*v for v in t))
    for x in I:
        pp=[set(t) for s,t in f if s==1 and x in t]
        nn=[set(-v for v in t) for s,t in f if s==-1 and x in t]
        assert len(pp)==len(nn)==2
        for p in pp:
            for n in nn:
                r=frozenset((p-{x})|(n-{-x}))
                assert len(r)==4 and all(-l not in r for l in r)
                out.append(r)
    assert len(set(untouched+out))==len(untouched+out)
    return untouched+out
def eval_res(g,a):
    return all(any((((a>>(abs(l)-1))&1)==(l>0)) for l in c) for c in g)
assert len({tuple(sorted(e)) for _,c in F for e in combinations(c,2)})==36
assert sum(sat(F,a) for a in range(512))==18
co=[0]*4
for z in range(256):
    co[2*int(sat(F,z<<1))+int(sat(F,(z<<1)|1))]+=1
assert co==[239,8,8,1]
for t in (1,2,3,4,8):
    source=block(t);I=[9*j+1 for j in range(t)]
    g=project(source,I)
    assert len(g)==12*t and sum(map(len,g))==40*t
    if t<=2:
        keep=[x for x in range(1,9*t+1) if x not in I]
        for z in range(1<<len(keep)):
            a=sum(((z>>j)&1)<<(v-1) for j,v in enumerate(keep))
            left=any(sat(source,a|sum(((b>>j)&1)<<(v-1) for j,v in enumerate(I))) for b in range(1<<t))
            assert left==eval_res(g,a)
print('PASS: AG9 models 18; K9 alpha=1; cofactor 239/8/8/1; batch m=12t L=40t; t<=2 exact projection')
