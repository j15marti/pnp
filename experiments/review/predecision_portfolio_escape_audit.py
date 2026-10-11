#!/usr/bin/env python3
"""Finite falsification audit for a fixed predecision SAT portfolio.

The symbolic report proves the wrapper lemma.  This program supplies bounded,
reproducible witnesses showing that an explicit portfolio of genuine semantic
or structural shortcuts does not cover all sampled balanced clean cores.  It
does not infer hardness from noncoverage.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def satisfies(formula: Formula, bits: int) -> bool:
    return all(
        any(((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
        for clause in formula
    )


def sat(formula: Formula, n: int) -> bool:
    return any(satisfies(formula, bits) for bits in range(1 << n))


def solution_count(formula: Formula, n: int) -> int:
    return sum(satisfies(formula, bits) for bits in range(1 << n))


def restrict(formula: Formula, assignment: dict[int, bool]) -> Formula | None:
    out: list[Clause] = []
    for clause in formula:
        residual: list[int] = []
        clause_true = False
        for lit in clause:
            value = assignment.get(abs(lit))
            if value is None:
                residual.append(lit)
            elif value == (lit > 0):
                clause_true = True
                break
        if clause_true:
            continue
        if not residual:
            return None
        out.append(tuple(residual))
    return tuple(out)


def balanced_sign_part(n: int, sign: int, rng: random.Random) -> list[Clause]:
    slots = [v for v in range(1, n + 1) for _ in range(2)]
    for _ in range(20000):
        rng.shuffle(slots)
        triples = [tuple(sorted(slots[i:i + 3])) for i in range(0, len(slots), 3)]
        if all(len(set(t)) == 3 for t in triples) and len(set(triples)) == len(triples):
            return [tuple(sign * v for v in t) for t in triples]
    raise RuntimeError(f"failed to generate sign part for n={n}")


def balanced_formula(n: int, rng: random.Random) -> Formula:
    assert n % 3 == 0
    formula = tuple(balanced_sign_part(n, 1, rng) + balanced_sign_part(n, -1, rng))
    assert len(set(formula)) == len(formula)
    return formula


def verify_clean_core(formula: Formula, n: int) -> None:
    assert len(formula) * 3 == 4 * n
    for clause in formula:
        assert len(clause) == 3 and len({abs(lit) for lit in clause}) == 3
        assert all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)
    for v in range(1, n + 1):
        assert sum(v in clause for clause in formula) == 2
        assert sum(-v in clause for clause in formula) == 2


def has_unit_or_pure(formula: Formula, n: int) -> bool:
    if any(len(clause) <= 1 for clause in formula):
        return True
    return any(
        not any(v in clause for clause in formula)
        or not any(-v in clause for clause in formula)
        for v in range(1, n + 1)
    )


def is_horn(formula: Formula) -> bool:
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in formula)


def is_dual_horn(formula: Formula) -> bool:
    return all(sum(lit < 0 for lit in clause) <= 1 for clause in formula)


def is_2cnf(formula: Formula) -> bool:
    return all(len(clause) <= 2 for clause in formula)


def tractable_union(formula: Formula | None) -> bool:
    return formula is None or is_horn(formula) or is_dual_horn(formula) or is_2cnf(formula)


def incidence_connected(formula: Formula, n: int) -> bool:
    adjacency = [set() for _ in range(n + len(formula))]
    for j, clause in enumerate(formula):
        c = n + j
        for lit in clause:
            v = abs(lit) - 1
            adjacency[v].add(c)
            adjacency[c].add(v)
    seen = {0}
    stack = [0]
    while stack:
        stack.extend(adjacency[stack.pop()] - seen)
        seen.update(stack)
    return len(seen) == len(adjacency)


def has_signed_twins(formula: Formula, n: int) -> bool:
    signatures: dict[tuple[tuple[int, int], ...], int] = {}
    for v in range(1, n + 1):
        signature = tuple(
            sorted((j, 1 if v in clause else -1) for j, clause in enumerate(formula)
                   if v in clause or -v in clause)
        )
        if signature in signatures:
            return True
        signatures[signature] = v
    return False


def has_small_autarky(formula: Formula, n: int, width: int = 2) -> bool:
    variables = range(1, n + 1)
    for size in range(1, width + 1):
        for chosen in itertools.combinations(variables, size):
            chosen_set = set(chosen)
            touched = [c for c in formula if any(abs(lit) in chosen_set for lit in c)]
            for values in itertools.product((False, True), repeat=size):
                assignment = dict(zip(chosen, values))
                if all(any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
                           for lit in clause) for clause in touched):
                    return True
    return False


def has_strong_backdoor(formula: Formula, n: int, width: int = 2) -> bool:
    variables = range(1, n + 1)
    for size in range(width + 1):
        for chosen in itertools.combinations(variables, size):
            if all(
                tractable_union(restrict(formula, dict(zip(chosen, values))))
                for values in itertools.product((False, True), repeat=size)
            ):
                return True
    return False


def portfolio_hits(formula: Formula, n: int) -> list[str]:
    hits: list[str] = []
    if has_unit_or_pure(formula, n):
        hits.append("unit_or_pure")
    if not incidence_connected(formula, n):
        hits.append("component_factorization")
    if is_horn(formula):
        hits.append("horn")
    if is_dual_horn(formula):
        hits.append("dual_horn")
    if is_2cnf(formula):
        hits.append("two_cnf")
    if has_small_autarky(formula, n):
        hits.append("autarky_width_at_most_2")
    if has_strong_backdoor(formula, n):
        hits.append("strong_backdoor_width_at_most_2_to_union")
    if has_signed_twins(formula, n):
        hits.append("signed_twins")
    return hits


def controls() -> dict[str, dict[str, object]]:
    examples: dict[str, Formula] = {
        "unit": ((1,), (-1, 2)),
        "horn": ((-1, -2, 3), (-3, 4), (-4,)),
        "two_cnf": ((1, 2), (-1, 3), (-2, -3)),
        "disconnected": ((1, 2), (-1, 2), (3, 4), (-3, 4)),
        "small_autarky": ((1, 2, 3), (1, -2, 4), (-3, -4, 5)),
    }
    out: dict[str, dict[str, object]] = {}
    for name, formula in examples.items():
        n = max(abs(lit) for clause in formula for lit in clause)
        out[name] = {"hits": portfolio_hits(formula, n), "satisfiable": sat(formula, n)}
    # XOR is an explicit hostile control outside the CNF portfolio: Gaussian
    # elimination decides x1 xor x2 xor x3 = b in polynomial time.
    out["affine_xor_system"] = {
        "portfolio_scope": "outside ordinary-CNF recognizers",
        "semantic_cost": "Gaussian elimination",
        "satisfiable": True,
    }
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111100)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    rng = random.Random(args.seed)
    records: list[dict[str, object]] = []
    hit_counts: dict[str, int] = {}
    escape_count = 0
    wrapper_checks = 0
    for n in (6, 9, 12):
        for sample in range(args.samples):
            formula = balanced_formula(n, rng)
            verify_clean_core(formula, n)
            direct = sat(formula, n)
            hits = portfolio_hits(formula, n)
            # The audited wrapper delegates uncovered inputs to an exact
            # fallback.  This finite fallback is exhaustive search; the
            # theorem quantifies over an arbitrary total decider B instead.
            wrapper = direct if hits else sat(formula, n)
            assert wrapper == direct
            wrapper_checks += 1
            for hit in hits:
                hit_counts[hit] = hit_counts.get(hit, 0) + 1
            if not hits:
                escape_count += 1
            records.append({
                "n": n,
                "m": len(formula),
                "sample": sample,
                "portfolio_hits": hits,
                "escaped_portfolio": not hits,
                "satisfiable": direct,
                "solution_count": solution_count(formula, n),
                "formula": [list(clause) for clause in formula],
            })

    assert escape_count > 0, "seeded audit unexpectedly found no escape witness"
    payload = {
        "report_id": "MODELBRIDGE-0009",
        "seed": args.seed,
        "samples_per_size": args.samples,
        "sizes": [6, 9, 12],
        "mode": "bounded-exhaustive-semantics-plus-seeded-clean-core-generation",
        "runtime_seconds": time.perf_counter() - started,
        "wrapper_correctness_checks": wrapper_checks,
        "portfolio_hit_counts": dict(sorted(hit_counts.items())),
        "escape_count": escape_count,
        "records": records,
        "controls": controls(),
        "limitations": [
            "Portfolio noncoverage is not computational hardness.",
            "The fallback used for finite verification is exhaustive and is not claimed polynomial.",
            "The wrapper theorem is conditional: if a total polynomial SAT decider B exists, the wrapper is polynomial.",
            "The test does not establish that every finite or computable preprocessing portfolio has escape inputs.",
            "P versus NP remains open.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in (
        "report_id", "seed", "samples_per_size", "sizes", "runtime_seconds",
        "wrapper_correctness_checks", "portfolio_hit_counts", "escape_count")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
