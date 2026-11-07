#!/usr/bin/env python3
"""LSPV-3/482 independent exhaustive projection check.
Not a historical R_mix341 checker. Python 3 standard library only.
"""
import json
from itertools import combinations, product

def verify_clause(clause):
    if (not clause or len(set(clause)) != len(clause)
        or any(type(x) is not int or x == 0 or -x in clause for x in clause)):
        raise ValueError("invalid original clause")

def satisfied(clause, assignment):
    return any(bool(assignment[abs(x)]) == (x>0) for x in clause)

def run(k):
    a=tuple(range(2,k+2))
    b=tuple(range(k+2,2*k+2))
    F=((1,)+a,(-1,)+b)
    for C in F: verify_clause(C)
    n=2*k+1
    source_models=[]
    for bs in product((0,1),repeat=n):
        v=dict(zip(range(1,n+1),bs))
        if all(satisfied(C,v) for C in F): source_models.append(v)
    projection_total=0
    nonfull=[]
    for width in range(4):
        for S in combinations(range(1,n+1),width):
            projection_total+=1
            seen={tuple(m[x] for x in S) for m in source_models}
            if len(seen)!=2**width: nonfull.append(S)
    D=a+b
    assert all(satisfied(D,m) for m in source_models)
    assert len(source_models)==2**(k+1)*(2**k-1)
    assert (len(nonfull)==0)==(k>=3)
    return {"k":k,"original_variables":n,"models":len(source_models),
            "projections_at_most_3":projection_total,"nonfull":nonfull,
            "wide_resolvent_width":len(D)}

def main():
    rows=[run(k) for k in (2,3,4,5)]
    rejected=0
    for invalid in ((0,1),(1,-1),(1,1),()):
        try: verify_clause(invalid)
        except ValueError: rejected+=1
        else: raise AssertionError("malformed accepted")
    assert rejected==4
    print(json.dumps({"run":"LSPV-3/482 independent Python",
        "scope":"finite source projections only; no full historical checker",
        "rows":rows,"malformed_rejected":rejected},indent=2))

if __name__=="__main__": main()
