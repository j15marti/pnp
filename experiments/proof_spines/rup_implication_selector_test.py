#!/usr/bin/env python3
"""Bounded exact tests for the RUP implication frontier selector.

The experiment is deliberately self-contained.  It uses exhaustive truth
tables only as a test oracle; the selector itself uses unit propagation.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import signal
import time
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def normalize_clause(clause: tuple[int, ...] | list[int]) -> Clause | None:
    literals = set(clause)
    if any(-lit in literals for lit in literals):
        return None
    return tuple(sorted(literals, key=lambda lit: (abs(lit), lit < 0)))


def normalize_cnf(clauses: tuple[Clause, ...] | list[Clause]) -> CNF:
    normalized: set[Clause] = set()
    for clause in clauses:
        item = normalize_clause(clause)
        if item is not None:
            normalized.add(item)
    return tuple(sorted(normalized, key=lambda c: (len(c), c)))


def unit_conflict(cnf: CNF, assumptions: tuple[int, ...] = ()) -> bool:
    assignment: dict[int, bool] = {}

    def assign(lit: int) -> bool:
        var, value = abs(lit), lit > 0
        old = assignment.get(var)
        if old is not None and old != value:
            return False
        assignment[var] = value
        return True

    for lit in assumptions:
        if not assign(lit):
            return True

    changed = True
    while changed:
        changed = False
        for clause in cnf:
            satisfied = False
            unset: list[int] = []
            for lit in clause:
                value = assignment.get(abs(lit))
                if value is None:
                    unset.append(lit)
                elif value == (lit > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unset:
                return True
            if len(unset) == 1:
                before = len(assignment)
                if not assign(unset[0]):
                    return True
                changed |= len(assignment) != before
    return False


def rup_implies(source: CNF, target: CNF) -> bool:
    """Soundly certify source => target, clause by clause, using RUP."""
    return all(unit_conflict(source, tuple(-lit for lit in clause)) for clause in target)


def truth_mask(cnf: CNF, variables: int) -> int:
    mask = 0
    for bits in range(1 << variables):
        satisfied = True
        for clause in cnf:
            if not any(((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                satisfied = False
                break
        if satisfied:
            mask |= 1 << bits
    return mask


def implication_graph(frontier: list[CNF]) -> list[list[int]]:
    graph = [[] for _ in frontier]
    for i, source in enumerate(frontier):
        for j, target in enumerate(frontier):
            if i != j and rup_implies(source, target):
                graph[i].append(j)
    return graph


def sink_scc_representatives(graph: list[list[int]]) -> list[int]:
    index = 0
    stack: list[int] = []
    on_stack: set[int] = set()
    indices = [-1] * len(graph)
    low = [0] * len(graph)
    components: list[list[int]] = []

    def visit(v: int) -> None:
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph[v]:
            if indices[w] == -1:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            component: list[int] = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            components.append(component)

    for vertex in range(len(graph)):
        if indices[vertex] == -1:
            visit(vertex)

    component_of = {}
    for cid, component in enumerate(components):
        for vertex in component:
            component_of[vertex] = cid
    outgoing = [False] * len(components)
    for source, targets in enumerate(graph):
        for target in targets:
            if component_of[source] != component_of[target]:
                outgoing[component_of[source]] = True
    return sorted(min(component) for cid, component in enumerate(components) if not outgoing[cid])


def select(frontier: list[CNF]) -> tuple[list[int], list[list[int]]]:
    graph = implication_graph(frontier)
    return sink_scc_representatives(graph), graph


def random_cnf(rng: random.Random, variables: int, max_clauses: int = 7) -> CNF:
    clauses: list[Clause] = []
    for _ in range(rng.randint(0, max_clauses)):
        width = rng.randint(0, min(3, variables))
        if width == 0:
            clause: Clause = ()
        else:
            vars_in_clause = rng.sample(range(1, variables + 1), width)
            clause = tuple(var if rng.getrandbits(1) else -var for var in vars_in_clause)
        clauses.append(clause)
    return normalize_cnf(clauses)


def rename_and_complement(cnf: CNF, permutation: list[int], flipped: set[int]) -> CNF:
    mapped: list[Clause] = []
    for clause in cnf:
        out: list[int] = []
        for lit in clause:
            var = permutation[abs(lit) - 1]
            sign = lit > 0
            if abs(lit) in flipped:
                sign = not sign
            out.append(var if sign else -var)
        mapped.append(tuple(out))
    return normalize_cnf(mapped)


def arc_antichain(variables: int) -> list[CNF]:
    return [
        normalize_cnf([tuple((i + 1) if ((bits >> i) & 1) else -(i + 1) for i in range(variables))])
        for bits in range(1 << variables)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=20261007)
    parser.add_argument("--budget", type=int, default=25)
    args = parser.parse_args()

    def timeout_handler(_signum: int, _frame: object) -> None:
        raise TimeoutError("cooperative time budget exceeded")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(args.budget)
    started = time.monotonic()
    rng = random.Random(args.seed)
    checks = 0

    strict_counts = []
    for copies in range(1, 13):
        weak = normalize_cnf([(copies + 1,)])
        frontier = [
            normalize_cnf([(i,), (-i, copies + 1)]) for i in range(1, copies + 1)
        ] + [weak]
        keep, graph = select(frontier)
        assert keep == [copies]
        assert all(copies in graph[i] for i in range(copies))
        assert all(not set(frontier[i]).issuperset(frontier[copies]) for i in range(copies))
        strict_counts.append({"copies": copies, "input": copies + 1, "kept": len(keep)})
        checks += 3

    random_portfolios = 300
    random_edges = 0
    for _ in range(random_portfolios):
        variables = rng.randint(2, 5)
        frontier = [random_cnf(rng, variables) for _ in range(rng.randint(2, 8))]
        keep, graph = select(frontier)
        masks = [truth_mask(cnf, variables) for cnf in frontier]
        for source, targets in enumerate(graph):
            for target in targets:
                assert masks[source] & ~masks[target] == 0
                random_edges += 1
                checks += 1
        assert (lambda xs: __import__("functools").reduce(int.__or__, xs, 0))(masks) == (
            lambda xs: __import__("functools").reduce(int.__or__, xs, 0)
        )([masks[i] for i in keep])
        checks += 1

        permutation = list(range(1, variables + 1))
        rng.shuffle(permutation)
        flipped = {i for i in range(1, variables + 1) if rng.getrandbits(1)}
        transformed = [rename_and_complement(cnf, permutation, flipped) for cnf in frontier]
        keep_transformed, _ = select(transformed)
        assert len(keep_transformed) == len(keep)
        checks += 1

        padded = [normalize_cnf(list(cnf) + [(1, -1)]) for cnf in frontier]
        assert padded == frontier
        checks += 1

    antichain_counts = []
    for variables in range(1, 9):
        frontier = arc_antichain(variables)
        keep, graph = select(frontier)
        edges = sum(map(len, graph))
        assert len(keep) == len(frontier)
        assert edges == 0
        antichain_counts.append(
            {"variables": variables, "input": len(frontier), "kept": len(keep), "edges": edges}
        )
        checks += 2

    # Independent-product control: formulas use disjoint variable blocks.
    left = [normalize_cnf([(1,)]), normalize_cnf([(-1,)])]
    right = [normalize_cnf([(2,)]), normalize_cnf([(-2,)])]
    product = [normalize_cnf(list(a) + list(b)) for a, b in itertools.product(left, right)]
    keep_product, graph_product = select(product)
    assert len(keep_product) == 4 and sum(map(len, graph_product)) == 0
    checks += 1

    signal.alarm(0)
    result = {
        "status": "COMPUTATIONAL",
        "claim": "RUP-IMPLICATION-SELECT1 bounded regression",
        "seed": args.seed,
        "cooperative_budget_seconds": args.budget,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "checks": checks,
        "random_portfolios": random_portfolios,
        "random_rup_edges_sound": random_edges,
        "strict_extension": strict_counts,
        "arc_antichain": antichain_counts,
        "independent_product": {"input": 4, "kept": len(keep_product), "edges": 0},
        "controls": {
            "renaming_and_literal_complement": "passed",
            "tautology_padding": "passed",
            "independent_products": "passed",
            "source_carry": "selector retains explicit CNFs and charges their storage",
            "current_scale_sat_calls": 0,
            "oracle_or_algebraic_replacement": "RUP soundness relativizes; no separation consequence",
        },
        "interpretation": (
            "The selector soundly preserves the OR of each tested frontier and strictly exceeds raw "
            "clause inclusion, but it leaves the assignment-residual antichain unchanged. Finite tests "
            "do not establish a universal density or asymptotic shrinkage theorem."
        ),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
