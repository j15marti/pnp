"""Exact arithmetic controls, not SAT coverage tests; bounded to 25 seconds."""
import hashlib
import itertools
import json
from pathlib import Path
import signal
import time

signal.alarm(25)
start = time.monotonic()
assertions = 0
for count in range(1, 6):
    for children in itertools.product(range(1, 9), repeat=count):
        maximum = max(children)
        volume = sum(children)
        for delta in (1, 2, 3):
            assert sum(m ** (1 + delta) for m in children) <= maximum ** delta * volume
            assertions += 1

heterogeneous = []
for root in (16, 256, 65536):
    largest = __import__('math').isqrt(root)
    count = root // 2 + 1
    volume = root // 2 + largest
    assert volume <= root
    assert largest * largest <= root
    assert count > largest
    assertions += 3
    heterogeneous.append(dict(root=root, child_count=count, volume=volume, maximum=largest))

no_shrinkage = []
for root in (16, 64, 256):
    total = sum(range(1, root + 1))
    assert total == root * (root + 1) // 2
    assertions += 1
    no_shrinkage.append(dict(root=root, total=total, child_volume=root - 1))

path = Path(__file__)
result = dict(
    status='COMPUTATIONAL',
    scope='Exact arithmetic recurrence controls only, no SAT construction or coverage evidence',
    assertions=assertions,
    heterogeneous=heterogeneous,
    no_shrinkage=no_shrinkage,
    seed=None,
    runtime_seconds=time.monotonic() - start,
    code_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
)
output = path.with_name('bridge_strengthen1_results.json')
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
