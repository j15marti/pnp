#!/usr/bin/env python3
"""SIGNED_NAE_TOKEN62 standalone stdlib reproducer.
Checks strict 2+/2- source grammar, mixed signed NAE pairs, and flip traces.
No unrestricted P vs NP claim.
"""
import collections, json, random, sys

def prism(h, frustration=True):
    assert h>=3
    edges={}
    for layer in range(2):
        for i in range(h):
            u=layer*h+i
            v=layer*h+(i+1)%h
            edges[tuple(sorted((u,v)))]=len(edges)+1
    for i in range(h):edges[(i,i+h)]=len(edges)+1
    incident=[[] for _ in range(2*h)]
    for (u,v),e in edges.items():
        incident[u].append(e);incident[v].append(e)
    clauses=[]
    for v,es in enumerate(incident):
        # Nonmonotone NAE: cycle edges positive, rung edges negative.
        c=tuple(-e if e>2*h or (frustration and v==0 and e==1) else e for e in es)
        clauses.extend((c,tuple(-e for e in c)))
    return clauses,3*h

def gram(C,n):
    counts=collections.Counter(l for c in C for l in c)
    assert len(C)*3==4*n
    assert len(set(tuple(sorted(c)) for c in C))==len(C)
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in C)
    assert all(counts[i]==counts[-i]==2 for i in range(1,n+1))

def pairs(C):
    index={tuple(sorted(c)):i for i,c in enumerate(C)}
    found=[];used=set()
    for i,c in enumerate(C):
        if i in used:continue
        j=index.get(tuple(sorted(-l for l in c)))
        if j is not None and j not in used:
            used.add(i);used.add(j);found.append(c)
    return found,[i for i in range(len(C)) if i not in used]

def bad(c,a):
    z=[bool(a[abs(l)])^(l<0) for l in c]
    return z[0]==z[1]==z[2]

def repair(supports,n,start):
    seen=[[] for _ in range(n+1)]
    for j,c in enumerate(supports):
        for lit in c:seen[abs(lit)].append(j)
    assert all(len(z)<=2 for z in seen)
    a=start[:]; b=[bad(c,a) for c in supports]; log=[];rounds=0
    while True:
        roots=[j for j,v in enumerate(b) if v]
        if not roots:break
        rounds+=1
        j=roots[0];incoming=0;walk=set()
        while True:
            assert j not in walk and b[j]
            walk.add(j)
            v=next(abs(l) for l in supports[j] if abs(l)!=incoming)
            k=next((z for z in seen[v] if z!=j),-1)
            a[v]=not a[v]
            b[j]=bad(supports[j],a)
            assert not b[j]
            if k>=0:b[k]=bad(supports[k],a)
            log.append((j,v,k))
            if k<0 or not b[k]:break
            incoming,j=v,k
            assert len(walk)<len(supports)
    assert len(log)<=len(supports)**2
    assert not any(b)
    return a,log,rounds

def replay(supports,start,log):
    a=start[:]
    for j,v,k in log:
        assert bad(supports[j],a)
        assert any(abs(l)==v for l in supports[j])
        a[v]=not a[v]
        assert not bad(supports[j],a)
        if k>=0:assert any(abs(l)==v for l in supports[k])
    assert not any(bad(c,a) for c in supports)
    return a

def run(h):
    C,n=prism(h);gram(C,n)
    supp,defects=pairs(C)
    assert not defects and len(supp)*2==len(C)
    rand=random.Random(202610231037+h)
    initial=[False]+[bool(rand.getrandbits(1)) for _ in range(n)]
    witness,log,rounds=repair(supp,n,initial)
    assert replay(supp,initial,log)==witness
    assert all(any(witness[abs(l)]==(l>0) for l in c) for c in C)
    return dict(h=h,n=n,m=len(C),complement_defects=len(defects),
                monotone_defects=len(C),flips=len(log),rounds=rounds,source_sat=True)

if __name__=="__main__":
    sizes=[int(x) for x in sys.argv[1:]] or [3,4,8,16,32,96]
    print(json.dumps([run(x) for x in sizes],indent=2))
