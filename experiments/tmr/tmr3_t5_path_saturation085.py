#!/usr/bin/env python3
"""TMR-3/085: exact path-saturation decision control for fixed T5 CSP.
No external dependencies. Intended as a source-validation reference.
"""
from itertools import product
from random import Random
import json
D={1,3}

def kernel(length):
    out=[1,0,0,0,0]
    for _ in range(length):
        nxt=[0]*5
        for i,v in enumerate(out):
            for d in D: nxt[(i+d)%5]+=v
        out=nxt
    return tuple(out)

def torus(k):
    assert k>=3
    return k*k,[(i*k+j,i*k+(j+1)%k) for i in range(k) for j in range(k)]+[
        (i*k+j,((i+1)%k)*k+j) for i in range(k) for j in range(k)]

def subdivide4(n,arcs):
    full=[];paths=[]
    for u,v in arcs:
        a,b,c=n,n+1,n+2;n+=3
        p=(u,a,b,c,v)
        paths.append(p);full.extend(zip(p,p[1:]))
    return n,full,paths

def check(n,arcs,x):
    return len(x)==n and all((x[v]-x[u])%5 in D for u,v in arcs)

def decode(n,arcs):
    """Returns all paths only when this is a complete 4-subdivision
    whose core vertices have total degree >=3 and private degree is (1,1).
    """
    if not n or len(arcs)!=len(set(arcs)):return None
    incoming=[[] for _ in range(n)];outgoing=[[] for _ in range(n)]
    for u,v in arcs:
        if not 0<=u<n or not 0<=v<n:return None
        outgoing[u].append(v);incoming[v].append(u)
    core={i for i in range(n) if len(incoming[i])+len(outgoing[i])>=3}
    private=set(range(n))-core
    if not core or any(len(incoming[i])!=1 or len(outgoing[i])!=1
                       for i in private):return None
    used=set();seen=set();paths=[]
    for u in sorted(core):
        for w in outgoing[u]:
            p=[u,w]
            for _ in range(3):
                t=p[-1]
                if t not in private or t in seen:return None
                seen.add(t);p.append(outgoing[t][0])
            if p[-1] not in core:return None
            for a,b in zip(p,p[1:]):
                if (a,b) in used:return None
                used.add((a,b))
            paths.append(tuple(p))
    if seen!=private or used!=set(arcs):return None
    return paths

def witness(n,arcs):
    paths=decode(n,arcs)
    if paths is None:return None
    x=[0]*n
    for _,a,b,c,_ in paths:x[a],x[b],x[c]=1,4,2
    assert check(n,arcs,x)
    return x

def brute(n,arcs):
    for x in product(range(5),repeat=n):
        if check(n,arcs,x):return x
    return None

def run():
    asserts=0
    want=[(0,1,0,1,0),(0,1,1,0,2),(3,0,3,1,1),(4,4,1,6,1)]
    for L,row in enumerate(want,1):
        assert kernel(L)==row;asserts+=1
        for u in range(5):
            for v in range(5):
                direct=sum((u+sum(ds))%5==v for ds in product((1,3),repeat=L))
                assert direct==row[(v-u)%5];asserts+=1
    assert min(kernel(4))>0 and min(kernel(3))==0;asserts+=1
    for k in range(3,9):
        nv,base=torus(k);n,arcs,expected=subdivide4(nv,base)
        assert n==7*k*k and len(arcs)==8*k*k;asserts+=1
        assert set(decode(n,arcs) or [])==set(expected);asserts+=1
        assert check(n,arcs,witness(n,arcs));asserts+=1
    rng=Random(85085)
    for n in range(1,6):
        for _ in range(30):
            arcs=list({(rng.randrange(n),rng.randrange(n))
                       for __ in range(rng.randrange(2*n+1))})
            # Unrecognized sources must be sent to exact fallback.
            got=witness(n,arcs)
            if got is not None:assert brute(n,arcs) is not None
            asserts+=1
    return dict(checks=asserts,failures=0,kernel4=kernel(4),
                torus_k8=dict(n=448,m=512,cycle_rank=65))
if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True))
