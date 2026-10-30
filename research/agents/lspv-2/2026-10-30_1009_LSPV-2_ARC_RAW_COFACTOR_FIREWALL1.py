#!/usr/bin/env python3
"""Exact reproducible strict22 raw one-pivot cofactor counts, both SAT and UNSAT.
Restricted syntactic control, not an all-algorithm SAT lower bound.
"""
import json, itertools, hashlib
from pathlib import Path

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'

def periodic(k):
    F=[]
    for i in range(k):
        a=3*i+1;b=3*i+2;c=3*i+3;bn=3*((i+1)%k)+2
        F.extend(((a,b,c),(a,-b,-c),(-a,bn,-c),(-a,-bn,c)))
    return F

def simplify(F,pins):
    out=[]
    for c in F:
        if any(abs(l) in pins and pins[abs(l)]==(l>0) for l in c):continue
        out.append(tuple(l for l in c if abs(l) not in pins))
    return out

def check(F):
    n=max(abs(l) for c in F for l in c);m=len(F)
    counts={v:(sum(l==v for c in F for l in c),sum(l==-v for c in F for l in c)) for v in range(1,n+1)}
    assert all(y==(2,2) for y in counts.values())
    assert m*3==n*4
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
    root={v:v for v in range(1,n+1)}
    def find(x):
        while root[x]!=x:x=root[x]
        return x
    for c in F:
        for l in c[1:]:root[find(abs(l))]=find(abs(c[0]))
    assert len(set(find(v) for v in range(1,n+1)))==1
    for v in range(1,n+1):
        for b in (False,True):
            child=simplify(F,{v:b})
            assert len(child)==m-2 and sum(map(len,child))==4*n-8
            assert sum(len(c)==2 for c in child)==2
    return {'n':n,'m':m,'lit_parent':4*n,'lit_child':4*n-8,
            'ratio':(4*n-8)/(4*n),'connected':True,'exact22':True,
            'sha256':hashlib.sha256(repr(F).encode()).hexdigest()}

out={'tag':'ARC_RAW_BRANCH_NO_POWER_SHRINK1','status':'PROVED/EXACT restricted, computational spotchecks',
     'families':[],'W1_unsat':None}
for k in (2,3,4,8,16,32,128):
    F=periodic(k);rec=check(F);n=3*k
    witness={3*i+1:True for i in range(k)}|{3*i+2:False for i in range(k)}|{3*i+3:False for i in range(k)}
    assert all(any(witness[abs(l)]==(l>0) for l in c) for c in F)
    rec['witness_verified']=True
    if n<=12:
        count=sum(all(any(bool(mask&(1<<(abs(l)-1)))==(l>0) for l in c) for c in F) for mask in range(1<<n))
        rec['exhaustive_models']=count
    out['families'].append(rec)
F=[tuple(map(int,c.split())) for c in W1.split(';')];out['W1_unsat']=check(F)
count=sum(all(any(bool(mask&(1<<(abs(l)-1)))==(l>0) for l in c) for c in F) for mask in range(1<<15))
assert count==0
out['W1_unsat']['exhaustive_models']=0
Path(__file__).with_name('arc_branch_firewall1_raw.json').write_text(json.dumps(out,indent=2)+'\n')
print('OK:',len(out['families']),'connected SAT witnesses; W1 UNSAT enumeration; all 2n single-variable cofactors per formula exact')
print([(f['n'],f['lit_child'],f['ratio']) for f in out['families']])
