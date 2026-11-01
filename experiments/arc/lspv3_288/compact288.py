#!/usr/bin/env python3
"""GATE288 compact source-sign and batch-ledger control (stdlib only).
The full original-source SAT/UNSAT verification is in the complete archive.
"""
from collections import Counter
from itertools import product

Y6 = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
      (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6)]


def valid(n, clauses):
    positives, negatives = Counter(), Counter()
    if not clauses:
        return False
    seen = set()
    for clause in clauses:
        if len(clause) != 3 or any(v == 0 or abs(v) > n for v in clause):
            return False
        if len({abs(v) for v in clause}) != 3:
            return False
        if not (all(v > 0 for v in clause) or all(v < 0 for v in clause)):
            return False
        key = tuple(sorted(clause))
        if key in seen:
            return False
        seen.add(key)
        for lit in clause:
            (positives if lit > 0 else negatives)[abs(lit)] += 1
    return (len(positives) == n and len(negatives) == n
            and all(positives[i] == negatives[i] == 2 for i in range(1, n+1)))


def models(n, clauses):
    return sum(all(any((bool(a[abs(lit)-1]) == (lit > 0)) for lit in clause)
                   for clause in clauses) for a in product((0, 1), repeat=n))


def record_reads(n, m, width):
    return 2*m + m*((n+width-1)//width) + m*((m+width-1)//width)


def check():
    n, F = 6, Y6
    assert valid(n, F)
    assert models(n, F) == 20
    assert len(F) == 4*n//3
    for j, clause in enumerate(F):
        flipped = list(F)
        flipped[j] = tuple(-v for v in clause)
        assert not valid(n, flipped), (j, 'clause sign')
        for k, lit in enumerate(clause):
            changed = list(clause)
            changed[k] = -lit
            flipped[j] = tuple(changed)
            assert not valid(n, flipped), (j, k, 'literal sign')
    for B, expected in [(1, 128), (2, 72), (6, 40)]:
        assert record_reads(n, len(F), B) == expected
    print('PASS: Y6 20 witnesses; 8 clause-sign and 24 literal-sign mutants rejected;')
    print('batch source fetches B=1/2/6: 128/72/40; full U198/V198 controls in archive')


if __name__ == '__main__':
    check()
