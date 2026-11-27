"""C05-09: exact affine forbidden-event pivot elimination + basis-only Rado.
Run from extracted C05-08 archive: PYTHONPATH=prior python flat09.py > results09.json.
"""
from protected08 import *
import math

def canon(rows):
    B={}
    for v,c in rows:
        if not insert(v,c,B): return None # empty bad event
    # Full reduced echelon form, deterministic representation
    for p in sorted(B):
        v,c=B[p]
        for q in sorted(B):
            if q>p and B[q][0]>>p&1:
                w,d=B[q]; B[q]=(w^v,d^c)
    return tuple(B[p] for p in sorted(B))

def hit(F,x): return all(parity(v&x)==c for v,c in F)
def ok(G,x): return not any(hit(F,x) for F in G)

def pivot(G,p):
    H=set();T=[];D=[];mask=1<<p
    for F in G:
        q=next(((v,c) for v,c in F if v&mask),None)
        if q is None:H.add(F);continue
        v,c=q;tr=tuple((w^v,d^c) if w&mask else (w,d) for w,d in F if (w,d)!=q)
        T.append((tr,v^mask,c));D.append(F)
    for i,(A,u,c) in enumerate(T):
        for B,v,d in T[i+1:]:
            K=canon((*A,*B,(u^v,1^c^d)))
            if K is not None:H.add(K)
    return H,D,len(T)*(len(T)-1)//2

def peel(G):
    # Candidate forms are only equation basis rows, not all nonzero span elements.
    P=sorted(G); I={};probes=0
    while True:
        B={}
        for j,v in I.items():assert insert(v,1<<j,B)
        parent={j:None for j in range(len(P)) if j not in I};Q=deque(parent);end=None
        while Q and end is None:
            j=Q.popleft()
            for v,c in P[j]:
                probes+=1;w,co=reduce_vec(v,B)
                if w:end=(j,v);break
                while co:
                    bit=co&-co;co^=bit;k=bit.bit_length()-1
                    if k not in parent:parent[k]=(j,v);Q.append(k)
        if end is None:break
        j,v=end
        while True:
            I[j]=v
            if parent[j] is None:break
            j,v=parent[j]
    C={P[j] for j in parent};E=[];B=span(v for F in C for v,c in F)
    for j,v in sorted(I.items()):
        if j not in parent:
            assert reduce_vec(v,B)[0];insert(v,0,B)
            E.append((v,1^dict(P[j])[v]))
    assert len(C)+len(E)==len(P)
    return C,E,probes

