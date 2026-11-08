#!/usr/bin/env python3
"""Exact-rational audit of joint FLMV contraction overheads; independent finite controls.
Not a native FLMV interpreter. Python 3 standard library only.
"""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
import json, random

HALF=Q(1,2); SIX_TENTHS=Q(3,5); RHO=Q(11,10)

def beta(c):
    assert c>0
    return ((c+2)/c**2-c)/2

def parms(delta):
    assert 0<=delta<HALF
    a=SIX_TENTHS+delta
    lam=HALF+delta
    rho=RHO+delta
    eta=HALF+delta
    c=max(rho,a/(1-lam))
    return a,lam,rho,eta,c

def gap(delta):
    return beta(parms(delta)[4])-parms(delta)[3]

def polynomial(delta):
    return 1000*delta**4+200*delta**3+510*delta**2-1765*delta+2

def recurrence(delta, t0, s0):
    a,lam,rho,eta,c=parms(delta)
    T,S=t0,s0
    D_t=max(Q(0),T-c)
    D_s=max(Q(0),S-eta)
    L=Q(433,216)
    A=L*D_t+D_s
    g=gap(delta)
    assert g>0
    j=0
    while lam**j*A>g/2:
        j+=1
        assert j<10000
    for step in range(j+1):
        assert T<=c+lam**step*D_t
        assert S<=eta+lam**step*D_s
        assert beta(T)-S >=g-lam**step*A
        if step<j:
            T=max(rho,a+lam*T)
            S=max(eta,lam*S)
    assert beta(T)-S>=g/2>0
    return j, float(beta(T)-S)

def tseitin_k4_controls():
    edges=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
    groups={v:[k for k,(a,b) in enumerate(edges) if a==v or b==v] for v in range(4)}
    sat=unsat=0; checks=0; models=[]
    for mask in range(16):
        clauses=[]
        for v in range(4):
            keys=groups[v]; b=(mask>>v)&1
            for a in range(8):
                bits=[(a>>i)&1 for i in range(3)]
                if bits[0]^bits[1]^bits[2] ==b:continue
                clauses.append(tuple((k+1)*(-1 if bit else 1) for k,bit in zip(keys,bits)))
        assert len(clauses)==16
        good=0
        for x in range(64):
            truth=all(any(((x>>(abs(lit)-1))&1)==(lit>0) for lit in clause) for clause in clauses)
            parity=all((sum((x>>k)&1 for k in keys)&1)==((mask>>v)&1) for v,keys in groups.items())
            assert truth==parity;checks+=1
            good+=truth
        assert good==(8 if mask.bit_count()%2==0 else 0)
        if good:sat+=1
        else:unsat+=1
        models.append(good)
        for v in range(4):
            assert len(groups[v])==3;checks+=1
    assert (sat,unsat)==(8,8)
    return {'SAT':sat,'UNSAT':unsat,'source_assignment_checks':checks,'models':models}

def main():
    tests=[Q(0),Q(1,10000),Q(1,1000),Q(1,900),Q(1,800),Q(1,100)]
    rows=[]; assert_count=0
    for d in tests:
        a,lam,rho,eta,c=parms(d)
        assert c==a/(1-lam)
        assert gap(d)==polynomial(d)/(20*(1-2*d)*(5*d+3)**2)
        assert_count+=2
        rows.append({'delta':str(d),'time_fixed':float(c),'space_fixed':float(eta),'gap':float(gap(d)),'admissible':gap(d)>0})
    assert gap(Q(1,900))>0
    assert gap(Q(1,800))<0
    assert_count+=2
    assert polynomial(Q(0))>0>polynomial(Q(1,100)); assert_count+=1
    with localcontext() as ctx:
        ctx.prec=65
        lo=Decimal(0); hi=Decimal('0.01')
        for _ in range(220):
            m=(lo+hi)/2
            p=1000*m**4+200*m**3+510*m**2-1765*m+2
            if p>0:lo=m
            else:hi=m
        critical=str((lo+hi)/2)
    rng=random.Random(482)
    configs=0; max_depth=0; minimum_gap=1.0
    for _ in range(1200):
        t0=Q(rng.randint(10,2000000),10)
        s0=Q(rng.randint(0,1500000),10)
        j,margin=recurrence(Q(1,1000),t0,s0)
        configs+=1;max_depth=max(max_depth,j);minimum_gap=min(minimum_gap,margin)
        assert_count+=3*(j+1)+2
    tiny=[(Q(1),Q(0)),(Q(1000000),Q(1000000)),(Q(6,5),HALF),(Q(1),Q(1000000))]
    for t0,s0 in tiny:
        j,margin=recurrence(Q(1,1000),t0,s0)
        configs+=1;max_depth=max(max_depth,j);minimum_gap=min(minimum_gap,margin)
        assert_count+=3*(j+1)+2
    data={'kind':'exact rational joint four-parameter exponent envelope','critical_delta':critical,'rows':rows,
          'random_seed':482,'configuration_checks':configs,'inequality_assertion_lower_count':assert_count,
          'max_depth':max_depth,'minimum_gap':minimum_gap,'source_controls':tseitin_k4_controls(),
          'status':'PROVED/RESTRICTED arithmetic, COMPUTATIONAL finite tests; no FLMV machine execution; P vs NP OPEN'}
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
