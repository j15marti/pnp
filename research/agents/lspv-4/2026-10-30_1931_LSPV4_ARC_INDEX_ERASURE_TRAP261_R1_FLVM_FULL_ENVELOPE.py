#!/usr/bin/env python3
"""Entire FLMV Theorem 5.7 positive envelope: certified finite search.
For rational 1<c<phi, exact Fraction arithmetic and a certified infinite tail.
Returns exact best index and bound, not a numerical sample of the tail."""
from fractions import Fraction as F

def dstar(c):
    assert c > 1 and c*(c-1) < 1, "positive FLMV regime 1<c<phi"
    f = F(1)
    best = F(-1)
    winner = None
    k = 0
    while True:
        k += 1
        f = c*f/(1+f)
        closed = (c-1)*c**k/(c**k+c-2)
        assert f == closed, "closed recurrence mismatch"
        d = min((1/f-c)/k, c**(-k))
        if d > best:
            best, winner = d, k
        tail_cap = c**(-(k+1))
        if best > 0 and tail_cap < best:
            # Every j >= k+1 has d_j <= c^-j <= this cap < best.
            return {"c":str(c),"winning_k":winner,"dstar":str(best),
                    "checked_k_through":k,"certified_tail_upper":str(tail_cap)}

if __name__ == "__main__":
    expected = {
      F(6,5): (2,F(23,45)),
      F(241,200): (2,F(11642479,23232400)),
      F(7,5): (3,F(949,5145)),
      F(3,2): (4,F(49,648)),
      F(8,5): (8,F(2145161,335544320)),
    }
    for c,(k,d) in expected.items():
        r=dstar(c)
        assert r["winning_k"]==k and F(r["dstar"])==d, (c,r)
        print(r)
    print("PASS exact certified full envelope at 5 rational anchors")
