#!/usr/bin/env python3
"""Exhaustive audit of the exact local-swap star query theorem.

The theorem is symbolic.  This program independently checks all sensitivity
graphs through two exact-(2,2) variables, all graph tuples through three
variables for matching/cover additivity, and the concrete Role-4 two-sign
source/witness replay.  Python standard library only.
"""

from __future__ import annotations

import ast
import functools
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


RUN_ID = "SWAP-STAR-CEILING104"
SEED = 202610240248
SOURCE = Path("results/raw/review/DOECKER61_original_source.txt")
WITNESS_HEX = "39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598"
BASE_EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))


def edges(mask):
    return tuple(edge for i, edge in enumerate(BASE_EDGES) if mask >> i & 1)


def min_vertex_cover(mask):
    es = edges(mask)
    for size in range(5):
        for chosen in itertools.combinations(range(4), size):
            cover = set(chosen)
            if all(u in cover or v in cover for u, v in es):
                return size
    raise AssertionError("unreachable")


def max_matching(mask):
    es = edges(mask)
    best = 0
    for size in range(len(es) + 1):
        for chosen in itertools.combinations(es, size):
            flat = [v for edge in chosen for v in edge]
            if len(flat) == len(set(flat)):
                best = max(best, size)
    return best


def star_examples(masks):
    """Return (bit-vector, label) examples: center 0, sensitive neighbors 1."""
    center = tuple(bit for _ in masks for bit in (1, 1, 0, 0))
    examples = [(center, 0)]
    for variable, mask in enumerate(masks):
        for u, v in edges(mask):
            neighbor = list(center)
            offset = 4 * variable
            neighbor[offset + u] = 0
            neighbor[offset + v] = 1
            examples.append((tuple(neighbor), 1))
    return tuple(examples)


def decision_tree_depth(examples):
    """Exact deterministic query depth for a finite promise problem."""
    coordinates = tuple(range(len(examples[0][0])))

    @functools.lru_cache(maxsize=None)
    def solve(indices, remaining):
        labels = {examples[i][1] for i in indices}
        if len(labels) <= 1:
            return 0
        best = 10**9
        for coordinate in remaining:
            zero = tuple(i for i in indices if examples[i][0][coordinate] == 0)
            one = tuple(i for i in indices if examples[i][0][coordinate] == 1)
            if not zero or not one:
                continue
            rest = tuple(c for c in remaining if c != coordinate)
            best = min(best, 1 + max(solve(zero, rest), solve(one, rest)))
        return best

    return solve(tuple(range(len(examples))), coordinates)


def load_source():
    lines = [line for line in SOURCE.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    return [tuple(map(int, clause))
            for clause in ast.literal_eval("\n".join(lines))]


def clause_satisfied(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def concrete_pair_audit():
    source = load_source()
    assert len(source) == 264
    counts = Counter(lit for clause in source for lit in clause)
    assert all(counts[x] == counts[-x] == 2 for x in range(1, 199))
    target = [list(clause) for clause in source]
    assert tuple(target[3]) == (-2, -3, -194)
    assert tuple(target[13]) == (3, 9, 10)
    target[3][1] = 3
    target[13][0] = -3
    target = [tuple(clause) for clause in target]
    counts2 = Counter(lit for clause in target for lit in clause)
    assert counts == counts2
    assert [tuple(abs(x) for x in c) for c in source] == [
        tuple(abs(x) for x in c) for c in target
    ]
    assignment_bits = format(int(WITNESS_HEX, 16), "0198b")
    assignment = {i + 1: bit == "1"
                  for i, bit in enumerate(assignment_bits)}
    old_bad = [i for i, c in enumerate(source)
               if not clause_satisfied(c, assignment)]
    new_bad = [i for i, c in enumerate(target)
               if not clause_satisfied(c, assignment)]
    assert old_bad == [3]
    assert new_bad == []
    return {
        "variables": 198,
        "clauses": 264,
        "changed_sign_fields": 2,
        "ordered_unsigned_support_preserved": True,
        "repaired_witness_verified": True,
        "original_unsat_label": "imported from DOECKER-CORE-CERT61",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    }


def main():
    checks = 0
    graph_rows = []
    for mask in range(16):
        cover = min_vertex_cover(mask)
        matching = max_matching(mask)
        assert cover == matching <= 2
        checks += 2
        graph_rows.append((mask, cover))

    # Exact decision-tree equality for every one- and two-variable star.
    star_instances = 0
    for n in (1, 2):
        for masks in itertools.product(range(16), repeat=n):
            predicted = sum(graph_rows[mask][1] for mask in masks)
            observed = decision_tree_depth(star_examples(masks))
            assert observed == predicted <= 2 * n
            checks += 2
            star_instances += 1

    # Exhaustive additivity/ceiling check for all three-variable graph tuples.
    triples = 0
    for masks in itertools.product(range(16), repeat=3):
        total_cover = sum(min_vertex_cover(mask) for mask in masks)
        total_matching = sum(max_matching(mask) for mask in masks)
        assert total_cover == total_matching <= 6
        checks += 2
        triples += 1

    concrete = concrete_pair_audit()
    checks += 10
    payload = {
        "run_id": RUN_ID,
        "status": {
            "star_query_theorem": "symbolic proof in report; exhaustive audit",
            "finite_audit": "COMPUTATIONAL",
            "unrestricted_time_lower_bound": "OPEN",
        },
        "seed": SEED,
        "one_variable_graphs": 16,
        "exact_star_decision_tree_instances": star_instances,
        "three_variable_graph_tuples": triples,
        "maximum_matching_per_exact_2_2_variable": 2,
        "maximum_star_query_depth_for_n_variables": "2n",
        "assertion_accounted_checks": checks,
        "concrete_role4_pair": concrete,
        "failures": 0,
        "limitations": [
            "The theorem concerns the center-plus-sensitive-neighbor promise.",
            "It is an addressed sign-field query statement, not a RAM/Turing time lower bound.",
            "Sensitivity-graph acquisition may itself require SAT classifications.",
            "The original 198-variable UNSAT certificate is imported, not rerun.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["sha256_without_sha_field"] = hashlib.sha256(
        canonical.encode()
    ).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
