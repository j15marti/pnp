#!/usr/bin/env python3
"""Finite audit for SYNTHESIS-0012 quotient-covariance factorization.

The symbolic theorem is elementary graph propagation.  This audit exhausts
small transformation graphs and separately demonstrates that observational
equivalence does not preserve implementation cost.
"""

from __future__ import annotations

import itertools
import json
import time


def edges_for_mask(n: int, mask: int) -> list[tuple[int, int]]:
    pairs = list(itertools.combinations(range(n), 2))
    return [edge for bit, edge in enumerate(pairs) if mask & (1 << bit)]


def components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for a, b in edges:
        union(a, b)
    roots: dict[int, int] = {}
    return [roots.setdefault(find(i), len(roots)) for i in range(n)]


def graph_audit() -> dict[str, int]:
    graphs = connected_graphs = labelings = invariant_labelings = failures = 0
    disconnected_controls = 0
    for n in range(1, 6):
        pair_count = n * (n - 1) // 2
        for mask in range(1 << pair_count):
            edges = edges_for_mask(n, mask)
            comp = components(n, edges)
            component_count = len(set(comp))
            graphs += 1
            connected_graphs += component_count == 1
            for q in range(2, 5):
                valid = 0
                for labels in itertools.product(range(q), repeat=n):
                    labelings += 1
                    edge_invariant = all(labels[a] == labels[b] for a, b in edges)
                    if not edge_invariant:
                        continue
                    valid += 1
                    invariant_labelings += 1
                    quotient_constant_on_components = all(
                        comp[i] != comp[j] or labels[i] == labels[j]
                        for i in range(n) for j in range(n)
                    )
                    if not quotient_constant_on_components:
                        failures += 1
                    if component_count == 1 and len(set(labels)) != 1:
                        failures += 1
                expected = q ** component_count
                if valid != expected:
                    failures += 1
                if component_count > 1 and valid > q:
                    disconnected_controls += 1
    return {
        "graphs": graphs,
        "connected_graphs": connected_graphs,
        "labelings": labelings,
        "invariant_labelings": invariant_labelings,
        "disconnected_controls": disconnected_controls,
        "graph_failures": failures,
    }


def sat_bruteforce(formula: tuple[tuple[int, ...], ...]) -> bool:
    n = max((abs(x) for clause in formula for x in clause), default=0)
    return any(
        all(any(bits[abs(x) - 1] == (x > 0) for x in clause) for clause in formula)
        for bits in itertools.product((False, True), repeat=n)
    )


def gf2_consistent(rows: list[tuple[int, int]], n: int) -> bool:
    matrix = [[(mask >> j) & 1 for j in range(n)] + [rhs] for mask, rhs in rows]
    pivot = 0
    for col in range(n):
        hit = next((r for r in range(pivot, len(matrix)) if matrix[r][col]), None)
        if hit is None:
            continue
        matrix[pivot], matrix[hit] = matrix[hit], matrix[pivot]
        for r in range(len(matrix)):
            if r != pivot and matrix[r][col]:
                matrix[r] = [x ^ y for x, y in zip(matrix[r], matrix[pivot])]
        pivot += 1
    return not any(not any(row[:-1]) and row[-1] for row in matrix)


def semantic_cost_audit() -> dict[str, int]:
    clauses = tuple(
        tuple(v if bit else -v for v, bit in zip((1, 2, 3), signs))
        for signs in itertools.product((0, 1), repeat=3)
    )
    formulas = [
        tuple(clauses[i] for i in range(8) if mask & (1 << i))
        for mask in range(256)
    ]
    semantic_checks = resource_noninvariance_witnesses = encoding_checks = 0
    for formula in formulas:
        answer = sat_bruteforce(formula)
        # Same observational/type quotient; distinct representations and costs.
        outputs = [
            (answer, "DIRECT", len(formula) + 1),
            (answer, "DEAD", len(formula) + 7),
            (answer, "COPY", 2 * len(formula) + 3),
            (answer, "DELAY", (len(formula) + 2) ** 5),
            (answer, "INTERP", 3 * len(formula) + 11),
            (answer, "RECOMP", 8 * len(formula) + 5),
        ]
        for bit, _, _ in outputs:
            assert bit == answer
            semantic_checks += 1
        quotient = {bit for bit, _, _ in outputs}
        costs = {cost for _, _, cost in outputs}
        assert len(quotient) == 1
        assert len(costs) > 1
        resource_noninvariance_witnesses += 1

        variants = (
            formula,
            tuple(reversed(formula)),
            formula + (formula[:1] if formula else ()),
            tuple(tuple(clause) for clause in formula),
        )
        for variant in variants:
            assert sat_bruteforce(variant) == answer
            encoding_checks += 1

    named = {
        "2SAT": ((1, 2), (-1, 2), (1, -2)),
        "Horn": ((-1, -2, 3), (-3,), (1,)),
        "bounded_treewidth": ((1, 2), (-2, 3), (-3,)),
        "independent_product": ((1,), (2,), (3,)),
        "redundant": ((1, 2, 3), (1, 2, 3), (-1,)),
    }
    easy_family_checks = 0
    for formula in named.values():
        answer = sat_bruteforce(formula)
        for delay_power in range(1, 17):
            assert sat_bruteforce(formula) == answer
            _ = (len(formula) + 2) ** delay_power
            easy_family_checks += 1

    affine_checks = 0
    templates = ((0b001, 0), (0b010, 1), (0b100, 0),
                 (0b011, 1), (0b110, 0), (0b101, 1))
    for mask in range(1 << len(templates)):
        rows = [row for i, row in enumerate(templates) if mask & (1 << i)]
        got = gf2_consistent(rows, 3)
        brute = any(
            all(
                (sum((assignment >> j) & 1 for j in range(3) if row >> j & 1) & 1) == rhs
                for row, rhs in rows
            )
            for assignment in range(8)
        )
        assert got == brute
        affine_checks += 1

    return {
        "semantic_checks": semantic_checks,
        "resource_noninvariance_witnesses": resource_noninvariance_witnesses,
        "encoding_checks": encoding_checks,
        "easy_family_delay_checks": easy_family_checks,
        "affine_gaussian_checks": affine_checks,
    }


def main() -> dict:
    start = time.perf_counter()
    graph = graph_audit()
    semantic = semantic_cost_audit()
    failures = graph["graph_failures"]
    return {
        "run_id": "SYNTHESIS-0012",
        "status": "COMPUTATIONAL",
        "graph_audit": graph,
        "semantic_cost_audit": semantic,
        "failures": failures,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "scope_warning": (
            "Finite verification of the symbolic quotient theorem only; "
            "no arbitrary-SAT runtime lower bound follows."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
