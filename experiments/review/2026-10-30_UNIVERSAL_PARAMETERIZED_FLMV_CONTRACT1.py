#!/usr/bin/env python3
"""Exact-rational FLMV Theorem 5.7 envelope and conditional ARC recurrence.
No actual compiler or forbidden achievable SAT resource pair is constructed.
"""
from fractions import Fraction as Q
from functools import lru_cache
import json
from pathlib import Path

@lru_cache(None)
def frontier(c, kmax=1000):
    assert c > 1
    f=Q(1)
    best=(Q(0),0)
    details=[]
    for k in range(1,kmax+1):
        f=c*f/(1+f)
        d=min((1/f-c)/k, c**(-k))
        if d>best[0]: best=(d,k)
        if k in (1,2,3,4,5,6): details.append([k,str(d)])
        # For j>k, d_j <= c^-j <= c^-(k+1). Strict comparison certifies tail.
        if best[0]>0 and c**(-(k+1)) < best[0]:
            return {"c":str(c),"d_exact":str(best[0]),"d_float":float(best[0]),
                    "k_opt":best[1],"certified_tail_from_k":k+1,
                    "tail_upper":str(c**(-(k+1))),"early":details}
    raise RuntimeError("No tail certificate")

def controller(alpha,gamma,lam,sigma,K0,L0,steps):
    K,L=K0,L0
    h=[]
    for j in range(steps+1):
        h.append({"j":j,"K":str(K),"L":str(L)})
        K,L=max(alpha,gamma+lam*K), max(sigma,lam*L)
    return h

if __name__ == "__main__":
    curves=[frontier(c) for c in [Q(6,5),Q(241,200),Q(7,5),Q(3,2),Q(8,5)]]
    c=Q(241,200); d=Q(frontier(c)["d_exact"])
    initials=[(2,1),(4,3),(10,8),(100,50)]
    examples=[]
    for k,l in initials:
        h=controller(Q(11,10),Q(3,5),Q(1,2),Q(1,2),Q(k),Q(l),40)
        first=next((x for x in h if Q(x["K"])<c and Q(x["L"])<d),None)
        assert first is not None
        examples.append({"initial_T":k,"initial_S":l,"first_certified_level":first,
                         "last_level":h[-1]})
    margins=[]
    for delta in [Q(0),Q(1,10000),Q(1,1000),Q(1,400),Q(1,300),Q(1,200),Q(1,100)]:
        Kstar=max(Q(11,10),(Q(3,5)+delta)/(1-Q(1,2)))
        margins.append({"delta":str(delta),"Kstar":str(Kstar),
                        "fixed_T_below_241_200":Kstar<c})
    assert Q(1,2)<Q(frontier(Q(6,5))["d_exact"])
    assert Q(1,2)<d
    out={"model":"FLMV deterministic indexed read-only-input random-access TM; conditional same-machine ARC recurrence",
         "forbidden_curves":curves,
         "conditional_arc":{"alpha":"11/10","gamma":"3/5","lambda":"1/2",
                            "sigma":"1/2","fixed_T":"6/5","fixed_S":"1/2",
                            "initial_examples":examples,"per_child_overhead":margins},
         "checks":{"status":"PASS","strict_L_vs_d2_6_5":True,
                   "strict_L_vs_d_opt_241_200":True,
                   "none_claimed_constructive":True}}
    p=Path("results/raw/separation/2026-10-30_UNIVERSAL_PARAMETERIZED_FLMV_CONTRACT1.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
