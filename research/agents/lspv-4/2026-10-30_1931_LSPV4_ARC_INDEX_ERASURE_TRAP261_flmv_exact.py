#!/usr/bin/env python3
"""Exact rational verification of FLMV Theorem 5.7 at the two ARC points.
No numeric scan substitutes for the certified infinite tail."""
from fractions import Fraction as F

def envelope(c):
    f = F(1)
    vals = {}
    for k in range(1, 4):
        f = c*f/(1+f)
        vals[k] = min((1/f-c)/k, c**(-k))
    best = vals[2]
    tail = c**(-4)
    assert best > vals[1] and best > vals[3] and best > tail
    # Every k>=4 obeys d_k <= c^(-k) <= c^(-4) < best.
    return {"c":str(c),"d1":str(vals[1]),"d2":str(best),
            "d3":str(vals[3]),"tail_k_ge_4":str(tail),"winning_k":2}

if __name__=="__main__":
    targets=[(F(6,5),F(23,45)),(F(241,200),F(11642479,23232400))]
    for c,exact in targets:
        result=envelope(c)
        assert F(result["d2"])==exact
        print(result)
    print("PASS: exact fraction identities and infinite-tail certification")
