#!/usr/bin/env python3
"""Exact finite audit of M22-SINGLE-EXPOSURE-ERASURE108; stdlib only.
Semantic checks and logical accesses, NOT FLMV bit-machine measurement.
"""
from itertools import combinations, product
import json

def src(H,X,Y):
    P={tuple(sorted(s)) for s in H|X}
    Q={tuple(sorted(s)) for s in H|Y}
    V=set().union(*(P|Q)); H=P&Q; X=P-H;Y=Q-H
    D=set().union(*(X|Y)) if X else set()
    Z=V-D
    assert len(P)==len(Q)==2*len(V)//3
    assert all(len(s)==3 for s in P|Q)
    assert all(sum(v in s for s in P)==sum(v in s for s in Q)==2 for v in V)
    assert set().union(*X)==set().union(*Y) if X else not Y
    return P,Q,H,X,Y,D,Z

def lift(H,D,Z,a):
    clauses=[]
    for h in sorted(H):
        d=next(iter(set(h)&D)); z=sorted(set(h)&Z)
        assert len(z)==2
        clauses.append((d,z))
    owner={}
    def aug(i,seen):
        for z in clauses[i][1]:
            if z in seen:continue
            seen.add(z)
            if z not in owner or aug(owner[z],seen):
                owner[z]=i;return True
        return False
    assert all(aug(i,set()) for i in range(len(clauses)))
    out={**a,**{z:0 for z in Z}}
    for z,i in owner.items():out[z]=1-a[clauses[i][0]]
    assert all(len({out[v] for v in h})==2 for h in H)
    return out

def sat(P,Q,a):
    return all(any(a[v] for v in s) for s in P) and all(any(not a[v] for v in s) for s in Q)

def paired_core(H,D,Z):
    ret=set()
    for dv in product((0,1),repeat=len(D)):
        a=dict(zip(sorted(D),dv))
        if any(all(len({({**a,**dict(zip(sorted(Z),zv))})[v] for v in h})==2 for h in H)
               for zv in product((0,1),repeat=len(Z))):ret.add(dv)
    return ret

def run():
    H={(0,6,7),(1,7,8),(2,6,8)}
    X={(0,3,4),(1,4,5),(2,3,5)}
    Y={(0,3,5),(1,3,4),(2,4,5)}
    P,Q,H,X,Y,D,Z=src(H,X,Y)
    assert len(D)==6 and len(Z)==3 and all(len(set(h)&D)==1 for h in H)
    assert any(sum(v in h for h in H)==0 for v in D)
    nvalid=0
    for dv in product((0,1),repeat=len(D)):
        a=dict(zip(sorted(D),dv))
        b=lift(H,D,Z,a)
        assert all(len({b[v] for v in h})==2 for h in H)
        if sat(X,Y,a):nvalid+=1;assert sat(P,Q,b)
    models=sum(sat(P,Q,dict(zip(range(9),v))) for v in product((0,1),repeat=9))
    assert nvalid==26 and models==86
    H2={(0,1,5),(2,3,5)};X2={(0,1,4),(2,3,4)};Y2={(0,2,4),(1,3,4)}
    P2,Q2,H2,X2,Y2,D2,Z2=src(H2,X2,Y2)
    forbidden=[]
    for dv in product((0,1),repeat=len(D2)):
        a=dict(zip(sorted(D2),dv))
        if not any(all(len({({**a,**dict(zip(sorted(Z2),zv))})[v] for v in h})==2 for h in H2)
                   for zv in product((0,1),repeat=len(Z2))):forbidden.append(''.join(map(str,dv)))
    assert forbidden==['00110','00111','11000','11001']
    triple=list(combinations(range(6),3))
    B=[set(f) for f in combinations(triple,4) if all(sum(v in s for s in f)==2 for v in range(6))]
    assert len(B)==75
    guard=nonempty=nonfull=0
    for A in B:
        for N in B:
            h=A&N;d=set().union(*(A^N)) if A!=N else set()
            if all(len(set(s)&d)==1 for s in h):
                guard+=1
                if h:nonempty+=1
            if h and all(len(set(s)&d)>=1 for s in h):
                z=set(range(6))-d
                feasible=0
                for dv in product((0,1),repeat=len(d)):
                    a=dict(zip(sorted(d),dv))
                    feasible+=any(all(len({({**a,**dict(zip(sorted(z),zv))})[v] for v in s})==2 for s in h)
                                  for zv in product((0,1),repeat=len(z)))
                if feasible<2**len(d):nonfull+=1
    assert (guard,nonempty,nonfull)==(2610,0,2940)
    ans={'k9_models':models,'k9_unmatched_models':nvalid,'k9_paired_boundary':64,
         'k6_e2_forbidden':forbidden,'all_k6_formulas':5625,'k6_exposure1_guard':guard,
         'k6_nonempty_exposure1_guard':nonempty,'k6_nonfull_e2_core':nonfull,'assertion_failures':0}
    print(json.dumps(ans,indent=2,sort_keys=True))
if __name__=='__main__':run()
