#!/usr/bin/env python3
"""547: high-precision threshold arithmetic ONLY, no native proof checker."""
from decimal import Decimal, localcontext
import json
def threshold(ell):
    if not isinstance(ell,int) or ell<32: raise ValueError("ell>=32 required")
    with localcontext() as c:
        c.prec=96
        n=1<<ell; m=n*n*(n+1)//2
        ln2=Decimal(2).ln()
        K=Decimal(n)/(Decimal(32768*ell*ell)*ln2)
        f=lambda b: Decimal(2*b)+Decimal(2*m+64*b+2).ln()/ln2
        lo,hi=-1,1
        while f(hi)<=K: lo,hi=hi,2*hi
        while lo+1<hi:
            mid=(lo+hi)//2
            if f(mid)<=K: lo=mid
            else: hi=mid
        assert (lo<0 or f(lo)<=K) and f(lo+1)>K
        return {"ell":ell,"minimum_paid_nodes":lo+1,"K":str(+K),
                "source_clause_count":str(m)}
if __name__=="__main__":
    cases=[threshold(i) for i in (32,40,48,56,64,80,96,128)]
    for t in (-1,0,31,"64",4.2):
        try: threshold(t)
        except (ValueError,TypeError): pass
        else: raise AssertionError("bad ell accepted")
    print(json.dumps({"status":"COMPUTATIONAL/ARITHMETIC ONLY",
        "cases":cases,"boundary_checks":16,"malformed_rejected":5},indent=2))
