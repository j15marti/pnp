#!/usr/bin/env python3
"""Standalone 2-label spotcheck of the LSPV-2 mixed-interface projection theorem.
Full 36-source producer, independent verifier, proof DAGs and raw frames are
in the corresponding reproducibility ZIP; this compact file is NOT their replacement.
Python 3.11+, no external packages.
"""
from itertools import product

def sat(clauses, assignment):
    return all(any(assignment[abs(l)] == (l > 0) for l in c)
               for c in clauses)

def blocker(gamma):
    return tuple(-v if value else v for v, value in sorted(gamma.items()))

def exists_private(source, boundary):
    free = sorted({abs(l) for c in source for l in c} - set(boundary))
    return any(sat(source, {**boundary, **dict(zip(free, values))})
               for values in product((False, True), repeat=len(free)))

def core(component, beta):
    assert not exists_private(component, beta)
    guard = dict(beta)
    for variable in tuple(guard):
        smaller = dict(guard)
        del smaller[variable]
        if not exists_private(component, smaller):
            guard = smaller
    assert not exists_private(component, guard)
    return blocker(guard)

def profile(component, boundary):
    blocked = set()
    for vals in product((False, True), repeat=len(boundary)):
        beta = dict(zip(boundary, vals))
        if not exists_private(component, beta):
            blocked.add(core(component, beta))
    return sorted(blocked)

def antichain(clauses):
    unique = sorted({tuple(sorted(c)) for c in clauses}, key=lambda c: (len(c), c))
    return [c for c in unique if not any(set(d) < set(c) for d in unique)]

# Distinct private variables in each original-source component.
comp1 = [(1, 3), (-3, 2)]
comp2 = [(1, 4), (-4, 2)]
components = [comp1, comp2]
assert {3}.isdisjoint({4})
for label, h in [('SAT', [(1,)]), ('UNSAT', [(-1,), (-2,)])]:
    original = h + [c for component in components for c in component]
    clauses = antichain(h + [d for component in components
                            for d in profile(component, (1, 2))])
    for values in product((False, True), repeat=2):
        b = dict(zip((1, 2), values))
        assert sat(clauses, b) == exists_private(original, b)
    ans_orig = any(exists_private(original, dict(zip((1, 2), values)))
                   for values in product((False, True), repeat=2))
    ans_child = any(sat(clauses, dict(zip((1, 2), values)))
                    for values in product((False, True), repeat=2))
    assert ans_orig == ans_child == (label == 'SAT')
    print(label, 'source clauses', len(original), 'child clauses', clauses,
          'projection checked on 4 boundary assignments')
# An omitted private-variable overlap is unsound.
assert exists_private([(3,)], {}) and exists_private([(-3,)], {})
assert not exists_private([(3,), (-3,)], {})
print('PASS source-covered two-label projection, subsumption and overlap countercontrol')
