#!/usr/bin/env python3
"""Exact certificate of an asymptotic slope near the threshold d = 1.

Claim certified: for the proof string A and slope g, there is eps0 > 0 such
that for every 0 < eps < eps0 the proof is valid at d = 1 - eps and
c = 1 + g*eps.  Hence liminf_{d -> 1-} (c*(d) - 1)/(1 - d) >= g.

Method: every exponent in the replay is a polynomial in eps with rational
coefficients (speedup parameters x_i(eps) = lam*(x0_i + x1_i*eps)).  For all
sufficiently small eps > 0, polynomials compare like their coefficient vectors
in lexicographic order (lowest degree first), so max/min and the final strict
inequality are decided exactly.  The real input exponent b_1 = 1 is kept.
Also replays the proof at a few explicit eps values in exact arithmetic.
Writes asymptotic_certify_results.json.
"""

import json
from fractions import Fraction as Fr
from pathlib import Path

from atp import build, solve

HERE = Path(__file__).resolve().parent


class P:
    """Polynomial in eps with Fraction coefficients; order = small-eps order."""

    def __init__(self, coeffs):
        c = [Fr(x) for x in coeffs]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c = c

    def __add__(self, o):
        o = o if isinstance(o, P) else P([o])
        n = max(len(self.c), len(o.c))
        return P([(self.c[i] if i < len(self.c) else 0) + (o.c[i] if i < len(o.c) else 0)
                  for i in range(n)])

    def __neg__(self):
        return P([-x for x in self.c])

    def __sub__(self, o):
        return self + (-(o if isinstance(o, P) else P([o])))

    def __mul__(self, o):
        o = o if isinstance(o, P) else P([o])
        out = [Fr(0)] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                out[i + j] += a * b
        return P(out)

    def sign(self):
        for x in self.c:
            if x != 0:
                return 1 if x > 0 else -1
        return 0

    def __lt__(self, o):
        return (self - o).sign() < 0

    def __le__(self, o):
        return (self - o).sign() <= 0

    def at(self, eps):
        return sum(x * eps ** i for i, x in enumerate(self.c))

    def __repr__(self):
        return ' + '.join(f'({x})e^{i}' for i, x in enumerate(self.c) if x != 0) or '0'


def pmax(*xs):
    best = xs[0]
    for x in xs[1:]:
        if best < x:
            best = x
    return best


def replay(ops, xs, c, d, a0, one):
    """Same rules as verify_exact.replay, with exponents of any ordered type."""
    E = 1
    zero = one * 0
    line = [[E, 'res', zero, one, zero]]
    beta, t = one, a0
    it = iter(xs)
    for op in ops:
        q, kind, a, sig, w = line[-1]
        if op == 'S':
            x = next(it)
            if x < zero or t < x:
                return None, 'x out of range'
            line[-1] = [q, 'big', pmax(a, x), sig, zero]
            line.append([-q, 'log', zero, pmax(x, beta), x])
            t = pmax(t - x, one)
        elif op == 'D':
            M = pmax(t, a, sig, beta)
            line[-1] = [q, 'res', zero, sig, d * M]
            beta, t = sig, c * M
        elif op == 'B':
            line.pop()
            beta, t = sig, t + w
        else:
            return None, 'unsupported op'
    if len(line) == 1 and line[0][1] == 'res':
        return t, 'ok'
    return None, 'bad end'


def certify(ops, g, lam=64, fit_eps=(Fr(1, 1000), Fr(2, 1000))):
    # zeroth- and first-order parameters from the LP at two small eps
    sols = []
    for e in fit_eps:
        L = build(ops, float(1 - e))
        r = solve(L, float(1 + g * e))
        if r.status != 0:
            return {'ops': ops, 'slope_g': str(g), 'certified': False,
                    'reason': 'LP infeasible at eps=%s (slope above this proof)' % e}
        sols.append([r.x[j] for j in L.xvars])
    e1, e2 = float(fit_eps[0]), float(fit_eps[1])
    x0 = [Fr((a * e2 - b * e1) / (e2 - e1)).limit_denominator(64) for a, b in zip(*sols)]
    x1 = [Fr((b - a) / (e2 - e1)).limit_denominator(10 ** 4) for a, b in zip(*sols)]
    xs = [P([lam * u, lam * v]) for u, v in zip(x0, x1)]
    c, d = P([1, g]), P([1, -1])
    tf, info = replay(ops, xs, c, d, P([lam]), P([1]))
    out = {'ops': ops, 'slope_g': str(g), 'lam': lam,
           'x0': [str(u) for u in x0], 'x1': [str(v) for v in x1]}
    if tf is None:
        out.update(certified=False, reason=info)
        return out
    gap = tf - P([lam])
    out.update(final_minus_a0=repr(gap), certified=gap.sign() < 0)
    # explicit-eps exact checks of the same parametrized proof
    checks = {}
    for e in (Fr(1, 10), Fr(1, 100), Fr(1, 1000)):
        xe = [lam * (u + v * e) for u, v in zip(x0, x1)]
        te, inf2 = replay(ops, xe, 1 + g * e, 1 - e, Fr(lam), Fr(1))
        checks[str(e)] = (te is not None and te < lam, float(lam - te) if te is not None else inf2)
    out['explicit_eps_checks'] = checks
    return out


if __name__ == '__main__':
    results = [
        certify('SDBD', Fr(1, 3) - Fr(1, 1000)),             # closed form slope 1/3
        certify('SSDBDBSDBD', Fr(45, 100)),
        certify('SSSDBDBSDBDBSDBD', Fr(55, 100)),
        certify('SSSSDBDBDBSDBDBSDBSDBD', Fr(58, 100)),
        certify('SSSSDBDBDBSDBDBSDBSDBD', Fr(60, 100)),        # above its slope: must fail
    ]
    (HERE / 'asymptotic_certify_results.json').write_text(json.dumps(results, indent=2))
    for r in results:
        print(r['ops'], 'g=', r['slope_g'], 'certified=', r['certified'],
              r.get('final_minus_a0', r.get('reason')), r.get('explicit_eps_checks'))
