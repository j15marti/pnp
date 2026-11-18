#!/usr/bin/env python3
"""Independent finite checks for the T5 girth-transfer red-team report.

This script does not attempt an asymptotic lower bound.  It checks the exact
short-path language, the four-vertex critical obstruction, and an explicit
counterexample to confusing directed girth with underlying undirected girth.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys


T5 = {1, 3}


def arc_ok(a: int, b: int) -> bool:
    return (b - a) % 5 in T5


def path_counts(word: str) -> tuple[int, ...]:
    """Endpoint-difference counts for F/B traversal orientations."""
    counts = [0] * 5
    for choices in itertools.product((0, 1), repeat=len(word)):
        diff = 0
        for orientation, bit in zip(word, choices):
            # Forward: 1 or 3.  Backward traversal: -1 or -3 = 4 or 2.
            diff += (1 + 2 * bit) if orientation == "F" else (4 - 2 * bit)
        counts[diff % 5] += 1
    return tuple(counts)


def short_language() -> dict:
    rows = []
    supports = {}
    for length in range(1, 5):
        for word_tuple in itertools.product("FB", repeat=length):
            word = "".join(word_tuple)
            counts = path_counts(word)
            support = tuple(i for i, value in enumerate(counts) if value)
            rows.append({"word": word, "counts": counts, "support": support})
            if length <= 3:
                supports.setdefault(support, []).append(word)

    distinct = sorted(supports)
    assert len(distinct) == 9, len(distinct)
    assert all(len(row["support"]) == 5 for row in rows if len(row["word"]) == 4)

    irredundant = []
    universe = set(range(5))
    for mask in range(1, 1 << len(distinct)):
        family = [set(distinct[i]) for i in range(len(distinct)) if mask >> i & 1]
        intersection = set.intersection(universe, *family)
        # A constraint is indispensable iff deleting it strictly enlarges
        # the intersection.  This covers both SAT and UNSAT intersections.
        indispensable = all(
            (
                set.intersection(universe, *(family[:j] + family[j + 1 :]))
                if len(family) > 1
                else universe
            )
            != intersection
            for j in range(len(family))
        )
        if indispensable:
            irredundant.append(
                {
                    "supports": [sorted(x) for x in family],
                    "intersection": sorted(intersection),
                    "size": len(family),
                }
            )
    maximum = max(item["size"] for item in irredundant)
    assert maximum == 4
    return {
        "orientation_rows": rows,
        "distinct_short_supports": [list(x) for x in distinct],
        "representatives": {str(list(k)): v for k, v in supports.items()},
        "irredundant_subfamilies": len(irredundant),
        "irredundant_empty_intersections": sum(
            not item["intersection"] for item in irredundant
        ),
        "max_irredundant_size": maximum,
        "max_irredundant_examples": [x for x in irredundant if x["size"] == maximum],
    }


def enumerate_models(n: int, arcs: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    return [
        assignment
        for assignment in itertools.product(range(5), repeat=n)
        if all(arc_ok(assignment[u], assignment[v]) for u, v in arcs)
    ]


def critical_four_vertex() -> dict:
    arcs = [(0, 2), (0, 3), (1, 2), (3, 1), (3, 2)]
    assert not enumerate_models(4, arcs)
    deletions = []
    for index, edge in enumerate(arcs):
        remaining = arcs[:index] + arcs[index + 1 :]
        models = enumerate_models(4, remaining)
        assert models
        support = sorted({(model[edge[1]] - model[edge[0]]) % 5 for model in models})
        assert set(support) <= {0, 2, 4}
        deletions.append(
            {
                "deleted_arc": edge,
                "model_count": len(models),
                "missing_arc_difference_support": support,
                "first_model": models[0],
            }
        )
    assert deletions[-1]["model_count"] == 5
    assert deletions[-1]["missing_arc_difference_support"] == [2]
    return {"arcs": arcs, "unsat": True, "deletions": deletions}


def directed_vs_undirected_girth() -> dict:
    # Transitive K4: all arcs from the smaller to the larger endpoint.
    arcs = [(u, v) for u in range(4) for v in range(u + 1, 4)]
    # Every arc increases the label, hence there is no directed cycle.
    directed_acyclic = all(u < v for u, v in arcs)
    # The underlying graph is K4, containing triangle 0-1-2-0.
    triangle = [(0, 1), (1, 2), (0, 2)]
    assert directed_acyclic and all(edge in arcs for edge in triangle)
    return {
        "arcs": arcs,
        "directed_girth": "infinity",
        "underlying_undirected_girth": 3,
        "witness_triangle": [0, 1, 2, 0],
        "conclusion": "arbitrarily large directed girth does not imply underlying undirected girth greater than 3",
    }


def main() -> None:
    result = {
        "run_id": "LSPV5_T5_GIRTH_TRANSFER_20261118",
        "python": sys.version,
        "t5_relation_differences": sorted(T5),
        "short_path_audit": short_language(),
        "critical_four_vertex_audit": critical_four_vertex(),
        "directed_vs_undirected_girth_counterexample": directed_vs_undirected_girth(),
        "assertions": {
            "distinct_short_relations": 9,
            "length_four_universal": True,
            "max_irredundant_intersection": 4,
            "critical_source_edge_deletions_sat": 5,
            "directed_girth_transfer_to_undirected_girth": False,
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
