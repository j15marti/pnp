#!/usr/bin/env python3
"""Independent truth-table validation of closure_parity (no solver helpers used).

The exhaustive component ranges over every distinct 2-CNF/Horn model relation
and every affine solution relation on at most three variables.  Random cases
exercise larger inputs, redundant clauses/rows, and resource-cap exits.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import closure_parity as engine


def clause_true(assignment, clause):
    return any(((assignment // (2 ** (abs(lit) - 1))) % 2) == int(lit > 0)
               for lit in clause)


def models(n, clauses, equations):
    return [x for x in range(2 ** n)
            if all(clause_true(x, clause) for clause in clauses)
            and all(sum(((x >> j) & 1) * ((mask >> j) & 1)
                        for j in range(n)) % 2 == rhs
                    for mask, rhs in equations)]


def canonical_relation_formulas(n, kind):
    """Return each definable truth relation exactly once with a defining CNF."""
    candidates = []
    for signs in itertools.product((-1, 0, 1), repeat=n):
        clause = tuple(sign * (j + 1) for j, sign in enumerate(signs) if sign)
        if ((kind == "2cnf" and len(clause) <= 2)
                or (kind == "horn" and sum(lit > 0 for lit in clause) <= 1)):
            mask = sum(1 << x for x in range(2 ** n) if clause_true(x, clause))
            candidates.append((clause, mask))
    full = (1 << (2 ** n)) - 1
    answer = []
    for relation in range(full + 1):
        clauses = [clause for clause, mask in candidates if relation & ~mask == 0]
        exact = full
        for clause, mask in candidates:
            if relation & ~mask == 0:
                exact &= mask
        if relation == exact:
            answer.append((relation, clauses))
    return answer


def affine_relations(n):
    full = (1 << (2 ** n)) - 1
    candidates = []
    for mask in range(2 ** n):
        for rhs in (0, 1):
            relation = sum(1 << x for x in range(2 ** n)
                           if sum(((x >> j) & 1) * ((mask >> j) & 1)
                                  for j in range(n)) % 2 == rhs)
            candidates.append(((mask, rhs), relation))
    answer = []
    for relation in range(full + 1):
        exact = full
        rows = []
        for row, row_relation in candidates:
            if relation & ~row_relation == 0:
                exact &= row_relation
                rows.append(row)
        if exact == relation:
            answer.append((relation, rows))
    return answer


def check_result(result, expected_mask, n, kind, cap=None):
    assert result["status"] in ("SAT", "UNSAT", "UNRESOLVED"), result
    if result["status"] == "UNRESOLVED":
        assert cap is not None
        assert result["witness"] is None
        return
    assert (result["status"] == "SAT") == bool(expected_mask), (kind, n, expected_mask, result)
    if result["status"] == "SAT":
        witness = result["witness"]
        assert isinstance(witness, int) and 0 <= witness < 2 ** n
        assert (expected_mask >> witness) & 1, (kind, n, expected_mask, result)
    else:
        assert result["witness"] is None


def exhaustive(kind, largest=3):
    solve = engine.solve_2cnf_affine if kind == "2cnf" else engine.solve_horn_affine
    counts = []
    for n in range(largest + 1):
        relations = canonical_relation_formulas(n, kind)
        affine = affine_relations(n)
        total = 0
        for relation, clauses in relations:
            for affine_relation, equations in affine:
                result = solve(n, clauses, equations)
                check_result(result, relation & affine_relation, n, kind)
                total += 1
        counts.append({"n": n, "formula_relations": len(relations),
                       "affine_relations": len(affine), "instances": total})
    return counts


def random_trials(kind, count=700, seed=187031):
    rng = random.Random(seed)
    solve = engine.solve_2cnf_affine if kind == "2cnf" else engine.solve_horn_affine
    outcomes = {"SAT": 0, "UNSAT": 0, "UNRESOLVED": 0}
    for trial in range(count):
        n = rng.randrange(1, 9)
        clauses = []
        for _ in range(rng.randrange(0, 3 * n + 1)):
            if kind == "2cnf":
                clause = tuple(rng.choice((-1, 1)) * rng.randrange(1, n + 1)
                               for _ in range(rng.randrange(0, 3)))
            else:
                variables = rng.sample(range(1, n + 1), rng.randrange(n + 1))
                clause = tuple(-x for x in variables)
                if clause and rng.randrange(2):
                    clause = (-clause[0],) + clause[1:]
            clauses.append(clause)
        equations = [(rng.randrange(2 ** n), rng.randrange(2))
                     for _ in range(rng.randrange(n + 3))]
        if equations and rng.randrange(2):
            equations.append(rng.choice(equations))
        expected = sum(1 << x for x in models(n, clauses, equations))
        cap = rng.choice((None, 0, 1, 2, 4, 8))
        result = solve(n, clauses, equations, term_cap=cap)
        check_result(result, expected, n, kind, cap)
        outcomes[result["status"]] += 1
    return outcomes


def structured_controls():
    # A pair of globally inconsistent abstractions whose separate projections
    # convey nothing: hull(H)=full cube, strongest 2CNF(A)=TRUE.
    clauses = [(-i, -j) for i in range(1, 7) for j in range(i + 1, 7)]
    equations = [(0b000111, 1), (0b111000, 1)]
    h_models = models(6, clauses, [])
    a_models = models(6, [], equations)
    assert h_models == [0, 1, 2, 4, 8, 16, 32]
    assert not models(6, clauses, equations)
    assert all({((x >> i) & 1, (x >> j) & 1) for x in a_models}
               == {(0, 0), (0, 1), (1, 0), (1, 1)}
               for i in range(6) for j in range(i + 1, 6))
    result = engine.solve_2cnf_affine(6, clauses, equations)
    assert result["status"] == "UNSAT", result
    # A seed of size one closes to n coordinates; degree is not key cardinality.
    chain = [(-i, i + 1) for i in range(1, 9)]
    result = engine.solve_2cnf_affine(9, chain, [(1, 1)])
    assert result["status"] == "SAT" and result["witness"] == 511
    result = engine.solve_2cnf_affine(0, [], [])
    assert result["status"] == "SAT" and result["witness"] == 0
    result = engine.solve_2cnf_affine(0, [()], [])
    assert result["status"] == "UNSAT"
    result = engine.solve_2cnf_affine(0, [], [(0, 1)])
    assert result["status"] == "UNSAT"
    return {"reduced_product_counterexample": "PASS", "long_closure": "PASS",
            "empty_variable_controls": "PASS"}


def main():
    include_horn = "--horn" in sys.argv
    report = {"engine_sha256": hashlib.sha256((ROOT / "closure_parity.py").read_bytes()).hexdigest(),
              "exhaustive_2cnf": exhaustive("2cnf"),
              "random_2cnf": random_trials("2cnf"),
              "controls": structured_controls()}
    if include_horn:
        report["exhaustive_horn"] = exhaustive("horn")
        report["random_horn"] = random_trials("horn", seed=187032)
    report["status"] = "PASS"
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
