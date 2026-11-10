#!/usr/bin/env python3
"""FLMV (2005), Theorem 5.7 k-level deterministic time-space tradeoff; exact rational verification.
This does not construct a SAT algorithm or execute any SAT/proof system.
"""
from fractions import Fraction as Q
from decimal import Decimal, getcontext
import json
getcontext().prec = 60

def f(c, k):
    a = Q(1)
    for j in range(k):
        a = c*a/(1+a)
    return a

def d(c, k):
    return min((1/f(c,k)-c)/k, 1/(c**k))

def optimize(c):
    assert Q(1)<c<Q(13,8)
    best=Q(0); winner=0; k=0; H=1/(c-1)-c
    assert H>0
    while True:
        k+=1
        value=d(c,k)
        if value>best:
            best,winner=value,k
        if k>=2 and H/(k+1)<best:
            return dict(c=str(c), best_k=winner, d=str(best),
                        d_decimal=str(Decimal(best.numerator)/Decimal(best.denominator)),
                        k_certified_through=k, beyond_k_bound=str(H/(k+1)),
                        beta2=str(d(c,2)))
        assert k<10000

def main():
    cases=[(Q(6,5),2),(Q(7,5),3),(Q(3,2),4),
           (Q(31,20),5),(Q(8,5),8)]
    rows=[]; checks=0
    for c,k0 in cases:
        row=optimize(c)
        assert row["best_k"]==k0; checks+=1
        for k in range(1,row["k_certified_through"]+1):
            assert f(c,k)==(c-1)/(1-(2-c)/(c**k)); checks+=1
            assert d(c,k)<=d(c,k0); checks+=1
        rows.append(row)
    c=Q(6,5)
    beta=( (c+2)/c**2-c)/2
    assert beta==Q(23,45); checks+=1
    ratios=[]
    for p in (6,12,24,60):
        assert (beta-Q(1,2))*p==Q(p,90); checks+=1
        ratios.append({"N":f"10^{p}", "log10_ratio":str(Q(p,90)),
                       "ratio":10**(p/90)})
    result={"classification":"Known published theorem; independently checked exact parameter optimization",
            "rows":rows,"checks":checks,"beta_6_5":"23/45",
            "space_exponent_half_ratio":ratios,
            "no_algorithm_constructed":True,"historical_R_mix341_checker_executed":False}
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
