#!/usr/bin/env python3
"""Restricted named-scoped-stream source-union DP, independently checkable."""
from random import Random
import json
R=Random(202610250112)

def build(k,sat):
    e=[('O',i) for i in (1,2,3)]
    for x in range(8):
        c=tuple(i if not x>>(i-1)&1 else -i for i in (1,2,3))
        if sat and x==7:c=(1,2,3)
        e.append(('C',c))
    for i in range(4,4+k):
        e.extend([('O',i),('C',(i,1,2))])
        if R.randrange(3):e.append(('C',(i,2,-3)))
        e.append(('X',i))
    e.extend([('X',i) for i in (1,2,3)])
    return e

def trace(e):
    active=set();states=[frozenset()];clauses=[]
    for typ,arg in e:
        if typ=='O':
            assert arg not in active
            active.add(arg)
        elif typ=='X':
            assert arg in active
            active.remove(arg)
        else:
            assert len({abs(x) for x in arg})==3
            assert all(abs(x) in active for x in arg)
            clauses.append(arg)
        states.append(frozenset(active))
    assert not active
    return states,clauses

def simple_sat(cs,n):
    return any(all(any(bool((a>>(abs(z)-1))&1)==(z>0) for z in c) for c in cs) for a in range(1<<n))

def dp(e,b,states=None,kind='union'):
    L=len(e);d=max(1,b//2);D=[None]*(L+1);D[0]=0;pred=[-1]*(L+1)
    width=0
    for j in range(1,L+1):
        if e[j-1][0]=='O':width+=1
        elif e[j-1][0]=='X':width-=1
        if kind=='sweep':
            u=width;closed=set()
            for i in range(j-1,max(-1,j-b-1),-1):
                typ,arg=e[i]
                if typ=='X':u+=1;closed.add(arg)
                elif typ=='O' and arg in closed:u-=1;closed.remove(arg)
                if j<L and j-i<d:continue
                if D[i] is None:continue
                v=D[i]+(1<<u)
                if D[j] is None or v<D[j]:D[j]=v;pred[j]=i
        else:
            for i in range(max(0,j-b),j):
                if j<L and j-i<d:continue
                if D[i] is None:continue
                exponent=len(states[i]|states[j]) if kind=='union' else len(states[i])+len(states[j])
                v=D[i]+(1<<exponent)
                if D[j] is None or v<=D[j]:D[j]=v;pred[j]=i
    assert D[L] is not None
    path=[L]
    while path[-1]:path.append(pred[path[-1]])
    return D[L],tuple(reversed(path))

def path_union(states,path):
    return sum(1<<len(states[i]|states[j]) for i,j in zip(path,path[1:]))

checks=0;best_ratio=1.0
for k in range(8):
    for sat in (False,True):
        e=build(k,sat);ss,cs=trace(e)
        assert simple_sat(cs,k+3)==sat;checks+=1
        for b in (2,3,5,7,11,min(len(e),20)):
            exact,p=dp(e,b,ss,'union');fast,q=dp(e,b,None,'sweep')
            proxy,r=dp(e,b,ss,'product')
            assert exact==fast and p==q;checks+=1
            actual=path_union(ss,r)
            assert exact<=actual<=exact*(1<<max(map(len,ss)));checks+=1
            best_ratio=max(best_ratio,actual/exact)
print(json.dumps({'run':'IDENTITY-SWEEP129-COMPACT','status':'PASS','checks':checks,
 'max_observed_product_path_ratio':round(best_ratio,5),
 'scope':'valid named event streams, exact schedule objective; ARC-EDGE-90 OPEN'}))
