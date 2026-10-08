#!/usr/bin/env python3
"""Finite audit for SIGNED-TWIN-REFINE1.

The theorem is proved separately.  This runner compares feature-by-feature
partition refinement with direct signed-column construction, checks the
three-child macro and a conservative pre-deduplication size gate, and records
hostile controls.  Every run has a cooperative 25-second alarm.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import signal
import time
from pathlib import Path

from signed_twin_macro_test import (
    CNF,
    canonical_cnf,
    random_twin_formula,
    restrict,
    signed_profile,
    signed_twin_children,
    token_length,
    twin_classes,
    variables,
)


def refinement_classes(cnf: CNF, declared: tuple[int, ...] | None = None):
    """Return signed-column classes by stable feature refinement.

    One feature is the positive or negative incidence set of one clause.
    The Python sets model the linked-list partition used in the proof; the
    counters expose the source-linear incidence ledger.
    """
    vs = tuple(sorted(set(declared or ()) | set(variables(cnf))))
    if not vs:
        return (), {"literal_touches": 0, "features": 2 * len(cnf), "splits": 0}
    blocks: dict[int, set[int]] = {0: set(vs)}
    block_of = {v: 0 for v in vs}
    next_block = 1
    touches = 0
    splits = 0

    for clause in cnf:
        for feature in (
            [lit for lit in clause if lit > 0],
            [-lit for lit in clause if lit < 0],
        ):
            touched: dict[int, list[int]] = {}
            for v in feature:
                touches += 1
                touched.setdefault(block_of[v], []).append(v)
            for bid, members in touched.items():
                old = blocks[bid]
                if len(members) == len(old):
                    continue
                new = set(members)
                old.difference_update(new)
                blocks[next_block] = new
                for v in new:
                    block_of[v] = next_block
                next_block += 1
                splits += 1

    classes = tuple(sorted(tuple(sorted(block)) for block in blocks.values() if len(block) >= 2))
    return classes, {"literal_touches": touches, "features": 2 * len(cnf), "splits": splits}


def prededup_child_bounds(cnf: CNF, group: tuple[int, ...]) -> tuple[int, int, int]:
    """Exact token sizes before duplicate-clause canonicalization.

    Clause and literal deletion can only reduce these values further.
    """
    g = set(group)
    sizes = [1, 1, 1]  # all-zero, all-one, one mixed
    for clause in cnf:
        pos = any(lit > 0 and lit in g for lit in clause)
        neg = any(lit < 0 and -lit in g for lit in clause)
        assert not (pos and neg), "canonical tautology-free clause required"
        removed = sum(1 for lit in clause if abs(lit) in g)
        base = 1 + len(clause)
        # all-zero satisfies negative occurrences; all-one satisfies positive.
        sizes[0] += 0 if neg else base - removed
        sizes[1] += 0 if pos else base - removed
        # A mixed assignment satisfies every incident signed-twin clause.
        sizes[2] += 0 if (pos or neg) else base
    return tuple(sizes)


def random_cnf(rng: random.Random, n: int, m: int, width: int = 4) -> CNF:
    clauses = []
    for _ in range(m):
        chosen = rng.sample(range(1, n + 1), rng.randint(0, min(width, n)))
        clauses.append([rng.choice((-1, 1)) * v for v in chosen])
    return canonical_cnf(clauses)


def direct_classes(cnf: CNF, declared: tuple[int, ...] | None = None):
    vs = tuple(sorted(set(declared or ()) | set(variables(cnf))))
    groups: dict[tuple[int, ...], list[int]] = {}
    for v in vs:
        groups.setdefault(signed_profile(cnf, v), []).append(v)
    return tuple(sorted(tuple(g) for g in groups.values() if len(g) >= 2))


def run(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    counts = {
        "exhaustive_formulas": 0,
        "random_formulas": 0,
        "twin_macro_checks": 0,
        "size_bound_checks": 0,
        "near_twin_controls": 0,
        "independent_product_controls": 0,
        "padding_controls": 0,
        "easy_family_controls": 0,
        "rename_complement_controls": 0,
    }
    total_touches = 0
    total_literals = 0
    max_splits = 0

    # Exhaust all subsets of a small clause universe, including the empty clause.
    universe = canonical_cnf([
        (), (1,), (-1,), (2,), (-2,), (3,), (-3,), (1, 2), (-1, -2),
        (1, 3), (-1, -3), (2, 3), (-2, -3),
    ])
    for mask in range(1 << len(universe)):
        cnf = tuple(universe[i] for i in range(len(universe)) if mask & (1 << i))
        got, ledger = refinement_classes(cnf, (1, 2, 3, 4))
        assert got == direct_classes(cnf, (1, 2, 3, 4))
        literal_count = sum(map(len, cnf))
        assert ledger["literal_touches"] == literal_count
        total_touches += ledger["literal_touches"]
        total_literals += literal_count
        max_splits = max(max_splits, ledger["splits"])
        counts["exhaustive_formulas"] += 1

    for _ in range(4000):
        n = rng.randint(2, 10)
        cnf = random_cnf(rng, n, rng.randint(0, 2 * n + 6))
        got, ledger = refinement_classes(cnf, tuple(range(1, n + 1)))
        assert got == direct_classes(cnf, tuple(range(1, n + 1)))
        literal_count = sum(map(len, cnf))
        assert ledger["literal_touches"] == literal_count
        total_touches += ledger["literal_touches"]
        total_literals += literal_count
        max_splits = max(max_splits, ledger["splits"])
        counts["random_formulas"] += 1
        for group in got:
            bounds = prededup_child_bounds(cnf, group)
            actual = tuple(token_length(child) for child in signed_twin_children(cnf, group))
            assert max(actual) <= max(bounds)
            assert all(size <= token_length(cnf) for size in actual)
            counts["twin_macro_checks"] += 1
            counts["size_bound_checks"] += len(actual)

    # Guaranteed twins, near-twin breakage, renaming/complementation, and padding.
    for _ in range(400):
        n = rng.randint(4, 9)
        group = tuple(sorted(rng.sample(range(1, n + 1), rng.randint(2, n - 1))))
        cnf = random_twin_formula(rng, n, group)
        certified = refinement_classes(cnf, tuple(range(1, n + 1)))[0]
        assert any(set(group) <= set(block) for block in certified)
        broken = canonical_cnf(list(cnf) + [(group[0], n + 1)])
        if signed_profile(broken, group[0]) != signed_profile(broken, group[1]):
            broken_classes = refinement_classes(broken)[0]
            assert not any(set(group) <= set(block) for block in broken_classes)
            counts["near_twin_controls"] += 1

        perm = list(range(n + 1))
        shuffled = list(range(1, n + 1))
        rng.shuffle(shuffled)
        for old, new in enumerate(shuffled, 1):
            perm[old] = new
        complemented = set(rng.sample(range(1, n + 1), rng.randint(0, n)))
        transformed = canonical_cnf([
            [
                (1 if lit > 0 else -1)
                * (-1 if abs(lit) in complemented else 1)
                * perm[abs(lit)]
                for lit in clause
            ]
            for clause in cnf
        ])
        assert refinement_classes(transformed)[0] == direct_classes(transformed)
        counts["rename_complement_controls"] += 1

        padded = canonical_cnf(list(cnf) + list(cnf) * 3)
        assert padded == cnf
        assert refinement_classes(padded)[0] == refinement_classes(cnf)[0]
        counts["padding_controls"] += 1

    # Easy structural families: Horn, 2-CNF, affine-XOR encodings, and paths.
    easy = []
    easy.append(canonical_cnf([(-1, -2, 3), (-3, 4), (-4,)]))
    easy.append(canonical_cnf([(1, 2), (-2, 3), (-3, -1)]))
    easy.append(canonical_cnf([(1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)]))
    easy.append(canonical_cnf([(i, i + 1) for i in range(1, 9)]))
    for cnf in easy:
        assert refinement_classes(cnf)[0] == direct_classes(cnf)
        counts["easy_family_controls"] += 1

    # Independent product: profiles acquire disjoint clause coordinates.
    for _ in range(200):
        left = random_twin_formula(rng, 5, (1, 2))
        right = canonical_cnf([
            [((1 if lit > 0 else -1) * (abs(lit) + 5)) for lit in clause]
            for clause in random_twin_formula(rng, 5, (1, 2))
        ])
        product = canonical_cnf(list(left) + list(right))
        assert refinement_classes(product)[0] == direct_classes(product)
        counts["independent_product_controls"] += 1

    gamma = (1 + math.sqrt(5)) / 2
    endpoint_grid = []
    for u in (0.50, 2 / 3, 0.75, 0.80, 0.82, 1.0):
        for b in (0.50, 2 / 3, 0.75, 0.80, 0.82):
            endpoint_grid.append({
                "u": u,
                "b": b,
                "C_plus_sigma": 1 + max(u, b),
                "below_Williams_phi": 1 + max(u, b) < gamma,
            })

    return {
        "claim": "SIGNED-TWIN-REFINE1",
        "status": "COMPUTATIONAL finite audit of a separately proved exact theorem",
        "seed": seed,
        "counts": counts,
        "incidence_ledger": {
            "total_literal_touches": total_touches,
            "total_literal_occurrences": total_literals,
            "touches_equal_occurrences": total_touches == total_literals,
            "max_partition_splits": max_splits,
        },
        "endpoint_grid": endpoint_grid,
        "source_scale_sat_calls": 0,
        "oracle_calls": 0,
        "notes": [
            "The finite run validates the implementation, not asymptotic coverage.",
            "The partition arrays require O(n log M) bits in the read-only source model.",
            "Explicit recursive children additionally require sigma=max(u,b).",
            "The macro is partial; it safely abstains when no accepted twin class exists.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=20261008)
    args = parser.parse_args()
    signal.alarm(25)
    started = time.perf_counter()
    result = run(args.seed)
    result["elapsed_seconds"] = time.perf_counter() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
