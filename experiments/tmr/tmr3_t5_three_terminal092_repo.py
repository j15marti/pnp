#!/usr/bin/env python3
"""TMR-3/092 independent compact 3-terminal counter for 3-connected T5 family."""
from itertools import product

def relation(a,b):
    return (b-a) % 5 in (1,3)

def build(k,p):
    edges=set(); next_v=3
    for _ in range(k):
        L=range(next_v,next_v+p-3);next_v+=p-3
        R=range(next_v,next_v+p);next_v+=p
        edges.update((u,v) for u in list(range(3))+list(L) for v in R)
    return next_v,edges

def recognize(n,E):
    if len(E)!=len(set(E)) or any(u==v or u<0 or v<0 or u>=n or v>=n for u,v in E):return None
    in_d=[0]*n;out_d=[0]*n; adj=[set() for _ in range(n)]
    for u,v in E:
        in_d[v]+=1;out_d[u]+=1;adj[u].add(v);adj[v].add(u)
    top=max(out_d,default=0)
    S={u for u in range(n) if out_d[u]==top and in_d[u]==0}
    if len(S)!=3 or top<8:return None
    seen=set(S); blocks=[]
    for v in range(n):
        if v in seen:continue
        q=[v];seen.add(v);C={v}
        for u in q:
            for w in adj[u]-S-seen:
                q.append(w);C.add(w);seen.add(w)
        blocks.append(C)
    if len(blocks)<2:return None
    expected=set(); p0=None
    for C in blocks:
        L={v for v in C if in_d[v]==0}
        R={v for v in C if out_d[v]==0}
        p=len(R)
        if L|R!=C or L&R or p<4 or len(L)!=p-3 or (p0 is not None and p!=p0):return None
        p0=p
        expected.update((u,v) for u in L|S for v in R)
    return (len(blocks),p0) if expected==set(E) else None

def count_formula(k,p):
    a=2**p+2**(p-2)-2
    b=2**(p-3)
    return 5*(a**k+6*b**k)

def count_independent(k,p):
    table=[]
    for d,e in product(range(5),repeat=2):
        q=0
        for rest in product(range(5),repeat=p-3):
            s=sum(all(relation(x,z) for x in (0,d,e)+rest) for z in range(5))
            q+=s**p
        table.append(q)
    return 5*sum(x**k for x in table)

def self_test():
    checks=0
    for k,p in ((2,4),(3,4),(2,5),(3,5)):
        n,E=build(k,p)
        assert recognize(n,E)==(k,p)
        assert count_formula(k,p)==count_independent(k,p)
        checks+=2
        assert recognize(n,E-{next(iter(E))}) is None
        checks+=1
    n,E=build(20,8)
    assert recognize(n,E)==(20,8)
    assert count_formula(20,8)==559129496820275798186261882797788214499516649308160
    checks+=2
    return checks

if __name__=='__main__':
    print({'checks':self_test(),'failures':0,'model':'T5/3-terminal exact count',
           'status':'COMPUTATIONAL upper bound; P vs NP OPEN'})
