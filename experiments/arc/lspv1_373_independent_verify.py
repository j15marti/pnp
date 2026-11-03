#!/usr/bin/env python3
"""Independently reconstruct and exhaustively check the finite 373 fixtures.
No import or call of the JavaScript producer; Python uses its own grammar/evaluator.
"""
import json
import itertools
import sys
from pathlib import Path

raw = json.loads(Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else
                 Path(__file__).with_name('lspv1_373_raw.json').read_text())
assert raw['experiment'] == 'REVERSIBLE_REPRESENTATION_TRAP373'


def php(k):
    source = []
    def var(bird, hole):
        return bird * k + hole + 1
    for bird in range(k + 1):
        source.append(tuple(var(bird, hole) for hole in range(k)))
    for hole in range(k):
        for left, right in itertools.combinations(range(k + 1), 2):
            source.append((-var(left, hole), -var(right, hole)))
    return k * (k + 1), tuple(source)


def count(n, clauses):
    total = 0
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in clauses):
            total += 1
    return total


def k4(flag):
    ends = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    clauses = []
    for vertex in range(4):
        variables = [index + 1 for index, pair in enumerate(ends) if vertex in pair]
        desired = int(bool(flag) and vertex == 0)
        for values in itertools.product((0, 1), repeat=3):
            if sum(values) % 2 != desired:
                clauses.append(tuple(-v if bit else v for v, bit in zip(variables, values)))
    return 6, tuple(clauses)


checks = 0
samples = []
for datum in raw['fixtures']:
    fam = datum['family']
    if fam == 'PHP':
        h = datum['h']
        n, clauses = php(h)
        z = n + 1
        encoded = clauses + ((z,), (-z,))
        changed = list(clauses)
        changed[-1] = (-changed[-1][0],) + changed[-1][1:]
        assert n == datum['variables']
        assert len(clauses) == datum['clauses']
        assert not count(n, clauses)
        assert not count(z, encoded)
        assert count(n, tuple(changed)) == datum['mutant_models']
        assert sum(c == (z,) for c in encoded) == 1
        assert sum(c == (-z,) for c in encoded) == 1
        assert all(z not in [abs(l) for l in c] for c in clauses)
        assert datum['encoded_resolution_minimum'] == 1
        checks += 8
        samples.append((fam, h, datum['mutant_models']))
    else:
        if fam == 'SAT_unit': n, clauses = 1, ((1,),)
        elif fam == 'SAT_mixed': n, clauses = 2, ((1, 2), (-1, 2))
        elif fam == 'UNSAT_units': n, clauses = 1, ((1,), (-1,))
        elif fam == 'UNSAT_empty': n, clauses = 0, ((),)
        elif fam == 'SAT_empty': n, clauses = 0, ()
        elif fam == 'TSEITIN_even': n, clauses = k4(False)
        elif fam == 'TSEITIN_odd': n, clauses = k4(True)
        else: raise AssertionError(fam)
        actual = count(n, clauses)
        encoded = clauses + ((n+1,),)
        augmented = count(n+1, encoded)
        assert actual == augmented == datum['source_models'] == datum['encoded_models']
        checks += 4
        samples.append((fam, actual))

assert next(x for x in samples if x[0] == 'TSEITIN_even')[1] == 8
assert next(x for x in samples if x[0] == 'TSEITIN_odd')[1] == 0
checks += 2
assert raw['assertions'] == 89
checks += 1
print(json.dumps({'independent_python_assertions': checks,
                  'source_and_encoding_fixture_count': len(samples),
                  'verified': True, 'samples': samples}, indent=2))