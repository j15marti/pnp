#!/usr/bin/env python3
"""Exhaustive audit of the smallest degree-feasible two-clause connector.

Boundary variables 0..5 have positive degree one and negative degree zero.
Internal variables 6..11 have positive and negative degree two.  The target
existential projection is (b0 or b1 or b2) and (b3 or b4 or b5).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


BOUNDARY = tuple(range(6))
INTERNAL = tuple(range(6, 12))
ALL_ASSIGNMENTS = (1 << 4096) - 1
NEGATIVE_TYPES = (
    ((6, 7, 8), (6, 7, 9), (8, 10, 11), (9, 10, 11)),
    ((6, 7, 8), (6, 9, 10), (7, 9, 11), (8, 10, 11)),
)


def clause_mask(edge: tuple[int, int, int], positive: bool) -> int:
    mask = 0
    for assignment in range(4096):
        satisfied = any(bool((assignment >> v) & 1) == positive for v in edge)
        if satisfied:
            mask |= 1 << assignment
    return mask


POSITIVE_MASKS = {
    edge: clause_mask(edge, True)
    for edge in itertools.combinations(range(12), 3)
}
NEGATIVE_MASKS = {
    edge: clause_mask(edge, False)
    for edge in itertools.combinations(INTERNAL, 3)
}
BOUNDARY_MASKS = []
for boundary_assignment in range(64):
    mask = 0
    for internal_assignment in range(64):
        mask |= 1 << (boundary_assignment | (internal_assignment << 6))
    BOUNDARY_MASKS.append(mask)


def target(boundary_assignment: int) -> bool:
    return bool((boundary_assignment & 0b000111) and
                (boundary_assignment & 0b111000))


def connected(edges: tuple[tuple[int, int, int], ...]) -> bool:
    adjacency = [set() for _ in range(12)]
    for edge in edges:
        for vertex in edge:
            adjacency[vertex].update(set(edge) - {vertex})
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == 12


def direct_projection(
    positive_edges: tuple[tuple[int, int, int], ...],
    negative_edges: tuple[tuple[int, int, int], ...],
) -> list[bool]:
    projection = [False] * 64
    for boundary_assignment in range(64):
        for internal_assignment in range(64):
            assignment = boundary_assignment | (internal_assignment << 6)
            positive_ok = all(
                any((assignment >> v) & 1 for v in edge)
                for edge in positive_edges
            )
            negative_ok = all(
                any(not ((assignment >> v) & 1) for v in edge)
                for edge in negative_edges
            )
            if positive_ok and negative_ok:
                projection[boundary_assignment] = True
                break
    return projection


def labeled_negative_hypergraphs() -> list[tuple[tuple[int, int, int], ...]]:
    triples = list(itertools.combinations(range(6), 3))
    result = []
    for edges in itertools.combinations(triples, 4):
        degrees = [0] * 6
        for edge in edges:
            for vertex in edge:
                degrees[vertex] += 1
        if degrees == [2] * 6:
            result.append(edges)
    return result


def canonical_under_permutation(
    edges: tuple[tuple[int, int, int], ...]
) -> tuple[tuple[int, int, int], ...]:
    return min(
        tuple(sorted(tuple(sorted(permutation[v] for v in edge)) for edge in edges))
        for permutation in itertools.permutations(range(6))
    )


def enumerate_positive_hypergraphs(callback) -> None:
    degrees = (1,) * 6 + (2,) * 6

    def recurse(
        remaining: tuple[int, ...],
        edges: tuple[tuple[int, int, int], ...],
    ) -> None:
        try:
            vertex = next(i for i, degree in enumerate(remaining) if degree)
        except StopIteration:
            if len(edges) == 6:
                callback(edges)
            return

        degree = remaining[vertex]
        later = [i for i in range(vertex + 1, 12) if remaining[i]]
        pairs = list(itertools.combinations(later, 2))
        for chosen_pairs in itertools.combinations(pairs, degree):
            used = [0] * 12
            for first, second in chosen_pairs:
                used[first] += 1
                used[second] += 1
            if any(used[i] > remaining[i] for i in later):
                continue
            next_remaining = list(remaining)
            next_remaining[vertex] = 0
            for i in later:
                next_remaining[i] -= used[i]
            new_edges = tuple((vertex, *pair) for pair in chosen_pairs)
            recurse(tuple(next_remaining), edges + new_edges)

    recurse(degrees, ())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()

    labeled_negative = labeled_negative_hypergraphs()
    canonical_counts: dict[str, int] = {}
    for edges in labeled_negative:
        canonical = canonical_under_permutation(edges)
        key = repr(canonical)
        canonical_counts[key] = canonical_counts.get(key, 0) + 1
    assert sorted(canonical_counts.values()) == [30, 45]
    assert len(canonical_counts) == 2

    negative_formula_masks = []
    for edges in NEGATIVE_TYPES:
        mask = ALL_ASSIGNMENTS
        for edge in edges:
            mask &= NEGATIVE_MASKS[edge]
        negative_formula_masks.append(mask)

    positive_count = 0
    relation_hits = [0, 0]
    connected_hits = [0, 0]
    boundary_clause_hits = [0, 0]
    examples = [None, None]
    direct_cross_checks = 0
    projection_tests = 0

    def inspect(positive_edges: tuple[tuple[int, int, int], ...]) -> None:
        nonlocal positive_count, direct_cross_checks, projection_tests
        positive_count += 1
        positive_formula_mask = ALL_ASSIGNMENTS
        for edge in positive_edges:
            positive_formula_mask &= POSITIVE_MASKS[edge]

        for type_index, negative_formula_mask in enumerate(negative_formula_masks):
            formula_mask = positive_formula_mask & negative_formula_mask
            relation_ok = True
            for boundary_assignment in range(64):
                projection_tests += 1
                exists = bool(formula_mask & BOUNDARY_MASKS[boundary_assignment])
                if exists != target(boundary_assignment):
                    relation_ok = False
                    break
            if not relation_ok:
                continue

            relation_hits[type_index] += 1
            has_original_clauses = ((0, 1, 2) in positive_edges and
                                    (3, 4, 5) in positive_edges)
            if has_original_clauses:
                boundary_clause_hits[type_index] += 1
            if connected(positive_edges + NEGATIVE_TYPES[type_index]):
                connected_hits[type_index] += 1
            if examples[type_index] is None:
                examples[type_index] = positive_edges

            direct = direct_projection(positive_edges, NEGATIVE_TYPES[type_index])
            assert direct == [target(value) for value in range(64)]
            direct_cross_checks += 4096

    enumerate_positive_hypergraphs(inspect)

    assert positive_count == 1_417_800
    assert relation_hits == [75, 75]
    assert boundary_clause_hits == relation_hits
    assert connected_hits == [0, 0]

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "SYNTHESIS-0004",
        "timestamp_utc": "2026-10-11T09:48:00Z",
        "model": {
            "boundary_variables": 6,
            "internal_variables": 6,
            "boundary_positive_degree": 1,
            "boundary_negative_degree": 0,
            "internal_positive_degree": 2,
            "internal_negative_degree": 2,
            "target_relation": "OR(0,1,2) AND OR(3,4,5)",
            "proper_unique_monotone_clauses": True,
        },
        "enumeration": {
            "positive_hypergraphs": positive_count,
            "negative_labeled_hypergraphs": len(labeled_negative),
            "negative_isomorphism_types": 2,
            "negative_orbit_sizes": sorted(canonical_counts.values()),
            "projection_tests_until_first_mismatch_or_completion": projection_tests,
            "relation_hits_by_negative_type": relation_hits,
            "hits_containing_both_original_boundary_clauses": boundary_clause_hits,
            "connected_relation_hits": connected_hits,
            "direct_assignment_cross_checks": direct_cross_checks,
            "examples": [list(map(list, example)) for example in examples],
        },
        "exact_arithmetic_guards": {
            "internal_count_congruence": "k = 0 mod 3",
            "k_0": "only the two boundary clauses; disconnected",
            "k_3": "requires two distinct negative triples on three internal variables; impossible",
            "k_6": "exhaustive computational search; every semantic hit is disconnected",
        },
        "status": {
            "K6-TWO-CLAUSE-CONNECTOR1": "COMPUTATIONAL (no connected hit)",
            "CONNECTED-BALANCED-PIN-LIFT1": "OPEN",
            "UCORE-TIME1": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "runtime_seconds": elapsed,
        "seed": None,
        "search_type": "exhaustive labeled positive hypergraphs modulo two proved negative orbits",
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("RESULT_SHA256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
