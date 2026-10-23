#!/usr/bin/env python3
"""GLOBALQUOTA80: exhaustive 6^6 balanced signings of the octahedron.
Standard library only. Independent symbolic proofs are in the paired LaTeX report.
"""
from collections import Counter
from itertools import combinations, product
import json

supports = tuple((a,b,c) for a in (0,1) for b in (2,3) for c in (4,5))
occ = {v: [(i,j) for i,row in enumerate(supports)
           for j,x in enumerate(row) if x == v] for v in range(6)}
assert all(len(occ[v]) == 4 for v in range(6))
signings = tuple(combinations(range(4), 2))
assert len(signings) == 6

def models(choice):
    signs = [[None]*3 for _ in range(8)]
    for v in range(6):
        pos = set(signings[choice[v]])
        for idx, (i,j) in enumerate(occ[v]):
            signs[i][j] = idx in pos
    count = 0
    for assignment in range(64):
        if all(any(bool((assignment >> x) & 1) == signs[i][j]
                   for j,x in enumerate(row)) for i,row in enumerate(supports)):
            count += 1
    return count

hist = Counter()
for selection in product(range(6), repeat=6):
    count = models(selection)
    assert count >= 1, (selection, "UNSAT")
    hist[count] += 1
assert sum(hist.values()) == 6**6 == 46656
assert min(hist) == 4 and max(hist) == 22
result = {
    "run_id": "GLOBALQUOTA80",
    "signed_blocks": sum(hist.values()),
    "unsat_blocks": 0,
    "model_count_histogram": {str(k): hist[k] for k in sorted(hist)},
    "independently_proved": [
        "one signed-source identification certificate: 2n queries",
        "uniform source-sign identification tree: 3n queries",
        "promised SAT-root decision on octahedra: zero sign queries",
    ],
    "status": "COMPUTATIONAL",
}
print(json.dumps(result, indent=2, sort_keys=True))
