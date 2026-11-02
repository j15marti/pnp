#!/usr/bin/env python3
"""LSPV-1 329 independent no-producer-import cofactor and source verifier.
Usage: python verify329_public.py path/to/2026-11-02_0532_LSPV1_SOURCE_INDEPENDENT_FACTORED_BATCH329_summary.json
"""
from itertools import combinations,product
from collections import Counter
import json,sys
A=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Z=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6)]
B=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(-1,-5,-9),(-2,-6,-7),(-3,-4,-8),(-1,-6,-8),(-2,-4,-9),(-3,-5,-7)]
H=A+[tuple((abs(z)+9)*(1 if z>0 else -1) for z in c) for c in Z]
S={'F9':A,'Z6':Z,'B9':B,'H15':H}
def C(c,b):return any(bool(b&(1<<(abs(z)-1)))==(z>0) for z in c)
def F(cs,b):return all(C(c,b) for c in cs)
def mask(names,values):return sum((1<<(v-1)) for v,a in zip(names,values) if a)
def test(cs,record):
    n=record['n'];m=len(cs);I=record['I'];rest=[x for x in range(1,n+1) if x not in I]
    assert n==max(abs(z) for c in cs for z in c) and 3*m==4*n
    counts=Counter((abs(z),z>0) for c in cs for z in c)
    assert all(counts[i,b]==2 for i in range(1,n+1) for b in (False,True))
    assert len({tuple(sorted(c)) for c in cs})==m
    assert all(len(c)==3 and len(set(map(abs,c)))==3 and all(z*c[0]>0 for z in c) for c in cs)
    assert all(not any(abs(z)==v for z in c) for u,v in combinations(I,2) for c in cs if any(abs(z)==u for z in c))
    U=[c for c in cs if all(abs(z) not in I for z in c)];R=list(U)
    for x in I:
        pos=[tuple(z for z in c if abs(z)!=x) for c in cs if x in c]
        neg=[tuple(z for z in c if abs(z)!=x) for c in cs if -x in c]
        assert len(pos)==len(neg)==2
        R.extend(p+q for p,q in product(pos,neg))
    assert len(R)==m and sum(map(len,R))==3*m+4*len(I)
    seen=0
    for profile in product((False,True),repeat=len(rest)):
        base=mask(rest,profile)
        truth=any(F(cs,base|mask(I,p)) for p in product((False,True),repeat=len(I)))
        raw=F(R,base)
        fact=all(C(c,base) for c in U)
        for x in I:
            p=[tuple(z for z in c if abs(z)!=x) for c in cs if x in c]
            q=[tuple(z for z in c if abs(z)!=x) for c in cs if -x in c]
            fact=fact and (all(C(c,base) for c in p) or all(C(c,base) for c in q))
        assert raw==fact==truth
        seen+=int(truth)
    assert seen==record['projected_models']
    assert sum(F(cs,b) for b in range(1<<n))==record['source_models']
    assert record['factored_gates']==3*m-4*len(I)-1 and record['raw_gates']==3*m+4*len(I)-1
    return (1<<n)+(1<<(n-len(I)))
raw=json.load(open(sys.argv[1]));assert len(raw['rows'])==4
checks=sum(test(S[row['source'].split('=')[0]],row) for row in raw['rows'])
fixed={3:0,5:1,6:0,7:0,8:0};free=[2,4,9];labels=[]
for x in (0,1):
    ct=0;leaves=0
    for bits in product((False,True),repeat=3):
        full=mask([1]+list(fixed)+free,[x]+list(fixed.values())+list(bits))
        if F(A,full):ct+=1
        elif x:assert any(not C(c,full) for c in A);leaves+=1
    labels.append(ct)
    if x:assert leaves==8
assert labels==[2,0]
counts=Counter()
for i,j in combinations(range(12),2):
    for q,r in product((True,False),repeat=2):
        want=any(all(C((z,),b)==s for c,s in ((A[i],q),(A[j],r)) for z in c) for b in range(512))
        values={};possible=True
        for c,s in ((A[i],q),(A[j],r)):
            for z in c:
                v=(z>0)==s
                if abs(z) in values and values[abs(z)]!=v:possible=False
                values[abs(z)]=v
        assert want==possible
        counts[('S' if q else 'U')+('S' if r else 'U')]+=want
assert counts==Counter({'SS':37,'SU':49,'US':49,'UU':37})
print(json.dumps({'status':'PASS','no_producer_import':True,'checks':checks+264+16,'same_F9':labels,'S_U':dict(counts)},sort_keys=True))
