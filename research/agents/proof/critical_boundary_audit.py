"""Finite accounting controls, not a SAT compiler. No random sampling."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import time

started = time.monotonic()
checks = 0
boundary = []
# n_d = 2^(2^d); sqrt n_d = n_(d-1), exactly.
total = 2
for d in range(1, 13):
    n = 1 << (1 << d)
    child = 1 << (1 << (d-1))
    total = n + child*total
    assert total == n*(d+1)
    checks += 1
    boundary.append({"depth":d, "log2_n":1 << d,
                     "time_over_n":d+1})
# Hostile control: arbitrary fixed eps slack makes an induction supersolution.
for h in (Q(1,2), Q(2,3), Q(9,10)):
    for eps in (Q(1,100), Q(1,10), Q(1,2)):
        delta = eps*(1-h)/(2*(2+eps))
        assert delta < eps
        assert 1+h*eps+delta*(2+eps) < 1+eps
        checks += 2
# Fixed-depth equality cannot remove K>1.
for K in (2,10,100):
    t = Q(K)
    for d in range(1,101):
        t = Q(1,2)+t/2
        assert t == 1+Q(K-1,2**d) and t>1
        checks += 1
# Williams Lemma 4.1 self-composition: a'=ab/(1+b), b'=b^2.
bootstrap = []
for b0 in (Q(2), Q(3,2), Q(11,10)):
    a, b = Q(1), b0
    floor = (b0-1)/b0
    for d in range(1,9):
        a, b = a*b/(1+b), b*b
        exact = (b0-1)*b0**(2**d-1)/(b0**(2**d)-1)
        assert a == exact and a > floor and b == b0**(2**d)
        checks += 1
    bootstrap.append({"initial_b":str(b0),"limit_a":str(floor),
                      "a_after_8":float(a),"b_growth":"b0^(2^d)"})
# Parent-scale semantic acquisition never disappears from an upper ledger.
for K in (2,10,100):
    for d in range(1,20):
        alleged = max(Q(K), 1+Q(K-1,2**d))
        assert alleged >= K
        checks += 1
elapsed = time.monotonic()-started
assert elapsed < 25
print(json.dumps({"status":"COMPUTATIONAL", "checks":checks,
    "code_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
    "seed":None,"method":"exact rational and integer identities",
    "boundary":boundary,"bootstrap":bootstrap,"seconds":elapsed,
    "limitation":"No general SAT reduction or asymptotic construction tested"},indent=2))
