#!/usr/bin/env python3
"""TMR-2/089 exact reproducible finite proof for T5 binary polymorphisms."""
from itertools import product, permutations
from math import prod
Q=range(5)
def R(a,b): return (b-a)%5 in (1,3)
def power(k):
    edges=[]
    for u in product(Q,repeat=k):
        for ds in product((1,3),repeat=k):
            v=tuple((a+d)%5 for a,d in zip(u,ds))
            edges.append((u,v))
    return edges

def AC(dom,edges):
    d={k:set(v) for k,v in dom.items()}
    while True:
        ch=False
        for u,v in edges:
            a={x for x in d[u] if any(R(x,y) for y in d[v])}
            if not a:return None
            b={y for y in d[v] if any(R(x,y) for x in a)}
            if not b:return None
            if a!=d[u] or b!=d[v]:ch=True
            d[u]=a;d[v]=b
        if not ch:return d

E2=power(2)
assert len(E2)==100
D2={u:set(Q) for u in product(Q,repeat=2)}
for x in Q:D2[x,x]={x}
D2=AC(D2,E2)
assert D2 and all(D2[a,b]=={a,b} for a,b in product(Q,repeat=2))
poly=[]
for choice in (0,1):
    d={u:set(v) for u,v in D2.items()}
    d[0,1]={choice}
    d=AC(d,E2)
    assert d and all(len(s)==1 for s in d.values())
    f={k:next(iter(v)) for k,v in d.items()}
    assert all(R(f[u],f[v]) for u,v in E2)
    assert all(f[a,b]==(a if choice==0 else b) for a,b in product(Q,repeat=2))
    for c in Q: poly.append(tuple((f[a,b]+c)%5 for a,b in product(Q,repeat=2)))
assert len(set(poly))==10

# The diagonal g(x)=f(x,x) of any binary polymorphism is unary T5
# endomorphism, and all unary endomorphisms are the five rotations.
# T5 is loopless complete oriented, so unary endomorphisms inject.
for a,b in product(Q,repeat=2):
    if a!=b:assert R(a,b)!=R(b,a)
for c in Q:
    assert all(R(a,b)==R((a+c)%5,(b+c)%5) for a,b in product(Q,repeat=2))

# Ternary majority has a three-entry AC obstruction.
E3=power(3)
assert len(E3)==1000
P={(4,3,3):3,(4,3,4):4,(4,4,3):4}
def testpins(P):
    d={u:set(Q) for u in product(Q,repeat=3)}
    for u,x in P.items():d[u]={x}
    return AC(d,E3)
assert testpins(P) is None
for p in P:assert testpins({k:v for k,v in P.items() if k!=p}) is not None
# Direct Maltsev refutation: (0,0,2) -> (1,3,3), but 2 !-> 1.
assert all(R(a,b) for a,b in zip((0,0,2),(1,3,3))) and not R(2,1)

# Exact 32-mask propagation maps and eight cyclic-shift orbits.
def shift(s,t):return frozenset((a+t)%5 for a in s)
S=[frozenset(a for a in Q if m>>a&1) for m in range(32)]
assert len(set(S))==32
for a in S:
    plus={v for u in a for v in Q if R(u,v)}
    minus={u for v in a for u in Q if R(u,v)}
    assert len(plus)==len(minus)
reps={min(tuple(sorted(shift(s,t))) for t in Q) for s in S}
assert len(reps)==8

A=[[int(R(a,b)) for b in Q] for a in Q]
def det5(A):
    return sum((-1)**sum(p[i]>p[j] for i in Q for j in range(i+1,5)) *
               prod(A[i][p[i]] for i in Q) for p in permutations(Q))
assert det5(A)==2
# Characteristic two: nonzero all-ones kernel, and rank exactly four.
rows=[sum(A[i][j]<<j for j in Q) for i in Q]
piv=[]
for m in rows:
    for j,p in piv:
        if m>>j&1:m^=p
    if m:
        j=m.bit_length()-1
        piv.append((j,m))
assert len(piv)==4
print('PASS: 32 subsets, 8 orbits, binary clone 10 operations, no majority/Maltsev; det 2; rank F2 4, rank F5 5')
