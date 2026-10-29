#!/usr/bin/env python3
"""Exact signed-affine prototype. Each suite is intended for timeout 25s.
Run: python THIS_FILE.py --suite small|strict22|hostile|modules --output result.json
No external packages. Counts operations, not physical machine bit steps.
"""
import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path


def rref(rows, n):
    rows = [int(r) for r in rows]
    j = 0
    for col in range(n):
        pivot = next((i for i in range(j, len(rows)) if rows[i] >> col & 1), None)
        if pivot is None:
            continue
        rows[j], rows[pivot] = rows[pivot], rows[j]
        for i in range(len(rows)):
            if i != j and rows[i] >> col & 1:
                rows[i] ^= rows[j]
        j += 1
    if any(r == 1 << n for r in rows[j:]):
        return None
    return tuple(rows[:j])


def pins(clause, n):
    return tuple((1 << (abs(lit)-1)) | ((lit < 0) << n) for lit in clause)


def count_affine(n, rows, clauses, record_cap=None):
    base = rref(rows, n)
    states = [] if base is None else [(base, 1)]
    widths = [len(states)]
    calls, candidates, inconsistent, cancellations = 1, 0, 0, 0
    for clause in clauses:
        generated = []
        for state, weight in states:
            if record_cap is not None and len(generated) + 2 > record_cap:
                return None, dict(status='UNKNOWN', gaussian_calls=calls,
                                  widths=widths, pending_records=len(generated))
            generated.append((state, weight))
            child = rref(state + pins(clause, n), n)
            calls += 1
            if child is None:
                inconsistent += 1
            else:
                generated.append((child, -weight))
        candidates += len(generated)
        generated.sort(key=lambda x: x[0])
        states = []
        for key, group in itertools.groupby(generated, key=lambda x: x[0]):
            weight = sum(item[1] for item in group)
            if weight:
                states.append((key, weight))
            else:
                cancellations += 1
        widths.append(len(states))
    answer = sum(weight * (1 << (n-len(state))) for state, weight in states)
    return answer, dict(widths=widths, peak=max(widths),
                        gaussian_calls=calls, generated_records=candidates,
                        inconsistent_children=inconsistent,
                        zero_weight_groups=cancellations)


def count_stream(n, rows, clauses):
    """Polynomial-space subset replay. Every repeated Gaussian call is paid."""
    total = 0
    for selection in range(1 << len(clauses)):
        equations = list(rows)
        for i, clause in enumerate(clauses):
            if selection >> i & 1:
                equations.extend(pins(clause, n))
        state = rref(equations, n)
        if state is not None:
            total += (-1 if selection.bit_count() & 1 else 1) * (1 << (n-len(state)))
    return total


def brute(n, rows, clauses):
    mask = (1 << n)-1
    return sum(all(((x & (row & mask)).bit_count() & 1) == row >> n for row in rows)
               and all(any(bool(x >> (abs(lit)-1) & 1) == (lit > 0)
                           for lit in clause) for clause in clauses)
               for x in range(1 << n))


def xor_clauses(variables, rhs):
    return [tuple(-v if bit else v for v, bit in zip(variables, bits))
            for bits in itertools.product((0, 1), repeat=len(variables))
            if sum(bits) % 2 != rhs]


def extract(n, clauses):
    """Source-syntactic exact XOR3 blocks only; no semantic inference."""
    groups = {}
    for index, clause in enumerate(clauses):
        assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
        ordered = tuple(sorted(clause, key=abs))
        scope = tuple(abs(x) for x in ordered)
        word = sum((x < 0) << i for i, x in enumerate(ordered))
        groups.setdefault(scope, {}).setdefault(word, []).append(index)
    removed, rows, blocks = set(), [], []
    for scope, words in sorted(groups.items()):
        for forbidden_parity in (0, 1):
            patterns = [w for w in range(8) if w.bit_count() % 2 == forbidden_parity]
            if all(w in words for w in patterns):
                indices = [words[w][0] for w in patterns]
                removed.update(indices)
                rows.append(sum(1 << (v-1) for v in scope) | ((1-forbidden_parity) << n))
                blocks.append(dict(scope=scope, indices=indices))
    return rows, [c for i, c in enumerate(clauses) if i not in removed], blocks


def connected(n, clauses):
    seen = {1}
    while True:
        enlarged = seen | {abs(lit) for c in clauses
                           if any(abs(x) in seen for x in c) for lit in c}
        if enlarged == seen:
            return len(seen) == n
        seen = enlarged


