#!/usr/bin/env python3
"""Bounded exact checks of proof-assembly distinctions, not a SAT lower bound."""
import hashlib
import json
import time
from fractions import Fraction as Q
from pathlib import Path

started = time.monotonic()
checks = 0
def check(condition):
    global checks
    assert time.monotonic() - started < 25, 'Split this experiment into batches'
    assert condition
    checks += 1

# A decision-guided restriction path exists for every small Boolean predicate.
# Calls are semantic truth-table lookups here, not free operations in a SAT proof.
paths = 0
for n in range(1, 4):
    for table in range(1 << (1 << n)):
        domain = list(range(1 << n))
        parent = any((table >> x) & 1 for x in domain)
        for bit in range(n):
            zero = [x for x in domain if not (x >> bit) & 1]
            zero_sat = any((table >> x) & 1 for x in zero)
            domain = zero if zero_sat else [x for x in domain if (x >> bit) & 1]
            check(any((table >> x) & 1 for x in domain) == parent)
        check(len(domain) == 1)
        paths += 1

# Cycle accounting admits scale-one edges, but unresolved K-cost is separate.
C1, C2 = Q(13, 10), Q(1)
check(C1 >= max(Q(1), Q(3, 10) + C2))
check(C2 >= max(Q(1), Q(1, 5) + C1 / 2))
check(C1 + Q(1, 5) < Q(9, 5))  # illustrative ledger only
for K in [2, 3, 10, 100]:
    check(max(C1, Q(K)) >= K)

# Shrinking a deliberately padded encoding does not shrink original size.
for r in range(2, 8):
    theta = Q(1, r)
    check(r * theta == 1)
    check(r * Q(1) >= 2)  # reading padded input costs n^r

# A strictly contracting distance can approach but never enter the boundary.
threshold = Q(9, 5)
v = Q(10)
for _ in range(50):
    v = threshold + (v - threshold) / 2
    check(v > threshold)

result = dict(status='COMPUTATIONAL', checks=checks, truth_tables=paths,
              elapsed_seconds=time.monotonic()-started,
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              scope='Exact finite arithmetic and decision-guided restriction controls only; no cheap SAT oracle, source selector, asymptotic coverage or separation inferred.',
              findings=['path correctness does not price its decision calls',
                        'same-scale typed edge can participate in contracting cycle',
                        'direct original-solver cost remains in a conservative ledger',
                        'padding quotient restores original size',
                        'boundary convergence need not give finite entry'])
Path(__file__).with_name('assembly_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
