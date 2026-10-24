#!/usr/bin/env python3
"""Compact independent checker. The full 194-check DIMACS audit is separate.
No result here constructs an all-input low-resource SAT solver.
"""
from fractions import Fraction as Q
from itertools import product
import json


def beta(c):
    return ((c + 2) / c**2 - c) / 2


def threshold(c, ell):
    u = Q(1)
    for _ in range(ell):
        u = (u + 1) / c
    return min((u - c) / ell, c**(-ell))


def envelope(c):
    a = 1 / (c - 1) - c
    if a <= 0:
        return Q(0), 0
    best, winner, u = Q(0), 0, Q(1)
    for ell in range(1, 10000):
        u = (u + 1) / c
        d = min((u - c) / ell, c**(-ell))
        if d > best:
            best, winner = d, ell
        # This bounds every omitted index, not just tested indices.
        if best > 0 and a / (ell + 1) <= best:
            return best, winner
    raise RuntimeError('Envelope iteration limit')


def main():
    assert beta(Q(241, 200)) == Q(11642479, 23232400)
    cases = [
        ('ARC', Q(6,5), Q(1,2), Q(241,200), 2),
        ('outside_old_box', Q(5,4), Q(3,10), Q(63,50), 2),
        ('beyond_beta2', Q(3,2), Q(1,20), Q(151,100), 4),
        ('smaller_space', Q(31,20), Q(1,50), Q(39,25), 5),
    ]
    results = []
    for name,t,s,c,ell in cases:
        value = threshold(c,ell)
        assert c > t and value > s
        results.append(dict(name=name,t=str(t),s=str(s),c=str(c),ell=ell,
                            threshold=str(value),margin=str(value-s)))
    assert beta(Q(3,2)) < Q(1,20)
    assert envelope(Q(3,2)) == (Q(49,648),4)
    assert envelope(Q(5,4))[0] == Q(83,200)
    assert envelope(Q(6,5))[0] < Q(3,5)
    assert envelope(Q(6,5))[0] < Q(1)
    sat = unsat = 0
    for q in range(2,6):
        for eta in product((0,1),repeat=q-1):
            support=((0,0),(1,0),(0,1))
            direct=any(states[0][0] == states[-1][0] == 1 and
                       all(states[i][0]^states[i+1][0] == eta[i]
                           for i in range(q-1))
                       for states in product(support,repeat=q))
            live={s for s in support if s[0] == 1}
            for e in eta:
                live={b for b in support if any(a[0]^b[0] == e for a in live)}
            joined=any(s[0] == 1 for s in live)
            assert joined == direct == (sum(eta)%2 == 0)
            sat += joined
            unsat += not joined
    print(json.dumps({'scope':'COMPUTATIONAL exact arithmetic and finite semantics',
                      'endpoint_certificates':results,'finite_SAT':sat,
                      'finite_UNSAT':unsat,'discrepancies':0},indent=2))

if __name__ == '__main__':
    main()
