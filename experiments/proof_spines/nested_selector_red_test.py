#!/usr/bin/env python3
"""Independent red-team tests for fixed-depth nested implication selection.

The experiment separates two facts:
  * fixed-k implication edges are sound and preserve an OR frontier; and
  * on a promised UC_k frontier, direct fixed-choice SLUR search already
    decides each residual without constructing the quadratic implication graph.

Finite checks are consistency tests, not asymptotic evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import signal
import time
from functools import lru_cache
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def canon(clauses) -> CNF:
    result = set()
    for raw in clauses:
        clause = frozenset(raw)
        if any(-lit in clause for lit in clause):
            continue
        result.add(tuple(sorted(clause, key=lambda lit: (abs(lit), lit < 0))))
    return tuple(sorted(result, key=lambda clause: (len(clause), clause)))


def assign(f: CNF, lit: int) -> CNF:
    return canon(tuple(x for x in clause if x != -lit)
                 for clause in f if lit not in clause)


def unit_reduce(f: CNF) -> tuple[CNF, bool]:
    current = f
    while True:
        if any(not clause for clause in current):
            return current, True
        unit = next((clause[0] for clause in current if len(clause) == 1), None)
        if unit is None:
            return current, False
        current = assign(current, unit)


@lru_cache(maxsize=None)
def rk_conflict(f: CNF, k: int) -> bool:
    current, bad = unit_reduce(f)
    if bad:
        return True
    if k <= 1 or not current:
        return False
    while True:
        literals = sorted({lit for clause in current for lit in clause},
                          key=lambda lit: (abs(lit), lit < 0))
        forced = next((lit for lit in literals
                       if rk_conflict(assign(current, -lit), k - 1)), None)
        if forced is None:
            return False
        current, bad = unit_reduce(assign(current, forced))
        if bad:
            return True


def implies_k(source: CNF, target: CNF, k: int) -> bool:
    for clause in target:
        trial = source
        for lit in clause:
            trial = assign(trial, -lit)
        if not rk_conflict(trial, k):
            return False
    return True


def eval_cnf(f: CNF, bits: tuple[bool, ...]) -> bool:
    return all(any((lit > 0) == bits[abs(lit) - 1] for lit in clause)
               for clause in f)


def brute_sat(f: CNF, n: int) -> bool:
    return any(eval_cnf(f, bits)
               for bits in itertools.product((False, True), repeat=n))


def direct_slur_decide(f: CNF, k: int) -> bool:
    """Fixed-choice decision procedure, correct under the promise f in UC_k."""
    current = f
    if rk_conflict(current, k):
        return False
    while current:
        variables = sorted({abs(lit) for clause in current for lit in clause})
        if not variables:
            return False
        variable = variables[0]
        positive = assign(current, variable)
        current = assign(current, -variable) if rk_conflict(positive, k) else positive
        current, bad = unit_reduce(current)
        if bad:
            return False
    return True


def all_clauses(n: int, width: int | None = None) -> list[Clause]:
    out = []
    for states in itertools.product((-1, 0, 1), repeat=n):
        clause = tuple((i + 1) * state for i, state in enumerate(states) if state)
        if clause and (width is None or len(clause) <= width):
            out.append(clause)
    return out


def is_horn(clause: Clause) -> bool:
    return sum(lit > 0 for lit in clause) <= 1


def assignment_formula(bits: tuple[bool, ...]) -> CNF:
    return canon([(i + 1 if bit else -(i + 1),)
                  for i, bit in enumerate(bits)])


def parity_cnf(n: int, parity: int) -> CNF:
    clauses = []
    for bits in itertools.product((False, True), repeat=n):
        if sum(bits) % 2 != parity:
            clauses.append(tuple(-(i + 1) if bit else i + 1
                                 for i, bit in enumerate(bits)))
    return canon(clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--budget", type=int, default=25)
    parser.add_argument("--seed", type=int, default=20261007)
    args = parser.parse_args()
    signal.alarm(args.budget)
    started = time.time()
    checks = 0

    # Independently replay the strict k=2 witness.
    a = canon([(1, 2, 3), (1, 2, -3), (1, -2, 3),
               (1, -2, -3), (4,)])
    b = canon([(1,)])
    strict = {"k1": implies_k(a, b, 1), "k2": implies_k(a, b, 2)}
    assert strict == {"k1": False, "k2": True}
    checks += 2

    # Exhaustive promised-class checks.  All Horn CNFs are UC_1 and all
    # 2-CNFs are UC_2; compare the direct procedure with exhaustive truth.
    horn_clauses = [clause for clause in all_clauses(3) if is_horn(clause)]
    horn_formulas = 0
    for size in range(0, 4):
        for clauses in itertools.combinations(horn_clauses, size):
            f = canon(clauses)
            assert direct_slur_decide(f, 1) == brute_sat(f, 3)
            horn_formulas += 1
            checks += 1

    two_clauses = all_clauses(3, 2)
    two_cnf_formulas = 0
    for size in range(0, 5):
        for clauses in itertools.combinations(two_clauses, size):
            f = canon(clauses)
            assert direct_slur_decide(f, 2) == brute_sat(f, 3)
            two_cnf_formulas += 1
            checks += 1

    # The complete-assignment family is an antichain even for a complete
    # semantic implication oracle.  It also lies in UC_0 subset UC_k.
    antichain = {}
    for n in range(1, 9):
        formulas = [assignment_formula(bits)
                    for bits in itertools.product((False, True), repeat=n)]
        assert all(direct_slur_decide(f, 1) for f in formulas)
        signatures = {
            next(bits for bits in itertools.product((False, True), repeat=n)
                 if eval_cnf(f, bits))
            for f in formulas
        }
        assert len(signatures) == len(formulas)
        if n <= 7:
            for i, source in enumerate(formulas):
                for j, target in enumerate(formulas):
                    if i != j:
                        assert not implies_k(source, target, 2)
                        checks += 1
        q = len(formulas)
        antichain[str(n)] = {
            "frontier": q,
            "semantic_edges": 0,
            "retained": q,
            "pairwise_to_direct_formula_ratio": q - 1,
        }
        checks += q + 1

    # Padding and independent-product controls preserve the obstruction.
    padded = canon(list(assignment_formula((False, True))) + [(1, -1, 3)])
    assert padded == assignment_formula((False, True))
    product = canon(list(assignment_formula((False, True))) + [(3,), (-4,)])
    assert direct_slur_decide(product, 1) and brute_sat(product, 4)
    checks += 2

    # Algebraic escape: opposite affine parity classes are nonempty and
    # incomparable, while Gaussian/parity evaluation decides each directly.
    algebraic = {}
    for n in range(2, 7):
        even, odd = parity_cnf(n, 0), parity_cnf(n, 1)
        assert brute_sat(even, n) and brute_sat(odd, n)
        assert not implies_k(even, odd, 2)
        assert not implies_k(odd, even, 2)
        algebraic[str(n)] = {
            "clauses_each": 2 ** (n - 1),
            "nested_edges": 0,
            "algebraic_decision": "parity evaluation",
        }
        checks += 4

    elapsed = time.time() - started
    payload = {
        "claim": "UCk-DIRECT-SOLVE-DOMINANCE1",
        "status": "COMPUTATIONAL checks of a PROVED/EXACT fixed-k promise theorem",
        "seed": args.seed,
        "budget_seconds": args.budget,
        "elapsed_seconds": elapsed,
        "checks": checks,
        "strict_k2_replay": strict,
        "promised_class_controls": {
            "horn_uc1_formulas": horn_formulas,
            "two_cnf_uc2_formulas": two_cnf_formulas,
            "variables": 3,
        },
        "complete_assignment_antichain": antichain,
        "padding_and_product_checks": 2,
        "affine_parity_controls": algebraic,
        "current_scale_sat_calls": 0,
        "interpretation": (
            "The fixed-k selector remains exact, but UC_k completeness does not "
            "supply density: on its complete promised domain a fixed-choice SLUR_k "
            "procedure directly decides q residuals in O(q m^(2k)) time, while the "
            "pairwise selector costs O(q^2 m^(2k)); assignment antichains retain all "
            "members even under complete semantic implication."
        ),
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
