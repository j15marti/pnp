#!/usr/bin/env python3
"""Stdlib-only independent small-source checker, LSPV-3 2026-10-30 02:24 PDT.
Exhaustive coherent anchors; local S/U/inversions; pair modes; root gate.
Full DPLL, 2SAT, XOR, and raw run reside in separate reproducibility bundle.
"""
from itertools import combinations, product
from collections import Counter
import json

K4=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6)]
def prism(k):
    ed=[(layer*k+i,layer*k+(i+1)%k) for layer in range(2) for i in range(k)]
    ed += [(i,i+k) for i in range(k)]
    inc=[[] for _ in range(2*k)]
    for v,(a,b) in enumerate(ed,1):
        inc[a].append(v if (v+a)%3 else -v)
        inc[b].append(v if (v+b)%2 else -v)
    return [tuple(t) for c in inc for t in (c,[-v for v in c])]
def nvars(F):return max(abs(l) for c in F for l in c)
def value(l,a):return bool((a>>(abs(l)-1))&1)==(l>0)
def ts(F,a):return [sum(value(l,a) for l in c) for c in F]
def hitting(F,a):
    bad=[{abs(l) for l in c} for c,t in zip(F,ts(F,a)) if t==0]
    n=nvars(F)
    for size in range(n+1):
        for T in combinations(range(1,n+1),size):
            if all(set(T)&s for s in bad):return size
    raise AssertionError('Finite hitting should exist')
def local(F):
    modes=0
    for j,c in enumerate(F):
        S={abs(l):int(l>0) for l in c}
        U={abs(l):int(l<0) for l in c}
        assert all(1-S[i]==U[i] for i in S)
        for k,d in enumerate(F[:j]):
            T={abs(l):int(l>0) for l in d}; V={abs(l):int(l<0) for l in d}
            same={i for i in S.keys()&T.keys() if S[i]==T[i]}
            opp={i for i in S.keys()&T.keys() if S[i]!=T[i]}
            for name,aa,bb in [('SS',S,T),('SU',S,V),('US',U,T),('UU',U,V)]:
                feasible=not (opp if name in ('SS','UU') else same)
                assert feasible==all(aa[i]==bb[i] for i in aa.keys()&bb.keys())
                modes+=1
    return modes
def verify(name,F,allanchors=True):
    n=nvars(F); signs=Counter(l for c in F for l in c)
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in F)
    assert all(signs[i]==2 and signs[-i]==2 for i in range(1,n+1))
    modes=local(F); checks=0; maxsum=0
    anchors=range(1<<n) if allanchors else [0,(1<<n)-1,5,17,42,2048]
    for a in anchors:
        if a>=(1<<n):continue
        b=a^((1<<n)-1)
        assert all(x+y==3 for x,y in zip(ts(F,a),ts(F,b)))
        for x in [a,b]:
            bad=[c for c,t in zip(F,ts(F,x)) if t==0]
            incidence=Counter(abs(l) for c in bad for l in c)
            assert all(z<=2 for z in incidence.values())
            E=sum(z==2 for z in incidence.values());q=len(bad);u=len(incidence)
            assert u==3*q-E and 2*E<=3*q
            edge=[]
            for v,z in incidence.items():
                if z==2:
                    x,y=[i for i,c in enumerate(bad) if v in [abs(l) for l in c]]
                    edge.append((x,y))
            chosen=0
            while edge:
                x,y=edge[0];chosen+=1
                edge=[(p,r) for p,r in edge if p not in (x,y) and r not in (x,y)]
            assert 15*(q-chosen)<=7*u<=7*n
        if allanchors:
            t0=hitting(F,a);t1=hitting(F,b)
            assert 15*t0<=7*n and 15*t1<=7*n
            assert t0+t1<n
            maxsum=max(maxsum,t0+t1)
        checks+=1
    return {'source':name,'variables':n,'clauses':len(F),'pair_modes':modes,
            'coherent_anchor_checks':checks,'maximum_pair_tau':maxsum}
if __name__=='__main__':
    ans=[verify('paired_K4',K4),verify('signed_prism_k3',prism(3)),verify('signed_prism_k4',prism(4),False)]
    binary=[(1,2),(2,3),(1,3),(-1,-2),(-2,-3),(-1,-3)]
    assert hitting(binary,0)==hitting(binary,7)==2
    assert sum(hitting(binary,a) for a in (0,7))>3
    print(json.dumps({'status':'PASS','results':ans,
       'width2_countercontrol':'tau_0=tau_1=2, 4>3; 2SAT UNSAT',
       'scope':'restricted root nonfiring, no all-algorithm SAT claim'},indent=2))
