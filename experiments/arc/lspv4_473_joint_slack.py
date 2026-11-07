#!/usr/bin/env python3
"""LSPV-4/473 independent exact-arithmetic verifier: conditional FLMV resource-envelope budgets.
This is algebraic verification, NOT an actual SAT solver or an FLMV native-machine simulator.
"""
import json, random, math
from fractions import Fraction as F
from decimal import Decimal, localcontext

def beta(c):
    return ((c+2)/(c*c)-c)/2

def tmap(t, theta):
    return max(F(11,10), F(3,5)+(t+theta)/2)

def smap(s, omega):
    return max(F(1,2), (s+omega)/2)

def equilibria(theta,omega):
    return F(6,5)+theta, max(F(1,2), omega)

def bprime_abs(c):
    return (1+1/(c*c)+4/(c*c*c))/2

def verify():
    rng=random.Random(473)
    counts={'map_bounds':0,'strict_entry':0,'fixed_point':0,'subcritical_boundary':0,
            'supercritical_boundary':0,'finite_overhead_controls':0}
    for j in range(4000):
        theta=F(rng.randrange(0,8),10000)
        omega=F(5000+rng.randrange(0,140),10000)
        t0=F(12,10)+F(rng.randrange(0,400),100)
        s0=F(1,2)+F(rng.randrange(0,500),100)
        tt,ss=equilibria(theta,omega)
        assert tmap(tt,theta)==tt
        assert smap(ss,omega)==ss
        counts['fixed_point']+=2
        margin=beta(tt)-ss
        Q=bprime_abs(tt)*max(F(0),t0-tt)+max(F(0),s0-ss)
        t,s=t0,s0
        for depth in range(28):
            assert t<=tt+max(F(0),t0-tt)*F(1,2)**depth
            assert s<=ss+max(F(0),s0-ss)*F(1,2)**depth
            counts['map_bounds']+=2
            if margin>0 and Q*F(1,2)**depth <margin:
                assert beta(t)>s
                counts['strict_entry']+=1
            t=tmap(t,theta)
            s=smap(s,omega)
        if margin>0: counts['subcritical_boundary']+=1
        else: counts['supercritical_boundary']+=1
    c_safe=F(241,200)
    b_safe=beta(c_safe)
    assert b_safe==F(11642479,23232400)
    assert beta(F(6,5))==F(23,45)
    assert b_safe>F(1,2)
    assert b_safe>F(501,1000)
    assert b_safe<F(502,1000)
    assert beta(F(603,500))<F(1,2)
    assert max(F(1,2),F(51,100))<beta(F(6,5))
    assert max(F(1,2),F(64,125))>beta(F(6,5))
    counts['finite_overhead_controls']+=8
    with localcontext() as ctx:
        ctx.prec=42
        lo=Decimal('1.2'); hi=Decimal('1.3')
        def bdec(x):return ((x+2)/(x*x)-x)/2
        for _ in range(210):
            mid=(lo+hi)/2
            if bdec(mid)>Decimal('0.5'): lo=mid
            else:hi=mid
        crit=(lo+hi)/2
    results={
       'status':'PROVED/RESTRICTED conditional exponent-envelope identity; FINITE arithmetic checks',
       'beta_6_5':'23/45','beta_241_200':'11642479/23232400',
       'critical_c_approx':str(crit),'critical_guest_time_overhead_approx':str(crit-Decimal('1.2')),
       'source':'FLMV Corollary 5.8 only; exact same-machine and full compiler OPEN',
       'joint_frontier':'max(1/2,omega)<beta(6/5+theta), theta>=0, omega>=0',
       'counts':counts,'seed':473,
       'controls':[
          {'theta':'1/200','omega':'501/1000','result':'strictly_inside','tstar':'241/200'},
          {'theta':'1/200','omega':'251/500','result':'outside','tstar':'241/200'},
          {'theta':'3/500','omega':'1/2','result':'outside','tstar':'603/500'}]}
    return results
if __name__=='__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
