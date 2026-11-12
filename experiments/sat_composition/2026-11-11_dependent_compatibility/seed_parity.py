#!/usr/bin/env python3
"""Polynomial-workspace reference solver for Horn/2-CNF with affine equations.

For affine rank d, a satisfiable Horn instance has a witness cl_H(S) with |S|<=d.
This program streams those seeds, recomputes each closure, and checks the affine
equations.  There is deliberately NO global memo table of seeds or closed sets.

The two APIs return status SAT/UNSAT/UNRESOLVED, an integer witness or None, a reason,
and counters. Clauses use signed one-based literals; affine rows are (mask,rhs).
seed_cap limits the number of attempted seeds, not elapsed time or preprocessing.
A capped exit is never classified as UNSAT. witness_seed uses one-based variables;
for 2-CNF these are coordinates after the recorded base-model XOR translation.

The bound is poly(N)*sum_{j<=d} binom(n,j) time and polynomial workspace. This is
an XP algorithm, not a uniform polynomial bound when d grows with the input.
"""
from __future__ import annotations

from itertools import combinations
from math import comb


def _validate(n, clauses, equations, seed_cap, kind):
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if seed_cap is not None and (not isinstance(seed_cap, int) or isinstance(seed_cap, bool) or seed_cap < 0):
        raise ValueError("seed_cap must be a nonnegative integer or None")
    raw_clauses = []
    cleaned = []
    for raw in clauses:
        clause = tuple(raw)
        if kind == "2cnf" and len(clause) > 2:
            raise ValueError("A 2-CNF clause has more than two literals")
        if any(not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > n for lit in clause):
            raise ValueError("Invalid literal")
        raw_clauses.append(clause)
        unique = set(clause)
        if any(-literal in unique for literal in unique):
            continue
        if kind == "horn" and sum(literal > 0 for literal in unique) > 1:
            raise ValueError("A nontautological clause is not Horn")
        cleaned.append(tuple(sorted(unique)))
    rows = []
    for row in equations:
        if len(row) != 2:
            raise ValueError("Every affine equation must be a pair")
        mask, rhs = row
        if (not isinstance(mask, int) or isinstance(mask, bool) or mask < 0 or mask >> n
                or rhs not in (0, 1)):
            raise ValueError("Invalid affine equation")
        rows.append((mask, int(rhs)))
    return raw_clauses, cleaned, rows


def _row_basis(rows, counters):
    """Independent highest-pivot echelon reduction, without back substitution."""
    pivots = {}
    for mask, rhs in rows:
        counters["matrix_input_rows"] += 1
        while mask:
            pivot = mask.bit_length() - 1
            counters["matrix_pivot_tests"] += 1
            if pivot not in pivots:
                pivots[pivot] = mask, rhs
                break
            other, value = pivots[pivot]
            mask ^= other
            rhs ^= value
            counters["matrix_row_additions"] += 1
        if not mask and rhs:
            return None
    return tuple(pivots[p] for p in sorted(pivots))


def _initial_counters(seed_cap):
    return {"seed_cap": seed_cap, "seeds_attempted": 0, "closure_work": 0,
            "closure_passes": 0, "closure_additions": 0, "closure_conflicts": 0,
            "equation_checks": 0, "matrix_input_rows": 0, "matrix_pivot_tests": 0,
            "matrix_row_additions": 0, "max_seed_size_attempted": 0,
            "witness_clause_checks": 0, "witness_affine_checks": 0,
            "witness_seed": None}


