#!/usr/bin/env python3
"""Independent exhaustive test of the small-pin closure lemma, n=4, e=2."""
import hashlib
import itertools
import json
from pathlib import Path
import signal
import time

signal.alarm(24)
started = time.monotonic()
n = 4
subsets = [sum(1 << i for i in s) for k in range(3)
           for s in itertools.combinations(range(n), k)]
relations = checks = 0
for mask in range(1, 1 << (1 << n)):
    models = [x for x in range(1 << n) if (mask >> x) & 1]
    if any(not ((mask >> (x & y)) & 1) for x in models for y in models):
        continue
    relations += 1
    closures = set()
    for pins in subsets:
        supersets = [x for x in models if x & pins == pins]
        if supersets:
            closure = (1 << n) - 1
            for x in supersets:
                closure &= x
            closures.add(closure)
    for first in range(1 << n):
        for second in range(1 << n):
            def signature(x):
                return ((x & first).bit_count() % 2,
                        (x & second).bit_count() % 2)
            wanted = {signature(x) for x in models}
            obtained = {signature(x) for x in closures}
            assert wanted == obtained, (mask, first, second)
            checks += 1
result = {
    "status": "COMPUTATIONAL",
    "mode": "exhaustive, no random seed",
    "variables": n,
    "parity_rows": 2,
    "meet_closed_nonempty_relations": relations,
    "pair_of_parity_checks": checks,
    "mismatches": 0,
    "elapsed_seconds": time.monotonic() - started,
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "All nonempty meet-closed Boolean relations at arity 4 and all ordered pairs of linear parity functionals; exact signature coverage by at-most-two-pin least models."
}
destination = Path(__file__).with_suffix(".json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
