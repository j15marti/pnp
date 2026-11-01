#!/usr/bin/env python3
"""ARC-TICKET-GATE-AMPLIFICATION304 compact reproducer.
Valid canonical F9 original; no general SAT/FLMV runtime claim.
Full independently tested producer and no-import verifier are in the
same-run reproducibility archive; this compact reproducer is self-contained.
"""
from collections import Counter
from itertools import combinations, product
from math import comb
import json

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P={5:0,6:1,7:0,8:0,9:1}
Q={**P,3:1}
U={8:0,3:0,7:0,6:0,1:1,5:1}
S={**U,1:0}

def grammar(F):
    if not F or any(len(c)!=3 for c in F):return False
    n=max(abs(l) for c in F for l in c)
    ct=Counter(l for c in F for l in c)
    return (3*len(F)==4*n and n%3==0 and
        len({tuple(sorted(c)) for c in F})==len(F) and
        all(len(set(map(abs,c)))==3 and (all(l>0 for l in c)
            or all(l<0 for l in c)) for c in F) and
        all(ct[v]==ct[-v]==2 for v in range(1,n+1)))

def models(p):
    free=[v for v in range(1,10) if v not in p]
    for bs in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bs))}
        if all(any(a[abs(l)]==int(l>0) for l in c) for c in F):
            yield tuple(a[v] for v in range(1,10))

def signed_ticket(p):
    covered=[];uncovered={}
    for j,c in enumerate(F):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
            covered.append(j)
        else:uncovered[j]=tuple(l for l in c if abs(l) not in p)
    assert all(uncovered.values())
    free=[v for v in range(1,10) if v not in p]
    sc=Counter((abs(l),int(l>0)) for j in covered for l in F[j] if abs(l) in free)
    eta=sum(min(sc[v,0],sc[v,1]) for v in free)
    weights=[abs(sc[v,1]-sc[v,0]) for v in free if sc[v,1]!=sc[v,0]]
    edges=[(j,tuple(sorted(map(abs,c)))) for j,c in uncovered.items() if len(c)==2]
    triangles=set()
    for es in combinations(edges,3):
        deg=Counter(v for _,uv in es for v in uv)
        if len(deg)==3 and all(d==2 for d in deg.values()):
            triangles.add(tuple(sorted(j for j,_ in es)))
    used=set();cycles=[]
    for cyc in sorted(triangles):
        if not used.intersection(cyc):
            cycles.append(cyc);used.update(cyc)
    f=len(free);u=len(uncovered);e=2*f-u;d=e-eta-len(cycles)
    if d<0:return dict(delta=d, tickets=0)
    coeff=[1]+[0]*d
    def multiply(v):
        nonlocal coeff
        nxt=[0]*(d+1)
        for i,a in enumerate(coeff):
            for j,b in enumerate(v):
                if i+j<=d:nxt[i+j]+=a*b
        coeff=nxt
    for cyc in cycles:
        v=[comb(len(cyc),k+1) if k%2==0 and k<len(cyc) else 0
           for k in range(d+1)]
        multiply(v)
    for j,c in uncovered.items():
        if j not in used:
            multiply({1:[1],2:[1,1],3:[1,3,1]}[len(c)])
    for w in weights:
        v=[1]+[0]*d
        if w<=d:v[w]+=1
        multiply(v)
    return dict(f=f,u=u,e=e,eta=eta,nu=len(cycles),delta=d,
        cycles=cycles,uncovered=sorted(uncovered),weights=weights,
        coefficients=coeff,tickets=coeff[d])

def main():
    assert grammar(F)
    mP=set(models(P));mQ=set(models(Q))
    assert len(mP)==len(mQ)==3 and mP==mQ
    assert len(list(models({})))==70
    assert len(list(models(U)))==0 and len(list(models(S)))==2
    gP=signed_ticket(P);gQ=signed_ticket(Q)
    assert (gP["f"],gP["u"],gP["e"],gP["eta"],gP["nu"],gP["delta"],gP["tickets"])==(4,5,3,2,1,0,3)
    assert (gQ["f"],gQ["u"],gQ["e"],gQ["eta"],gQ["nu"],gQ["delta"],gQ["tickets"])==(3,3,3,2,0,1,5)
    products=[]
    for t in range(1,9):
        before=3**t;one=5*t*3**(t-1);after=comb(5*t,t)
        assert after>=5**t
        products.append(dict(t=t,source_models=3**t,parent_tickets=before,
                             one_forced_pin_tickets=one,all_forced_tickets=after))
    out=dict(status="PASS",label="COMPUTATIONAL",
        theorem="restricted source-entailing forced-pin ticket amplification",
        source="canonical F9",parent=gP,child=gQ,
        source_models_P_Q=3,source_models_F9=70,
        same_source_UNSAT_SAT_models=[0,2],
        product=products,guest_calls=0,canonical_child_outputs=0,
        native_FLMV_tape_time_space="UNMEASURED",P_vs_NP="OPEN")
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=="__main__":main()
