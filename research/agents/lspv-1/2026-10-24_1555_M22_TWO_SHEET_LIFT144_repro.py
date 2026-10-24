#!/usr/bin/env python3
"""M22-TWO-SHEET-LIFT144 exact finite audit, Python standard library only.

Run: python 2026-10-24_1555_M22_TWO_SHEET_LIFT144_repro.py
Optionally pass research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt.
Döcker UNSAT is a published/imported theorem, not proved by this script.
"""
import ast
import itertools
import json
import sys
from collections import Counter, defaultdict, deque


def signature(formula):
    signs = defaultdict(lambda: [0, 0])
    positive, negative, seen = set(), set(), set()
    for clause in formula:
        assert len(clause) == 3 and all((v > 0) == (clause[0] > 0) for v in clause)
        supp = tuple(sorted(abs(v) for v in clause))
        assert len(set(supp)) == 3
        key = (clause[0] > 0, supp)
        assert key not in seen
        seen.add(key)
        (positive if clause[0] > 0 else negative).add(supp)
        for lit in clause:
            signs[abs(lit)][int(lit < 0)] += 1
    assert all(p == 2 and n == 2 for p, n in signs.values())
    names = set(signs)
    assert names == set(range(1, len(names) + 1))
    assert len(formula) * 3 == len(names) * 4
    q = len(positive - negative)
    assert q == len(negative - positive)
    return dict(k=len(names), m=len(formula), q=q, paired=q == 0)


def lift(formula):
    """Third sorted variable takes the opposite sheet from the first two."""
    result = []
    for clause in formula:
        names = sorted(abs(x) for x in clause)
        sign = 1 if clause[0] > 0 else -1
        for sheet in (0, 1):
            result.append(tuple(sign * (2 * v - 1 + (sheet ^ int(i == 2)))
                                for i, v in enumerate(names)))
    return result


def canonical_witness(k):
    return {v: int(v % 2 == 0) for v in range(1, k + 1)}


def evaluate(formula, witness):
    return all(any(witness[abs(lit)] == int(lit > 0) for lit in clause)
               for clause in formula)


def component_sizes(formula):
    edges = defaultdict(set)
    for clause in formula:
        names = [abs(v) for v in clause]
        for v in names:
            edges[v].update(u for u in names if u != v)
    visited, result = set(), []
    for start in edges:
        if start in visited:
            continue
        frontier = deque([start])
        visited.add(start)
        count = 0
        while frontier:
            v = frontier.popleft()
            count += 1
            for w in edges[v]:
                if w not in visited:
                    visited.add(w)
                    frontier.append(w)
        result.append(count)
    return sorted(result, reverse=True)


def validate_two_levels(formula):
    base = signature(formula)
    first = lift(formula)
    x = signature(first)
    assert (x['k'], x['m'], x['q'], x['paired']) == (
        2 * base['k'], 2 * base['m'], 2 * base['q'], base['paired'])
    assert evaluate(first, canonical_witness(x['k']))
    second = lift(first)
    y = signature(second)
    assert (y['k'], y['m'], y['q'], y['paired']) == (
        4 * base['k'], 4 * base['m'], 4 * base['q'], base['paired'])
    assert evaluate(second, canonical_witness(y['k']))
    return base, x, y


def y_fixture():
    p = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    n = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return p + [tuple(-v for v in clause) for clause in n]


def small_census():
    supports = list(itertools.combinations(range(1, 7), 3))
    families = [f for f in itertools.combinations(supports, 4)
                if all(sum(v in c for c in f) == 2 for v in range(1, 7))]
    assert len(families) == 75
    counts = Counter()
    for p in families:
        for n in families:
            f = list(p) + [tuple(-v for v in c) for c in n]
            before, one, two = validate_two_levels(f)
            counts['instances'] += 1
            counts['fully_paired' if before['paired'] else 'nonpaired'] += 1
            counts[f'q={before["q"]}'] += 1
            counts['lift_one_checked'] += 1
            counts['lift_two_checked'] += 1
    assert counts['instances'] == 5625
    return dict(sorted(counts.items()))


def inspect_fixture(name, f):
    a, b, c = validate_two_levels(f)
    return dict(name=name, base=a, sheet1=b, sheet2=c,
                components0=component_sizes(f),
                components1=component_sizes(lift(f)),
                components2=component_sizes(lift(lift(f))))


def main():
    output = {'status': 'COMPUTATIONAL finite checks only; no hardness claim',
              'method': 'exhaustive over all 75^2 M22 sources on 6 named variables',
              'census': small_census(),
              'Y': inspect_fixture('canonical Y', y_fixture())}
    y = y_fixture()
    models = sum(evaluate(y, {v: bits[v-1] for v in range(1, 7)})
                 for bits in itertools.product((0, 1), repeat=6))
    assert models == 20
    output['Y']['models_exact'] = models
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf8') as src:
            txt = ''.join(ln for ln in src if not ln.lstrip().startswith('#'))
        f = ast.literal_eval(txt)
        output['Doecker_198_imported_label_UNSAT'] = inspect_fixture('Doecker source', f)
        assert output['Doecker_198_imported_label_UNSAT']['components0'] == [198]
        assert output['Doecker_198_imported_label_UNSAT']['components1'] == [396]
        assert output['Doecker_198_imported_label_UNSAT']['components2'] == [396, 396]
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
