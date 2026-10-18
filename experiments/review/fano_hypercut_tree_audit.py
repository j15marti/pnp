#!/usr/bin/env python3
"""Exact finite audit for the FANO-HYPERCUT-TREE29 separator theorem."""

from __future__ import annotations

import itertools
import json
from collections import Counter


NAMES = ("a", "b", "u1", "u2", "u3", "u4", "u5")
SUPPORTS = (
    ("a", "b", "u1"),
    ("a", "u2", "u3"),
    ("a", "u4", "u5"),
    ("b", "u2", "u4"),
    ("b", "u3", "u5"),
    ("u1", "u2", "u5"),
    ("u1", "u3", "u4"),
)


def fano_partition_audit() -> dict:
    hist = Counter()
    minimizers = []
    for aux in itertools.product((0, 1), repeat=5):
        side = {"a": 0, "b": 1, **dict(zip(NAMES[2:], aux))}
        crossing = sum(len({side[x] for x in support}) == 2 for support in SUPPORTS)
        hist[crossing] += 1
        minimizers.append((crossing, aux))
    minimum = min(x[0] for x in minimizers)
    return {
        "minimum_crossing_clause_supports": minimum,
        "minimizing_auxiliary_partitions": [list(a) for c, a in minimizers if c == minimum],
        "histogram": {str(k): hist[k] for k in sorted(hist)},
    }


def prufer_tree(seq: tuple[int, ...], n: int) -> tuple[tuple[int, int], ...]:
    degree = [1] * n
    for x in seq:
        degree[x] += 1
    edges = []
    for x in seq:
        leaf = next(i for i, d in enumerate(degree) if d == 1)
        edges.append((leaf, x))
        degree[leaf] -= 1
        degree[x] -= 1
    last = [i for i, d in enumerate(degree) if d == 1]
    edges.append(tuple(last))
    return tuple(edges)


def coordinate_loads(edges: tuple[tuple[int, int], ...], k: int) -> tuple[int, ...]:
    return tuple(sum(((u >> j) & 1) != ((v >> j) & 1) for u, v in edges) for j in range(k))


def exhaustive_tree_audit(k: int) -> dict:
    n = 1 << k
    best = n * n
    witness = None
    checked = 0
    lower = (n - 1 + k - 1) // k
    violations = 0
    for seq in itertools.product(range(n), repeat=max(0, n - 2)):
        edges = prufer_tree(seq, n) if n > 1 else ()
        loads = coordinate_loads(edges, k)
        maximum = max(loads)
        if maximum < lower:
            violations += 1
        if maximum < best:
            best = maximum
            witness = {"prufer": list(seq), "edges": [list(e) for e in edges], "loads": list(loads)}
        checked += 1
    return {
        "k": k,
        "m": n,
        "trees_checked": checked,
        "theorem_lower_bound": lower,
        "minimum_observed_max_coordinate_load": best,
        "violations": violations,
        "tight_witness": witness,
    }


def main() -> None:
    pair_intersections = [
        len(set(SUPPORTS[i]) & set(SUPPORTS[j]))
        for i in range(len(SUPPORTS))
        for j in range(i + 1, len(SUPPORTS))
    ]
    result = {
        "artifact": "FANO-HYPERCUT-TREE29",
        "status": "COMPUTATIONAL_AUDIT_OF_PROVED_FINITE_IDENTITIES",
        "fano_support_count": len(SUPPORTS),
        "maximum_pairwise_support_intersection": max(pair_intersections),
        "separated_terminal_partition": fano_partition_audit(),
        "exhaustive_labelled_tree_audits": [exhaustive_tree_audit(k) for k in (1, 2, 3)],
        "claim": "For m=2^k gauge copies labelled by the k-cube, every connected equality graph has a coordinate cut meeting at least ceil((m-1)/k) equality edges. Replacing edges by fresh Fano equality gadgets forces at least three crossing clause supports per crossed equality edge.",
        "scope_firewall": "This is aligned-cut additive distortion, not target treewidth, PC degree, or unrestricted machine time/space.",
    }
    with open("FANO_HYPERCUT_TREE29_results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
