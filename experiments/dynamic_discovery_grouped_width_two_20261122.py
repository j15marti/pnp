"""Boolean decision after exact-one grouping and degree-two elimination."""
from itertools import product
from collections import Counter
import json


def decide(factors, checks):
    owner = {v: (i, k) for i, row in enumerate(factors) for k, v in enumerate(row)}
    domain = {i: range(3) for i in range(len(factors))}
    for v in sorted(set().union(*map(set, checks)) - set(owner)):
        i = len(domain)
        domain[i] = range(2)
        owner[v] = (i, 1)
    tables = []
    for row in checks:
        terms = [owner[v] for v in row]
        scope = tuple(sorted({i for i, _ in terms}))
        allowed = set()
        for values in product(*(domain[i] for i in scope)):
            state = dict(zip(scope, values))
            if sum(state[i] == k for i, k in terms) % 2 == 0:
                allowed.add(values)
        tables.append((scope, allowed))
    while domain:
        for pivot in sorted(domain):
            bucket = [(s, r) for s, r in tables if pivot in s]
            neighbors = sorted(set().union(*(set(s) for s, _ in bucket)) - {pivot})
            if len(neighbors) <= 2:
                break
        else:
            return 'UNKNOWN'
        allowed = set()
        for values in product(*(domain[i] for i in neighbors)):
            state = dict(zip(neighbors, values))
            for x in domain[pivot]:
                state[pivot] = x
                if all(tuple(state[i] for i in s) in r for s, r in bucket):
                    allowed.add(values)
                    break
        tables = [(s, r) for s, r in tables if pivot not in s]
        tables.append((tuple(neighbors), allowed))
        del domain[pivot]
    return 'SAT' if all(() in r for _, r in tables) else 'UNSAT'


def audit():
    factors = [(0,1,2), (3,4,5), (6,7,8)]
    # First three supports form the odd all-C cycle. Port 9 is internal.
    pool = [(0,1,5), (3,4,8), (6,7,2), (0,3,9), (3,6,9), (0,6,9),
            (1,4,7), (1,4,8)]
    witnesses = [bits for bits in product(range(2), repeat=10)
                 if all(sum(bits[v] for v in row) == 1 for row in factors)]
    counts = Counter()
    for mask in range(1 << len(pool)):
        checks = [row for j, row in enumerate(pool) if mask & (1 << j)]
        truth = 'SAT' if any(all(sum(bits[v] for v in row) % 2 == 0
                                 for row in checks) for bits in witnesses) else 'UNSAT'
        label = decide(factors, checks)
        assert label in (truth, 'UNKNOWN')
        counts[label + '/' + truth] += 1
    return dict(sorted(counts.items()))


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
