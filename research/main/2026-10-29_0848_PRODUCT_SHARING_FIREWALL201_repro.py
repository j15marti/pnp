#!/usr/bin/env python3
"""Finite controls for PRODUCT-SHARING-FIREWALL201.

The experiment checks a full-cube UNSAT 3CNF, its always-SAT occurrence-
disjoint product, and restoration of the source semantics by equality trees.
It also tests the same identity on deterministic random proper 3CNFs.  These
are finite controls, not a SAT runtime lower bound.
"""

from __future__ import annotations

import itertools
import json
import random


VARIABLES = ("x", "y", "z")


def eval_clause(clause: tuple[tuple[str, bool], ...], assignment: dict[str, int]) -> bool:
    return any(bool(assignment[var]) == positive for var, positive in clause)


def eval_formula(clauses: tuple[tuple[tuple[str, bool], ...], ...], assignment: dict[str, int]) -> bool:
    return all(eval_clause(clause, assignment) for clause in clauses)


def full_cube_unsat() -> tuple[tuple[tuple[str, bool], ...], ...]:
    """One clause falsified by each assignment to x,y,z."""
    clauses = []
    for bits in itertools.product((0, 1), repeat=3):
        clauses.append(tuple((var, bit == 0) for var, bit in zip(VARIABLES, bits)))
    return tuple(clauses)


class DSU:
    def __init__(self, items: list[str]) -> None:
        self.parent = {x: x for x in items}

    def find(self, x: str) -> str:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def components(self, items: list[str]) -> int:
        return len({self.find(x) for x in items})


def occurrence_data(clauses: tuple[tuple[tuple[str, bool], ...], ...]):
    by_variable: dict[str, list[str]] = {}
    occurrence_clauses = []
    for ci, clause in enumerate(clauses):
        lifted = []
        for li, (var, positive) in enumerate(clause):
            name = f"{var}@{ci}:{li}"
            by_variable.setdefault(var, []).append(name)
            lifted.append((name, positive))
        occurrence_clauses.append(tuple(lifted))
    equality_edges = []
    for names in by_variable.values():
        equality_edges.extend(zip(names, names[1:]))
    return tuple(occurrence_clauses), by_variable, tuple(equality_edges)


def source_models(clauses: tuple[tuple[tuple[str, bool], ...], ...]) -> int:
    variables = sorted({var for clause in clauses for var, _ in clause})
    return sum(
        eval_formula(clauses, dict(zip(variables, bits)))
        for bits in itertools.product((0, 1), repeat=len(variables))
    )


def verify_instance(clauses: tuple[tuple[tuple[str, bool], ...], ...]) -> dict[str, int | bool]:
    occurrence_clauses, by_variable, equality_edges = occurrence_data(clauses)
    m = len(clauses)
    n = len(by_variable)
    occurrences = sum(map(len, occurrence_clauses))
    assert occurrences == 3 * m

    # Each proper three-literal clause has exactly seven satisfying local rows;
    # after occurrence splitting, the clause scopes are disjoint.
    local_counts = []
    for clause in occurrence_clauses:
        names = [name for name, _ in clause]
        local_counts.append(
            sum(
                eval_clause(clause, dict(zip(names, bits)))
                for bits in itertools.product((0, 1), repeat=3)
            )
        )
    assert set(local_counts) == {7}
    disjoint_product_models = 7**m

    # A tree on d occurrence copies has d-1 edges and makes exactly one
    # component.  Removing any tree edge leaves two components.
    offset = 0
    for names in by_variable.values():
        tree = list(zip(names, names[1:]))
        dsu = DSU(names)
        for a, b in tree:
            dsu.union(a, b)
        assert len(tree) == len(names) - 1
        assert dsu.components(names) == 1
        if tree:
            reduced = DSU(names)
            for a, b in tree[:-1]:
                reduced.union(a, b)
            assert reduced.components(names) == 2
        offset += len(tree)
    assert offset == occurrences - n == 3 * m - n == len(equality_edges)

    # Equality identifies every occurrence copy with its source variable.
    # Consequently the lifted formula has exactly the source model count.
    models = source_models(clauses)
    return {
        "clauses": m,
        "variables": n,
        "occurrences": occurrences,
        "source_models": models,
        "disjoint_product_models": disjoint_product_models,
        "minimum_pairwise_equality_links": 3 * m - n,
        "equality_restores_source_model_count": True,
    }


def random_proper_formula(rng: random.Random, n: int, m: int):
    names = tuple(f"v{i}" for i in range(n))
    clauses = []
    for _ in range(m):
        scope = rng.sample(names, 3)
        clauses.append(tuple((var, bool(rng.getrandbits(1))) for var in scope))
    return tuple(clauses)


def main() -> None:
    cube = full_cube_unsat()
    cube_result = verify_instance(cube)
    assert cube_result["source_models"] == 0
    assert cube_result["disjoint_product_models"] == 7**8 == 5_764_801
    assert cube_result["minimum_pairwise_equality_links"] == 21

    rng = random.Random(20261029)
    random_results = []
    for n in range(3, 8):
        for m in range(1, 9):
            for _ in range(20):
                random_results.append(verify_instance(random_proper_formula(rng, n, m)))
    assert len(random_results) == 800

    m, n = 8, 3
    links = 3 * m - n
    hypothetical_exact22_additive_ledger = {
        "multiport_base_variables": 15 * m,
        "multiport_base_clauses": 20 * m,
        "two_swap_equality_variables": 15 * links,
        "two_swap_equality_clauses": 20 * links,
        "composed_variables": 15 * m + 15 * links,
        "composed_clauses": 20 * m + 20 * links,
    }
    assert hypothetical_exact22_additive_ledger == {
        "multiport_base_variables": 120,
        "multiport_base_clauses": 160,
        "two_swap_equality_variables": 315,
        "two_swap_equality_clauses": 420,
        "composed_variables": 435,
        "composed_clauses": 580,
    }

    result = {
        "status": "PASS",
        "seed": 20261029,
        "full_cube_unsat": cube_result,
        "full_cube_clause_count": len(cube),
        "full_cube_base_assignments_checked": 8,
        "local_clause_rows_checked": 8 * len(cube),
        "random_proper_instances_checked": len(random_results),
        "random_source_assignments_checked": sum(2 ** r["variables"] for r in random_results),
        "all_random_identities_passed": True,
        "hypothetical_two_swap_additive_ledger": hypothetical_exact22_additive_ledger,
        "limitations": [
            "The 3m-n lower bound is for pairwise equality graphs on explicit occurrence copies.",
            "Higher-arity relations, shared-variable encodings, semantic preprocessing, or history-discarding summaries may escape it.",
            "The two-swap counts are a hypothetical additive ledger, not an optimality theorem for all gadgets.",
            "Report198 fans out an existing source variable; it does not directly join two independently saturated ports, so this additive ledger is not a verified composition.",
            "Finite truth-table checks do not prove a SAT runtime lower bound.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
