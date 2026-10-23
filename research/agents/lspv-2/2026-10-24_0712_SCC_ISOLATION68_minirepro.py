#!/usr/bin/env python3
"""SCC_ISOLATION68 restricted proof-audit reproduction, stdlib only.
Run: python 2026-10-24_0712_SCC_ISOLATION68_minirepro.py
This checks finite controls; mathematical proof is in the .tex report.
"""
from collections import defaultdict, Counter
from itertools import product

def strict(F):
    assert F and all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    n=max(abs(x) for c in F for x in c)
    assert {abs(x) for c in F for x in c}==set(range(1,n+1))
    signs=Counter(l for c in F for l in c)
    assert all(signs[v]==signs[-v]==2 for v in range(1,n+1))
    assert 3*len(F)==4*n
    assert len(F)==len(set(tuple(sorted(c)) for c in F))
    return n

def cycle(q):
    assert q>=4 and q%2==0
    F=[]
    for i in range(q):
        y=q+i//2+1
        F.extend([(-(i+1), (i+1)%q+1, y),
                  (-(i+1), (i+1)%q+1, -y)])
    strict(F)
    return F

def core():
    F=[(1,2,4),(1,2,-4),(-1,3,5),(-1,3,-5),
       (-2,4,6),(-2,-4,-6),(-3,5,6),(-3,-5,-6)]
    strict(F)
    return F

def pairs(F):
    signatures=defaultdict(list)
    for i,c in enumerate(F):
        for j in range(3):
            base=tuple(sorted(v for k,v in enumerate(c) if k!=j))
            signatures[(base,abs(c[j]))].append((i,c[j]))
    proposals=[]
    for (base,v),rows in signatures.items():
        for i,li in rows:
            for j,lj in rows:
                if li==v and lj==-v:proposals.append((min(i,j),max(i,j),base))
    used=set();B=[]
    for i,j,base in sorted(set(proposals)):
        if i in used or j in used:continue
        used|={i,j};B.append(base)
    T=[c for i,c in enumerate(F) if i not in used]
    return B,T

def scc(B):
    V={v for c in B for v in c}|{-v for c in B for v in c}
    g={v:[] for v in V}
    for a,b in B:g[-a].append(b);g[-b].append(a)
    ids={};low={};stk=[];instk=set();clock=0;comps=[]
    def visit(u):
        nonlocal clock
        ids[u]=low[u]=clock;clock+=1;stk.append(u);instk.add(u)
        for v in g[u]:
            if v not in ids:visit(v);low[u]=min(low[u],low[v])
            elif v in instk:low[u]=min(low[u],ids[v])
        if low[u]==ids[u]:
            comp=[]
            while True:
                w=stk.pop();instk.remove(w);comp.append(w)
                if w==u:break
            comps.append(comp)
    for v in sorted(V):
        if v not in ids:visit(v)
    return comps

def projected(B,T):
    U={abs(x) for c in T for x in c}
    adjacent=defaultdict(list)
    for e,c in enumerate(B):
        for l in c:adjacent[abs(l)].append((e,l))
    assert all(len(z)<=2 for z in adjacent.values())
    assert all((v in U and len(z)==1) or (v not in U and len(z)==2)
               for v,z in adjacent.items())
    visited=set();P=[];cycles=0
    for start in sorted(U):
        if start not in adjacent:continue
        e,a=adjacent[start][0]
        if e in visited:continue
        visited.add(e)
        l=next(v for v in B[e] if abs(v)!=start);previous=e
        while abs(l) not in U:
            v=abs(l)
            e2=next(edge for edge,_ in adjacent[v] if edge!=previous)
            assert e2 not in visited
            opposite=next(z for z in B[e2] if abs(z)==v)
            assert opposite==-l
            visited.add(e2);previous=e2
            l=next(z for z in B[e2] if abs(z)!=v)
        assert abs(l)!=start
        P.append((a,l))
    for e in range(len(B)):
        if e in visited:continue
        cycles+=1;todo=[e]
        while todo:
            j=todo.pop()
            if j in visited:continue
            visited.add(j)
            for l in B[j]:
                assert abs(l) not in U
                todo.extend(i for i,_ in adjacent[abs(l)] if i not in visited)
    assert len(visited)==len(B)
    ends=[abs(l) for c in P for l in c]
    assert len(ends)==len(set(ends))
    return P,cycles

def sat(F,a):
    return all(any(a[abs(l)]==(l>0) for l in c) for c in F)

def check(F):
    n=strict(F)
    B,T=pairs(F)
    U={abs(x) for c in T for x in c}
    signed=Counter(l for c in B for l in c)
    assert all(signed[x]<=1 and signed[-x]<=1 for x in range(1,n+1))
    assert all(abs(l) not in U for group in scc(B)
               if len(group)>1 for l in group)
    P,cyc=projected(B,T)
    assert all(abs(l) in U for c in P for l in c)
    return n,len(B),len(T),len(P),cyc

def main():
    count=0
    for q in (4,8,16,32,64,128):
        n,b,t,p,c=check(cycle(q))
        assert n==3*q//2 and b==q and t==0 and p==0
        count+=1
    F=core()
    assert check(F)==(6,2,4,1,0)
    B,T=pairs(F);P,_=projected(B,T)
    assert {abs(l) for l in P[0]}=={2,3}
    U=sorted({abs(l) for c in T for l in c})
    Y=[x for x in range(1,7) if x not in U]
    for vals in product((False,True),repeat=len(U)):
        prescribed=dict(zip(U,vals))
        kernel=all(any(prescribed[abs(l)]==(l>0) for l in c) for c in T+P)
        extend=False
        for yy in product((False,True),repeat=len(Y)):
            a=[False]*7
            for v,z in prescribed.items():a[v]=z
            for v,z in zip(Y,yy):a[v]=z
            if sat(F,a):extend=True
        assert kernel==extend
        count+=1
    print("SCC_ISOLATION68 mini assertions:",count,
          "source-connected strict path and cycle controls: PASS")
if __name__=="__main__":main()
