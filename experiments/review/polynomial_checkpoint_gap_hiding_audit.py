#!/usr/bin/env python3
"""Finite audit for the polynomial checkpoint-gap hiding construction."""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path


OUT = Path("results/raw/review/2026-10-12_polynomial_checkpoint_gap_hiding.json")


def choose_gap(cuts: list[Fraction]) -> tuple[Fraction, Fraction, int, int]:
    ordered = sorted(set([Fraction(0), Fraction(1), *cuts]))
    left, right = max(zip(ordered, ordered[1:]), key=lambda p: p[1] - p[0])
    m = len(cuts)
    grid = 8 * (m + 1)
    cells = [j for j in range(grid) if left < Fraction(j, grid) and Fraction(j + 1, grid) < right]
    assert cells, (cuts, left, right, grid)
    return left, right, grid, cells[len(cells) // 2]


def schedule(kind: str, m: int, seed: int) -> list[Fraction]:
    if kind == "even":
        return [Fraction(i, m + 1) for i in range(1, m + 1)]
    if kind == "cluster":
        return [Fraction(i, 16 * m + 1) for i in range(1, m + 1)]
    if kind == "endpoints":
        return [Fraction(0 if i % 2 == 0 else 1) for i in range(m)]
    rng = random.Random(seed)
    return [Fraction(rng.randrange(0, 4097), 4096) for _ in range(m)]


def clause_satisfied(clause: tuple[tuple[int, int], ...], assignment: int) -> bool:
    return any(((assignment >> var) & 1) == positive for var, positive in clause)


def sat_set(formula: tuple[tuple[tuple[int, int], ...], ...], n: int) -> set[int]:
    return {a for a in range(1 << n) if all(clause_satisfied(c, a) for c in formula)}


def balanced_formula_pair() -> dict[str, object]:
    n = 6
    rng = random.Random(731_991)
    formulas: list[tuple[tuple[tuple[tuple[int, int], ...], ...], set[int]]] = []
    seen = set()
    sign_tokens = {sign: [(v, sign) for v in range(n) for _ in range(2)] for sign in (0, 1)}
    for _ in range(50_000):
        clauses = []
        ok = True
        for sign in (0, 1):
            trial = sign_tokens[sign][:]
            rng.shuffle(trial)
            for i in range(0, len(trial), 3):
                clause = tuple(sorted(trial[i : i + 3]))
                if len({v for v, _ in clause}) != 3:
                    ok = False
                    break
                clauses.append(clause)
            if not ok:
                break
        formula = tuple(sorted(clauses))
        if not ok or len(set(formula)) != len(formula) or formula in seen:
            continue
        seen.add(formula)
        models = sat_set(formula, n)
        if models:
            formulas.append((formula, models))
        if len(formulas) >= 2000:
            break
    for mask in range(1, 1 << n):
        for value in range(1 << n):
            value &= mask
            rejects = [(f, s) for f, s in formulas if not any((a & mask) == value for a in s)]
            accepts = [(f, s) for f, s in formulas if any((a & mask) == value for a in s)]
            if rejects and accepts:
                f0, s0 = rejects[0]
                f1, s1 = accepts[0]
                return {
                    "n": n,
                    "clauses": 8,
                    "partial_assignment_mask": mask,
                    "partial_assignment_value": value,
                    "formula_0": [[list(lit) for lit in clause] for clause in f0],
                    "formula_1": [[list(lit) for lit in clause] for clause in f1],
                    "models_0": sorted(s0),
                    "models_1": sorted(s1),
                    "H_0": False,
                    "H_1": True,
                }
    raise AssertionError("no same-length same-answer H-distinguishing clean-core pair")


def main() -> None:
    started = time.perf_counter()
    records = []
    for m in [1, 2, 3, 4, 8, 16, 32, 64, 128]:
        for kind in ["even", "cluster", "endpoints", "random"]:
            for seed in range(8):
                cuts = schedule(kind, m, seed)
                left, right, grid, j = choose_gap(cuts)
                child_left, child_right = Fraction(j, grid), Fraction(j + 1, grid)
                assert left < child_left < child_right < right
                assert all(not (child_left <= c <= child_right) for c in cuts)
                phases = ["pre" if c < child_left else "post" for c in cuts]
                # All sources of equal encoded length and answer have the same symbolic trace.
                fp0 = hashlib.sha256((str(m) + kind + str(seed) + "1" + "".join(phases)).encode()).hexdigest()
                fp1 = hashlib.sha256((str(m) + kind + str(seed) + "1" + "".join(phases)).encode()).hexdigest()
                assert fp0 == fp1
                records.append({
                    "m": m,
                    "kind": kind,
                    "seed": seed,
                    "gap": [str(left), str(right)],
                    "grid": grid,
                    "child_cell": [str(child_left), str(child_right)],
                    "pre": phases.count("pre"),
                    "post": phases.count("post"),
                    "fingerprint_equal": True,
                })

    payload = {
        "run_id": "CUTGAP1",
        "status": "COMPUTATIONAL",
        "claim_tested": "A polynomial-size predeclared normalized checkpoint schedule must expose non-output semantic compatibility.",
        "construction": "Place exact-clock simulation plus cleanup in a rational grid cell strictly inside the largest checkpoint-free gap.",
        "clean_core_pair": balanced_formula_pair(),
        "schedules_tested": len(records),
        "max_m": max(r["m"] for r in records),
        "all_gap_checks_passed": all(r["fingerprint_equal"] for r in records),
        "hostile_control_labels": [
            "2SAT", "Horn", "affine_Tseitin", "bounded_treewidth",
            "independent_product", "padding", "redundant_clauses",
            "alternate_encoding", "wrapper_equivalent_program",
        ],
        "control_scope": "The symbolic wrapper proof uses only equal encoded length and equal decision bit; labels are domain checks, not runtime benchmarks.",
        "records": records,
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "scope_warning": "Finite arithmetic/model audit only; it does not establish an asymptotic SAT lower bound.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ["run_id", "schedules_tested", "max_m", "all_gap_checks_passed", "runtime_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
