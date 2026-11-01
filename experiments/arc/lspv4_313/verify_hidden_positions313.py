#!/usr/bin/env python3
"""Independent mathematical checker of the pair-hidden-position distribution."""
from math import comb
from fractions import Fraction
import json
checks=0
for m in (3,6,9,12,24,48,264):
    first=[min(i,j)+1 for i in range(m) for j in range(i+1,m)]
    assert Fraction(sum(first),len(first))==Fraction(m+1,3)
    checks+=len(first)
    for q in range(m+1):
        p=Fraction(sum(k>q for k in first),len(first))
        expected=Fraction(comb(m-2,q),comb(m,q)) if q<=m-2 else Fraction(0)
        assert p==expected
        checks+=1
print(json.dumps(dict(run="INDEPENDENT_HIDDEN_POSITIONS313",status="PASS",
                      checks=checks,P_vs_NP="OPEN"),indent=2))
