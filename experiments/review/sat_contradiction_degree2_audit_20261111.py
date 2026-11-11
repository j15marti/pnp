#!/usr/bin/env python3
"""Finite audit of 3-CNF -> arity-3 / factor-degree-2 circuit-CSP.

This audit checks a representation theorem, not an unrestricted SAT time bound.
Clauses may contain repeated variables, repeated literals, or both polarities.
"""

from collections import Counter
from itertools import combinations_with_replacement, product
import json
import hashlib
from pathlib import Path


def reduce_to_csp(source):
    factors = []
    copies = {}
    origins = []

    def fresh(original=None):
        v = len(origins)
        origins.append(original)
        return v

    for clause in source:
        literals = []
        for literal in clause:
            original = abs(literal)
            v = fresh(original)
            copies.setdefault(original, []).append(v)
            literals.append((v, literal > 0))
        factors.append(("OR", tuple(literals)))

    for original, vs in copies.items():
        r = len(vs)
        if r == 1:
            continue
        if r <= 3:
            factors.append(("EQ", tuple(vs)))
            continue
        aux = [fresh(original) for _ in range(r - 3)]
        factors.append(("EQ", (vs[0], vs[1], aux[0])))
        for i in range(1, r - 3):
            factors.append(("EQ", (aux[i - 1], vs[i + 1], aux[i])))
        factors.append(("EQ", (aux[-1], vs[-2], vs[-1])))

    return factors, copies, origins


def expand_factors_to_cnf(factors):
    cnf = []
    for kind, data in factors:
        if kind == "OR":
            cnf.append(tuple((v + 1) if positive else -(v + 1)
                             for v, positive in data))
        else:
            assert 2 <= len(data) <= 3
            # A directed implication cycle forces all incident variables equal.
            for i, v in enumerate(data):
                w = data[(i + 1) % len(data)]
                cnf.append((-(v + 1), w + 1))
    return tuple(cnf)


def compile_cnf(cnf):
    result = []
    for clause in cnf:
        pos = neg = 0
        for literal in clause:
            if literal > 0:
                pos |= 1 << (literal - 1)
            else:
                neg |= 1 << (-literal - 1)
        result.append((pos, neg))
    return result


def sat_cnf(compiled, assignment):
    return all((assignment & pos) or ((~assignment) & neg)
               for pos, neg in compiled)


def compile_csp(factors):
    result = []
    for kind, data in factors:
        if kind == "OR":
            pos = sum(1 << v for v, positive in data if positive)
            neg = sum(1 << v for v, positive in data if not positive)
            result.append((kind, pos, neg))
        else:
            result.append((kind, sum(1 << v for v in data), 0))
    return result


def sat_csp(compiled, assignment):
    for kind, p, q in compiled:
        if kind == "OR":
            if not ((assignment & p) or ((~assignment) & q)):
                return False
        else:
            bits = assignment & p
            if bits != 0 and bits != p:
                return False
    return True


