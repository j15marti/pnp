#!/usr/bin/env python3
"""Compact original-source independent same-formula SAT/UNSAT control, stdlib only.
Full 1458-cube independent producer/verifier, U198 proof and event-sourced
physical XOR tape records: LSPV2_SATURATED_AFFINE_CLOSURE292_2026-11-01.zip.
This compact checker is a sample theorem trace, NOT a native FLMV solver.
"""
from itertools import product
from collections import Counter
P=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
   (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
Q=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
   (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F=P+[tuple(-x for x in row) for row in Q]
assert len(F)==20
def sat(a):
    return all(any(a[abs(x)]==(x>0) for x in row) for row in F)
def models(p):
    free=[x for x in range(1,16) if x not in p]
    return [{**p,**dict(zip(free,choice))}
            for choice in product((False,True),repeat=len(free))
            if sat({**p,**dict(zip(free,choice))})]
def source_budget(p,cycle_ids):
    covered=[];uncovered=[]
    for j,row in enumerate(F,1):
        if any(abs(x) in p and p[abs(x)]==(x>0) for x in row):covered.append(row)
        else:uncovered.append((j,tuple(x for x in row if abs(x) not in p)))
    assert all(rem for _,rem in uncovered)
    free=[x for x in range(1,16) if x not in p]
    eta=sum(min(sum(x in row for row in covered),
                sum(-x in row for row in covered)) for x in free)
    e=2*len(free)-len(uncovered)
    # cycle_indices is externally checked, NOT a free optimal-cycle oracle
    for cyc in cycle_ids:
        a,b,c=(next(rem for j,rem in uncovered if j==z) for z in cyc)
        assert len(a)==len(b)==len(c)==2
        assert len({abs(x) for row in (a,b,c) for x in row})==3
        assert all(sum(abs(x) in map(abs,row) for row in (a,b,c))==2
                   for x in a+b+c if abs(x) in [abs(y) for y in a+b+c])
    assert len({j for cyc in cycle_ids for j in cyc})==3*len(cycle_ids)
    return e,eta,len(cycle_ids),e-eta-len(cycle_ids)
pU=dict(zip(range(7,16),map(lambda x:x=="1","000011110")))
pS=dict(zip(range(7,16),map(lambda x:x=="1","100011110")))
assert len(models({}))==1032
assert source_budget(pU,[(1,2,12),(3,4,15)])==(2,1,2,-1)
assert not models(pU)
assert source_budget(pS,[(2,11,12),(3,4,15)])==(3,1,2,0)
w=models(pS)
assert len(w)==2
assert all((not a[1] and not a[2] and a[3] and a[4] and not a[5])
           for a in w)
# Opposite-source-original units x4=x5=1 plus C3=(x4 or x5 or x9)
# under x9=0, pU,x6=0: saturation exact-one gives x4 XOR x5=1.
pB={**pU,6:False}
assert source_budget(pB,[(1,2,12)])[3]==0
assert not models(pB)
assert all(x in F[2] for x in (4,5,9))
print("PASS: F15 connected target, 1032 models, UNSAT pU, two SAT pS,"
      " saturated source-binary GF2 contradiction on pU+{x6=0}; "
      "P versus NP OPEN")
