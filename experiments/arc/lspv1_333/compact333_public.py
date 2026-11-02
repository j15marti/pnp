#!/usr/bin/env python3
"""LSPV-1 weighted source-independent projection 333. Stdlib only.
The full exhaustive producer, independent Node checker, JSON grammar tests and raw
Davis-Putnam auditor are in the dated user-facing reproducibility archive.
"""
from itertools import product
from collections import Counter
import json
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
PB=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9)]
NB=[(1,5,9),(2,6,7),(3,4,8),(1,6,8),(2,4,9),(3,5,7)]
Z=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
T=[(1,2,3),(1,2,4),(3,5,6),(4,5,6)]
def formula(p,q):
    return tuple(map(tuple,p))+tuple(tuple(-v for v in c) for c in q)
def valid(n,clauses):
    if type(n)!=int or n<3 or n%3 or type(clauses) not in (tuple,list) or len(clauses)*3!=4*n:return False
    seen=set(); occ=Counter()
    for c in clauses:
        if type(c) not in (list,tuple) or len(c)!=3 or any(type(v)!=int or not v or abs(v)>n for v in c):return False
        if len({abs(v) for v in c})!=3 or not (all(v>0 for v in c) or all(v<0 for v in c)):return False
        s=tuple(sorted(c))
        if s in seen:return False
        seen.add(s);occ.update(c)
    return all(occ[v]==occ[-v]==2 for v in range(1,n+1))
def sat(cs,mask):
    return all(any(bool(mask&(1<<(abs(l)-1)))==(l>0) for l in c) for c in cs)
def choose(n,cs):
    adj=[set() for _ in range(n+1)]
    for c in cs:
        v={abs(l) for l in c}
        for x in v:adj[x].update(v-{x})
    I=[];seen=set()
    for x in range(1,n+1):
        if x not in seen:
            I.append(x);seen.update(adj[x]);seen.add(x)
    assert len(I)>=(n+8)//9
    return I
def weight(cs,I,z):
    if any(not sat((c,),z) for c in cs if all(abs(l) not in I for l in c)):return 0
    answer=1
    for x in I:
        p=[tuple(l for l in c if l!=x) for c in cs if x in c]
        n=[tuple(l for l in c if l!=-x) for c in cs if -x in c]
        assert len(p)==len(n)==2
        answer*=int(sat(p,z))+int(sat(n,z))
    return answer
def audit(n,cs,I):
    assert valid(n,cs)
    assert all(sum(abs(l) in I for l in c)<=1 for c in cs)
    R=[v for v in range(1,n+1) if v not in I];hist=Counter()
    for z in range(1<<len(R)):
        a=sum(((z>>j)&1)<<(v-1) for j,v in enumerate(R))
        w=weight(cs,I,a)
        assert w==sum(sat(cs,a|sum(((b>>j)&1)<<(v-1) for j,v in enumerate(I))) for b in range(1<<len(I)))
        hist[w]+=1
    return {'selected':I,'projected_models':sum(v for k,v in hist.items() if k),
            'source_models':sum(k*v for k,v in hist.items()),
            'weights':dict(sorted(hist.items())),
            'mixed_operator_nodes':3*len(cs)-4*len(I)-1}
def main():
    fixtures={'F9':(9,formula(P9,N9)),'B9':(9,formula(PB,NB)),
              'Z6':(6,formula(Z,Z)),'T6':(6,formula(T,T))}
    result={}
    for key,(n,cs) in fixtures.items():result[key]=audit(n,cs,choose(n,cs))
    assert [(result[k]['source_models'],result[k]['projected_models']) for k in fixtures]==[(70,48),(18,17),(18,12),(26,16)]
    B=fixtures['B9'][1]
    assert all(audit(9,B,[x])['projected_models']==17 for x in range(1,10))
    two=tuple(tuple((1 if l>0 else -1)*(abs(l)+9*j) for l in c) for j in range(2) for c in B)
    result['B9x2']=audit(18,two,[1,10]);assert (result['B9x2']['source_models'],result['B9x2']['projected_models'])==(324,289)
    for cs,n in ((B,9),(fixtures['F9'][1],9)):
        pins={2:0,3:0} if cs==B else {3:0,5:1,6:0,7:0,8:0}
        cnt=[]
        for x in (0,1):
            cnt.append(sum(sat(cs,a) for a in range(1<<n)
                       if (a&1)==x and all(((a>>(v-1))&1)==b for v,b in pins.items())))
        assert cnt==([0,4] if cs==B else [2,0])
    assert not valid(9,list(fixtures['F9'][1])+[fixtures['F9'][1][0]])
    assert not valid(9,'bad original string')
    print(json.dumps({'status':'PROVED exact scoped identity, not universal SAT decision lower bound',
       'results':result,'same_source_B9':[0,4],'same_source_F9':[2,0],
       'arbitrary_A_FLMV':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
