#!/usr/bin/env python3
"""LSPV-4/394, signed PHP acquisition controls, standard library only.
This is a finite verifier, NOT a SAT lower bound or a proof of P!=NP.
"""
import itertools, json

def php(h):
    v=lambda i,j:(i-1)*h+j
    clauses=[]; meta=[]
    for i in range(1,h+2):
        clauses.append([v(i,j) for j in range(1,h+1)])
        meta.append(('pigeon',i,0,0))
    for j in range(1,h+1):
        for i in range(1,h+2):
            for k in range(i+1,h+2):
                clauses.append([-v(i,j),-v(k,j)])
                meta.append(('collision',i,k,j))
    return clauses,meta

def sat(f,a):
    return all(any(a[abs(z)]==(z>0) for z in clause) for clause in f)

def witness(h,record):
    kind,i,k,j=record
    a=[False]*(h*(h+1)+1)
    v=lambda i,j:(i-1)*h+j
    if kind=='pigeon':
        for p,hole in zip((q for q in range(1,h+2) if q!=i),range(1,h+1)):
            a[v(p,hole)]=True
    else:
        a[v(i,j)]=a[v(k,j)]=True
        for p,hole in zip((q for q in range(1,h+2) if q not in (i,k)),
                          (q for q in range(1,h+1) if q!=j)):
            a[v(p,hole)]=True
    return a

def brute(f,n):
    for mask in range(1<<n):
        a=[False]+[bool((mask>>i)&1) for i in range(n)]
        if sat(f,a): return True
    return False

def valid(f,n):
    return type(f)==list and bool(f) and type(n)==int and n>0 and all(
        type(c)==list and bool(c) and all(type(z)==int and 1<=abs(z)<=n for z in c) for c in f)

def run():
    count=0; cases=[]
    for h in range(1,9):
        f,meta=php(h)
        L=sum(map(len,f))
        assert L==h*(h+1)**2
        assert len(f)==(h+1)+h*(h*(h+1)//2)
        count+=2
        if h<=3:
            assert not brute(f,h*(h+1));count+=1
        checked=0
        for ci,c in enumerate(f):
            for slot,z in enumerate(c):
                mutated=[list(t) for t in f]
                mutated[ci][slot]=-z
                a=witness(h,meta[ci])
                assert sat(mutated,a)
                assert not sat(f,a)
                count+=2
                if h<=3:
                    assert brute(mutated,h*(h+1));count+=1
                checked+=1
        assert checked==L
        cases.append({'h':h,'sign_flips':checked,'variables':h*(h+1),'clauses':len(f)})
    bad=[None,[],[[0]],[[1],[]],[[True]],[['1']],[[3]],[[1,0]],[[1,-4]]]
    for x in bad:
        assert not valid(x,2);count+=1
    for x in [[[1]],[[-1]],[[1],[-1]],[[1,2],[-2]],[[1,-1]]]:
        assert valid(x,2);count+=1
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    def k4_models(charges):
        out=0
        for mask in range(64):
            p=[0]*4
            for i,(u,v) in enumerate(edges):
                p[u]^=(mask>>i)&1
                p[v]^=(mask>>i)&1
            out+=p==charges
        return out
    assert k4_models([1,0,0,0])==0;count+=1
    assert k4_models([0,0,0,0])==8;count+=1
    print(json.dumps({'schema':'LSPV4-394-compact','checks':count,'cases':cases,
                      'malformed_rejected':len(bad),'k4_models':{'odd':0,'even':8},
                      'status':'COMPUTATIONAL; proof status in linked report'},indent=2))
if __name__=='__main__':run()
