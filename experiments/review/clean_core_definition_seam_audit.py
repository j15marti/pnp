#!/usr/bin/env python3
"""Finite audit for the Monotone-3SAT-(2,2) definition seam.

The symbolic theorem is elementary: an all-positive CNF is satisfied by the
all-one assignment.  This audit exhausts the smallest nonempty duplicate-free
proper exact-two-occurrence family (n=6), compares it with the correctly
signed 2P2N family on the same small universe, and runs representation,
wrapper, padding, and easy-family scope controls.
"""

from __future__ import annotations

import itertools
import json
import time
from collections import Counter


def clause_value(clause: tuple[int, ...], assignment: tuple[bool, ...]) -> bool:
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def formula_value(
    formula: tuple[tuple[int, ...], ...], assignment: tuple[bool, ...]
) -> bool:
    return all(clause_value(c, assignment) for c in formula)


def sat_count(formula: tuple[tuple[int, ...], ...], n: int) -> int:
    return sum(
        formula_value(formula, a)
        for a in itertools.product((False, True), repeat=n)
    )


def exact_positive_hypergraphs(n: int) -> list[tuple[tuple[int, ...], ...]]:
    """All simple 3-uniform hypergraphs with vertex degree exactly two."""
    clauses = tuple(itertools.combinations(range(1, n + 1), 3))
    m = 2 * n // 3
    out = []
    for chosen in itertools.combinations(clauses, m):
        degree = Counter(v for c in chosen for v in c)
        if all(degree[v] == 2 for v in range(1, n + 1)):
            out.append(chosen)
    return out


def permute_formula(
    formula: tuple[tuple[int, ...], ...], permutation: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(permutation[abs(lit) - 1] * (1 if lit > 0 else -1) for lit in c)
        for c in reversed(formula)
    )


