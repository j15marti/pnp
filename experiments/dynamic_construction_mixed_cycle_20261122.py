"""Audit mixed cycles. Run with Python 3, standard library only."""
import itertools
import json


def source(word):
    triples = [(3*i+1, 3*i+2, 3*i+3) for i in range(len(word))]
    checks = []
    clauses = []
    for i, (a, b, z) in enumerate(triples):
        target = triples[(i+1) % len(word)][0 if word[i] == 'A' else 2]
        checks.append((a, b, target))
    for supports, parity in [(triples, False), (checks, True)]:
        for row in supports:
            for bits in itertools.product(range(2), repeat=3):
                allowed = sum(bits) % 2 == 0 if parity else sum(bits) == 1
                if not allowed:
                    clauses.append(tuple(-v if bit else v for v, bit in zip(row, bits)))
    return triples, checks, clauses


def rank(rows):
    pivots = {}
    for row in rows:
        mask = sum(1 << v for v in row)
        while mask:
            pivot = mask.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = mask
                break
            mask ^= pivots[pivot]
    return len(pivots)


def audit():
    totals = []
    for t in range(3, 8):
        sat = 0
        for word in itertools.product('AC', repeat=t):
            triples, checks, clauses = source(word)
            assert rank(checks) == t and len(clauses) == 9*t
            ports = {v for row in triples for v in row}
            seen = {1}
            for _ in range(3*t):
                for row in triples + checks:
                    if seen.intersection(row):
                        seen.update(row)
            assert seen == ports == set(range(1, 3*t+1))
            expected = t % 2 == 0 or 'A' in word
            found = False
            for picks in itertools.product(range(3), repeat=t):
                ones = {row[j] for row, j in zip(triples, picks)}
                if all(sum(v in ones for v in row) % 2 == 0 for row in checks):
                    assert all(any((abs(v) in ones) == (v > 0) for v in row) for row in clauses)
                    found = True
                    break
            assert found == expected
            sat += found
        totals.append(dict(t=t, words=2**t, sat=sat, unsat=2**t-sat))
    return totals


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
