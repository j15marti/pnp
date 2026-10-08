#!/usr/bin/env python3
"""Bounded audit for the q-Horn zero-child portfolio transfer.

The q-Horn test below is exhaustive over the certifying weights from the
primary definition.  It is deliberately a finite reference implementation,
not the literature's linear-time recognition/decision algorithm.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import signal
import time
from pathlib import Path

SEED = 20261007


def canon_clause(clause):
    s = set(clause)
    if any(-x in s for x in s):
        return None
    return tuple(sorted(s, key=lambda z: (abs(z), z < 0)))


def canon_formula(clauses):
    out = {canon_clause(c) for c in clauses}
    out.discard(None)
    return tuple(sorted(out, key=lambda c: (len(c), c)))


def variables(formula):
    return sorted({abs(lit) for clause in formula for lit in clause})


def satisfies(formula, assignment):
    return all(any(assignment[abs(l)] == (l > 0) for l in c) for c in formula)


def truth_sat(formula):
    vs = variables(formula)
    for bits in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if satisfies(formula, a):
            return True, a
    return False, None


def qhorn_certificate(formula):
    """Return integer weights 0,1,2 representing beta 0,1/2,1."""
    vs = variables(formula)
    for vals in itertools.product((0, 1, 2), repeat=len(vs)):
        weight = dict(zip(vs, vals))
        good = True
        for clause in formula:
            total = sum(weight[lit] if lit > 0 else 2 - weight[-lit] for lit in clause)
            if total > 2:
                good = False
                break
        if good:
            return weight
    return None


def verify_qhorn_certificate(formula, weight):
    if weight is None:
        return False
    return all(
        sum(weight[lit] if lit > 0 else 2 - weight[-lit] for lit in clause) <= 2
        for clause in formula
    )


def is_horn(formula):
    return all(sum(l > 0 for l in c) <= 1 for c in formula)


def is_antihorn(formula):
    return all(sum(l < 0 for l in c) <= 1 for c in formula)


def is_2cnf(formula):
    return all(len(c) <= 2 for c in formula)


def rename_formula(formula, flipped):
    return canon_formula(
        tuple(-lit if abs(lit) in flipped else lit for lit in clause)
        for clause in formula
    )


def is_renamable_horn(formula):
    vs = variables(formula)
    for bits in itertools.product((False, True), repeat=len(vs)):
        flipped = {v for v, b in zip(vs, bits) if b}
        if is_horn(rename_formula(formula, flipped)):
            return True
    return False


def restrict(formula, partial):
    residual = []
    for clause in formula:
        kept = []
        satisfied_clause = False
        for lit in clause:
            v = abs(lit)
            if v not in partial:
                kept.append(lit)
            elif partial[v] == (lit > 0):
                satisfied_clause = True
                break
        if not satisfied_clause:
            residual.append(tuple(kept))
    return canon_formula(residual)


def has_strong_horn_backdoor(formula, max_size):
    vs = variables(formula)
    for size in range(max_size + 1):
        for subset in itertools.combinations(vs, size):
            if all(
                is_horn(restrict(formula, dict(zip(subset, bits))))
                for bits in itertools.product((False, True), repeat=size)
            ):
                return True
    return False


def all_clauses(n, max_width=3):
    lits = tuple(range(1, n + 1)) + tuple(range(-1, -n - 1, -1))
    out = []
    for width in range(1, max_width + 1):
        for c in itertools.combinations(lits, width):
            cc = canon_clause(c)
            if cc is not None:
                out.append(cc)
    return sorted(set(out), key=lambda c: (len(c), c))


def strict_search():
    rng = random.Random(SEED)
    # Generate from one explicit q-Horn certificate, then demand strict
    # escape from every smaller portfolio member below.
    seed_weight = {1: 0, 2: 2, 3: 1, 4: 1, 5: 1}
    pool = [
        c for c in all_clauses(5, 3)
        if sum(seed_weight[l] if l > 0 else 2 - seed_weight[-l] for l in c) <= 2
    ]
    checked = 0
    # Seeded search is bounded and reproducible.  A witness is rechecked below.
    for clause_count in range(5, 13):
        for _ in range(16000):
            f = canon_formula(rng.sample(pool, clause_count))
            checked += 1
            cert = qhorn_certificate(f)
            if cert is None:
                continue
            if is_horn(f) or is_antihorn(f) or is_2cnf(f) or is_renamable_horn(f):
                continue
            phases = []
            vs = variables(f)
            for bit in (False, True):
                phases.append(satisfies(f, {v: bit for v in vs}))
            if any(phases):
                continue
            if has_strong_horn_backdoor(f, 2):
                continue
            return f, cert, checked
    raise AssertionError("no strict q-Horn witness found within seeded budget")


def product_formula(formula, copies):
    n = max(variables(formula), default=0)
    clauses = []
    for j in range(copies):
        off = j * n
        clauses.extend(tuple((abs(l) + off) * (1 if l > 0 else -1) for l in c) for c in formula)
    return canon_formula(clauses)


def complement_all(formula):
    return canon_formula(tuple(-lit for lit in c) for c in formula)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    signal.alarm(25)
    start = time.perf_counter()
    checks = 0

    strict, cert, search_checks = strict_search()
    checks += search_checks
    assert verify_qhorn_certificate(strict, cert)
    checks += 1
    sat, model = truth_sat(strict)
    assert sat and model is not None
    checks += 1
    assert not any((is_horn(strict), is_antihorn(strict), is_2cnf(strict), is_renamable_horn(strict)))
    checks += 4
    assert not has_strong_horn_backdoor(strict, 2)
    checks += 1

    controls = {}
    families = {
        "horn_chain": canon_formula([(-1, 2), (-2, 3), (-3, 4), (1,)]),
        "antihorn_chain": canon_formula([(1, -2), (2, -3), (3, -4), (-1,)]),
        "two_cnf_cycle": canon_formula([(1, 2), (-2, 3), (-3, -1)]),
        "contradictory_units": canon_formula([(1,), (-1,)]),
        "strict_qhorn": strict,
        "strict_complement": complement_all(strict),
        "strict_product_3": product_formula(strict, 3),
        "positive_4_clause": canon_formula([(1, 2, 3, 4)]),
    }
    for name, formula in families.items():
        qcert = qhorn_certificate(formula)
        sat_value, _ = truth_sat(formula)
        if qcert is not None:
            assert verify_qhorn_certificate(formula, qcert)
            checks += 1
        controls[name] = {
            "clauses": len(formula),
            "variables": len(variables(formula)),
            "qhorn": qcert is not None,
            "sat": sat_value,
            "horn": is_horn(formula),
            "antihorn": is_antihorn(formula),
            "two_cnf": is_2cnf(formula),
            "renamable_horn": is_renamable_horn(formula),
            "fixed_all_false": satisfies(formula, {v: False for v in variables(formula)}),
            "fixed_all_true": satisfies(formula, {v: True for v in variables(formula)}),
        }
        checks += 7

    # Certificate invariance under a signed permutation.
    renamed = rename_formula(strict, {1, 3})
    assert qhorn_certificate(renamed) is not None
    assert truth_sat(renamed)[0] == sat
    checks += 2

    # Tautological padding normalizes away and changes no classification.
    padded = canon_formula(list(strict) + [(1, -1, 2), (2, -2, 3)])
    assert padded == strict
    checks += 1

    gamma = 1.8019377358048383
    endpoint_cells = {
        "safe_linear_time_linear_space": {"C": 1.0, "sigma": 1.0},
        "hypothetical_linear_time_log_space": {"C": 1.0, "sigma": 0.0},
    }
    for cell in endpoint_cells.values():
        cell["sum"] = cell["C"] + cell["sigma"]
        cell["below_gamma"] = cell["sum"] < gamma
        checks += 1

    result = {
        "status": "COMPUTATIONAL",
        "claim": "QHORN-VALUE1 strict finite coverage and QHORN-SPACE-GATE1 accounting",
        "seed": SEED,
        "elapsed_seconds": time.perf_counter() - start,
        "checks": checks,
        "search_candidates_checked": search_checks,
        "strict_witness": [list(c) for c in strict],
        "strict_certificate_integer_weights": cert,
        "strict_has_size_two_strong_horn_backdoor": has_strong_horn_backdoor(strict, 2),
        "controls": controls,
        "endpoint_cells": endpoint_cells,
        "williams_gamma": gamma,
        "limitations": [
            "Finite exhaustive certificate/model checks do not implement the literature linear-time algorithm.",
            "The safe (1,1) exponent cell is an upper-bound ledger, not a space lower bound.",
            "No all-CNF coverage, ARC closure, or separation follows.",
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({
        "checks": checks,
        "elapsed_seconds": result["elapsed_seconds"],
        "strict_witness": result["strict_witness"],
        "sha256": hashlib.sha256(payload.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
