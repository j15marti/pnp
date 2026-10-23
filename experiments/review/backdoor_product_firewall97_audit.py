#!/usr/bin/env python3
"""Independent finite audit for BACKDOOR-PRODUCT-FIREWALL97.

Stdlib only.  This verifies the disjoint-product extension of the
SHARED-SWITCH-MINIMAL-UNSAT57 family and its exact syntactic 2-CNF
backdoor number on finite controls.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path


Literal = tuple[int, bool]  # (variable id, positive?)
Clause = tuple[Literal, Literal, Literal]


def add_copy(q: int, sigma: tuple[int, ...], offset: int) -> tuple[list[Clause], int]:
    assert q >= 3 and len(sigma) == q
    xs = [offset + i for i in range(q)]
    s, t, y1, y2 = (offset + q + i for i in range(4))
    clauses: list[Clause] = []
    for i, bit in enumerate(sigma):
        a, b = xs[i], xs[(i + 1) % q]
        if bit:
            clauses.extend([((s, True), (a, True), (b, True)),
                            ((s, True), (a, False), (b, False))])
        else:
            clauses.extend([((s, True), (a, False), (b, True)),
                            ((s, True), (a, True), (b, False))])
    clauses.extend([
        ((s, False), (t, True), (y1, True)),
        ((s, False), (t, True), (y1, False)),
        ((s, False), (t, False), (y2, True)),
        ((s, False), (t, False), (y2, False)),
    ])
    return clauses, q + 4


def product_formula(q: int, sigmas: tuple[tuple[int, ...], ...]) -> tuple[list[Clause], int]:
    clauses: list[Clause] = []
    offset = 0
    for sigma in sigmas:
        part, width = add_copy(q, sigma, offset)
        clauses.extend(part)
        offset += width
    return clauses, offset


def sat_count(clauses: list[Clause], n: int) -> int:
    total = 0
    for mask in range(1 << n):
        if all(any(bool(mask & (1 << v)) == positive for v, positive in c)
               for c in clauses):
            total += 1
    return total


def hits_all_ternaries(clauses: list[Clause], chosen: frozenset[int]) -> bool:
    return all(any(v in chosen for v, _ in c) for c in clauses)


def brute_backdoor_number(clauses: list[Clause], n: int) -> int:
    # For proper width-three CNF, a strong syntactic 2-CNF backdoor is
    # exactly a variable hitting set of all ternary supports.
    for h in range(n + 1):
        for subset in itertools.combinations(range(n), h):
            if hits_all_ternaries(clauses, frozenset(subset)):
                return h
    raise AssertionError("unreachable")


def proper(clauses: list[Clause]) -> bool:
    for c in clauses:
        variables = [v for v, _ in c]
        if len(c) != 3 or len(set(variables)) != 3:
            return False
    return True


def main() -> None:
    assertions = 0
    brute_assignments = 0
    deletion_checks = 0
    cases = []

    # Both labels and exact model counts for one copy.
    for q in (3, 4, 5):
        for sigma in itertools.product((0, 1), repeat=q):
            clauses, n = product_formula(q, (sigma,))
            count = sat_count(clauses, n)
            brute_assignments += 1 << n
            expected = 16 if sum(sigma) % 2 == 0 else 0
            assert count == expected
            assert proper(clauses)
            assert brute_backdoor_number(clauses, n) == 1
            assertions += 3
            cases.append({"p": 1, "q": q, "sigma": list(sigma), "models": count})

    # Exact disjoint-product count and exact backdoor p for small products.
    product_controls = [
        (3, ((0, 0, 0), (1, 1, 0))),       # SAT, 16^2 models
        (3, ((0, 0, 0), (1, 0, 0))),       # UNSAT
        (4, ((0, 0, 0, 0), (1, 1, 0, 0))), # SAT
    ]
    for q, sigmas in product_controls:
        clauses, n = product_formula(q, sigmas)
        count = sat_count(clauses, n)
        brute_assignments += 1 << n
        expected = 16 ** len(sigmas) if all(sum(s) % 2 == 0 for s in sigmas) else 0
        assert count == expected
        assert brute_backdoor_number(clauses, n) == len(sigmas)
        assert proper(clauses)
        assertions += 3
        cases.append({"p": len(sigmas), "q": q, "models": count,
                      "backdoor": len(sigmas)})

    # Every clause is necessary on an odd one-copy input.
    q = 5
    sigma = (1, 0, 0, 0, 0)
    clauses, n = product_formula(q, (sigma,))
    assert sat_count(clauses, n) == 0
    brute_assignments += 1 << n
    assertions += 1
    for j in range(len(clauses)):
        assert sat_count(clauses[:j] + clauses[j + 1:], n) > 0
        brute_assignments += 1 << n
        deletion_checks += 1
        assertions += 1

    # All-even p-product is sensitive to every orientation bit.
    for p, q in ((1, 3), (2, 3), (4, 5), (8, 7)):
        base = [[0] * q for _ in range(p)]
        assert all(sum(s) % 2 == 0 for s in base)
        for a in range(p):
            for i in range(q):
                flipped = [row[:] for row in base]
                flipped[a][i] ^= 1
                assert not all(sum(s) % 2 == 0 for s in flipped)
                assertions += 1
        # Exact structural counts and transport-margin check.
        clauses, n = product_formula(q, tuple(tuple(s) for s in base))
        m = p * (2 * q + 4)
        assert n == p * (q + 4) and len(clauses) == m
        assert m > p * q  # materialized clause-record writes consume source query bound
        assertions += 2

    payload = {
        "artifact": "BACKDOOR-PRODUCT-FIREWALL97",
        "status": "COMPUTATIONAL finite audit; exact lemmas proved separately",
        "assertions": assertions,
        "failures": 0,
        "brute_force_source_assignments": brute_assignments,
        "clause_deletion_checks": deletion_checks,
        "tested_cases": cases,
        "asymptotic_family": {
            "variables": "n=p(q+4)",
            "clauses": "m=p(2q+4)",
            "minimum_strong_2cnf_backdoor": "h=p",
            "models": "16^p iff every component parity is even; otherwise 0",
            "decision": "O(pq) addressed-word operations after grammar recognition",
            "input_word_lower_bound": "pq on the all-even member",
            "materializing_transport": "R >= p(2q+4) record writes > L_old=pq",
        },
    }
    out = Path(__file__).resolve().parents[2] / "results/raw/review/BACKDOOR_PRODUCT_FIREWALL97_raw.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
