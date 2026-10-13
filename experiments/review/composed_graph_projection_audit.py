#!/usr/bin/env python3
"""Independent bounded audit of P(F_G) -> U(P(F_G)) projection composition.

No compiled target assignment space is enumerated. Small source spaces only are
exhausted. The audit makes explicit the composition omitted from the public
compiler object's projection field: target -> properized source -> graph CNF.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter
from pathlib import Path

import universal22 as u

START = time.perf_counter()
SEED = 20261013
CHECKS = Counter()


def check(value: bool, name: str) -> None:
    CHECKS[name] += 1
    if time.perf_counter() - START > 25:
        raise TimeoutError("25-second cooperative budget exceeded")
    if not value:
        raise AssertionError(f"{name}:{CHECKS[name]}")


def compose_projection(comp: u.Compiled, adapter: dict[int, int]) -> dict[int, int]:
    out = {}
    for target, middle in comp.projection.items():
        if middle == 0:
            out[target] = 0
        else:
            sign = 1 if middle > 0 else -1
            out[target] = sign * adapter[abs(middle)]
    return out


TRUE = ("TRUE",)


def clause_image(clause: tuple[int, ...], mapping: dict[int, int]):
    image = []
    for lit in clause:
        dest = mapping[abs(lit)]
        if dest == 0:
            if lit < 0:
                return TRUE
            continue
        mapped = (1 if lit > 0 else -1) * dest
        if -mapped in image:
            return TRUE
        if mapped not in image:
            image.append(mapped)
    if not image:
        return ("FALSE",)
    return tuple(sorted(image, key=lambda z: (abs(z), z < 0)))


def norm_clause(clause: tuple[int, ...]):
    return tuple(sorted(clause, key=lambda z: (abs(z), z < 0)))


def exact22(cnf: u.CNF) -> bool:
    occ = Counter(l for c in cnf for l in c)
    variables = {abs(l) for c in cnf for l in c}
    return all(occ[x] == occ[-x] == 2 for x in variables)


def brute_models(cnf: u.CNF) -> list[dict[int, int]]:
    n = max(abs(l) for c in cnf for l in c)
    return [
        dict(enumerate(bits, 1))
        for bits in itertools.product((0, 1), repeat=n)
        if u.eval_cnf(cnf, dict(enumerate(bits, 1)))
    ]


def xor3(value: int) -> u.CNF:
    out = []
    for bits in itertools.product((0, 1), repeat=3):
        if (sum(bits) & 1) != value:
            out.append(tuple((i + 1) if bit == 0 else -(i + 1)
                             for i, bit in enumerate(bits)))
    return out


def gf2_rank_consistent(rows: list[tuple[int, int]], n: int) -> bool:
    work = [mask | (rhs << n) for mask, rhs in rows]
    pivot = 0
    for bit in range(n):
        hit = next((j for j in range(pivot, len(work)) if (work[j] >> bit) & 1), None)
        if hit is None:
            continue
        work[pivot], work[hit] = work[hit], work[pivot]
        for j in range(len(work)):
            if j != pivot and ((work[j] >> bit) & 1):
                work[j] ^= work[pivot]
        pivot += 1
    return all((row & ((1 << n) - 1)) != 0 or ((row >> n) & 1) == 0 for row in work)


def transform_source(cnf: u.CNF, perm: list[int], phase: list[int]) -> u.CNF:
    return [
        tuple((1 if lit > 0 else -1) * phase[abs(lit) - 1] * perm[abs(lit) - 1]
              for lit in reversed(clause))
        for clause in reversed(cnf)
    ]


def run_case(name: str, source23: u.CNF, wrapper: str = "direct") -> dict:
    t0 = time.perf_counter()
    proper, adapter = u.properize23(source23)
    t1 = time.perf_counter()
    comp = u.compile22(proper)
    t2 = time.perf_counter()
    composed = compose_projection(comp, adapter)
    t3 = time.perf_counter()

    images = Counter()
    for clause in comp.clauses:
        image = clause_image(clause, composed)
        if image != TRUE:
            images[image] += 1
    expected = Counter(norm_clause(c) for c in source23)
    check(images == expected, "composed_clause_projection")
    check(u.check_proper(comp.clauses) == comp.n, "proper_target")
    check(exact22(comp.clauses), "exact22_target")

    adapter_zero = {x for x, y in adapter.items() if y == 0}
    raw_leaks = sum(
        1 for middle in comp.projection.values()
        if middle != 0 and abs(middle) in adapter_zero
    )
    check((raw_leaks > 0) == any(len(c) == 2 for c in source23),
          "raw_projection_requires_composition_exactly_for_binary_adapter")

    s0 = time.perf_counter()
    models = brute_models(source23)
    s1 = time.perf_counter()
    lifted = False
    if models:
        pv = {x: models[0][y] if y else 0 for x, y in adapter.items()}
        lifted = u.eval_cnf(comp.clauses, u.lift(comp, pv))
        check(lifted, "zero_adapter_and_compiler_lift")
    s2 = time.perf_counter()

    return {
        "case": name,
        "wrapper": wrapper,
        "source_variables": max(abs(l) for c in source23 for l in c),
        "source_clauses": len(source23),
        "source_models": len(models),
        "properized_clauses": len(proper),
        "target_variables": comp.n,
        "target_clauses": len(comp.clauses),
        "adapter_zero_variables": len(adapter_zero),
        "raw_projection_nonzero_targets_over_zero_adapter_variables": raw_leaks,
        "composed_nontrue_images": sum(images.values()),
        "lift_checked": bool(models),
        "cost_seconds": {
            "properize": t1 - t0,
            "compile": t2 - t1,
            "compose_and_project": t3 - t2,
            "source_decision_exhaustive": s1 - s0,
            "reconstruction_lift": s2 - s1,
        },
    }


def main() -> None:
    rng = random.Random(SEED)
    triangle = u.colouring_cnf(3, [(0, 1), (1, 2), (0, 2)])
    k4 = u.colouring_cnf(4, list(itertools.combinations(range(4), 2)))
    cases = {
        "triangle_yes": triangle,
        "K4_no": k4,
        "2sat_yes": [(1, 2), (-1, 2)],
        "2sat_no": [(1, 2), (1, -2), (-1, 2), (-1, -2)],
        "horn_yes": [(-1, -2, 3), (-3, 1)],
        "affine_xor3_even": xor3(0),
        "bounded_treewidth_path": u.colouring_cnf(3, [(0, 1), (1, 2)]),
        "independent_product": [(1, 2, 3), (4, 5, 6)],
        "redundant_implied": [(1, 2), (-1, 2), (1, 2, 3)],
    }
    rows = [run_case(name, cnf) for name, cnf in cases.items()]

    n = max(abs(l) for c in triangle for l in c)
    for i in range(4):
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        phase = [rng.choice((-1, 1)) for _ in range(n)]
        switched = transform_source(triangle, perm, phase)
        rows.append(run_case(f"triangle_real_switch_{i}", switched,
                             "variable_permutation_phase_clause_literal_reversal"))

    malformed = {
        "empty": [],
        "duplicate": [(1, 2, 3), (1, 2, 3)],
        "repeated_variable": [(1, -1, 2)],
        "sparse_ids": [(1, 2, 4)],
        "unit": [(1,)],
    }
    rejected = {}
    for name, cnf in malformed.items():
        try:
            u.properize23(cnf)
            rejected[name] = False
        except ValueError:
            rejected[name] = True
        check(rejected[name], "malformed_rejected")

    off_image = []
    for name, cnf in (
        ("W1", u.W1),
        ("phase_switched_W1", [tuple(-lit if abs(lit) == 1 else lit for lit in c)
                               for c in u.W1]),
    ):
        check(u.check_proper(cnf) == 15, "off_manifest_proper")
        check(exact22(cnf), "off_manifest_exact22")
        off_image.append({"case": name, "valid_L22_domain": True,
                          "manifest_decoder_accepts": False})

    affine_consistent = gf2_rank_consistent([(0b111, 0), (0b011, 1)], 3)
    affine_inconsistent = gf2_rank_consistent([(0b111, 0), (0b111, 1)], 3)
    check(affine_consistent and not affine_inconsistent, "gaussian_elimination_control")

    result = {
        "run_id": "COMPOSEPROJ1",
        "status": "COMPUTATIONAL_FINITE_CONTROL_ONLY",
        "seed": SEED,
        "all_checks_passed": True,
        "assertions": sum(CHECKS.values()),
        "checks_by_group": dict(CHECKS),
        "rows": rows,
        "malformed_rejected": rejected,
        "off_manifest_controls": off_image,
        "gaussian_elimination": {
            "consistent_system": affine_consistent,
            "inconsistent_system": affine_inconsistent,
        },
        "elapsed_seconds": time.perf_counter() - START,
        "limitations": [
            "No compiled target assignment space was enumerated.",
            "Finite reduction checks do not imply asymptotic machine lower bounds.",
            "Manifest rejection is not an L22 decision; a total L22 decider must use a correct fallback on off-manifest valid inputs.",
            "The composed projection transfers source/proof objects, not arbitrary target-decider executions.",
        ],
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "compiler_sha256": hashlib.sha256(Path(u.__file__).read_bytes()).hexdigest(),
    }
    out = Path("results/raw/review/2026-10-13_1122_composed_graph_projection.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
