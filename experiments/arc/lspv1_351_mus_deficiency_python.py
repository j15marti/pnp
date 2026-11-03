#!/usr/bin/env python3
"""Independent finite replay for MUS deficiency stability (standard library)."""
from itertools import combinations, product
from collections import Counter
from random import Random
import json
BASE=[(),(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]
def models(F):
    vs=sorted({abs(v) for c in F for v in c})
    return sum(all(any((bits[vs.index(abs(lit))]==(lit>0)) for lit in cl) for cl in F)
               for bits in product((False,True),repeat=len(vs)))
def delta(F):return len(F)-len({abs(v) for cl in F for v in cl})
def parts(F):
    for s in range(len(F)+1):
        yield from combinations(F,s)
def is_mus(F):
    return models(F)==0 and all(models(F[:i]+F[i+1:])>0 for i in range(len(F)))
def check(F):
    d=delta(F)
    return is_mus(F) and all(delta(H)<d for H in parts(F) if len(H)<len(F))
counts=Counter();dh=Counter()
for mask in range(512):
    F=tuple(BASE[j] for j in range(9) if mask&(1<<j))
    counts["total"]+=1
    if models(F): counts["SAT"]+=1
    else:
        counts["UNSAT"]+=1
        if is_mus(F):
            counts["MUS"]+=1
            if not check(F):raise AssertionError("MUS stability")
            dh[delta(F)]+=1
tri=[tuple(a*(i+1) for i,a in enumerate(p) if a) for p in product((-1,0,1),repeat=3)
     if any(p)]
rng=Random(351);seen=set();sampled=Counter()
for _ in range(1600):
    F=list(rng.sample(tri,rng.randrange(4,16)))
    if models(F):continue
    rng.shuffle(F)
    i=0
    while i<len(F):
        if models(F[:i]+F[i+1:])==0:F.pop(i)
        else:i+=1
    F=tuple(sorted(F))
    if F in seen:continue
    seen.add(F)
    if not check(F):raise AssertionError("3-variable MUS stability")
    sampled[delta(F)]+=1
block=tuple(tuple(-(i+1) if (a>>i)&1 else i+1 for i in range(3)) for a in range(8))
peitl=((1,2),(3,4),(-1,-3),(-2,-4),(1,-2,-3,4),(-1,2,3,-4))
if not check(block) or delta(block)!=5:raise AssertionError("blocking")
if not check(peitl) or delta(peitl)!=2:raise AssertionError("Peitl")
for n in range(2,9):
    horn=tuple([(1,)]+[(-i,i+1) for i in range(1,n)]+[(-n,)])
    if not check(horn):raise AssertionError("Horn")
if check(((1,),(-1,),(2,))):raise AssertionError("redundant control")
out={"status":"COMPUTATIONAL","two_variable":dict(counts),
     "two_var_MUS_deficiency":dict(dh),"three_var_distinct_MUS":len(seen),
     "three_var_MUS_deficiency":dict(sampled),
     "controls":["3-variable 8-clause blocker","Peitl 4-variable 6-clause source",
                 "Horn n=2..8","redundant UNSAT non-MUS"]}
print(json.dumps(out,sort_keys=True,indent=2))
