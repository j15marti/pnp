#!/usr/bin/env python3
"""Independent finite audit for HORN-TRANSPORT-CEILING100 (stdlib only)."""
from __future__ import annotations

import itertools
import json
import random


def clause_true(clause, assignment):
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def cnf_true(clauses, assignment):
    return all(clause_true(clause, assignment) for clause in clauses)


def baseline(q, bits):
    # z_0,...,z_q,u,v use one-based variable identifiers.
    z = list(range(1, q + 2))
    u, v = q + 2, q + 3
    clauses = [(z[0], u), (z[0], -u), (-z[-1], v), (-z[-1], -v)]
    for i, bit in enumerate(bits, start=1):
        clauses.append((-z[i - 1], z[i] if bit else -z[i]))
    return clauses, q + 3


def satisfiable(clauses, n):
    for assignment in itertools.product((False, True), repeat=n):
        if cnf_true(clauses, assignment):
            return True
    return False


def pad_binary(clauses, n):
    out = []
    next_var = n + 1
    for a, b in clauses:
        out.extend(((a, b, next_var), (a, b, -next_var)))
        next_var += 1
    return out, next_var - 1


def horn_selector_lift(source, n):
    out = []
    next_var = n + 1
    source_word_positions = []
    for clause in source:
        selectors = tuple(range(next_var, next_var + 3))
        next_var += 3
        out.append(selectors)
        positions = []
        for selector, literal in zip(selectors, clause):
            out.append((-selector, literal))
            positions.append((len(out) - 1, 1))
        source_word_positions.append(tuple(positions))
    return out, next_var - 1, source_word_positions


def record_signature(clauses):
    return tuple((len(c), tuple(abs(x) for x in c)) for c in clauses)


def max_clause_matching(clauses):
    """Return clause->variable matching, or None if no saturating matching."""
    owner = {}

    def augment(ci, seen):
        for lit in clauses[ci]:
            var = abs(lit)
            if var in seen:
                continue
            seen.add(var)
            if var not in owner or augment(owner[var], seen):
                owner[var] = ci
                return True
        return False

    for ci in range(len(clauses)):
        if not augment(ci, set()):
            return None
    result = [None] * len(clauses)
    for var, ci in owner.items():
        result[ci] = var
    return result


def matched_witness(clauses, n, matching):
    assignment = [False] * n
    for clause, var in zip(clauses, matching):
        lit = next(lit for lit in clause if abs(lit) == var)
        assignment[var - 1] = lit > 0
    return assignment


def random_degree_three_source(rng, n, attempts=40):
    degree = [0] * n
    clauses = []
    for _ in range(attempts):
        available = [v + 1 for v, d in enumerate(degree) if d < 3]
        if len(available) < 3 or rng.random() < 0.2:
            break
        vars_ = rng.sample(available, 3)
        clause = tuple(v if rng.getrandbits(1) else -v for v in vars_)
        clauses.append(clause)
        for v in vars_:
            degree[v - 1] += 1
    return clauses


def raw_restrict(clauses, selected, values):
    value = dict(zip(selected, values))
    residual = []
    for clause in clauses:
        kept = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var not in value:
                kept.append(lit)
            elif value[var] == (lit > 0):
                satisfied = True
                break
        if not satisfied:
            residual.append(tuple(kept))
    return residual


def is_horn(clauses):
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in clauses)


def strong_backdoor_minimum(clauses, candidates, target):
    predicate = (lambda cs: all(len(c) <= 2 for c in cs)) if target == "2cnf" else is_horn
    for size in range(len(candidates) + 1):
        for selected in itertools.combinations(candidates, size):
            if all(predicate(raw_restrict(clauses, selected, values))
                   for values in itertools.product((False, True), repeat=size)):
                return size
    raise AssertionError("no strong backdoor")


def selector_formula(m):
    clauses = []
    selectors = []
    source_var = 3 * m + 1
    for j in range(m):
        triple = tuple(range(3 * j + 1, 3 * j + 4))
        selectors.extend(triple)
        clauses.append(triple)
        clauses.extend((-s, source_var + 3 * j + a) for a, s in enumerate(triple))
    return clauses, selectors