def main() -> None:
    started = time.perf_counter()
    checks = 0
    failures: list[str] = []

    positive = exact_positive_hypergraphs(6)
    if not positive:
        failures.append("n=6 positive family unexpectedly empty")
    checks += 1

    all_ones = (True,) * 6
    sat_counts = []
    for i, f in enumerate(positive):
        checks += 1
        if not formula_value(f, all_ones):
            failures.append(f"all-ones failure at positive formula {i}")
        sat_counts.append(sat_count(f, 6))

    # Wrapper-equivalent promised deciders all return YES.  DEAD ignores a
    # dead branch; DELAY's loop count is bounded in the finite audit.
    wrappers = {
        "DIRECT": lambda f: True,
        "COPY": lambda f: bool(True),
        "DEAD": lambda f: True if f else (_ for _ in ()).throw(AssertionError()),
        "DELAY": lambda f: (sum(range(8)) >= 0),
        "INTERP": lambda f: formula_value(f, all_ones),
        "RECOMP": lambda f: formula_value(tuple(tuple(c) for c in f), all_ones),
    }
    for name, wrapper in wrappers.items():
        for i, f in enumerate(positive):
            checks += 1
            if wrapper(f) is not True:
                failures.append(f"{name} wrapper failed at positive formula {i}")

    # Clause order, variable renaming, and a textual alternate encoding do
    # not disturb the all-ones witness.
    perms = (
        (1, 2, 3, 4, 5, 6),
        (6, 5, 4, 3, 2, 1),
        (2, 3, 1, 5, 6, 4),
    )
    encoding_checks = 0
    for f in positive:
        for p in perms:
            g = permute_formula(f, p)
            checks += 1
            encoding_checks += 1
            if not formula_value(g, all_ones):
                failures.append("renaming/order control failed")
            text_encoding = "&".join(
                "(" + "|".join(map(str, clause)) + ")" for clause in g
            )
            checks += 1
            encoding_checks += 1
            if "-" in text_encoding:
                failures.append("positive alternate encoding gained a negation")

    # Independent products and redundant-clause padding stay satisfiable by
    # all ones.  The variable shift makes the two factors disjoint.
    product_checks = 0
    for left in positive[: min(12, len(positive))]:
        for right in positive[: min(12, len(positive))]:
            shifted = tuple(tuple(v + 6 for v in c) for c in right)
            product = left + shifted
            checks += 1
            product_checks += 1
            if not formula_value(product, (True,) * 12):
                failures.append("independent-product control failed")
        padded = left + (left[0],)
        checks += 1
        product_checks += 1
        if not formula_value(padded, all_ones):
            failures.append("redundant-clause padding failed")

    # Build all small correctly signed 2P2N instances by pairing two
    # exact-degree-two hypergraphs as positive and negative clause sets.
    # They need not be unsatisfiable at n=6; the purpose is to verify that
    # all-ones is no longer a universal witness and that m doubles.
    signed_total = 0
    signed_all_ones_false = 0
    signed_sat_count_range = [2**6, 0]
    for pos in positive:
        for neg_base in positive:
            neg = tuple(tuple(-v for v in c) for c in neg_base)
            f = pos + neg
            signed_total += 1
            checks += 3
            if len(f) != 8:
                failures.append("signed 2P2N clause count is not 4n/3")
            if formula_value(f, all_ones):
                failures.append("all-ones unexpectedly satisfies a signed 2P2N formula")
            else:
                signed_all_ones_false += 1
            count = sat_count(f, 6)
            signed_sat_count_range[0] = min(signed_sat_count_range[0], count)
            signed_sat_count_range[1] = max(signed_sat_count_range[1], count)

    # Scope guards: constant YES must not be exported to other families.
    # Each formula below is an elementary UNSAT member/control.
    unsat_controls = {
        "Horn": ((1,), (-1,)),
        "2SAT": ((1, 2), (-1, 2), (1, -2), (-1, -2)),
        "bounded_treewidth": ((1,), (-1,)),
        "affine_as_cnf": ((1,), (-1,)),
        "Tseitin_odd_charge": ((1,), (-1,)),
    }
    control_checks = 0
    for name, f in unsat_controls.items():
        n = max(abs(lit) for clause in f for lit in clause)
        count = sat_count(f, n)
        checks += 1
        control_checks += 1
        if count != 0:
            failures.append(f"{name} UNSAT scope guard failed")

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "MODELBRIDGE-0021",
        "claim": "CLEANCORE-DEFINITION-SEAM1",
        "status": "COMPUTATIONAL",
        "symbolic_result": {
            "all_positive_exact_two_occurrence": "all-ones satisfies every promised formula",
            "all_positive_clause_count": "m=2n/3",
            "signed_2P2N_clause_count": "m=4n/3",
            "transfer_warning": "the two promise families are not interchangeable",
        },
        "parameters": {
            "n": 6,
            "exhaustive": True,
            "random_seed": None,
        },
        "counts": {
            "positive_formulas": len(positive),
            "positive_min_satisfying_assignments": min(sat_counts) if sat_counts else None,
            "positive_max_satisfying_assignments": max(sat_counts) if sat_counts else None,
            "signed_2P2N_formulas": signed_total,
            "signed_all_ones_false": signed_all_ones_false,
            "signed_min_satisfying_assignments": signed_sat_count_range[0],
            "signed_max_satisfying_assignments": signed_sat_count_range[1],
            "encoding_checks": encoding_checks,
            "product_padding_checks": product_checks,
            "easy_family_scope_checks": control_checks,
            "assertions": checks,
            "failures": len(failures),
        },
        "wrappers": list(wrappers),
        "limitations": [
            "Finite enumeration is only a regression check.",
            "NP-completeness of signed Monotone 3-SAT-(2,2) is a literature theorem, not inferred from this audit.",
            "No runtime lower bound is inferred from satisfying-assignment counts.",
        ],
        "runtime_seconds": round(elapsed, 6),
        "failure_details": failures[:20],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
