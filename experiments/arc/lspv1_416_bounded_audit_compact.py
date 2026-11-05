#!/usr/bin/env python3
"""LSPV-1/416 compact reproducibility, Python 3 stdlib. Run without args."""
from itertools import product
from collections import Counter
import json
CLAUSES=((1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2))
def restrict(f,a):
    out=[]
    for clause in f:
        rem=[];hit=False
        for l in clause:
            i=abs(l)-1
            if i>=len(a):rem.append(l)
            elif (a[i]==1)==(l>0):hit=True;break
        if not hit:out.append(tuple(rem))
    return tuple(out)
def truth(f):
    return any(all(any((a[abs(l)-1]==1)==(l>0) for l in c) for c in f)
               for a in product((0,1),repeat=2))
def alg(k,f):
    if k=='exact':return truth(f)
    if k=='no':return False
    if k=='yes':return True
    if k=='empty':return not any(len(c)==0 for c in f)
    if k=='parity':return len(f)%2==0
    if k=='poison':return not truth(f) if f==((1,),) else truth(f)
    raise ValueError(k)
def bad(k,f):
    for d in (0,1,2):
        for a in product((0,1),repeat=d):
            p=alg(k,restrict(f,a))
            if d==2:
                if p!=(not any(len(c)==0 for c in restrict(f,a))):return True
            else:
                left=alg(k,restrict(f,a+(0,)))
                right=alg(k,restrict(f,a+(1,)))
                if p!=(left or right):return True
    return False
expected={
'exact':(0,0,0),'no':(95,95,0),'yes':(161,255,94),
'empty':(161,183,22),'parity':(129,253,124),'poison':(1,1,0)}
rows=[]
for k in expected:
    c=Counter()
    for mask in range(256):
        f=tuple(CLAUSES[i] for i in range(8) if mask>>i & 1)
        truth_root=truth(f);pred=alg(k,f);viol=bad(k,f)
        c['wrong']+=pred!=truth_root;c['bad']+=viol
        c['root_correct_but_bad']+=(pred==truth_root and viol)
        assert pred==truth_root or viol,('false negative audit',k,mask)
    found=(c['wrong'],c['bad'],c['root_correct_but_bad'])
    assert found==expected[k],(k,found)
    rows.append({'classifier':k,**c})
print(json.dumps({'schema':'LSPV1-416-COMPACT','instances':256,
       'clauses':len(CLAUSES),'rules':rows,'wrong_root_escaped':0,
       'B3':'OPEN','P_vs_NP':'OPEN'},indent=2))
