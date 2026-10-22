#!/usr/bin/env python3
"""Finite accounting audit for SEMANTIC-PARENT-CALL-CIRCULARITY66."""

from __future__ import annotations

import itertools
import json
import math
import random


def sat_bruteforce(n, clauses):
    steps = 0
    for bits in itertools.product((False, True), repeat=n):
        steps += 1
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in clauses):
            return True, steps
    return False, steps


def constant_semantic_child(label):
    # A one-variable SAT child or a one-variable UNSAT child.
    return [[1]] if label else [[1], [-1]]


def main():
    rng = random.Random(66)
    checks = 0
    semantic_cases = 0
    max_parent_steps = 0

    for n in range(1, 9):
        literals = [i for i in range(1, n + 1)] + [-i for i in range(1, n + 1)]
        for _ in range(120):
            clauses = [
                [rng.choice(literals) for _ in range(3)]
                for _ in range(rng.randrange(0, 4 * n + 1))
            ]
            parent_label, parent_steps = sat_bruteforce(n, clauses)
            child = constant_semantic_child(parent_label)
            child_label, _ = sat_bruteforce(1, child)
            assert child_label == parent_label
            assert parent_steps >= 1
            checks += 2
            semantic_cases += 1
            max_parent_steps = max(max_parent_steps, parent_steps)

    exponent_rows = []
    for j in range(10, 101):
        c = j / 10
        no_parent = max(1.1, 0.6 + c / 2)
        with_parent = max(c, no_parent)
        assert with_parent >= c
        if c > 1.2:
            assert no_parent < c
        checks += 2
        exponent_rows.append({
            "c": c,
            "without_parent_call": no_parent,
            "with_full_parent_call": with_parent,
        })

    space_rows = []
    for j in range(5, 101):
        s = j / 10
        with_parent = max(s, 0.5, s / 2)
        assert with_parent == s
        checks += 1
        space_rows.append({"s": s, "with_full_parent_call": with_parent})

    near_full_rows = []
    previous_beta = 0.0
    for k in range(8, 129):
        # A child of length N/log N for N=2^k has effective exponent
        # beta=log_N(N/log N)=1-log_2(k)/k, which tends to one.
        beta = 1.0 - math.log2(k) / k
        if k >= 16:
            assert beta > previous_beta
            checks += 1
        previous_beta = beta
        near_full_rows.append({"log2_N": k, "effective_beta_N_over_logN": beta})

    print(json.dumps({
        "status": "finite_accounting_audit_only_no_class_separation",
        "semantic_cases": semantic_cases,
        "max_parent_bruteforce_assignments_examined": max_parent_steps,
        "checks": checks,
        "failures": 0,
        "identity": "max(c,1.1,0.6+c/2) >= c",
        "space_identity": "max(s,0.5,s/2)=s for s>=0.5",
        "semantic_control": "constant child is exact only after parent SAT label is computed",
        "exponent_rows": exponent_rows,
        "space_rows": space_rows,
        "near_full_rows": near_full_rows,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
