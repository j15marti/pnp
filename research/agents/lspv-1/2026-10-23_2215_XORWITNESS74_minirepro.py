#!/usr/bin/env python3
"""Compact standalone signed exact-(2,2) 3-CNF regression, seed 202610231259.
Finite test, not the proof. Full sampler/extension audit: xorwitness74_audit.py.
"""
import random
from collections import Counter

rng = random.Random(202610231259)

def canon(c):
    return tuple(sorted(c, key=lambda x: (abs(x), x)))

def base(g=3):
    out=[]
    for i in range(g):
        x,y,z=3*i+1,3*i+2,3*i+3
        zn=3*((i+1)%g)+3
        out.extend(map(canon, [(x,-y,z),(x,-y,-z),(-x,y,zn),(-x,y,-zn)]))
    return tuple(out)

def legal(F):
    if len(F)!=len(set(F)) or any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in F):
        return False
    n=max(abs(x) for c in F for x in c)
    return all(sum(x==v for c in F for x in c)==2 and
               sum(x==-v for c in F for x in c)==2 for v in range(1,n+1))

def defect(F):
    lookup=set(F)
    matched=set()
    for c in F:
        for x in c:
            other=canon((-x if z==x else z) for z in c)
            if other in lookup:
                matched.add(tuple(sorted((c, other))))
    assert len(set(x for pair in matched for x in pair))==2*len(matched)
    return len(F)-2*len(matched)

def sat(F):
    n=max(abs(x) for c in F for x in c)
    for a in range(1<<n):
        if all(any(bool((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in F):
            return True
    return False

def mutate(F):
    for _ in range(500):
        a,b=rng.sample(range(len(F)),2)
        x=rng.choice(F[a]); same=[v for v in F[b] if (v>0)==(x>0) and abs(v)!=abs(x)]
        if not same:continue
        y=rng.choice(same)
        G=list(F)
        G[a]=canon(y if v==x else v for v in F[a])
        G[b]=canon(x if v==y else v for v in F[b])
        if legal(G):return tuple(G)
    raise AssertionError('No valid same-sign swap')

F=base(); assert legal(F)
counts=Counter()
for i in range(320):
    d=defect(F)
    counts[d]+=1
    if d<=8:
        assert sat(F), ('counterexample to delta<=8 theorem',F)
    if i!=319:F=mutate(F)
# Independent SAT/UNSAT nonregular controls.
assert not sat([(1,),(-1,)])
assert sat([(1,),(-2,),(-1,2)]) is False
assert sat([(1,2,3)])
assert not sat([tuple(-v if (mask>>(v-1))&1 else v for v in (1,2,3)) for mask in range(8)])
print('PASS:',sum(counts.values()),'valid exact-(2,2) signed sources; defects',dict(sorted(counts.items())))
