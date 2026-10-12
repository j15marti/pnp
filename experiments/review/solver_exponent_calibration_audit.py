#!/usr/bin/env python3
"""Finite arithmetic and hostile-control audit for KCALIB1.

This script does not construct a SAT compressor.  It verifies the exact
exponent ledger and the quantifier separation between one fixed shrink exponent
and a shrink exponent calibrated after a polynomial SAT decider is fixed.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


PHI = (1.0 + math.sqrt(5.0)) / 2.0


def ledger(*, K: float, D: float, lam: float, u: float, v: float,
           r: float, p: float, eta: float, beta: float) -> tuple[float, float]:
    """One-level streamed OR compiler preceded by a clean-core reduction."""
    time_exp = max(u, lam * r, lam * (eta + beta * K))
    space_exp = max(v, lam * p, lam * beta * D)
    return time_exp, space_exp


def calibrated_beta(K: int, D: int, lam: float, epsilon: float) -> float | None:
    """A positive beta that leaves strict FLMV product slack when lam < phi."""
    if lam + epsilon >= PHI:
        return None
    # r=1, eta=0, u=lam, v=0, p=beta.  The first term keeps beta*K < 1;
    # the second reserves at least half the available product slack.
    return min(0.5 / K, (PHI - lam - epsilon) / (2.0 * lam * max(1, D)), 0.5)


def sat_clause(clause: tuple[int, ...], assignment: tuple[bool, ...]) -> bool:
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def sat(formula: tuple[tuple[int, ...], ...], nvars: int) -> bool:
    return any(all(sat_clause(c, a) for c in formula)
               for a in itertools.product((False, True), repeat=nvars))


def decision_compiler(formula: tuple[tuple[int, ...], ...], nvars: int):
    """Exact but deliberately charged toy compiler: decide, then emit YES/NO."""
    answer = sat(formula, nvars)
    child = ((1,),) if answer else ((1,), (-1,))
    return (child,), 1, answer


def run() -> dict[str, object]:
    epsilon = 1e-3
    lambdas = [1.0, 1.1, 1.25, 1.5, PHI - 0.01, PHI + 0.01]
    calibrated_rows = []
    calibrated_checks = 0
    impossible_frontend_checks = 0
    for lam in lambdas:
        successes = 0
        for K in range(1, 65):
            for D in range(1, 65):
                beta = calibrated_beta(K, D, lam, epsilon)
                if beta is None:
                    # The input reduction/local reading floor already meets or
                    # exceeds the cited product endpoint in this ledger.
                    assert lam + epsilon >= PHI
                    impossible_frontend_checks += 1
                    continue
                c, rho = ledger(K=K, D=D, lam=lam, u=lam, v=0.0,
                                r=1.0, p=beta, eta=0.0, beta=beta)
                assert beta > 0.0 and beta * K < 1.0
                assert c + rho < PHI
                successes += 1
                calibrated_checks += 1
        calibrated_rows.append({"lambda": lam, "successful_pairs": successes})

    # Every fixed beta>0 loses to a sufficiently delayed exact wrapper.
    fixed_beta_rows = []
    for beta in [0.5, 0.25, 0.1, 0.01]:
        witness_K = math.floor(PHI / beta) + 2
        c, rho = ledger(K=witness_K, D=1, lam=1.0, u=1.0, v=0.0,
                        r=1.0, p=beta, eta=0.0, beta=beta)
        assert c + rho >= PHI
        fixed_beta_rows.append({
            "fixed_beta": beta,
            "delay_exponent_witness": witness_K,
            "time_exponent": c,
            "space_exponent": rho,
            "sum": c + rho,
        })

    # The truth-bit compiler is exact on hostile easy and hard-looking controls,
    # but its semantic decision work is part of local time and is not free.
    controls = {
        "horn_yes": (((1,), (-1, 2)), 2),
        "horn_no": (((1,), (-1,)), 1),
        "two_sat_yes": (((1, 2), (-1, 2)), 2),
        "two_sat_no": (((1,), (-1, 2), (-2,)), 2),
        "affine_tseitin_yes": (((1, 2), (-1, -2)), 2),
        "bounded_treewidth": (((1, 2), (-2, 3), (-3, 4)), 4),
        "independent_product": (((1,), (2,), (-3, 4)), 4),
        "redundant_padding": (((1, 2, 3), (1, 2, 3), (1, -1, 2)), 3),
    }
    control_rows = []
    for name, (formula, nvars) in controls.items():
        children, child_n, answer = decision_compiler(formula, nvars)
        child_or = any(sat(child, child_n) for child in children)
        assert answer == child_or
        control_rows.append({
            "name": name,
            "source_answer": answer,
            "child_or_answer": child_or,
            "children": len(children),
            "decision_work_charged": True,
        })

    return {
        "claim_id": "KCALIB1",
        "status": "COMPUTATIONAL",
        "phi": PHI,
        "calibrated_parameter_checks": calibrated_checks,
        "frontend_floor_rejections": impossible_frontend_checks,
        "calibrated_rows": calibrated_rows,
        "fixed_beta_delay_witnesses": fixed_beta_rows,
        "hostile_controls": control_rows,
        "interpretation": (
            "A fixed positive beta cannot cover unbounded polynomial solver exponents, "
            "but after K,D are fixed a positive beta can be calibrated whenever the "
            "fully charged front-end floor is below the FLMV product endpoint."
        ),
        "construction_claim": "none; existence of the required SAT compressor remains OPEN",
        "asymptotic_inference": "none",
    }


if __name__ == "__main__":
    result = run()
    path = Path("results/raw/review/2026-10-12_solver_exponent_calibration.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "claim_id": result["claim_id"],
        "calibrated_parameter_checks": result["calibrated_parameter_checks"],
        "frontend_floor_rejections": result["frontend_floor_rejections"],
        "hostile_controls": len(result["hostile_controls"]),
        "all_passed": True,
        "result": str(path),
    }, sort_keys=True))
