#!/usr/bin/env python3
"""PROMISESLOPE1 exact-rational exponent arithmetic. No complexity lower bounds are inferred."""
from fractions import Fraction
import json

def fr(x):
    return f"{x.numerator}/{x.denominator}"

def main():
    beta0, a0, q = Fraction(9,10), Fraction(199,100), Fraction(6,5)
    rows = []
    for t in range(9):
        Q = q**t
        beta, g = beta0/Q, a0/Q-1
        rows.append({"t":t, "Q":fr(Q), "beta":fr(beta),
                     "excess":fr(g), "slope":fr(g/beta),
                     "positive_excess":g>0})
    ncases = declines = positive = 0
    for bi in range(1,10):
        beta = Fraction(bi,10)
        for gi in range(1,20):
            g = Fraction(gi,20)
            for qi in range(2,20):
                q = Fraction(qi+9,10)
                gnew = (1+g)/q-1
                bnew = beta/q
                ncases += 1
                declines += (gnew/bnew < g/beta)
                positive += (gnew>0)
    windows = []
    for n in (128,256):
        for k in (2,3,4):
            for q in (2,3):
                s = 1 << (n*k//5)
                low = Fraction(s,10*n)
                lownew = Fraction(s,10*q*n)
                windows.append({"n":n, "beta":f"{k}/5", "q":q,
                                "low":fr(low), "lownew":fr(lownew),
                                "slack":fr(low-lownew),
                                "slack_gt_100n":low-lownew>100*n})
    result = {
        "run":"PROMISESLOPE1", "status":"COMPUTATIONAL exact rational control",
        "seed":{"beta0":fr(beta0),"a0":fr(a0),"q":fr(q)},
        "steps":rows,
        "grid":{"cases":ncases,"strict_declines":declines,
                "positive_excess":positive,"nonpositive_excess":ncases-positive},
        "gap_windows":windows,
        "scope":"Verifies exponent arithmetic and large threshold windows, not MCSP circuit complexity."
    }
    assert ncases==3078 and declines==3078 and positive==729
    assert all(w["slack_gt_100n"] for w in windows)
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
