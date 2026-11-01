#!/usr/bin/env python3
"""GATE311 standalone compact reproducer. Source-authenticated G2 original;
no SAT-label oracle, no third-party libraries; Python work != native FLMV.
Full producer, independently written verifier and original-clause raw data
are in the separate GATE311 reproducibility archive."""
from itertools import product
import json

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
def original(k):
    clauses=[]
    for i in range(k):
        for j,vs in enumerate(P):
            clauses.append(tuple(i*9+v if j or v!=5 else ((i+1)%k)*9+5 for v in vs))
        clauses.extend(tuple(-i*9-v for v in vs) for vs in M)
    return clauses
def canonical(cs,n):
    pos=[0]*(n+1);neg=[0]*(n+1);seen=set()
    if 3*len(cs)!=4*n:return False
    for c in cs:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if not all(0<abs(x)<=n for x in c):return False
        if len({x>0 for x in c})!=1:return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for x in c:(pos if x>0 else neg)[abs(x)]+=1
    return all(pos[i]==neg[i]==2 for i in range(1,n+1))
def pins(b,s):
    out={5:1}
    if b:out.update({4:0,6:0})
    if s:out.update({10:0,14:0,15:0})
    return out
def count(cs,p):
    total=0;first=None;checked=0
    for a in range(1<<18):
        if any(((a>>(x-1))&1)!=v for x,v in p.items()):continue
        checked+=1
        if all(any(((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in cs):
            total+=1
            if first is None:first=a
    return total,first,checked
def safe(s,t):
    return all(((s>>(2*i))&3)!=3 for i in range(t))
def normalized(colors):
    ids={}
    return tuple(ids.setdefault(x,len(ids)) for x in colors)
def classes(t):
    n=4**t
    old=[int(safe(s,t)) for s in range(n)]
    while True:
        sig=[(int(safe(s,t)),tuple(old[s|(1<<a)] for a in range(2*t))) for s in range(n)]
        keys={k:i for i,k in enumerate(sorted(set(sig)))}
        new=[keys[x] for x in sig]
        if normalized(new)==normalized(old):return len(set(new))
        old=new
def main():
    F=original(2)
    assert canonical(F,18)
    counts={};leaves={}
    for name,b,s in [('AZ',0,0),('AQ',0,1),('BZ',1,0),('BQ',1,1)]:
        c,w,z=count(F,pins(b,s));counts[name]=c;leaves[name]=z
        assert (w is None)==(c==0)
    assert counts=={'AZ':2377,'AQ':299,'BZ':108,'BQ':0}
    K=[classes(t) for t in range(1,7)]
    assert K==[3**t+1 for t in range(1,7)]
    result={'status':'PASS','target':'G_(2t), connected canonical monotone 3-SAT-(2,2)',
            'models_G2':counts,'complete_pinned_assignments_checked':leaves,
            'monotone_classes_t1_to_6':K,'minimum_one_pass_bits_t1_to_6':[(q-1).bit_length() for q in K],
            'statement':'ADD-only continuation quotient 3^t+1; not arbitrary-decider hardness',
            'P_versus_NP':'OPEN'}
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