def strict22(n, clauses):
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses) and all(
        sum(c.count(lit) for c in clauses) == 2
        for v in range(1, n+1) for lit in (v, -v))


def compile_modules(n, clauses, groups, width_cap=10):
    """Authenticate a clause partition; compute exact boundary supports.
    The returned count is of boundary assignments, not full source models.
    Discovery of groups is caller-owned and must be charged separately.
    """
    assert sorted(i for group in groups for i in group) == list(range(len(clauses)))
    scopes = [set(abs(x) for i in group for x in clauses[i]) for group in groups]
    assert all(len(scope) <= width_cap for scope in scopes)
    boundary = sorted(v for v in range(1, n+1) if sum(v in s for s in scopes) > 1)
    positions = {v: i for i, v in enumerate(boundary)}
    equations, defects, counts = [], [], []
    assignment_trials = affine_modules = 0
    for group, scope in zip(groups, scopes):
        scope = sorted(scope)
        bvars = sorted(set(scope) & set(boundary))
        support = set()
        for a in range(1 << len(scope)):
            assignment_trials += 1
            values = {v: a >> j & 1 for j, v in enumerate(scope)}
            if all(any(values[abs(x)] == (x > 0) for x in clauses[i]) for i in group):
                support.add(sum(values[v] << j for j, v in enumerate(bvars)))
        counts.append(len(support))
        if not support:
            equations.append(1 << len(boundary))
            affine_modules += 1
            continue
        base = min(support)
        difference_basis = rref([x ^ base for x in support], len(bvars))
        if len(support) == 1 << len(difference_basis):
            affine_modules += 1
            for mask in range(1, 1 << len(bvars)):
                if all((mask & (x ^ base)).bit_count() % 2 == 0 for x in support):
                    eq = sum(1 << positions[v] for j, v in enumerate(bvars) if mask >> j & 1)
                    eq |= (((mask & base).bit_count() & 1) << len(boundary))
                    equations.append(eq)
        else:
            for a in range(1 << len(bvars)):
                if a not in support:
                    defects.append(tuple(-(positions[v]+1) if a >> j & 1 else positions[v]+1
                                         for j, v in enumerate(bvars)))
    return len(boundary), equations, defects, dict(boundary=boundary,
            assignment_trials=assignment_trials, support_sizes=counts,
            affine_modules=affine_modules, defect_clauses=len(defects))


def module_suite():
    rng = random.Random(122912)
    records = []
    for case in range(120):
        n = rng.randrange(3, 8)
        formula, groups = [], []
        for _ in range(rng.randrange(2, 6)):
            scope = rng.sample(range(1, n+1), rng.randrange(1, min(4, n)+1))
            group = []
            for _ in range(rng.randrange(1, 5)):
                clause = tuple(rng.choice((-1, 1))*v for v in rng.sample(scope, rng.randrange(1, len(scope)+1)))
                group.append(len(formula))
                formula.append(clause)
            groups.append(group)
        bn, rows, defects, metrics = compile_modules(n, formula, groups)
        answer, _ = count_affine(bn, rows, defects)
        boundary = metrics['boundary']
        feasible = set()
        for x in range(1 << n):
            if all(any(bool(x >> (abs(l)-1) & 1) == (l > 0) for l in c) for c in formula):
                feasible.add(sum((x >> (v-1) & 1) << j for j, v in enumerate(boundary)))
        assert answer == len(feasible)
        assert (answer > 0) == (brute(n, [], formula) > 0)
        records.append(dict(case=case, sat=answer > 0, boundary_count=answer, metrics=metrics))
    # A cyclic, jointly inconsistent source whose individual XOR modules are SAT.
    formula = xor_clauses((1, 2, 3), 0) + xor_clauses((1, 2, 3), 1)
    bn, rows, defects, metrics = compile_modules(3, formula, [list(range(4)), list(range(4, 8))])
    assert not defects and count_affine(bn, rows, defects)[0] == 0
    try:
        compile_modules(3, formula, [list(range(8)), [0]])
        raise RuntimeError('duplicate source ownership accepted')
    except AssertionError:
        pass
    return dict(seed=122912, cases=len(records), sat=sum(r['sat'] for r in records),
                unsat=sum(not r['sat'] for r in records), cyclic_xor=metrics,
                malformed_partition_rejected=True, records=records)


