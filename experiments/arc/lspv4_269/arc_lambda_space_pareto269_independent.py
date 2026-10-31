"""Independent source-enumeration and exact FLMV audit, stdlib only.
Run: python experiments/arc/lspv4_269/arc_lambda_space_pareto269_independent.py
No imports from the JavaScript producer; no randomness or SAT oracle.
"""
from fractions import Fraction as F
import json

W1 = [tuple(map(int, c.split())) for c in (
    '-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;'
    '4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;'
    '-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;'
    '-5 -12 15;-1 13 14').split(';')]
SWAP = [list(c) for c in W1]
SWAP[7][0] = -1
SWAP[19][0] = 1
H8 = [tuple(v if (mask >> (v-1)) & 1 else -v
            for v in (1, 2, 3)) for mask in range(8)]
SOURCES = [('W1', W1, 0), ('W1-swap', SWAP, 168),
           ('H8', H8, 0), ('H7', H8[:7], 1)]
checks = 0
rows = []
for name, clauses, target in SOURCES:
    n = max(abs(l) for cl in clauses for l in cl)
    models = 0
    for a in range(1 << n):
        def lit_true(l, mask):
            return bool(mask >> (abs(l)-1) & 1) == (l > 0)
        sat = all(any(lit_true(l, a) for l in cl) for cl in clauses)
        models += sat
        comp = (1 << n) - 1 - a
        for cl in clauses:
            assert sum(lit_true(l, a) for l in cl) + sum(
                lit_true(l, comp) for l in cl) == 3
            checks += 1
    assert models == target, (name, models, target)
    checks += 1
    rows.append(dict(source=name, models=models, exhaustive_assignments=1 << n))

# Distinct exact-arithmetic FLMV algorithm using closed 1/f_k, not the
# producer's successive f_k recurrence.
def envelope(c):
    best = F(-1)
    winner = []
    for k in range(1, 120):
        inv = (c**k + c - 2) / ((c-1) * c**k)
        d = min((inv-c)/k, c**(-k))
        if d > best:
            best, winner = d, [k]
        elif d == best:
            winner.append(k)
        if c**(-(k+1)) < best:
            return best, winner, k+1
    raise AssertionError('FLMV tail missing')
assert envelope(F(6, 5))[:2] == (F(23, 45), [2])
assert envelope(F(241, 200))[:2] == (F(11642479, 23232400), [2])
checks += 2

def p(c, z):
    return c**3 + (1+2*z)*c*c - c - 2
def root_interval(z):
    lo, hi = F(6, 5), F(603, 500)
    assert p(lo, z) < 0 < p(hi, z)
    for i in range(72):
        mid = (lo+hi)/2
        if p(mid, z) < 0:
            lo = mid
        else:
            hi = mid
    assert hi-lo < F(1, 10**20)
    return lo, hi
for z in (F(0), F(1, 1000), F(3, 2000), F(19, 10000)):
    root_interval(z)
    checks += 1

def gate(xi, eta, theta, beta, rho, c):
    lam = F(1, 2) + xi
    K = max(F(11, 10), F(3, 5)+theta+rho,
            (F(3, 5)+theta+beta)/(1-lam))
    L = max(F(1, 2)+eta, lam)
    return K < c and L < envelope(c)[0]
assert gate(F(3, 2000), F(0), F(0), F(0), F(1, 2), F(301, 250))
assert not gate(F(3, 2000), F(0), F(0), F(0), F(1, 2), F(241, 200))
assert gate(F(19, 10000), F(0), F(0), F(0), F(1, 2), F(6023, 5000))
assert not gate(F(1, 500), F(0), F(0), F(0), F(1, 2), F(6023, 5000))
assert not gate(F(0), F(26279, 23232400), F(0), F(0),
                F(1, 2), F(241, 200))
checks += 5
print(json.dumps(dict(independent_checks=checks, source_models=rows,
    global_threshold_c_interval=[str(v) for v in root_interval(F(0))],
    status='PASS: conditional algebra, both source labels; P versus NP OPEN'), indent=2))
