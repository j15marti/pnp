#!/usr/bin/env python3
"""Exact finite audits for independent strict-C5 residual levels.

Run all checks: python t5_one_two_unknown_audit.py --stage all
The template checks and global-source checks can be run independently.
No external dependencies. The exhaustive source has only 5**7 assignments.
"""
import argparse
import itertools
import json
from collections import Counter

D = tuple(range(5))
TRIPLES = {frozenset((i, (i + 1) % 5, (i + 2) % 5)) for i in D}


def strict_c(a, b, c):
    return len({a, b, c}) == 3 and frozenset((a, b, c)) in TRIPLES


def templates():
    supports = sorted(
        {tuple(x for x in D if strict_c(x, a, b))
         for a, b in itertools.combinations(D, 2)},
        key=lambda s: (len(s), s),
    )
    rows = []
    for variable in (0, 1):
        for support in supports:
            mask = sum(1 << (5 * x + y) for x in D for y in D
                       if (x, y)[variable] in support)
            rows.append((['x' if variable == 0 else 'y', list(support)], mask))
    for a in D:
        mask = sum(1 << (5 * x + y) for x in D for y in D
                   if strict_c(x, y, a))
        rows.append((['Cxy', a], mask))
    full = (1 << 25) - 1
    counts = {}
    witnesses = {}
    for size in range(1, 7):
        count = 0
        witness = None
        for chosen in itertools.combinations(range(len(rows)), size):
            mask = full
            for index in chosen:
                mask &= rows[index][1]
            if mask:
                continue
            minimal = True
            for omitted in chosen:
                partial = full
                for index in chosen:
                    if index != omitted:
                        partial &= rows[index][1]
                if not partial:
                    minimal = False
                    break
            if minimal:
                count += 1
                if witness is None:
                    witness = [rows[index][0] for index in chosen]
        counts[size] = count
        witnesses[size] = witness
    assert counts == {1: 0, 2: 75, 3: 230, 4: 10, 5: 0, 6: 0}

    seen = {full}
    frontier = [full]
    while frontier:
        state = frontier.pop()
        for _, row in rows:
            nxt = state & row
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    histogram = dict(sorted(Counter(s.bit_count() for s in seen).items()))
    assert len(seen) == 157
    assert histogram == {0: 1, 1: 25, 2: 60, 3: 10, 4: 35,
                         5: 10, 6: 5, 10: 10, 25: 1}
    return {
        'unary_supports': supports,
        'nonempty_atomic_two_unknown_relations': len(rows),
        'minimal_core_counts_through_six': counts,
        'first_core_witnesses': witnesses,
        'one_unknown_states': 12,
        'two_unknown_states': len(seen),
        'two_unknown_state_cardinality_histogram': histogram,
        'exact_context_summary_fixed_bits': {'one_unknown': 4, 'two_unknown': 8},
    }


# Names a0,...,a4 are indices 0,...,4; X=5 and Y=6.
ROWS = [(i, (i + 1) % 5, (i + 2) % 5) for i in D]
ROWS += [(5, 3, 4), (5, 1, 2), (5, 6, 1), (5, 6, 4)]
REFERENCE = (0, 1, 2, 3, 4, 2, 3)


def satisfies(assignment, selected):
    return all(strict_c(*(assignment[v] for v in ROWS[j])) for j in selected)


def completions(free):
    for values in itertools.product(D, repeat=len(free)):
        assignment = list(REFERENCE)
        for variable, value in zip(free, values):
            assignment[variable] = value
        yield tuple(assignment)


def global_source():
    indices = tuple(range(len(ROWS)))
    global_count = sum(satisfies(a, indices)
                       for a in itertools.product(D, repeat=7))
    assert global_count == 0
    frame_count = sum(
        all(strict_c(a[i], a[(i + 1) % 5], a[(i + 2) % 5]) for i in D)
        for a in itertools.product(D, repeat=5)
    )
    assert frame_count == 10
    failed = [j for j in indices if not satisfies(REFERENCE, (j,))]
    assert failed == [6]

    levels = []
    for free in ((), (5,), (5, 6)):
        possible = list(completions(free))
        assert not any(satisfies(a, indices) for a in possible)
        first_core = None
        for size in range(1, len(ROWS) + 1):
            cores = [list(chosen) for chosen in itertools.combinations(indices, size)
                     if not any(satisfies(a, chosen) for a in possible)]
            if cores:
                first_core = {'free_variables': list(free),
                              'minimum_source_core_size': size,
                              'minimum_cores': cores}
                break
        levels.append(first_core)
    assert [level['minimum_source_core_size'] for level in levels] == [1, 2, 4]

    deletion_witnesses = {}
    for omitted in range(5, 9):
        selected = [j for j in indices if j != omitted]
        witness = next((a for a in completions((5, 6)) if satisfies(a, selected)), None)
        assert witness is not None
        deletion_witnesses[omitted] = list(witness)
    return {
        'variable_order': ['a0', 'a1', 'a2', 'a3', 'a4', 'X', 'Y'],
        'source_rows_zero_indexed': ROWS,
        'all_assignments_examined': 5 ** 7,
        'global_satisfying_assignments': global_count,
        'valid_anchor_frames': frame_count,
        'reference_assignment': REFERENCE,
        'reference_false_row_indices': failed,
        'independent_level_cores': levels,
        'four_core_row_deletion_witnesses': deletion_witnesses,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=('template', 'global', 'all'), default='all')
    args = parser.parse_args()
    result = {'status': 'PASS', 'stage': args.stage}
    if args.stage in ('template', 'all'):
        result['template'] = templates()
    if args.stage in ('global', 'all'):
        result['global_source'] = global_source()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
