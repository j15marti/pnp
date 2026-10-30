#!/usr/bin/env python3
"""Self-contained independent check of MIXED-EXTREME-FOREST245.
Full 11-family solver/work audit and raw source records are in repro ZIP.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
C=((7,8,-3),(7,5,-1),(3,-4,-2),(-3,5,-4),(6,-8,3),(-7,1,8),
   (6,2,-3),(8,7,4),(-5,-3,-6),(-6,1,-5),(6,8,1),(1,2,3))
n=8
def sat(a):return all(any(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in C)
def req(c,mode):return {abs(l):int((l>0)==(mode=='S')) for l in c}
def merge(d,e):
    if any(k in d and d[k]!=v for k,v in e.items()):return None
    return d|e
def count(j,a):return sum(((a>>(abs(l)-1))&1)==(l>0) for l in C[j])
source=[]
for j,c in enumerate(C):
    source.append({'j':j,'literals':c,'S':req(c,'S'),'U':req(c,'U')})
    for l in c:assert req(c,'S')[abs(l)]==1-req(c,'U')[abs(l)]
pair_count=0
for j,k in combinations(range(len(C)),2):
    for p in 'SU':
        for q in 'SU':
            possible=merge(req(C[j],p),req(C[k],q)) is not None
            actual=any(count(j,a)==(3 if p=='S' else 0)
                       and count(k,a)==(3 if q=='S' else 0) for a in range(1<<n))
            assert possible==actual
            pair_count+=1
source_pairs=defaultdict(list)
for j in range(len(C)):
    for k in range(len(C)):
        if j==k:continue
        r=merge(req(C[j],'U'),req(C[k],'S'))
        if r is not None:source_pairs[tuple(sorted(r.items()))].append((j,k))
E=[dict(x) for x in source_pairs]
assert sum(map(len,source_pairs.values()))==74 and len(E)==72
def inter(x,y):return merge(x,y)
def number(x,pin):
    r=inter(x,pin)
    return 0 if r is None else 1<<(n-len(r))
def maximum_forest():
    used={0};links=[]
    while len(used)<len(E):
        best=(-1,None,None)
        for i in used:
            for j in set(range(len(E)))-used:
                z=inter(E[i],E[j])
                w=number(z,{}) if z is not None else 0
                if w>best[0]:best=w,i,j
        _,i,j=best;used.add(j);links.append((i,j))
    return links
T=maximum_forest()
I=[inter(E[i],E[j]) for i,j in T]
def bound(pin):
    base=1<<(n-len(pin))
    return base-sum(number(e,pin) for e in E)+sum(number(e,pin) for e in I if e is not None)
assert Fraction(bound({}),1<<n)==Fraction(5,64)
old_gamma=sum((Fraction(1,1<<len(merge(req(C[j],'U'),req(C[k],'S'))))
    for j in range(len(C)) for k in range(len(C)) if j!=k
    and merge(req(C[j],'U'),req(C[k],'S')) is not None),Fraction(0))
assert old_gamma==Fraction(69,32)
pin={};trail=[]
for x in range(1,n+1):
    b0,b1=bound(pin|{x:0}),bound(pin|{x:1})
    assert b0+b1==bound(pin)
    v=0 if b0>0 else 1
    pin[x]=v;trail.append((x,v,b0,b1))
a=sum(v<<(x-1) for x,v in pin.items())
w=a if sat(a) else a^((1<<n)-1)
assert sat(w)
assert sum(sat(a) for a in range(1<<n))==47
assert sum(sat(a) or sat(a^((1<<n)-1)) for a in range(1<<n))==82
for a in range(1<<n):
    comp=a^255
    assert [count(j,comp) for j in range(len(C))]==[3-count(j,a) for j in range(len(C))]
    active={i for i,e in enumerate(E) if all(((a>>(x-1))&1)==v for x,v in e.items())}
    H=1-len(active)+sum(i in active and j in active for i,j in T)
    assert H<=int(sat(a) or sat(comp))
print({'status':'PASS','source_clauses':len(C),'pair_modes_checked':pair_count,
       'mixed_original_pairs':74,'unique_event_cubes':72,'forest_edges':len(T),
       'forest_bound':'5/64','old_gamma':'69/32',
       'exact_models':47,'successful_orientations':82,
       'constructed_witness_mask':w,'coherent_conditional_flip_trail':trail,
       'P_versus_NP':'OPEN'})
