#!/usr/bin/env python3
"""Exact-rational FLMV 2005 Theorem 5.7 exponent envelope.
This tests arithmetic; it neither runs a SAT decider nor establishes P != NP.
"""
from fractions import Fraction
from decimal import Decimal, getcontext, ROUND_FLOOR
import json
from pathlib import Path
getcontext().prec = 100
PHI = (Decimal(1)+Decimal(5).sqrt())/2

def f_value(c,k):
    if c==1: return Fraction(1,k+1)
    return (c-1)/(1-(2-c)/c**k)

def d_value(c,k):
    f=f_value(c,k)
    return min((1/f-c)/k,1/c**k)

def optimize(c):
    assert isinstance(c,Fraction) and 1<c<2 and 1+c-c*c>0
    best=Fraction(0); arg=None; k=1
    while True:
        d=d_value(c,k)
        if d>best: best,arg=d,k
        # Valid global upper bound on EVERY unexamined level.
        if best>0 and (1/(c-1)-c)/(k+1)<best:
            return best,arg,k
        k+=1
        assert k<2000

def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)

def record(c):
    D=1+c-c*c; E=2-c
    best,k,K=optimize(c)
    positives=[j for j in range(1,K+1) if d_value(c,j)>0]
    assert positives
    kpos=min(positives)
    assert all(d_value(c,j)<=0 for j in range(1,kpos))
    assert D>E/c**kpos and (kpos==1 or D<=E/c**(kpos-1))
    assert all(d_value(c,j)<=best for j in range(1,K+1))
    assert (1/(c-1)-c)/(K+1)<best
    delta=PHI-dec(c)
    prediction=(Decimal(5).sqrt()*PHI.ln()/(PHI-1)) * delta/(1/delta).ln()
    return {"c":str(dec(c)), "first_positive_k":kpos,
            "optimal_k":k,"checked_k_through":K,
            "optimal_d":str(dec(best)),
            "phi_edge_predicted_d":str(prediction),
            "actual_over_prediction":str(dec(best)/prediction),
            "N_exponents":{f"1e{e}":str(dec(best)*e) for e in (6,12,24,60)}}

results=[]
for num,den in [(6,5),(7,5),(3,2),(31,20),(8,5),
                (161,100),(323,200),(1617,1000),(809,500),(161803,100000)]:
    results.append(record(Fraction(num,den)))
for j in (4,6,8,10,12):
    c=(PHI-Decimal(10)**(-j)).quantize(Decimal("1e-35"),rounding=ROUND_FLOOR)
    results.append(record(Fraction(str(c))))
checks=0
for r in results:
    c=Fraction(r["c"]); f=Fraction(1)
    for j in range(int(r["checked_k_through"])+1):
        assert f==f_value(c,j)
        if j>=1:
            assert d_value(c,j)==min((1/f-c)/j,1/c**j)
        f=c*f/(1+f); checks+=1
data={"status":"COMPUTATIONAL; arithmetic only, no SAT solver",
      "paper":"FLMV JACM 2005, Theorem 5.7 and Eq. (14)",
      "recurrence_checks":checks,"cases":results,"random_seed":None}
p=Path(__file__).resolve().parents[2]/"results/raw/arc/2026-11-09_1818_LSPV1_550_FLMV_PHI_RAW.json"
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(data,indent=2)+"\n")
print("cases:",len(results),"recurrence checks:",checks)
for r in results:
    print(r["c"],r["first_positive_k"],r["optimal_k"],r["optimal_d"])
print("raw:",p)
