#!/usr/bin/env python3
"""Exact hostile control for full-interface tree composition.

All arithmetic is over GF(2).  The generated star has a rank-one affine
constraint in every module and two variables on every edge separator, but
the centre's full interface contains 2q variables.  Every child message is
essential to the global contradiction.
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path


def gf2_rank(rows: list[int], width: int) -> int:
    work = rows[:]
    rank = 0
    for col in range(width - 1, -1, -1):
        pivot = next((i for i in range(rank, len(work)) if (work[i] >> col) & 1), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> col) & 1):
                work[i] ^= work[rank]
        rank += 1
    return rank


def ranks(equations: list[tuple[int, int]], nvars: int) -> tuple[int, int]:
    coefficient = [mask for mask, _ in equations]
    augmented = [mask | (rhs << nvars) for mask, rhs in equations]
    return gf2_rank(coefficient, nvars), gf2_rank(augmented, nvars + 1)


def satisfied(assignment: int, equations: list[tuple[int, int]]) -> bool:
    return all(((assignment & mask).bit_count() & 1) == rhs for mask, rhs in equations)


def make_star(q: int) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    centre_mask = (1 << (2 * q)) - 1
    centre = (centre_mask, 1)
    leaves = [((1 << (2 * i)) | (1 << (2 * i + 1)), 0) for i in range(q)]
    return centre, leaves


def audit(q: int, brute: bool) -> dict:
    centre, leaves = make_star(q)
    equations = [centre] + leaves
    coeff_rank, aug_rank = ranks(equations, 2 * q)
    deletion_checks = []
    for j in range(q):
        reduced = [centre] + leaves[:j] + leaves[j + 1 :]
        cr, ar = ranks(reduced, 2 * q)
        deletion_checks.append({"leaf": j, "coefficient_rank": cr, "augmented_rank": ar, "consistent": cr == ar})

    brute_models = None
    if brute:
        brute_models = sum(satisfied(a, equations) for a in range(1 << (2 * q)))
        for j in range(q):
            reduced = [centre] + leaves[:j] + leaves[j + 1 :]
            assert sum(satisfied(a, reduced) for a in range(1 << (2 * q))) == 1 << q

    record = {
        "q": q,
        "variables": 2 * q,
        "modules": q + 1,
        "source_constraints": q + 1,
        "max_local_affine_codimension": 1,
        "max_edge_separator_width": 2,
        "centre_full_interface_width": 2 * q,
        "centre_full_table_assignments": 1 << (2 * q),
        "coefficient_rank": coeff_rank,
        "augmented_rank": aug_rank,
        "globally_consistent": coeff_rank == aug_rank,
        "all_child_messages_essential": all(x["consistent"] for x in deletion_checks),
        "parent_only_nonempty_shortcut_answer": "SAT",
        "correct_answer": "UNSAT",
        "deletion_checks": deletion_checks,
        "brute_force_model_count": brute_models,
    }
    assert coeff_rank == q and aug_rank == q + 1
    assert not record["globally_consistent"]
    assert record["all_child_messages_essential"]
    if brute:
        assert brute_models == 0
    return record


def main() -> None:
    start = time.perf_counter()
    cases = [audit(q, brute=(q <= 6)) for q in (1, 2, 3, 4, 5, 6, 8, 16, 32)]
    result = {
        "claim": "bounded edge separators and local codimension do not bound a module's full accumulated interface",
        "status": "PROVED/EXACT (symbolic rank proof); COMPUTATIONAL (finite execution checks)",
        "arithmetic": "GF(2)",
        "brute_force_scope": "q=1..6",
        "symbolic_scope": "every integer q>=1",
        "cases": cases,
        "elapsed_seconds": time.perf_counter() - start,
        "limitations": [
            "This family is polynomial-time solvable by Gaussian elimination.",
            "It is not a SAT lower bound and does not challenge the full-interface sufficient theorem.",
            "It falsifies only replacing full-interface width by maximum edge-separator width in raw table enumeration."
        ],
    }
    out = Path(__file__).with_name("2026-10-29_1248_FULL_INTERFACE_GLUING_REFEREE204_raw.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "max_q": 32, "elapsed_seconds": result["elapsed_seconds"], "output": str(out)}, sort_keys=True))


if __name__ == "__main__":
    main()
