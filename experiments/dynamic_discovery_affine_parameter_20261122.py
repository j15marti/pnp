"""New certificate-parameter control, exhaustive RHS for five variables."""
from itertools import combinations, product
from collections import Counter
import hashlib, json
from pathlib import Path


def eliminate(equations, n):
    rows = [sum(1 << i for i in scope) | (rhs << n) for scope, rhs in equations]
    pivot = 0
    for bit in range(n):
        found = next((i for i in range(pivot, len(rows)) if rows[i] >> bit & 1), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        for i in range(len(rows)):
            if i != pivot and rows[i] >> bit & 1:
                rows[i] ^= rows[pivot]
        pivot += 1
    return (1 << n) not in rows


n = 5
scopes = list(combinations(range(n), 3))
degree = Counter(i for scope in scopes for i in scope)
assert all(v > 2 for v in degree.values())
totals = Counter()
for rhs in product((0, 1), repeat=len(scopes)):
    equations = list(zip(scopes, rhs))
    accepted = eliminate(equations, n)
    oracle = any(all(sum(bits[i] for i in s) % 2 == b for s, b in equations)
                 for bits in product((0, 1), repeat=n))
    assert accepted == oracle
    totals["SAT" if accepted else "UNSAT"] += 1
controls = []
for n in (5, 6, 8, 12):
    scopes = list(combinations(range(n), 3))
    for flip in (False, True):
        equations = [(s, int(flip and s == (0, 1, 2))) for s in scopes]
        assert eliminate(equations, n) == (not flip)
        controls.append(dict(d=n,c=4*len(scopes),h=n,sat=not flip))
print(json.dumps(dict(totals=dict(totals),controls=controls,
    mode="all 1024 RHS vectors at d=5; eight symbolic-family cases; no randomness",
    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))