def main():
    assertions = 0
    chain_instances = 0
    target_rows = []
    for q in range(1, 8):
        all_one = None
        for bits in itertools.product((0, 1), repeat=q):
            base, n0 = baseline(q, bits)
            sat = satisfiable(base, n0)
            assert sat == (not all(bits))
            assertions += 1
            chain_instances += 1
            padded, npad = pad_binary(base, n0)
            lifted, ntarget, positions = horn_selector_lift(padded, npad)
            assert npad == 2 * q + 7
            assert len(padded) == 2 * q + 8
            assert ntarget == 8 * q + 31
            assert len(lifted) == 8 * q + 32
            assertions += 4
            if all(bits):
                all_one = (lifted, positions)
        lifted_one, positions_one = all_one
        sig = record_signature(lifted_one)
        sensitivity_sets = []
        for i in range(q):
            bits = [1] * q
            bits[i] = 0
            base, n0 = baseline(q, bits)
            padded, npad = pad_binary(base, n0)
            lifted_flip, _, _ = horn_selector_lift(padded, npad)
            assert record_signature(lifted_flip) == sig
            changed = []
            for ci, (c0, c1) in enumerate(zip(lifted_one, lifted_flip)):
                for li, (x0, x1) in enumerate(zip(c0, c1)):
                    if x0 != x1:
                        assert abs(x0) == abs(x1) and x0 == -x1
                        changed.append((ci, li))
            assert len(changed) == 2
            sensitivity_sets.append(frozenset(changed))
            assertions += 4
        assert len(set().union(*sensitivity_sets)) == 2 * q
        assert all(a.isdisjoint(b) for i, a in enumerate(sensitivity_sets)
                   for b in sensitivity_sets[i + 1:])
        words = 4 * len(lifted_one) + 2
        assert words == 32 * q + 130
        assert q - words < 0
        assertions += 4
        target_rows.append({
            "q": q,
            "target_variables": 8 * q + 31,
            "target_clauses": 8 * q + 32,
            "target_words": words,
            "necessary_disjoint_sensitivity_reads": q,
            "paid_transport_numerator_upper_bound": q - words,
        })

    rng = random.Random(20261023100)
    hall_instances = 0
    hall_clauses = 0
    for _ in range(600):
        n = rng.randint(3, 24)
        clauses = random_degree_three_source(rng, n)
        matching = max_clause_matching(clauses)
        assert matching is not None
        assignment = matched_witness(clauses, n, matching)
        assert cnf_true(clauses, assignment)
        assertions += 2
        hall_instances += 1
        hall_clauses += len(clauses)

    backdoor_rows = []
    for m in range(1, 4):
        clauses, selectors = selector_formula(m)
        b2 = strong_backdoor_minimum(clauses, selectors, "2cnf")
        bh = strong_backdoor_minimum(clauses, selectors, "horn")
        assert b2 == m and bh == 2 * m
        assertions += 2
        backdoor_rows.append({"m": m, "strong_2cnf": b2, "strong_horn": bh})

    # Independent selector-extension count checks for one-clause sources.
    extension_checks = 0
    for truth_pattern in itertools.product((False, True), repeat=3):
        count = 0
        for selectors in itertools.product((False, True), repeat=3):
            positive = any(selectors)
            implications = all((not selectors[i]) or truth_pattern[i] for i in range(3))
            count += positive and implications
        expected = (1 << sum(truth_pattern)) - 1
        assert count == expected
        assertions += 1
        extension_checks += 1

    out = {
        "artifact": "HORN_TRANSPORT_CEILING100",
        "status": "COMPUTATIONAL finite verification; symbolic proofs are separate",
        "seed": 20261023100,
        "chain_instances": chain_instances,
        "target_rows": target_rows,
        "hall_instances": hall_instances,
        "hall_clauses": hall_clauses,
        "backdoor_rows": backdoor_rows,
        "selector_extension_checks": extension_checks,
        "assertions": assertions,
        "failures": 0,
        "limitations": "Finite tests do not prove asymptotic hardness or unrestricted time lower bounds; peak Python memory not measured.",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
