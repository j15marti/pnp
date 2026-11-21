"""Finite controls for T5-QUOTIENT-SIDEINFO1. No external imports or sampler."""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json


def encode(clause):
    return '1110' + '010' + ''.join(format(x + 1, '02b') for x in clause)


def guess(joint, key):
    grouped = defaultdict(lambda: defaultdict(Fraction))
    for (x, y), mass in joint.items():
        grouped[key(x)][y] += mass
    return sum(max(row.values()) for row in grouped.values())


def main():
    clauses = [(0, 1, 2), (1, 0, 2)]
    allowed = {frozenset((i, (i+1) % 5, (i+2) % 5)) for i in range(5)}
    counts = [sum(frozenset(a[i] for i in clause) in allowed
                  for a in product(range(5), repeat=3)) for clause in clauses]
    encodings = [encode(c) for c in clauses]
    assert counts == [30, 30] and all(len(x) == 13 for x in encodings)
    assert encodings[0] != encodings[1]
    correlated = {(0, 0): Fraction(1, 2), (1, 30): Fraction(1, 2)}
    independent = {(x, y): Fraction(1, 4) for x in range(2) for y in (0, 30)}
    assert guess(correlated, lambda x: x) == 1
    assert guess(correlated, lambda x: 0) == Fraction(1, 2)
    assert guess(independent, lambda x: x) == Fraction(1, 2)
    cases = 0
    # Every denominator-four joint law on two presentations and two candidate counts.
    for weights in product(range(5), repeat=4):
        if sum(weights) != 4:
            continue
        law = dict(zip(product(range(2), (0, 30)), map(lambda w: Fraction(w, 4), weights)))
        assert guess(law, lambda x: 0) <= guess(law, lambda x: x)
        cases += 1
    print(json.dumps(dict(lemma='T5-QUOTIENT-SIDEINFO1', encodings=encodings,
                         N=13, exact_counts=counts, E=0,
                         correlated_guess_full='1', correlated_guess_quotient='1/2',
                         correlated_conditional_entropy_bits=[0, 1],
                         independent_guess_full='1/2', independent_guess_quotient='1/2',
                         probability_laws_checked=cases,
                         status='PASS; finite controls; general proof in report'), indent=2))


if __name__ == '__main__':
    main()
