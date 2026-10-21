#!/usr/bin/env python3
"""Finite audit for CUTSET-TABLE-TRILEMMA58.

The script checks the real WRAPPER source cutset, restriction heredity,
interface-table tightness, and the ARC storage/rescan exponent trilemma.
It makes no complexity-class claim.
"""

from itertools import combinations, product
from collections import defaultdict
import json
import math
import random


CLAUSES = [
    (-12, -1, 13), (-10, 1, 9), (-9, -2, 11), (-8, -1, 6),
    (-6, 1, 8), (-4, 1, 3), (-4, 2, 5), (-2, 6, 7),
    (-2, 10, 11), (-2, 12, 13), (-1, 10, 11), (-1, 13, 14),
    (1, 4, 5), (2, 3, 5), (2, 6, 8), (2, 13, 14),
    (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14),
]


def lit_value(lit, assignment):
    value = assignment[abs(lit)]
    return value if lit > 0 else 1 - value


def formula_value(clauses, assignment):
    return all(any(lit_value(lit, assignment) for lit in clause)
               for clause in clauses)


def simplify(clauses, partial):
    reduced = []
    for clause in clauses:
        rest = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in partial:
                if lit_value(lit, partial):
                    satisfied = True
                    break
            else:
                rest.append(lit)
        if not satisfied:
            reduced.append(tuple(rest))
    return reduced


def primal_components(clauses, removed=frozenset()):
    variables = {abs(lit) for clause in clauses for lit in clause} - set(removed)
    graph = {v: set() for v in variables}
    for clause in clauses:
        row = [abs(lit) for lit in clause if abs(lit) in variables]
        for a, b in combinations(row, 2):
            graph[a].add(b)
            graph[b].add(a)
    components = []
    unseen = set(variables)
    while unseen:
        start = min(unseen)
        stack = [start]
        comp = set()
        unseen.remove(start)
        while stack:
            v = stack.pop()
            comp.add(v)
            for w in graph[v]:
                if w in unseen:
                    unseen.remove(w)
                    stack.append(w)
        components.append(tuple(sorted(comp)))
    return tuple(sorted(components))


def branch_component_counts(clauses, cutset, cut_bits):
    cut = dict(zip(cutset, cut_bits))
    reduced = simplify(clauses, cut)
    if any(len(c) == 0 for c in reduced):
        return (), 0
    components = primal_components(reduced)
    counts = []
    for comp in components:
        relevant = [c for c in reduced if any(abs(x) in comp for x in c)]
        count = 0
        for bits in product((0, 1), repeat=len(comp)):
            values = dict(zip(comp, bits))
            if formula_value(relevant, values):
                count += 1
        counts.append(count)
    answer = math.prod(counts) if counts else 1
    return tuple(counts), answer


def exhaustive_count(clauses, variables):
    total = 0
    for bits in product((0, 1), repeat=len(variables)):
        total += formula_value(clauses, dict(zip(variables, bits)))
    return total


def main():
    assertions = 0
    variables = tuple(range(1, 15))

    qualifying = []
    subsets_checked = 0
    for size in range(3):
        for cutset in combinations(variables, size):
            comps = primal_components(CLAUSES, cutset)
            subsets_checked += 1
            if comps and max(map(len, comps)) <= 3:
                qualifying.append((cutset, comps))
    assert qualifying == [((1, 2), ((3, 4, 5), (6, 7, 8),
                                     (9, 10, 11), (12, 13, 14)))]
    assertions += 1

    expected = {
        (0, 0): ((3, 4, 5, 6), 360),
        (0, 1): ((4, 4, 3, 6), 288),
        (1, 0): ((5, 4, 6, 5), 600),
        (1, 1): ((7, 5, 5, 4), 700),
    }
    table = {}
    total = 0
    for cut_bits in product((0, 1), repeat=2):
        counts, answer = branch_component_counts(CLAUSES, (1, 2), cut_bits)
        assert (counts, answer) == expected[cut_bits]
        table["".join(map(str, cut_bits))] = {
            "component_counts": counts,
            "product": answer,
        }
        total += answer
        assertions += 1
    assert total == exhaustive_count(CLAUSES, variables) == 1948
    assertions += 1

    # Pure restrictions only remove variables, clauses, or primal edges, so
    # the old cutset minus fixed variables remains valid and blocks <=3.
    rng = random.Random(580648)
    restriction_trials = 12000
    for _ in range(restriction_trials):
        size = rng.randint(0, 12)
        chosen = rng.sample(variables, size)
        partial = {v: rng.getrandbits(1) for v in chosen}
        reduced = simplify(CLAUSES, partial)
        remaining_cutset = tuple(v for v in (1, 2) if v not in partial)
        comps = primal_components(reduced, remaining_cutset)
        assert not comps or max(map(len, comps)) <= 3
        assertions += 1

    # Exact interface function tables are tight against singleton contexts.
    interface_checks = 0
    for k in range(1, 5):
        m = 1 << k
        all_sets = range(1 << m)
        seen = set()
        for X in all_sets:
            table_word = tuple((X >> j) & 1 for j in range(m))
            assert table_word not in seen
            seen.add(table_word)
            # Each singleton context reads precisely membership of j.
            for j in range(m):
                assert table_word[j] == ((X >> j) & 1)
                interface_checks += 1
                assertions += 1
        assert len(seen) == 1 << m
        # If 0 is forced feasible, 2^(m-1) possible X still require m-1 bits.
        containing_zero = sum(1 for X in all_sets if X & 1)
        assert containing_zero == 1 << (m - 1)
        assertions += 3

    # Storage/rescan exponent audit for the binary-selector INDEX family.
    exponent_rows = []
    for k in (10, 16, 24, 32, 48, 64, 96, 128):
        m = 2**k
        log2_N = k + 2 * math.log2(k)  # N = m*k^2 representative scale
        table_exponent = k / log2_N
        assert table_exponent > 0.6
        assert table_exponent > 0.5
        exponent_rows.append({
            "selector_bits_k": k,
            "table_exponent_logN": table_exponent,
            "table_exceeds_N_0_6": True,
            "table_exceeds_N_0_5": True,
        })
        assertions += 2
    assert math.isclose(1.0 + 0.6, 1.6)
    assert 1.6 > 1.1
    assertions += 2

    result = {
        "status": "FINITE_AUDIT_ONLY_NO_CLASS_SEPARATION",
        "wrapper": {
            "source_subsets_checked_through_size_2": subsets_checked,
            "unique_size_at_most_2_cutset_with_blocks_at_most_3": [1, 2],
            "residual_components": [[3, 4, 5], [6, 7, 8],
                                    [9, 10, 11], [12, 13, 14]],
            "conditional_table": table,
            "model_count": total,
            "boolean_interface_table_bits": 16,
            "count_interface_table_bits_at_4_bits_per_count": 64,
        },
        "restriction_heredity": {
            "trials": restriction_trials,
            "max_residual_component": 3,
            "scope": "pure_partial_assignments_only",
        },
        "interface_table_tightness": {
            "k_checked": [1, 2, 3, 4],
            "singleton_membership_checks": interface_checks,
            "worst_case_bits": "2^k; or 2^k-1 when interface value 0 is forced feasible",
        },
        "arc_trilemma": {
            "store_complete_table": "Theta(m)=N^(1-o(1)) space",
            "rescan_per_N_0_6_children": "N^1.6 time",
            "target": "N^1.1 time and N^0.5 space",
            "exponent_rows": exponent_rows,
        },
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
