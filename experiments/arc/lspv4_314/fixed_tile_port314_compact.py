#!/usr/bin/env python3
"""314: independent, executable pure 131-record tile and port-mod3 audit.
The published Doecker 131-clause mixed enforcer is NOT implemented here.
"""
from collections import Counter
from itertools import product, combinations
import json

P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=[tuple(t) for t in P]+[tuple(-v for v in t) for t in Q]
A=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Y=[tuple(t) for t in A]+[tuple(-v for v in t) for t in A]

def true(c,a):
    return any(a[abs(v)] == (v>0) for v in c)

def count(cs,n,pins=None):
    pins=pins or {}
    free=[x for x in range(1,n+1) if x not in pins]
    return sum(all(true(c,pins|dict(zip(free,bits))) for c in cs)
               for bits in product((0,1),repeat=len(free)))

def valid(cs,n):
    if not all(len(c)==3 and len({abs(v) for v in c})==3 and
               (all(v>0 for v in c) or all(v<0 for v in c))
               for c in cs):return False
    if len({tuple(sorted(c)) for c in cs})!=len(cs):return False
    q=Counter((abs(v),v>0) for c in cs for v in c)
    return all(q[x,s]==2 for x in range(1,n+1) for s in (False,True))

def tile(j):
    i,t=divmod(j,131)
    if t<3:
        return tuple((1 if v>0 else -1)*(9*t+abs(v)) for v in F[i])
    b,k=divmod(t-3,8)
    return tuple((1 if v>0 else -1)*(27+96*i+6*b+abs(v)) for v in Y[k])

assert valid(F,9) and valid(Y,6)
assert count(F,9)==70 and count(Y,6)==18
T=[tile(j) for j in range(12*131)]
assert valid(T,1179) and len(T)==1572
PS={1:0,3:0,5:1,6:0,7:0,8:0}
PU={1:1,3:0,5:1,6:0,7:0,8:0}
assert count(F,9,PS)==2 and count(F,9,PU)==0
assert len(T)==131*len(F)
for c in T: assert len(c)==3
# Original-clause-indexed eight-leaf sound UNSAT certificate.
free=[x for x in range(1,10) if x not in PU]
leaves=[]
for b in product((0,1),repeat=len(free)):
    d=PU|dict(zip(free,b))
    bad=next(j for j,c in enumerate(F) if not true(c,d))
    leaves.append(bad)
assert len(leaves)==8
# Signed variable quotas survive a polarity swap on one positive and
# one negative x1 occurrence, producing a proper nonmonotone test input.
M=list(F)
M[0]=(-1,5,6);M[7]=(1,-6,-7)
q=Counter((abs(v),v>0) for c in M for v in c)
assert all(q[x,s]==2 for x in range(1,10) for s in (False,True))
assert count(M,9)==69
assert sum(any(v<0 for v in c) and any(v>0 for v in c) for c in M)==2
# Modular impossibility: 3(mp-mn) = P-Q for self-balanced auxiliary names.
for pp,qq in [(2,1),(1,2)]:
    assert (pp-qq)%3 != 0
assert (6-3)%3==0 and (3-6)%3==0
# Every original pair of clauses: all SAT/all UNSAT extreme compatibility.
modes=0
for i,j in combinations(range(12),2):
    for e,f in product((0,1),repeat=2):
        di={abs(v):((v>0)==bool(e)) for v in F[i]}
        dj={abs(v):((v>0)==bool(f)) for v in F[j]}
        yes=all(di[x]==dj[x] for x in di.keys()&dj.keys())
        # Independent existence check by exhaustive assignments on shared names.
        names=sorted(set(di)|set(dj))
        brute=any(all(d.get(x)==y for x,y in di.items()) and
                  all(d.get(x)==y for x,y in dj.items())
                  for z in product((0,1),repeat=len(names))
                  for d in [dict(zip(names,z))])
        assert yes==brute
        modes+=1
assert modes==264
print(json.dumps(dict(tag="LSPV4_FIXED_TILE_PORT_CONGRUENCE314_GITHUB",
    source_n=9,source_m=12,source_models=70,pad_models=18,
    output_n=1179,output_m=1572,source_pair_modes=264,
    SAT_cube_models=2,UNSAT_cube_models=0,UNSAT_clause_IDs=leaves,
    mixed_comparison_models=69,program_verified=True,
    mixed_131_clause_template="NOT VERIFIED; conditional on Doecker",
    target_language="Döcker proper duplicate-free monotone 3-SAT-(2,2)",
    P_vs_NP="OPEN"),indent=2))
