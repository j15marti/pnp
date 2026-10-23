#!/usr/bin/env python3
"""Standalone compact check of ADAPTIVE-TERNARY-COLLAPSE69, stdlib only."""
from collections import deque
from itertools import product
import json

def construct(q,b):
    z=lambda i:i+1
    p=lambda i:q+4+i
    y=lambda i:2*q+5+i
    u,v=q+2,q+3
    cs=[(z(0),u),(z(0),-u),(y(q),v),(y(q),-v),(-z(0),p(0))]
    cs += [(-p(i-1),p(i)) for i in range(1,q+1)]
    cs += [(-z(i-1),z(i) if b[i-1] else -z(i)) for i in range(1,q+1)]
    for i in range(q+1):
        a,c,d=z(i),y(i),p(i)
        cs.extend(((a,c,-d),(a,-c,d),(-a,c,d),(-a,-c,-d)))
    return 3*q+5,tuple(cs)

def scc_2sat(n,cs):
    assert all(0<len(c)<=2 for c in cs)
    g=[[] for _ in range(2*n)]
    gr=[[] for _ in range(2*n)]
    idx=lambda l:2*(abs(l)-1)+(l>0)
    for c in cs:
        links=[(-c[0],c[0])] if len(c)==1 else [(-c[0],c[1]),(-c[1],c[0])]
        for a,b in links:
            x,y=idx(a),idx(b)
            g[x].append(y);gr[y].append(x)
    seen=[False]*(2*n);order=[]
    for i in range(2*n):
        if seen[i]:continue
        seen[i]=True;stack=[(i,0)]
        while stack:
            v,k=stack[-1]
            if k<len(g[v]):
                w=g[v][k];stack[-1]=(v,k+1)
                if not seen[w]:seen[w]=True;stack.append((w,0))
            else:order.append(v);stack.pop()
    comp=[-1]*(2*n);number=0
    for i in reversed(order):
        if comp[i]>=0:continue
        comp[i]=number;stack=[i]
        while stack:
            v=stack.pop()
            for w in gr[v]:
                if comp[w]<0:comp[w]=number;stack.append(w)
        number+=1
    return all(comp[2*i]!=comp[2*i+1] for i in range(n))

def adaptive(n,cs):
    bs=[c for c in cs if len(c)==2]
    lookup={tuple(sorted(c)) for c in bs}
    q=deque()
    for a,b in bs:
        if tuple(sorted((a,-b))) in lookup:q.append(a)
        if tuple(sorted((-a,b))) in lookup:q.append(b)
    links={}
    for a,b in bs:
        links.setdefault(-a,[]).append(b)
        links.setdefault(-b,[]).append(a)
    forced={}
    while q:
        a=q.popleft()
        if abs(a) in forced:
            if forced[abs(a)]!=(a>0):return False,0,"binary-conflict"
            continue
        forced[abs(a)]=(a>0)
        q.extend(links.get(a,()))
    reduced=[]
    for c in cs:
        if any(forced[abs(l)]==(l>0) for l in c if abs(l) in forced):continue
        rem=tuple(l for l in c if abs(l) not in forced)
        if not rem:return False,0,"simplification-conflict"
        reduced.append(rem)
    assert all(len(c)<=2 for c in reduced)
    return scc_2sat(n,reduced),len(reduced),"SCC"

def satisfies(cs,assignment):
    return all(any(assignment[abs(l)]==(l>0) for l in c) for c in cs)

def run():
    checks=0;rows=[]
    for q in range(1,4):
        for b in product((0,1),repeat=q):
            n,f=construct(q,b)
            assert n==3*q+5 and len(f)==6*q+9;checks+=1
            assert scc_2sat(n,[c for c in f if len(c)==2]);checks+=1
            sat,remaining,stage=adaptive(n,f)
            assert sat==(0 in b);checks+=1
            count=sum(satisfies(f,(False,)+assignment)
                      for assignment in product((False,True),repeat=n))
            assert (count>0)==sat;checks+=1
            rows.append(dict(q=q,b=''.join(map(str,b)),SAT=sat,
                             models=count,stage=stage,residual=remaining))
    for q in (32,128,512):
        for b in ((1,)*q,(0,)+(1,)*(q-1)):
            n,f=construct(q,b)
            sat,remaining,stage=adaptive(n,f)
            assert sat==(0 in b);checks+=1
            assert scc_2sat(n,[c for c in f if len(c)==2]);checks+=1
            rows.append(dict(q=q,SAT=sat,stage=stage,residual=remaining))
    return dict(checks=checks,failures=0,status="COMPUTATIONAL",records=rows)

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
