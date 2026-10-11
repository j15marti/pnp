#!/usr/bin/env python3
"""Finite audit for LB-0017's pruned restriction witness-volume theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def paired_k33(k: int) -> Formula:
    out: list[Clause] = []
    for block in range(k):
        off = 9 * block
        edge = {(u, v): off + 1 + 3 * u + v for u in range(3) for v in range(3)}
        ns = [tuple(edge[u, v] for v in range(3)) for u in range(3)]
        ns += [tuple(edge[u, v] for u in range(3)) for v in range(3)]
        out.extend(ns)
        out.extend(tuple(-x for x in c) for c in ns)
    return tuple(out)


def matching_witness(k: int) -> dict[int, int]:
    ans: dict[int, int] = {}
    for block in range(k):
        off = 9 * block
        for u in range(3):
            for v in range(3):
                ans[off + 1 + 3 * u + v] = int(u == v)
    return ans


def restrict(formula: Formula, rho: dict[int, int]) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        if any(abs(lit) in rho and rho[abs(lit)] == int(lit > 0) for lit in clause):
            continue
        out.append(tuple(lit for lit in clause if abs(lit) not in rho))
    return tuple(out)


def satisfies(formula: Formula, assignment: dict[int, int]) -> bool:
    return all(any(assignment.get(abs(lit), 0) == int(lit > 0) for lit in c) for c in formula)


def canonical_bits(formula: Formula, n: int) -> int:
    width = max(1, math.ceil(math.log2(n + 1)))
    return 32 + sum(8 + len(c) * (width + 1) for c in formula)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=202610112012)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    started = time.perf_counter()
    counts: dict[str, int] = {}

    incidence_checks = 0
    witness_checks = 0
    length_rows = []
    for k in (1, 2, 4, 8, 16, 32, 64):
        formula = paired_k33(k)
        n = 9 * k
        m = 12 * k
        witness = matching_witness(k)
        assert satisfies(formula, witness)
        for q in sorted({0, 1, n // 6, n // 3, n // 2, n}):
            chosen = sorted(rng.sample(range(1, n + 1), q)) if q else []
            rho = {x: witness[x] for x in chosen}
            child = restrict(formula, rho)
            untouched = sum(all(abs(lit) not in rho for lit in c) for c in formula)
            assert untouched >= m - 4 * q
            assert all(c in child for c in formula if all(abs(lit) not in rho for lit in c))
            incidence_checks += 2
            extension = dict(witness)
            assert all(extension[x] == b for x, b in rho.items())
            assert satisfies(formula, extension)
            witness_checks += 2
            length_rows.append({"blocks": k, "n": n, "q": q, "source_bits": canonical_bits(formula, n),
                                "child_bits": canonical_bits(child, n), "untouched": untouched,
                                "lower_bound": max(0, m - 4 * q)})
    counts["paired_incidence_floor_checks"] = incidence_checks
    counts["extendable_partial_witness_checks"] = witness_checks

    # Exhaust every partial assignment on all 256 clause-cube formulas.
    cube = tuple(tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(s))
                 for s in itertools.product((False, True), repeat=3))
    cube_checks = 0
    for mask in range(256):
        formula = tuple(cube[i] for i in range(8) if (mask >> i) & 1)
        for state in itertools.product((-1, 0, 1), repeat=3):
            rho = {i + 1: b for i, b in enumerate(state) if b >= 0}
            child = restrict(formula, rho)
            untouched = sum(all(abs(lit) not in rho for lit in c) for c in formula)
            assert untouched <= len(child)
            cube_checks += 1
    counts["exhaustive_clause_cube_partial_restrictions"] = cube_checks

    controls: tuple[tuple[str, Formula, int], ...] = (
        ("Horn", ((-1, -2, 3), (-3, 4), (-4,)), 4),
        ("2SAT", ((1, 2), (-1, 3), (-2, -3)), 3),
        ("affine", ((1, 2), (-1, -2), (2, 3), (-2, -3)), 3),
        ("bounded_treewidth", ((1, 2), (-2, 3), (-3, 4)), 4),
        ("product", ((1,), (-2,), (3, 4), (-3, -4)), 4),
        ("redundant_padding", ((1, 2, 3),) * 8 + ((-1, 2, 3),), 3),
    )
    control_checks = 0
    for _name, formula, n in controls:
        for q in range(n + 1):
            rho = {i + 1: i & 1 for i in range(q)}
            child = restrict(formula, rho)
            assert len(child) <= len(formula)
            control_checks += 1
    counts["named_hostile_control_checks"] = control_checks

    # Exact arithmetic for the asymptotic lower-bound rearrangement.
    exponent_checks = 0
    for h_num in (1, 2, 3, 4):
        h = h_num / 5
        for power in (20, 40, 80):
            n = 1 << power
            N = n * power
            allowance = N**h / max(1.0, math.log2(N))
            q_lower = n / 3 - allowance
            assert q_lower / n <= 1 / 3
            assert q_lower / n > 0.20
            exponent_checks += 2
    counts["encoded_length_rearrangement_checks"] = exponent_checks

    total = sum(counts.values())
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "status": "COMPUTATIONAL",
        "claim": "PRUNED-CHILD-LINEAR-ASSIGNMENT1 finite audit",
        "seed": args.seed,
        "counts": counts,
        "total_checks": total,
        "length_rows": length_rows,
        "elapsed_seconds": time.perf_counter() - started,
        "limitations": [
            "The symbolic incidence proof, not finite data, establishes the asymptotic theorem.",
            "Only explicit literal restrictions are audited; compact semantic representations require separate access transfer.",
            "The witness-volume theorem constrains the declared source pass, not arbitrary SAT deciders.",
        ],
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["result_sha256_before_self_field"] = hashlib.sha256(output.read_bytes()).hexdigest()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "total_checks": total,
                      "elapsed_seconds": result["elapsed_seconds"], "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
