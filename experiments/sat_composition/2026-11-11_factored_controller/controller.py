#!/usr/bin/env python3
"""Discover small interfaces and solve mixed SAT exactly with factored messages.

Python 3.10+, standard library only. This is a parameterized research solver.
Uncapped local solving is exact but can be exponential on irreducible pieces.
Discovery caps preserve the full residual as a bag; local resource caps return
UNRESOLVED. Neither cap is a wall-clock or whole-process memory limit.
"""
import argparse
import itertools
import json

from factored_solver import solve_decomposed
from separator_decomp import discover_decomposition


def lower_small_affine(n, clauses, equations, mode):
    """Compile small affine rows into the selected clause language exactly.

    For 2-CNF, all rows of arity <=2 are compiled. In general Horn mode,
    unary rows and binary equalities are compiled; binary disequality stays
    affine because its positive clause is not Horn.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError('n must be a nonnegative integer')
    output = [tuple(clause) for clause in clauses]
    remaining = []
    record = {'input_affine_rows': len(equations), 'lowered_rows': 0,
              'generated_clauses': 0, 'kept_affine_rows': 0,
              'lowered_source_indices': []}
    for index, row in enumerate(equations):
        if len(row) != 2:
            raise ValueError('an affine row needs mask and right-hand side')
        mask, rhs = row
        if (not isinstance(mask, int) or isinstance(mask, bool) or mask < 0
                or mask.bit_length() > n or rhs not in (0, 1)):
            raise ValueError('invalid affine row')
        size = mask.bit_count()
        if size > 2 or (size == 2 and mode == 'horn' and rhs == 1):
            remaining.append((mask, int(rhs)))
            continue
        variables = []
        working = mask
        while working:
            bit = working & -working
            variables.append(bit.bit_length())
            working ^= bit
        before = len(output)
        if not variables:
            if rhs:
                output.append(())
        elif len(variables) == 1:
            output.append((variables[0] if rhs else -variables[0],))
        else:
            left, right = variables
            if rhs:
                output.extend(((left, right), (-left, -right)))
            else:
                output.extend(((-left, right), (left, -right)))
        record['lowered_rows'] += 1
        record['generated_clauses'] += len(output) - before
        record['lowered_source_indices'].append(index)
    record['kept_affine_rows'] = len(remaining)
    return output, remaining, record


def _backend_totals(answer):
    summed = ('candidate_products', 'rejected_products', 'seeds_attempted',
              'closure_calls', 'closure_work', 'closure_edge_scans',
              'closure_incidence_scans', 'consistency_variable_scans',
              'gaussian_pivot_tests', 'affine_rows_processed')
    maxima = ('peak_polynomial_terms', 'peak_live_polynomial_terms',
              'max_prospective_polynomial_terms')
    totals = {name: 0 for name in summed}
    totals.update({name: 0 for name in maxima})
    for bag in answer.get('bag_results', []):
        for state in bag['states']:
            counters = state['backend']['counters']
            for name in summed:
                totals[name] += counters.get(name, 0)
            for name in maxima:
                totals[name] = max(totals[name], counters.get(name, 0))
    return totals


def solve_auto(n, clauses, equations, mode='2cnf', strategy='polynomial',
               max_separator=None, candidate_cap=100000, max_splits=None,
               term_cap=None, seed_cap=None):
    """Normalize, discover, validate, solve, and verify the original witness."""
    if mode not in ('2cnf', 'horn'):
        raise ValueError('mode must be 2cnf or horn')
    bound = 2 if mode == '2cnf' else 1
    if max_separator is None:
        max_separator = bound
    if (not isinstance(max_separator, int) or isinstance(max_separator, bool)
            or max_separator not in range(bound + 1)):
        raise ValueError('separator exceeds the selected message language')
    for name, value in (('candidate_cap', candidate_cap), ('max_splits', max_splits)):
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            raise ValueError(name + ' must be nonnegative or None')
    original_clauses = [tuple(clause) for clause in clauses]
    original_equations = [tuple(row) for row in equations]
    compiled, affine, preprocessing = lower_small_affine(n, original_clauses, original_equations, mode)
    # Preserve the polynomial affine terminal before binary row lowering turns
    # equalities into nonunit clauses. Validate even when discovery is skipped.
    unit_affine_input = True
    constant_false_clause = False
    active = set()
    for clause in original_clauses:
        if mode == '2cnf' and len(clause) > 2:
            raise ValueError('a 2-CNF clause has more than two literals')
        if any(not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > n
               for lit in clause):
            raise ValueError('invalid clause literal')
        active.update(abs(lit) - 1 for lit in clause)
        unique = set(clause)
        tautological = any(-lit in unique for lit in unique)
        if mode == 'horn' and not tautological and sum(lit > 0 for lit in unique) > 1:
            raise ValueError('a nontautological input clause is not Horn')
        constant_false_clause |= not unique
        unit_affine_input &= tautological or len(unique) <= 1
    if unit_affine_input or constant_false_clause:
        for mask, _ in original_equations:
            while mask:
                bit = mask & -mask
                active.add(bit.bit_length() - 1)
                mask ^= bit
        compiled, affine = original_clauses, original_equations
        preprocessing = {'input_affine_rows': len(affine), 'lowered_rows': 0,
                         'generated_clauses': 0, 'kept_affine_rows': len(affine),
                         'lowered_source_indices': [], 'path': 'original_unit_affine_terminal'}
        decomposition = {'bags': [sorted(active)], 'edges': [],
                         'discovery_counters': {'discovery_skipped_for_affine_terminal': True,
                                                'bags': 1, 'tree_edges': 0,
                                                'largest_bag': len(active),
                                                'separator_candidates': 0,
                                                'observed_max_separator': 0}}
    else:
        preprocessing['path'] = 'small_affine_lowering_then_separator_discovery'
        decomposition = discover_decomposition(n, compiled, affine, max_separator,
                                              candidate_cap, max_splits)
    answer = solve_decomposed(n, compiled, affine, decomposition, mode,
                              strategy, term_cap, seed_cap)
    answer['decomposition'] = decomposition
    answer['preprocessing'] = preprocessing
    answer['backend_totals'] = _backend_totals(answer)
    answer['original_witness_checks'] = {'clauses': 0, 'affine_rows': 0}
    if answer['status'] == 'SAT':
        witness = answer['witness']
        for clause in original_clauses:
            answer['original_witness_checks']['clauses'] += 1
            if not any(bool((witness >> (abs(literal) - 1)) & 1) == (literal > 0)
                       for literal in clause):
                raise AssertionError('witness violates a pre-normalization clause')
        for mask, rhs in original_equations:
            answer['original_witness_checks']['affine_rows'] += 1
            if (mask & witness).bit_count() % 2 != rhs:
                raise AssertionError('witness violates a pre-normalization affine row')
    return answer


def selector_encoding(n, clauses):
    """Exact prior selector reduction, densely relabeled before bit allocation."""
    clauses = tuple(tuple(clause) for clause in clauses)
    if (not isinstance(n, int) or isinstance(n, bool) or n < 0
            or any(not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > n
                   for clause in clauses for lit in clause)):
        raise ValueError('invalid CNF input')
    identifiers = sorted({abs(lit) for clause in clauses for lit in clause})
    renaming = {old: new + 1 for new, old in enumerate(identifiers)}
    dense_clauses = [tuple(renaming[abs(lit)] * (1 if lit > 0 else -1)
                          for lit in clause) for clause in clauses]
    next_name = len(identifiers) + 1
    horn, equations = [], []
    for clause in dense_clauses:
        selectors = list(range(next_name, next_name + len(clause)))
        next_name += len(clause)
        equations.append((sum(1 << (name - 1) for name in selectors), 1))
        horn.extend((-left, -right) for left, right in itertools.combinations(selectors, 2))
        horn.extend((-selector, literal) for selector, literal in zip(selectors, clause))
    return next_name - 1, horn, equations, identifiers, dense_clauses


def solve_cnf(n, clauses, **options):
    size, horn, equations, identifiers, dense_original = selector_encoding(n, clauses)
    answer = solve_auto(size, horn, equations, mode='2cnf', **options)
    answer['selector_bridge'] = {'original_occurring_variables': len(identifiers),
                                'encoded_variables': size, 'horn_binary_clauses': len(horn),
                                'input_parity_rows': len(equations)}
    if answer['status'] == 'SAT':
        encoded = answer['witness']
        dense = encoded & ((1 << len(identifiers)) - 1)
        if not all(any(bool((dense >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
                   for clause in dense_original):
            raise AssertionError('selector witness violates original CNF')
        answer['encoded_witness'] = encoded
        answer['witness'] = dense
        answer['original_cnf_clause_checks'] = len(dense_original)
        answer['original_assignment'] = {str(old): bool((dense >> index) & 1)
                                          for index, old in enumerate(identifiers)}
    return answer


def read_dimacs(path):
    n, expected, clauses, current = None, None, [], []
    with open(path, encoding='utf-8') as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith('c'):
                continue
            if line.startswith('p'):
                header = line.split()
                if n is not None or len(header) != 4 or header[:2] != ['p', 'cnf']:
                    raise ValueError('expected one DIMACS CNF header')
                n, expected = map(int, header[2:])
                if n < 0 or expected < 0:
                    raise ValueError('negative DIMACS dimensions')
                continue
            if n is None:
                raise ValueError('DIMACS clauses precede header')
            for token in line.split():
                literal = int(token)
                if literal:
                    if abs(literal) > n:
                        raise ValueError('DIMACS literal exceeds declared range')
                    current.append(literal)
                else:
                    clauses.append(tuple(current))
                    current = []
    if n is None or current or len(clauses) != expected:
        raise ValueError('malformed DIMACS clause count or terminator')
    return n, clauses


def compact_result(answer):
    """CLI view; the API and --full-audit retain every message and local witness."""
    keys = ('status', 'witness', 'reason', 'counters', 'backend_totals',
            'preprocessing', 'original_witness_checks', 'selector_bridge',
            'encoded_witness', 'original_assignment', 'original_cnf_clause_checks')
    output = {key: answer[key] for key in keys if key in answer}
    if 'preprocessing' in output:
        output['preprocessing'] = {key: value for key, value in output['preprocessing'].items()
                                   if key != 'lowered_source_indices'}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('2cnf', 'horn', 'cnf'))
    parser.add_argument('input', help='mixed JSON or CNF DIMACS file')
    parser.add_argument('--strategy', choices=('polynomial', 'seeds'), default='polynomial')
    parser.add_argument('--max-separator', type=int, choices=(0, 1, 2))
    parser.add_argument('--candidate-cap', type=int, default=100000)
    parser.add_argument('--split-cap', type=int)
    parser.add_argument('--unlimited-discovery', action='store_true',
                        help='remove pair-candidate cap; the polynomial split cap remains')
    parser.add_argument('--term-cap', type=int, default=100000)
    parser.add_argument('--seed-cap', type=int, default=100000)
    parser.add_argument('--uncapped', action='store_true', help='uncap local exact search only')
    parser.add_argument('--full-audit', action='store_true', help='include complete messages and bags')
    args = parser.parse_args()
    options = dict(strategy=args.strategy, max_separator=args.max_separator,
                   candidate_cap=None if args.unlimited_discovery else args.candidate_cap,
                   max_splits=args.split_cap, term_cap=None if args.uncapped else args.term_cap,
                   seed_cap=None if args.uncapped else args.seed_cap)
    if args.mode == 'cnf':
        n, clauses = read_dimacs(args.input)
        answer = solve_cnf(n, clauses, **options)
    else:
        with open(args.input, encoding='utf-8') as handle:
            data = json.load(handle)
        answer = solve_auto(data['n'], data['clauses'], data.get('equations', []),
                            mode=args.mode, **options)
    print(json.dumps(answer if args.full_audit else compact_result(answer), indent=2))


if __name__ == '__main__':
    main()
