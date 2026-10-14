#!/usr/bin/env python3
"""RS6CAP1 core audit, Python 3.10+, standard library only.

Checks exact symbolic sums for the cap-removal lemma and the critical-deletion
counterexample. Does not test the full RS5 theorem or a SAT-decider transfer.
Usage: python cap_deletion_standalone.py --output result.json
"""
from __future__ import annotations
import argparse
import collections
import copy
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

EDGES = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
FORMULA = [c for e in EDGES for c in (e, tuple(-v for v in e))]

def verify_sum(premises, weights, target):
    if len(premises) != len(weights):
        raise ValueError('one multiplier per premise is required')
    lhs = collections.defaultdict(Fraction)
    rhs = Fraction(0)
    for (terms, bound), weight in zip(premises, weights):
        w = Fraction(weight)
        if w < 0:
            raise ValueError('negative multiplier')
        for variable, coefficient in terms.items():
            lhs[variable] += w * Fraction(coefficient)
        rhs += w * Fraction(bound)
    lhs = {v: c for v, c in lhs.items() if c}
    expected = {v: Fraction(c) for v, c in target[0].items() if c}
    if lhs != expected or rhs != Fraction(target[1]):
        raise ValueError('incorrect symbolic identity')


def false_clauses(assignment):
    return [i for i, clause in enumerate(FORMULA)
            if not any(bool(assignment >> (abs(lit)-1) & 1) == (lit > 0)
                       for lit in clause)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('rs6_core.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    common = [({'s0': 1, 'd0': -1}, 0), ({'B': 1, 's0': -1}, 0),
              ({'d0': 1, 'H': -1}, 0)]
    identities = [
        (common, [1, 1, 1], ({'B': 1, 'H': -1}, 0)),
        ([({'S': 1, 'D': -1}, 0), ({'D': 1, 'H': -1}, 0),
          ({'H': 1, 'S': -1}, 1)], [1, 1, 1], ({}, 1)),
        (common + [({'S': 1, 'B': -1}, 1), ({'H': 1, 'S': -1}, 1)],
         [1, 1, 1, 1, 1], ({}, 2)),
    ]
    rejected = 0
    for premises, weights, target in identities:
        verify_sum(premises, weights, target)
        for mutation in ('rhs', 'coefficient', 'negative'):
            p, w, t = copy.deepcopy((premises, weights, target))
            if mutation == 'rhs':
                t = (t[0], t[1] + 1)
            elif mutation == 'coefficient':
                t[0]['spurious'] = 1
            else:
                w[0] = -1
            try:
                verify_sum(p, w, t)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError('malformed identity accepted')
    counts = collections.Counter(lit for c in FORMULA for lit in c)
    assert len({frozenset(c) for c in FORMULA}) == 8
    assert all(len(set(map(abs, c))) == 3 for c in FORMULA)
    assert all(counts[v] == counts[-v] == 2 for v in range(1, 7))
    models = [a for a in range(64) if not false_clauses(a)]
    assert len(models) == 18
    critical = []
    for i, edge in enumerate(EDGES):
        a = sum(1 << (v-1) for v in range(1, 7) if v not in edge)
        assert false_clauses(a) == [2*i]
        assert false_clauses(a ^ 63) == [2*i+1]
        critical.extend([a, a ^ 63])
    # The capped statement can hold vacuously without an in-cap witness.
    proof_sizes_and_depths = [(2, 1)]
    assert all(d >= 10 for s, d in proof_sizes_and_depths if s <= 1)
    assert min(s for s, _ in proof_sizes_and_depths) < 10
    output = {
        'run': 'RS6CAP1', 'scope': 'standalone core reproduction',
        'universal_linear_identities': len(identities),
        'malformed_identities_rejected': rejected,
        'vacuous_cap_countermodel_checked': True,
        'formula': FORMULA, 'assignments_enumerated': 64,
        'models': models, 'critical_deletion_witnesses': critical,
        'failures': 0, 'seconds': time.perf_counter() - start,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitations': ['No independent verification of the asymptotic RS5 premise.',
                        'No arbitrary-decider lower bound.',
                        'This reruns part of the larger audit, not additional evidence to add to its totals.'],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