def audit_formula(source, n_original, stats):
    factors, copies, origins = reduce_to_csp(source)
    expanded = expand_factors_to_cnf(factors)
    source_eval = compile_cnf(source)
    expanded_eval = compile_cnf(expanded)
    csp_eval = compile_csp(factors)
    degree = Counter()
    for kind, data in factors:
        vs = [v for v, _ in data] if kind == "OR" else list(data)
        assert len(vs) <= 3
        assert len(vs) == len(set(vs))
        degree.update(vs)
    assert max(degree.values(), default=0) <= 2

    positive = Counter()
    negative = Counter()
    for clause in expanded:
        assert len(clause) <= 3
        for literal in clause:
            (positive if literal > 0 else negative)[abs(literal)] += 1
    assert max(positive.values(), default=0) <= 2
    assert max(negative.values(), default=0) <= 2

    source_sat = 0
    for a in range(1 << n_original):
        expected = sat_cnf(source_eval, a)
        source_sat += expected
        lifted = sum(1 << v for v, original in enumerate(origins)
                     if ((a >> (original - 1)) & 1))
        assert sat_csp(csp_eval, lifted) == expected
        assert sat_cnf(expanded_eval, lifted) == expected
        stats["source_assignments_lifted"] += 1

    csp_sat = 0
    for a in range(1 << len(origins)):
        answer = sat_csp(csp_eval, a)
        assert answer == sat_cnf(expanded_eval, a)
        stats["csp_assignments_checked"] += 1
        if answer:
            csp_sat += 1
            projected = 0
            for original, vs in copies.items():
                value = (a >> vs[0]) & 1
                assert all(((a >> v) & 1) == value for v in vs)
                if value:
                    projected |= 1 << (original - 1)
            assert sat_cnf(source_eval, projected)
    assert csp_sat * (1 << (n_original - len(copies))) == source_sat

    stats["formulas_checked"] += 1
    stats["max_csp_variables"] = max(stats["max_csp_variables"], len(origins))
    stats["max_factor_degree"] = max(stats["max_factor_degree"], max(degree.values(), default=0))
    stats["max_positive_occurrences_expanded"] = max(
        stats["max_positive_occurrences_expanded"], max(positive.values(), default=0))
    stats["max_negative_occurrences_expanded"] = max(
        stats["max_negative_occurrences_expanded"], max(negative.values(), default=0))
    stats["max_total_literal_occurrences_expanded"] = max(
        stats["max_total_literal_occurrences_expanded"],
        max((positive[v] + negative[v] for v in range(1, len(origins) + 1)), default=0))
    stats["occurrence_counts_covered"].update(len(vs) for vs in copies.values())


def main():
    stats = Counter()
    stats["occurrence_counts_covered"] = set()

    # Exhaust all unordered clauses of width at most 3 over two variables,
    # including repeated literals and the empty clause; then all multisets
    # containing 0, 1, or 2 such clauses.
    alphabet = (-2, -1, 1, 2)
    clauses = [()]
    for width in range(1, 4):
        clauses.extend(combinations_with_replacement(alphabet, width))
    assert len(clauses) == 35
    for count in range(3):
        for source in combinations_with_replacement(clauses, count):
            audit_formula(source, 2, stats)

    # Focused longer chains and an UNSAT two-variable instance requiring
    # all four non-tautological binary clauses.
    controls = [
        (((1,),), 1),
        (((1,), (-1,)), 1),
        (((1, 1, -1),), 1),
        (((1, 1), (-1, -1)), 1),
        (((1, 1, 1), (-1, -1)), 1),
        (((1, 1, 1), (-1, -1, -1)), 1),
        (((1, 1, 1), (-1, -1, -1), (1,)), 1),
        (((1, 2), (1, -2), (-1, 2), (-1, -2)), 2),
        (((1, 2), (1, -2), (-1, 2), (-1, 2)), 2),
        (((1, 2, 3), (-1, -2, 3), (1, -2, -3)), 3),
    ]
    for source, n_original in controls:
        audit_formula(source, n_original, stats)

    # Opposite SAT labels with identical factor scopes, types and GF(2) rank.
    unsat_source = ((1, 2), (1, -2), (-1, 2), (-1, -2))
    sat_source = ((1, 2), (1, -2), (-1, 2), (-1, 2))
    unsat_factors, _, unsat_origins = reduce_to_csp(unsat_source)
    sat_factors, _, sat_origins = reduce_to_csp(sat_source)

    def scopes(factors):
        return tuple((kind, tuple(v for v, _ in data)
                      if kind == "OR" else data)
                     for kind, data in factors)

    assert unsat_origins == sat_origins
    assert scopes(unsat_factors) == scopes(sat_factors)
    assert sum(sat_cnf(compile_cnf(unsat_source), a) for a in range(4)) == 0
    assert sum(sat_cnf(compile_cnf(sat_source), a) for a in range(4)) == 1
    basis = {}
    for _, vs in scopes(unsat_factors):
        row = sum(1 << v for v in vs)
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    assert len(unsat_factors) == 8
    assert len(unsat_origins) == 10
    assert len(basis) == 7
    stats["opposite_labels_same_incidence_pairs"] = 1
    stats["paired_incidence_rows"] = 8
    stats["paired_incidence_columns"] = 10
    stats["paired_incidence_gf2_rank"] = 7

    stats["occurrence_counts_covered"] = sorted(stats["occurrence_counts_covered"])
    stats["failures"] = 0
    stats["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(dict(stats), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
