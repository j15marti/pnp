#!/usr/bin/env python3
"""Independent reproducible C_M22/P_pair/C_star and two-stage restriction checks.
Source lengths are a declared fixed-width encoding proxy, not FLMV measurements.
"""
from collections import Counter
from itertools import product
from math import ceil,log2
import json

def stats(F):
    assert all(len(c)==3 and len(set(map(abs,c)))==3 and
               (all(z>0 for z in c) or all(z<0 for z in c)) for c in F)
    assert len({tuple(sorted(c)) for c in F})==len(F)
    k=max(abs(z) for c in F for z in c)
    P=Counter(abs(z) for c in F for z in c if z>0)
    M=Counter(abs(z) for c in F for z in c if z<0)
    assert all(P[i]==M[i]==2 for i in range(1,k+1))
    assert 3*len(F)==4*k
    A={tuple(sorted(c)) for c in F if c[0]>0}
    B={tuple(sorted(-z for z in c)) for c in F if c[0]<0}
    assert len(A)==len(B)==len(F)//2
    a=A-B; b=B-A
    assert Counter(z for c in a for z in c)==Counter(z for c in b for z in c)
    q=len(a)
    assert q==len(b) and q!=1
    D={z for c in a for z in c}
    return k,len(F),q,D

def prism(h,swaps):
    assert h%4==0 and h>=8
    edges=[]
    for layer in range(2):
        for j in range(h):edges.append(tuple(sorted(((layer,j),(layer,(j+1)%h)))))
    for j in range(h):edges.append(tuple(sorted(((0,j),(1,j)))))
    labels={e:i+1 for i,e in enumerate(edges)}
    stars={v:sorted(i for e,i in labels.items() if v in e)
           for v in [(t,j) for t in range(2) for j in range(h)]}
    neg={v:c.copy() for v,c in stars.items()}
    for a,b in swaps:
        va,vb=(0,a),(0,b)
        ea=labels[tuple(sorted((va,(0,(a+1)%h))))]
        eb=labels[tuple(sorted((vb,(0,(b+1)%h))))]
        neg[va].remove(ea);neg[vb].remove(eb)
        neg[va].append(eb);neg[vb].append(ea)
    F=[tuple(c) for v,c in sorted(stars.items())]+[
      tuple(-i for i in sorted(c)) for v,c in sorted(neg.items())]
    witness={i:int(e[0][0]==e[1][0]) for e,i in labels.items()}
    assert all(any(witness[abs(z)]==int(z>0) for z in c) for c in F)
    return F,witness

def restriction(F,pins):
    return [tuple(z for z in c if abs(z) not in pins)
            for c in F if not any(abs(z) in pins and pins[abs(z)]==int(z>0) for z in c)]

def Nbits(F):
    k=max((abs(z) for c in F for z in c),default=0)
    w=ceil(log2(64*(k+len(F)+1)))
    return (2+len(F)+sum(map(len,F)))*w

def check():
    Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
       (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
    assert stats(Y)[:3]==(6,8,4)
    models=[''.join(map(str,x)) for x in product([0,1],repeat=6)
            if all(any(x[abs(z)-1]==int(z>0) for z in c) for c in Y)]
    assert len(models)==20 and '111000' in models
    rows=[]
    for h in (8,12,16,24,48,96):
        P,w=prism(h,[])
        assert stats(P)[:3]==(3*h,4*h,0)
        plans=[[(0,h//2)]]
        if h>=16:plans.append([(0,h//4),(h//2,3*h//4)])
        for swaps in plans:
            F,w=prism(h,swaps)
            k,m,q,D=stats(F)
            assert q==2*len(swaps) and len(D)==3*q
            split=sorted(D);mid=len(split)//2
            A=restriction(F,{v:w[v] for v in split[:mid]})
            B=restriction(A,{v:w[v] for v in split[mid:]})
            assert len(B)>=m-4*len(D)
            assert any(len(c)<3 for c in B)
            assert all(any(w[abs(z)]==int(z>0) for z in c) for c in B)
            rows.append({'h':h,'q':q,'k':k,'m':m,'N':Nbits(F),
                         'D':len(D),'L1':len(A),'L2':len(B),
                         'childN':Nbits(B),'ratio':round(Nbits(B)/Nbits(F),5)})
    return {'run':'M22-DEFECT-ADAPTER131','Y_models':len(models),
            'controls':len(rows),'status':'PASS; restricted cases only',
            'rows':rows}

if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
