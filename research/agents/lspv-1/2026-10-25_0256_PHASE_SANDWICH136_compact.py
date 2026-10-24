#!/usr/bin/env python3
"""Finite deferred-first-bit semantics on a fixed proper-3CNF source grammar.
Not a random-access Turing-machine time/space measurement.
"""
import json, random
from collections import Counter
from itertools import product

SEED = 202610250256

def sat(bits):
    assert len(bits) == 24
    for assignment in product((0, 1), repeat=3):
        if all(any(assignment[k] != bits[3*j+k] for k in range(3))
               for j in range(8)):
            return True
    return False

def late_pivot(source):
    assert len(source) == 24
    seen = set()
    def read(pos):
        seen.add(pos)
        return source[pos]
    # The pivot at position zero is never physically read in the simulations.
    for i in range(1, 24):
        read(i)
    def virtual(b):
        return [b] + [read(i) for i in range(1, 24)]
    a0, a1 = sat(virtual(0)), sat(virtual(1))
    assert seen == set(range(1, 24))
    b = read(0)
    assert len(seen) == 24
    output = (a0, a1)[b]
    assert output == sat(source)
    return output, a0 != a1

def main():
    rng = random.Random(SEED)
    clauses = [tuple((j >> k) & 1 for k in range(3)) for j in range(8)]
    tally = Counter()
    for _ in range(128):
        base = clauses[:]
        rng.shuffle(base)
        bits = [v for triple in base for v in triple]
        for changed in (False, True):
            x = bits[:]
            if changed:
                x[0] ^= 1
            label, pivotal = late_pivot(x)
            assert label == changed
            tally['checks'] += 1
            tally['SAT' if label else 'UNSAT'] += 1
            tally['pivotal'] += int(pivotal)
    for _ in range(350):
        x = [rng.randrange(2) for _ in range(24)]
        label, pivotal = late_pivot(x)
        tally['checks'] += 1
        tally['SAT' if label else 'UNSAT'] += 1
        tally['pivotal'] += int(pivotal)
    result = {'run': 'PHASE-SANDWICH136-COMPACT', 'seed': SEED,
              'grammar': 'fixed 8 proper ternary clauses on variables 1,2,3; 24 sign bits',
              'counts': dict(sorted(tally.items())), 'all_passed': True,
              'post_complete_acquisition_steps': 'one saved-bit select and halt; abstract, not physical TM'}
    print(json.dumps(result, indent=2, sort_keys=True))
    return result

if __name__ == '__main__':
    main()
