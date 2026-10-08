"""Exact finite recurrence controls; not a test of an actual SAT compiler."""
from fractions import Fraction as Q
import json, time

start = time.monotonic()
checks = 0
cases = []
for h in (Q(1,2), Q(2,3), Q(9,10)):
    for eta in (Q(0), (1-h)/2):
        for K in (2, 10, 100):
            t = Q(K)
            d = 0
            while t > 1 and d < 1000:
                t = max(Q(1), eta+h*t)
                d += 1
            assert t == 1
            checks += 1
            cases.append(dict(h=str(h), eta=str(eta), K=K, depth=d))
    t = Q(10)
    for d in range(1, 101):
        t = (1-h)+h*t
        assert t == 1+9*h**d and t > 1
        checks += 1
print(json.dumps(dict(status="COMPUTATIONAL", checks=checks, cases=cases,
    boundary="At eta+h=1 finite depth does not reach exponent 1 for K>1",
    limitation="Recurrence arithmetic only; no SAT constructor tested",
    seconds=time.monotonic()-start), indent=2))
