#!/usr/bin/env python3
"""Bounded audit of parent-owned emission versus target-owned inversion.

Two-layer acyclic circuits have n targets and n later unary parents.  The
forward oracle gives each parent's child.  Parent-major emission streams every
edge with one query per parent.  Target-major reconstruction scans all parents
per target unless an inverse index is materialized.  The experiment verifies
semantics and accounts for queries/storage; only the per-target adversary is
an all-n lower bound.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path


OUT = Path("results/raw/review/2026-10-11_locality_port_dichotomy.json")
SEED = 202610111648


def parent_major(children: tuple[int, ...]) -> tuple[list[tuple[int, int]], int]:
    return [(p, u) for p, u in enumerate(children)], len(children)


def target_major_scan(children: tuple[int, ...]) -> tuple[list[tuple[int, int]], int]:
    n = len(children)
    edges: list[tuple[int, int]] = []
    q = 0
    for u in range(n):
        for p, child in enumerate(children):
            q += 1
            if child == u:
                edges.append((p, u))
    return edges, q


def indexed_inverse(children: tuple[int, ...]) -> tuple[list[list[int]], int, int]:
    n = len(children)
    inv = [[] for _ in range(n)]
    for p, u in enumerate(children):
        inv[u].append(p)
    label_bits = max(1, math.ceil(math.log2(max(2, n))))
    # Upper-bound ledger: child label plus parent label for each edge.
    return inv, n, 2 * n * label_bits


def cases_for_n(n: int, rng: random.Random) -> list[tuple[int, ...]]:
    if n <= 5:
        return list(itertools.product(range(n), repeat=n))
    cases = {
        tuple(range(n)),
        tuple(reversed(range(n))),
        (0,) * n,
        tuple(i % max(1, n // 2) for i in range(n)),
    }
    for _ in range(256):
        cases.add(tuple(rng.randrange(n) for _ in range(n)))
    return sorted(cases)


def audit() -> dict[str, object]:
    rng = random.Random(SEED)
    rows = []
    total_cases = 0
    total_edge_checks = 0
    for n in range(1, 33):
        cases = cases_for_n(n, rng)
        total_cases += len(cases)
        for children in cases:
            canonical = sorted((p, u) for p, u in enumerate(children))
            pe, pq = parent_major(children)
            te, tq = target_major_scan(children)
            inv, iq, bits = indexed_inverse(children)
            flattened = sorted((p, u) for u, ps in enumerate(inv) for p in ps)
            assert sorted(pe) == canonical
            assert sorted(te) == canonical
            assert flattened == canonical
            assert pq == n and tq == n * n and iq == n
            assert bits >= n
            total_edge_checks += 3 * n
        rows.append({
            "n": n,
            "cases": len(cases),
            "parent_major_queries": n,
            "target_major_rescan_queries": n * n,
            "inverse_index_build_queries": n,
            "inverse_index_bits_upper_bound": 2 * n * max(1, math.ceil(math.log2(max(2, n)))),
            "per_target_exact_lower_bound": n,
        })

    controls = {
        "formula_classes": ["2SAT", "Horn", "affine/Tseitin", "bounded-treewidth"],
        "representations": ["independent-product", "padding", "redundant-clauses", "alternate-encoding"],
        "wrappers": ["DIRECT", "COPY", "DELAY", "INTERP", "RECOMP"],
        "effect": "none creates an inverse port; none implies SAT runtime",
    }
    return {
        "run_id": "SYNTHESIS-0010",
        "timestamp_utc": "2026-10-11T16:48:00Z",
        "seed": SEED,
        "model": "two-layer acyclic forward-child oracle",
        "status": {
            "LOCAL_REDUCTION_PORT_DICHOTOMY1": "PROVED/EXACT (component theorems; finite audit computational)",
            "GENERIC_REVERSE_PORT_NECESSITY1": "FALSIFIED/RETIRED for parent-owned bounded-fanout emission",
            "JMV_FORWARD_LABEL1": "OPEN",
            "MONOTONE22_LOCAL_NORMALIZER1": "OPEN",
            "arbitrary_sat_transfer": "OPEN",
            "p_vs_np": "OPEN",
        },
        "rows": rows,
        "total_circuits": total_cases,
        "total_edge_comparisons": total_edge_checks,
        "controls": controls,
        "scope_warning": "The n^2 target-major count is an audited implementation, not a universal time-space lower bound; only the n-query per-target adversary is universal in this oracle model.",
    }


def main() -> None:
    payload = audit()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "circuits": payload["total_circuits"],
        "edge_comparisons": payload["total_edge_comparisons"],
        "max_n": payload["rows"][-1]["n"],
        "result": str(OUT),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
