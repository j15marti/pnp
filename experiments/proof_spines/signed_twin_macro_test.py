#!/usr/bin/env python3
"""Exact finite audit for the SIGNED-TWIN-MACRO1 CNF quotient.

The program uses exhaustive truth tables only on small formulas.  It tests
the semantic theorem, hostile near-twins, independent products, duplicate
padding normalization, and a concrete monotone token-length ledger.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import signal
import time
from pathlib import Path


Literal = int
Clause = tuple[Literal, ...]
CNF = tuple[Clause, ...]


def canonical_clause(clause: list[int] | tuple[int, ...]) -> Clause | None:
    lits = set(clause)
    if any(-lit in lits for lit in lits):
        return None
    return tuple(sorted(lits, key=lambda lit: (abs(lit), lit < 0)))


def canonical_cnf(clauses: list[list[int] | tuple[int, ...]] | tuple[Clause, ...]) -> CNF:
    out = set()
    for clause in clauses:
        normalized = canonical_clause(clause)
        if normalized is not None:
            out.add(normalized)
    return tuple(sorted(out, key=lambda c: (len(c), c)))


def restrict(cnf: CNF, assignment: dict[int, bool]) -> CNF:
    residual: list[Clause] = []
    for clause in cnf:
        satisfied = False
        kept: list[int] = []
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                kept.append(lit)
                continue
            value = assignment[var]
            if (lit > 0 and value) or (lit < 0 and not value):
                satisfied = True
                break
        if not satisfied:
            residual.append(tuple(kept))
    return canonical_cnf(residual)


def variables(cnf: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in cnf for lit in clause}))


def sat(cnf: CNF) -> bool:
    vs = variables(cnf)
    for bits in itertools.product((False, True), repeat=len(vs)):
        if not restrict(cnf, dict(zip(vs, bits))):
            return True
    return False


def signed_profile(cnf: CNF, var: int) -> tuple[int, ...]:
    profile = []
    for clause in cnf:
        profile.append(1 if var in clause else (-1 if -var in clause else 0))
    return tuple(profile)


def twin_classes(cnf: CNF) -> tuple[tuple[int, ...], ...]:
    groups: dict[tuple[int, ...], list[int]] = {}
    for var in variables(cnf):
        groups.setdefault(signed_profile(cnf, var), []).append(var)
    return tuple(sorted(tuple(group) for group in groups.values() if len(group) >= 2))


def signed_twin_children(cnf: CNF, group: tuple[int, ...]) -> tuple[CNF, ...]:
    assert len(group) >= 2
    profiles = {signed_profile(cnf, var) for var in group}
    assert len(profiles) == 1
    all_zero = {var: False for var in group}
    all_one = {var: True for var in group}
    mixed = {var: False for var in group}
    mixed[group[1]] = True
    # Deduplication is allowed: the fanout is at most three.
    return tuple(dict.fromkeys((
        restrict(cnf, all_zero),
        restrict(cnf, all_one),
        restrict(cnf, mixed),
    )))


def token_length(cnf: CNF) -> int:
    # A deletion-monotone word encoding: header, clause delimiters, literals.
    return 1 + len(cnf) + sum(len(clause) for clause in cnf)


def check_semantics(cnf: CNF, group: tuple[int, ...]) -> tuple[bool, tuple[int, ...]]:
    children = signed_twin_children(cnf, group)
    exact = sat(cnf) == any(sat(child) for child in children)
    sizes = tuple(token_length(child) for child in children)
    return exact, sizes


def family_clauses(group: tuple[int, ...], outside: int) -> tuple[Clause, ...]:
    clauses: list[Clause] = [(), (outside,), (-outside,)]
    for sign in (1, -1):
        base = tuple(sign * var for var in group)
        clauses.extend((base, base + (outside,), base + (-outside,)))
    return canonical_cnf(clauses)


def random_twin_formula(rng: random.Random, n: int, group: tuple[int, ...]) -> CNF:
    outside = [v for v in range(1, n + 1) if v not in group]
    clauses: list[list[int]] = []
    for _ in range(rng.randint(0, 2 * n + 5)):
        clause: list[int] = []
        if rng.random() < 0.7:
            sign = rng.choice((-1, 1))
            clause.extend(sign * v for v in group)
        for v in outside:
            if rng.random() < 0.25:
                clause.append(rng.choice((-1, 1)) * v)
        clauses.append(clause)
    return canonical_cnf(clauses)


def renamed(cnf: CNF, offset: int) -> CNF:
    return canonical_cnf([
        [((1 if lit > 0 else -1) * (abs(lit) + offset)) for lit in clause]
        for clause in cnf
    ])


def run(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    counters = {
        "exhaustive_formulas": 0,
        "exhaustive_truth_checks": 0,
        "random_formulas": 0,
        "random_truth_checks": 0,
        "near_twin_rejections": 0,
        "independent_product_checks": 0,
        "padding_checks": 0,
        "size_monotonicity_checks": 0,
        "threshold_accepts": 0,
        "threshold_rejects": 0,
    }
    max_child_ratio = 0.0
    max_fanout = 0

    # Exhaust all duplicate-free subsets of the nine clause types for two
    # different twin-class sizes.  This includes the empty clause.
    for group, outside in (((1, 2), 3), ((1, 2, 3), 4)):
        universe = family_clauses(group, outside)
        for mask in range(1 << len(universe)):
            cnf = tuple(universe[i] for i in range(len(universe)) if mask & (1 << i))
            exact, sizes = check_semantics(cnf, group)
            assert exact
            counters["exhaustive_formulas"] += 1
            counters["exhaustive_truth_checks"] += 1 + len(signed_twin_children(cnf, group))
            parent_size = token_length(cnf)
            for child_size in sizes:
                assert child_size <= parent_size
                counters["size_monotonicity_checks"] += 1
                max_child_ratio = max(max_child_ratio, child_size / parent_size)
            max_fanout = max(max_fanout, len(sizes))

    # Seeded larger samples.
    for _ in range(2000):
        n = rng.randint(3, 8)
        gsize = rng.randint(2, n - 1)
        group = tuple(sorted(rng.sample(range(1, n + 1), gsize)))
        cnf = random_twin_formula(rng, n, group)
        exact, sizes = check_semantics(cnf, group)
        assert exact
        counters["random_formulas"] += 1
        counters["random_truth_checks"] += 1 + len(signed_twin_children(cnf, group))
        parent_size = token_length(cnf)
        for child_size in sizes:
            assert child_size <= parent_size
            counters["size_monotonicity_checks"] += 1
            max_child_ratio = max(max_child_ratio, child_size / parent_size)
        threshold = int(parent_size ** 0.8)
        if max(sizes) <= threshold:
            counters["threshold_accepts"] += 1
        else:
            counters["threshold_rejects"] += 1
        max_fanout = max(max_fanout, len(sizes))

    # Near-twin hostile controls: one occurrence differs, so the pair must not
    # be certified.  Failure is abstention, never UNSAT.
    for _ in range(500):
        cnf = random_twin_formula(rng, 5, (1, 2))
        broken = canonical_cnf(list(cnf) + [(1, 3)])
        if signed_profile(broken, 1) != signed_profile(broken, 2):
            assert (1, 2) not in twin_classes(broken)
            counters["near_twin_rejections"] += 1

    # Independent products preserve exactness but need not pass a power-size
    # threshold because the untouched factor is carried into every child.
    for _ in range(200):
        left = random_twin_formula(rng, 4, (1, 2))
        right = renamed(random_twin_formula(rng, 4, (1, 2)), 4)
        product = canonical_cnf(list(left) + list(right))
        exact, _ = check_semantics(product, (1, 2))
        assert exact
        counters["independent_product_checks"] += 1

    # Duplicate padding is removed before the source length and shrink gate
    # are measured; it cannot counterfeit a favorable exponent.
    for _ in range(100):
        cnf = random_twin_formula(rng, 6, (1, 2, 3))
        padded = list(cnf) + [rng.choice(cnf) for _ in range(20)] if cnf else []
        normalized = canonical_cnf(padded)
        assert normalized == cnf
        assert signed_twin_children(normalized, (1, 2, 3)) == signed_twin_children(cnf, (1, 2, 3))
        assert token_length(normalized) == token_length(cnf)
        counters["padding_checks"] += 1

    return {
        "claim": "SIGNED-TWIN-MACRO1",
        "status": "COMPUTATIONAL finite audit of a separately proved exact theorem",
        "seed": seed,
        "counters": counters,
        "max_fanout": max_fanout,
        "max_child_parent_token_ratio": max_child_ratio,
        "source_scale_sat_calls": 0,
        "oracle_calls": 0,
        "notes": [
            "Finite tests do not establish asymptotic coverage or a power-size bound.",
            "The transformer is exact only after signed-column equality is verified.",
            "Duplicate clauses are canonicalized before encoded length is measured.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=20261008)
    args = parser.parse_args()
    signal.alarm(25)
    started = time.perf_counter()
    result = run(args.seed)
    result["elapsed_seconds"] = time.perf_counter() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
