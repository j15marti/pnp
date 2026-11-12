#!/usr/bin/env python3
"""Independent truth-table checks for the streaming seed reference solver."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import seed_parity as engine
from validate_closure_solver import (
    affine_relations, canonical_relation_formulas, check_result,
    clause_true, models,
)


def solver(kind):
    return (engine.solve_2cnf_affine_seeds if kind == "2cnf"
            else engine.solve_horn_affine_seeds)


def check_seed_metadata(result, formula_relation, n, kind, cap=None):
    counters = result["counters"]
    if cap is not None:
        assert counters["seeds_attempted"] <= cap, result
    if result["status"] == "UNRESOLVED":
        assert counters["seeds_attempted"] == cap, result
    if result["status"] != "SAT":
        return
    seed = counters["witness_seed"]
    assert seed is not None and len(seed) <= counters["affine_rank"], result
    assert len(set(seed)) == len(seed) and all(1 <= j <= n for j in seed), result
    base = counters.get("base_assignment", 0) if kind == "2cnf" else 0
    seed_mask = sum(1 << (j - 1) for j in seed)
    eligible = [(x ^ base) for x in range(2 ** n)
                if (formula_relation >> x) & 1
                and ((x ^ base) & seed_mask) == seed_mask]
    assert eligible, result
    least = (1 << n) - 1
    for point in eligible:
        least &= point
    assert least == (result["witness"] ^ base), result


def exhaustive(kind):
    solve = solver(kind)
    counts = []
    for n in range(4):
        relations = canonical_relation_formulas(n, kind)
        affine = affine_relations(n)
        total = 0
        for relation, clauses in relations:
            for affine_relation, equations in affine:
                result = solve(n, clauses, equations)
                check_result(result, relation & affine_relation, n, kind)
                check_seed_metadata(result, relation, n, kind)
                total += 1
        counts.append({"n": n, "formula_relations": len(relations),
                       "affine_relations": len(affine), "instances": total})
    return counts


def random_trials(kind, count=700, seed=481092):
    rng = random.Random(seed)
    solve = solver(kind)
    outcomes = {"SAT": 0, "UNSAT": 0, "UNRESOLVED": 0}
    for trial in range(count):
        n = rng.randrange(1, 10)
        planted = rng.randrange(2 ** n)
        clauses = []
        for _ in range(rng.randrange(0, 4 * n + 1)):
            if kind == "2cnf":
                clause = tuple(rng.choice((-1, 1)) * rng.randrange(1, n + 1)
                               for _ in range(rng.randrange(1, 3)))
            else:
                variables = rng.sample(range(1, n + 1), rng.randrange(1, n + 1))
                clause = tuple(-x for x in variables)
                if rng.randrange(2):
                    clause = (-clause[0],) + clause[1:]
            if trial % 2 or clause_true(planted, clause):
                clauses.append(clause)
        equations = []
        for _ in range(rng.randrange(n + 3)):
            mask = rng.randrange(2 ** n)
            rhs = (sum(((planted >> j) & 1) * ((mask >> j) & 1)
                       for j in range(n)) % 2 if not trial % 2 else rng.randrange(2))
            equations.append((mask, rhs))
        if equations and rng.randrange(2):
            equations.append(rng.choice(equations))
        expected = sum(1 << x for x in models(n, clauses, equations))
        cap = rng.choice((None, 0, 1, 2, 5, 10))
        result = solve(n, clauses, equations, seed_cap=cap)
        check_result(result, expected, n, kind, cap)
        relation = sum(1 << x for x in models(n, clauses, []))
        check_seed_metadata(result, relation, n, kind, cap)
        outcomes[result["status"]] += 1
    return outcomes


def controls():
    horn = [(3,), (-1, -2, 4)]
    rows = [(1, 1), (2, 1)]
    result = engine.solve_horn_affine_seeds(4, horn, rows)
    assert result["status"] == "SAT" and result["witness"] == 15, result
    # The same fixed-point obstruction is decided exactly by the reference.
    clauses = [(-i, -j) for i in range(1, 7) for j in range(i + 1, 7)]
    equations = [(0b000111, 1), (0b111000, 1)]
    for solve in (engine.solve_horn_affine_seeds, engine.solve_2cnf_affine_seeds):
        assert solve(6, clauses, equations)["status"] == "UNSAT"
        assert solve(0, [], [])["status"] == "SAT"
        assert solve(0, [()], [])["status"] == "UNSAT"
    return {"multi_antecedent_nonzero_least_model": "PASS",
            "separate_summary_counterexample": "PASS",
            "zero_variable_controls": "PASS"}


def main():
    report = {"engine_sha256": hashlib.sha256((ROOT / "seed_parity.py").read_bytes()).hexdigest(),
              "exhaustive_2cnf": exhaustive("2cnf"),
              "exhaustive_horn": exhaustive("horn"),
              "random_2cnf": random_trials("2cnf"),
              "random_horn": random_trials("horn", seed=481093),
              "controls": controls(), "status": "PASS"}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
