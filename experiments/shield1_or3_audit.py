#!/usr/bin/env python3
"""Independent, exhaustive small-domain audit of OR3 and anchored functional OR3.

Each CNF is a list of signed-integer clauses. Source variables are 1..3 (A),
4..6 (B). Standard library only. The script does not claim complexity lower bounds.
"""
from itertools import product
from hashlib import sha256
import json, platform


def eval_lit(lit, assignment):
    bit = assignment[abs(lit)]
    return bit if lit > 0 else not bit


def holds(formula, assignment):
    return all(any(eval_lit(lit, assignment) for lit in clause) for clause in formula)


def proper(formula):
    return len(set(map(tuple, formula))) == len(formula) and all(
        len(c) == 3 and len({abs(x) for x in c}) == 3
        for c in formula)


def original(a, b):
    q = len(a) + len(b)
    s, ystart = 7, 8
    out = []
    for i, (x, y, z) in enumerate(a):
        aux = ystart + i
        out += [(s, x, aux), (-aux, y, z)]
    for j, (x, y, z) in enumerate(b):
        aux = ystart + len(a) + j
        out += [(-s, x, aux), (-aux, y, z)]
    return out, 7 + q


def functional(a, b):
    q = len(a) + len(b)
    s, ystart, u, v, w = 7, 8, 8 + q, 9 + q, 10 + q
    out = []
    for i, (x, y, z) in enumerate(a):
        aux = ystart + i
        out += [(s, x, aux), (-aux, y, z), (-aux, -s, -u), (-aux, -x, -u)]
    for j, (x, y, z) in enumerate(b):
        aux = ystart + len(a) + j
        out += [(-s, x, aux), (-aux, y, z), (-aux, s, -u), (-aux, -x, -u)]
    # Forbid each (u,v,w) != (1,1,1). Each clause is falsified at one triple.
    for ub, vb, wb in product((False, True), repeat=3):
        if (ub, vb, wb) != (True, True, True):
            out.append(((-u if ub else u), (-v if vb else v), (-w if wb else w)))
    return out, w


def expected_original(a, b, bits):
    def value(lit):
        return int(eval_lit(lit, bits))
    factor_a_active = 1
    factor_a_disabled = 1
    for x, y, z in a:
        t = value(y) | value(z)
        factor_a_active *= value(x) + t
        factor_a_disabled *= 1 + t
    factor_b_active = 1
    factor_b_disabled = 1
    for x, y, z in b:
        t = value(y) | value(z)
        factor_b_active *= value(x) + t
        factor_b_disabled *= 1 + t
    return factor_a_active * factor_b_disabled + factor_a_disabled * factor_b_active


def evaluate_all(a, b):
    form, max_var = original(a, b)
    form_f, max_var_f = functional(a, b)
    q = len(a) + len(b)
    assert len(form) == 2 * q and max_var == 7 + q and proper(form)
    assert len(form_f) == 4 * q + 7 and max_var_f == 10 + q and proper(form_f)
    checks = 0
    old_count_total = new_count_total = 0
    for source_bits in product((False, True), repeat=6):
        src = {i + 1: b for i, b in enumerate(source_bits)}
        t_a, t_b = holds(a, src), holds(b, src)
        expected = int(t_a) + int(t_b)
        count_old = 0
        for extra in product((False, True), repeat=q+1):
            full = dict(src)
            full.update({7 + i: val for i, val in enumerate(extra)})
            count_old += holds(form, full)
        count_new = 0
        for extra in product((False, True), repeat=q+4):
            full = dict(src)
            full.update({7 + i: val for i, val in enumerate(extra)})
            count_new += holds(form_f, full)
        assert count_old == expected_original(a, b, src), (a, b, src, count_old)
        assert count_new == expected, (a, b, src, count_new, expected)
        assert (count_old > 0) == (t_a or t_b)
        assert (count_new > 0) == (t_a or t_b)
        checks += 4
        old_count_total += count_old
        new_count_total += count_new
    # If A or B holds on a source assignment, there is exactly one extension for
    # each compatible selector branch, but not necessarily one overall.
    expected_total_f = sum(holds(a, dict(zip(range(1, 7), bits))) for bits in product((False, True), repeat=6)) + sum(
        holds(b, dict(zip(range(1, 7), bits))) for bits in product((False, True), repeat=6))
    assert new_count_total == expected_total_f
    return dict(q=q, old_models=old_count_total, functional_models=new_count_total, checks=checks)


def simplify(formula, assignments):
    result = []
    for clause in formula:
        if any(abs(lit) in assignments and eval_lit(lit, assignments) for lit in clause):
            continue
        rem = tuple(x for x in clause if abs(x) not in assignments)
        result.append(rem)
    return result


def retraction_test(a, b):
    original_formula, _ = original(a, b)
    functional_formula, _ = functional(a, b)
    q = len(a) + len(b)
    s = 7
    # Original auxiliary-to-literal retractions (not constant restrictions).
    for formula, anchored in ((original_formula, False), (functional_formula, True)):
        for which in ('A', 'B'):
            # Perform substitution symbolically using tuples ('var', sign) or const.
            target = a if which == 'A' else b
            sub = {s: False if which == 'A' else True}
            if anchored:
                sub.update({8 + q: True, 9 + q: True, 10 + q: True})
            for i, clause in enumerate(a):
                sub[8 + i] = ('not', abs(clause[0]), clause[0] > 0) if which == 'A' else False
            for j, clause in enumerate(b):
                sub[8 + len(a) + j] = ('not', abs(clause[0]), clause[0] > 0) if which == 'B' else False
            def lit_image(lit):
                val = sub.get(abs(lit), None)
                if val is None:
                    return lit
                if isinstance(val, bool):
                    return val if lit > 0 else not val
                # val represents negation of signed source literal; e.g. -x if source x.
                _, var, positive = val
                base = -var if positive else var
                return base if lit > 0 else -base
            remaining = []
            for clause in formula:
                ims = [lit_image(lit) for lit in clause]
                if any(v is True for v in ims):
                    continue
                ims = [v for v in ims if v is not False]
                if any(-v in ims for v in ims):
                    continue
                remaining.append(tuple(ims))
            assert sorted(map(frozenset, remaining), key=str) == sorted(map(frozenset, target), key=str), (which, remaining, target)
    # Verify no constant assignment to just the original three auxiliaries
    # (s,y,z) gives literally A or B on the same disjoint source alphabet.
    if len(a) == len(b) == 1:
        for values in product((False, True), repeat=3):
            restricted = simplify(original_formula, dict(zip((7, 8, 9), values)))
            assert restricted != a and restricted != b, (values, restricted)
    return True


def main():
    a_clause = (1, 2, 3)
    b_clause = (4, 5, 6)
    examples = [([a_clause], [b_clause]),
                ([(1, 2, 3), (-1, -2, -3)], [(-4, 5, -6)]),
                ([(1, -2, 3), (1, 2, -3)], [(4, 5, 6), (-4, -5, -6)])]
    results = []
    for a,b in examples:
        results.append(evaluate_all(a,b))
        retraction_test(a,b)
    result = dict(version='SHIELD1-OR3-FUNCTIONAL-RETRACTION-2026-11-18',
                  python=platform.python_version(), cases=results,
                  total_source_assignments=len(results)*64,
                  total_asserted_checks=sum(row['checks'] for row in results)+len(results)*2,
                  proper=True, constant_only_retractions_on_original_single_clause=False,
                  observations='Finite checks only; symbolic theorems separately required.')
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