def small():
    clauses = [tuple((-v if bit else v) for v, bit in zip((1, 2, 3), bits))
               for bits in itertools.product((0, 1), repeat=3)]
    cases = sat = unsat = 0
    for mask in range(256):
        formula = [c for i, c in enumerate(clauses) if mask >> i & 1]
        for rows in ([], [7], [7 | 8], [1, 1 | 8]):
            actual, _ = count_affine(3, rows, formula)
            assert actual == brute(3, rows, formula)
            cases += 1
            sat += actual > 0
            unsat += actual == 0
        rows, residual, _ = extract(3, formula)
        assert count_affine(3, rows, residual)[0] == brute(3, [], formula)
    rng = random.Random(122910)
    for _ in range(180):
        n = rng.randrange(1, 8)
        rows = [rng.randrange(1 << (n+1)) for _ in range(rng.randrange(5))]
        formula = [tuple(rng.choice((-1, 1))*v for v in rng.sample(range(1, n+1), rng.randrange(1, min(n, 3)+1)))
                   for _ in range(rng.randrange(9))]
        actual, _ = count_affine(n, rows, formula)
        assert actual == brute(n, rows, formula)
        assert actual == count_stream(n, rows, formula)
        assert actual == count_affine(n, list(reversed(rows)), list(reversed(formula)))[0]
        cases += 1
        sat += actual > 0
        unsat += actual == 0
    return dict(cases=cases, sat=sat, unsat=unsat, extraction_checks=256,
                seed=122910)


def strict_suite():
    rng = random.Random(122911)
    records = []
    rejected = 0
    for n in (3, 6, 9):
        found = 0
        while found < 24:
            literals = [lit for v in range(1, n+1) for lit in (v, v, -v, -v)]
            rng.shuffle(literals)
            formula = [tuple(literals[i:i+3]) for i in range(0, len(literals), 3)]
            if not strict22(n, formula):
                rejected += 1
                continue
            found += 1
            rows, residual, blocks = extract(n, formula)
            actual, metric = count_affine(n, rows, residual)
            assert actual == brute(n, [], formula)
            for block in blocks:
                scope, indices = set(block['scope']), set(block['indices'])
                assert not any(scope & {abs(x) for x in c}
                               for i, c in enumerate(formula) if i not in indices)
            conn = connected(n, formula)
            if conn and n > 3:
                assert not blocks
            records.append(dict(n=n, connected=conn, blocks=len(blocks),
                                residual_clauses=len(residual), count=actual,
                                metric=metric, formula=formula))
    return dict(seed=122911, cases=len(records), rejected_draws=rejected,
                connected_large=sum(r['connected'] and r['n'] > 3 for r in records),
                records=records)


def hostile():
    examples = []
    for d in range(1, 11):
        formula = [(1, 2*i+2, 2*i+3) for i in range(d)]
        answer, metric = count_affine(2*d+1, [], formula)
        assert metric['widths'] == [1 << i for i in range(d+1)]
        assert answer == 4**d + 3**d
        negative = [tuple(-x for x in c) for c in formula]
        assert count_affine(2*d+1, [], negative)[0] == answer
        examples.append(dict(d=d, count=answer, metric=metric))
    repeated, repeated_metric = count_affine(3, [], [(1, 2, 3)]*30)
    assert repeated == 7 and repeated_metric['peak'] == 2
    # Every term below is individually nonempty, but the signed sum is zero.
    cancellation, cancellation_metric = count_affine(1, [], [(1,), (-1,)])
    assert cancellation == 0
    capped, cap_metric = count_affine(5, [], [(1, 2, 3), (1, 4, 5)], record_cap=2)
    assert capped is None and cap_metric['status'] == 'UNKNOWN'
    for n in (3, 6, 9, 12):
        formula = sum((xor_clauses((v, v+1, v+2), v % 2) for v in range(1, n+1, 3)), [])
        assert strict22(n, formula)
        rows, residual, blocks = extract(n, formula)
        assert not residual and len(blocks) == n//3
        assert count_affine(n, rows, residual)[0] == 1 << (2*n//3)
    return dict(stars=examples, repeated_clause=repeated_metric,
                cancellation=cancellation_metric, cap=cap_metric,
                isolated_parity_cases=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', choices=('small', 'strict22', 'hostile', 'modules'), required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = {'suite': args.suite, 'status': 'COMPUTATIONAL',
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'result': {'small': small, 'strict22': strict_suite, 'hostile': hostile,
                         'modules': module_suite}[args.suite]()}
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'suite': args.suite, 'status': 'PASS', 'output': args.output}))
