#!/usr/bin/env python3
"""Exact-arithmetic verification of computer-found proofs (CLAUDE TPORT-0001).

For each (op string, d, target c): solve the homogeneous LP at c, read off the
speedup parameters, scale by lam (so the original input length n^1 is present
but negligible), round to rationals, and replay the proof with exact Fraction
arithmetic using the real input exponent b_1 = 1 and actual maxima (no LP
slack).  A proof is verified when the final time is STRICTLY below a0; the
strict gap absorbs the n^{o(1)} and polylog factors of every step.
Writes verify_exact_results.json.
"""

import json
from fractions import Fraction as Fr
from pathlib import Path

from atp import build, solve

HERE = Path(__file__).resolve().parent
E = 1


def replay(ops, xs, c, d, a0):
    line = [[E, 'res', Fr(0), Fr(1), Fr(0)]]   # q, kind, a, sigma, w
    beta, t = Fr(1), a0
    xi = iter(xs)
    trace = []
    for op in ops:
        q, kind, a, sig, w = line[-1]
        if op == 'S':
            x = next(xi)
            if not (0 <= x <= t):
                return None, 'x out of range'
            line[-1] = [q, 'big', max(a, x), sig, Fr(0)]
            line.append([-q, 'log', Fr(0), max(x, beta), x])
            t = max(t - x, Fr(1))
        elif op == 'D':
            if kind == 'res':
                return None, 'D on residual'
            M = max(t, a, sig, beta)
            line[-1] = [q, 'res', Fr(0), sig, d * M]
            beta, t = sig, c * M
        elif op == 'B':
            if kind != 'res' or len(line) == 1:
                return None, 'bad B'
            line.pop()
            beta, t = sig, t + w
        else:
            return None, 'op not supported in exact replay: ' + op
        trace.append((op, float(t)))
    ok = len(line) == 1 and line[0][1] == 'res' and line[0][0] == E
    return (t, trace) if ok else (None, 'bad end')


def verify(ops, d, c, lam=1000):
    L = build(ops, float(d))
    res = solve(L, float(c))
    if res.status != 0:
        return {'ops': ops, 'd': str(d), 'c': str(c), 'verified': False,
                'reason': 'LP infeasible at this c'}
    xs = [Fr(res.x[j] * lam).limit_denominator(10**6) for j in L.xvars]
    a0 = Fr(lam)
    tf, info = replay(ops, xs, c, d, a0)
    if tf is None:
        return {'ops': ops, 'd': str(d), 'c': str(c), 'verified': False, 'reason': info}
    return {'ops': ops, 'd': str(d), 'c': str(c), 'a0': str(a0),
            'speedup_params': [str(x) for x in xs],
            'final_time': str(tf), 'final_time_float': float(tf),
            'verified': tf < a0, 'margin': float(a0 - tf)}


if __name__ == '__main__':
    cases = [
        ('SDBD', Fr(0), Fr(141, 100)),                          # Lipton-Viglas sqrt(2)
        ('SSDBDBSDBD', Fr(0), Fr(16, 10)),                      # Williams 1.6004
        ('SSSSDBDBDBSDBDBSDBSDBD', Fr(0), Fr(169, 100)),        # control, length 22
        ('SSSDBDBSDBDBSDBD', Fr(1, 2), Fr(13, 10)),              # d = 0.5
        ('SSSDBDBSDBDBSDBD', Fr(3, 4), Fr(114, 100)),            # d = 0.75
        ('SSSDBDBSDBDBSDBD', Fr(9, 10), Fr(105, 100)),           # d = 0.9
        ('SSSDBDBSDBDBSDBD', Fr(1, 2), Fr(1305, 1000)),          # beats collapse 1.3019
        ('SDBD', Fr(9, 10), Fr(103, 100)),                       # closed form, Thm 2
        ('SDBD', Fr(99, 100), Fr(1003, 1000)),                   # closed form, Thm 2
        ('SSSDBDBSDBDBSDBD', Fr(1), Fr(1001, 1000)),             # d = 1: must FAIL
        ('SDBD', Fr(1), Fr(1001, 1000)),                         # d = 1: must FAIL
    ]
    out = [verify(*cs) for cs in cases]
    (HERE / 'verify_exact_results.json').write_text(json.dumps(out, indent=2))
    for r in out:
        print(r['ops'], 'd=', r['d'], 'c=', r['c'], 'verified=', r['verified'],
              r.get('margin', r.get('reason')))