def solve_horn_affine_seeds(n: int, clauses, equations, seed_cap: int | None = None):
    """Stream all seeds of size <= affine rank and recompute exact Horn closure."""
    raw, cleaned, original_rows = _validate(n, clauses, equations, seed_cap, "horn")
    counters = _initial_counters(seed_cap)
    counters.update(input_clauses=len(raw), input_literal_visits=sum(map(len, raw)),
                    input_affine_rows=len(original_rows))

    def finish(status, reason, witness=None):
        if status == "SAT":
            for clause in raw:
                counters["witness_clause_checks"] += 1
                if not any(bool((witness >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                    raise AssertionError("Seed witness failed an original Horn clause")
            for mask, rhs in original_rows:
                counters["witness_affine_checks"] += 1
                if (witness & mask).bit_count() % 2 != rhs:
                    raise AssertionError("Seed witness failed an original affine equation")
        return {"status": status, "witness": witness, "reason": reason, "counters": counters}

    rows = _row_basis(original_rows, counters)
    if rows is None:
        return finish("UNSAT", "inconsistent_affine_system")
    rank = len(rows)
    counters.update(affine_rank=rank, seed_space_bound=sum(comb(n, j) for j in range(rank + 1)))
    rules = []
    for clause in cleaned:
        body = sum(1 << (-literal - 1) for literal in clause if literal < 0)
        head = next((1 << (literal - 1) for literal in clause if literal > 0), None)
        rules.append((body, head))

    def closure(seed):
        point = seed
        while True:
            counters["closure_passes"] += 1
            changed = False
            for body, head in rules:
                counters["closure_work"] += 1  # one explicitly recorded antecedent-mask test
                if point & body != body:
                    continue
                if head is None:
                    counters["closure_conflicts"] += 1
                    return None
                if point & head == 0:
                    point |= head
                    changed = True
                    counters["closure_additions"] += 1
            if not changed:
                return point

    # combinations holds one seed at a time; duplicate closures are recomputed.
    for size in range(rank + 1):
        for seed in combinations(range(n), size):
            if seed_cap is not None and counters["seeds_attempted"] >= seed_cap:
                return finish("UNRESOLVED", "seed_attempt_cap_exceeded")
            counters["seeds_attempted"] += 1
            counters["max_seed_size_attempted"] = size
            point = closure(sum(1 << j for j in seed))
            if point is None:
                continue
            valid = True
            for mask, rhs in rows:
                counters["equation_checks"] += 1
                if (point & mask).bit_count() % 2 != rhs:
                    valid = False
                    break
            if valid:
                counters["witness_seed"] = [j + 1 for j in seed]
                return finish("SAT", "bounded_seed_horn_closure_witness", point)
    return finish("UNSAT", "all_seeds_through_affine_rank_exhausted")


def solve_2cnf_affine_seeds(n: int, clauses, equations, seed_cap: int | None = None):
    """Translate by one 2-SAT model, stream Horn seeds, and lift the witness."""
    raw, cleaned, original_rows = _validate(n, clauses, equations, seed_cap, "2cnf")
    preprocessing = _initial_counters(seed_cap)
    rows = _row_basis(original_rows, preprocessing)
    if rows is None:
        return {"status": "UNSAT", "witness": None,
                "reason": "inconsistent_affine_system", "counters": preprocessing}
    preprocessing["affine_rank"] = len(rows)
    # Only the polynomial 2-SAT base-model path is reused from the frozen engine.
    from closure_parity import solve_2cnf_affine
    base_result = solve_2cnf_affine(n, cleaned, [])
    if base_result["status"] == "UNSAT":
        preprocessing["base_model_counters"] = base_result["counters"]
        return {"status": "UNSAT", "witness": None,
                "reason": "two_cnf_unsatisfiable", "counters": preprocessing}
    if base_result["status"] != "SAT":
        raise AssertionError("An uncapped empty-equations 2-SAT call must resolve")
    base = base_result["witness"]
    translated = [tuple(-lit if (base >> (abs(lit) - 1)) & 1 else lit for lit in clause)
                  for clause in cleaned]
    translated_rows = [(mask, rhs ^ ((mask & base).bit_count() % 2)) for mask, rhs in rows]
    result = solve_horn_affine_seeds(n, translated, translated_rows, seed_cap)
    result["counters"]["base_assignment"] = base
    result["counters"]["base_model_counters"] = base_result["counters"]
    result["counters"]["wrapper_preprocessing"] = preprocessing
    result["counters"]["wrapper_input_affine_rows"] = len(original_rows)
    result["counters"]["witness_seed_coordinates"] = "y=x XOR base_assignment"
    if result["status"] == "SAT":
        result["witness"] ^= base
        witness = result["witness"]
        for clause in raw:
            result["counters"]["witness_clause_checks"] += 1
            if not any(bool((witness >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                raise AssertionError("Lifted seed witness failed an original 2-CNF clause")
        for mask, rhs in original_rows:
            result["counters"]["witness_affine_checks"] += 1
            if (witness & mask).bit_count() % 2 != rhs:
                raise AssertionError("Lifted seed witness failed an original affine equation")
        result["reason"] = "bounded_seed_translated_two_cnf_witness"
    return result


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON object with n, clauses, equations")
    parser.add_argument("--seed-cap", type=int)
    parser.add_argument("--horn", action="store_true")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as handle:
        instance = json.load(handle)
    solver = solve_horn_affine_seeds if args.horn else solve_2cnf_affine_seeds
    print(json.dumps(solver(instance["n"], instance["clauses"], instance["equations"], args.seed_cap), indent=2))
