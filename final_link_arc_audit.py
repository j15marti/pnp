#!/usr/bin/env python3
"""Finite arithmetic audit for the FINAL-LINK-ARC report.

This script checks only exponent bookkeeping.  It does not construct a SAT
wrapper and it does not prove P != NP.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import signal
import time


OUT = Path(__file__).with_name("final_link_arc_audit_results.json")


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def one_type_fixed_point(
    r: Fraction,
    p: Fraction,
    channels: list[tuple[Fraction, Fraction]],
) -> tuple[Fraction, Fraction]:
    """Return C*=max(r,w/(1-lambda)) and S*=p."""
    assert channels
    assert all(Fraction(0) <= lam < Fraction(1) for _, lam in channels)
    c_star = max([r] + [w / (1 - lam) for w, lam in channels])
    return c_star, p


def iterate_successor(
    t0: Fraction,
    s0: Fraction,
    r: Fraction,
    p: Fraction,
    channels: list[tuple[Fraction, Fraction]],
    steps: int,
) -> tuple[Fraction, Fraction]:
    t, s = t0, s0
    for _ in range(steps):
        t = max([r] + [w + lam * t for w, lam in channels])
        s = max([p] + [lam * s for _, lam in channels])
    return t, s


def first_crossing(
    t0: Fraction,
    s0: Fraction,
    r: Fraction,
    p: Fraction,
    channels: list[tuple[Fraction, Fraction]],
    gamma: float,
    cap: int = 10000,
) -> tuple[int, Fraction, Fraction]:
    t, s = t0, s0
    if float(t + s) < gamma:
        return 0, t, s
    for step in range(1, cap + 1):
        t, s = iterate_successor(t, s, r, p, channels, 1)
        if float(t + s) < gamma:
            return step, t, s
    raise AssertionError("no crossing inside audit cap")


def bellman_iterate(
    local: list[Fraction],
    edges: list[tuple[int, int, Fraction, Fraction]],
    steps: int,
) -> list[Fraction]:
    values = list(local)
    for _ in range(steps):
        new_values = list(local)
        for src, dst, weight, scale in edges:
            new_values[src] = max(new_values[src], weight + scale * values[dst])
        values = new_values
    return values


def main() -> None:
    signal.signal(
        signal.SIGALRM,
        lambda *_: (_ for _ in ()).throw(TimeoutError("25-second budget")),
    )
    signal.alarm(25)
    started = time.perf_counter()
    deadline = started + 24.5
    checks = 0
    gamma = 2.0 * math.cos(math.pi / 7.0)

    candidate_specs = [
        ("one-third/two-thirds", Fraction(1, 3), Fraction(2, 3), Fraction(1), Fraction(2, 3)),
        ("half/half", Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(1, 2)),
        ("two-fifths/three-fifths", Fraction(2, 5), Fraction(3, 5), Fraction(1), Fraction(1, 5)),
        ("one-quarter/three-quarters", Fraction(1, 4), Fraction(3, 4), Fraction(1), Fraction(1, 2)),
    ]
    candidates = []
    for name, fanout, child, local_time, local_space in candidate_specs:
        c_star = max(local_time, fanout / (1 - child))
        s_star = max(local_space, child)
        total = c_star + s_star
        passes = float(total) < gamma
        assert passes
        assert fanout + child == 1
        checks += 2
        candidates.append(
            {
                "name": name,
                "a": fs(fanout),
                "b": fs(child),
                "c": fs(local_time),
                "s": fs(local_space),
                "C_star": fs(c_star),
                "S_star": fs(s_star),
                "sum": fs(total),
                "margin_decimal": gamma - float(total),
                "passes_williams_product": passes,
            }
        )

    # PRF3-0079 correction: the old pointwise test omits all-block fanout.
    k = Fraction(2)
    target_c = Fraction(4, 3)
    lam = Fraction(1, 2)
    beta_old = Fraction(1, 7)
    one_child = beta_old + lam * k
    all_block = (1 - lam) + beta_old + lam * k
    assert one_child < target_c
    assert beta_old < Fraction(1, 6)
    assert all_block > target_c
    checks += 3

    # Williams endpoint for the corrected all-block recurrence.
    # At half scale, a=1/2, so w=1/2+beta when g=0.
    explicit_beta = Fraction(1, 7)
    explicit_w = (1 - lam) + explicit_beta
    explicit_c, explicit_s = one_type_fixed_point(
        Fraction(1), Fraction(1, 2), [(explicit_w, lam)]
    )
    assert explicit_c == Fraction(9, 7)
    assert explicit_s == Fraction(1, 2)
    assert explicit_c + explicit_s == Fraction(25, 14)
    assert float(explicit_c + explicit_s) < gamma
    checks += 4

    beta_one_sixth = Fraction(1, 6)
    boundary_w = (1 - lam) + beta_one_sixth
    boundary_c, boundary_s = one_type_fixed_point(
        Fraction(1), Fraction(1, 2), [(boundary_w, lam)]
    )
    assert boundary_c + boundary_s == Fraction(11, 6)
    assert float(boundary_c + boundary_s) > gamma
    checks += 2

    virtual_c, virtual_s = one_type_fixed_point(
        Fraction(1), Fraction(1, 6), [(boundary_w, lam)]
    )
    assert virtual_c == Fraction(4, 3)
    assert virtual_c + virtual_s == Fraction(3, 2)
    assert float(virtual_c + virtual_s) < gamma
    checks += 3

    beta_threshold = (gamma - 1.5) / 2.0
    assert float(Fraction(1, 7)) < beta_threshold < float(Fraction(1, 6))
    checks += 1

    crossings = []
    for start in (Fraction(2), Fraction(5), Fraction(20), Fraction(100)):
        step, t_fin, s_fin = first_crossing(
            start,
            start,
            Fraction(1),
            Fraction(1, 2),
            [(explicit_w, lam)],
            gamma,
        )
        assert float(t_fin + s_fin) < gamma
        checks += 1
        crossings.append(
            {
                "start": fs(start),
                "first_crossing_step": step,
                "time_exponent": fs(t_fin),
                "space_exponent": fs(s_fin),
                "sum_decimal": float(t_fin + s_fin),
            }
        )

    # Exhaustive small-rational audit of the one-type fixed-point formula.
    grid_checks = 0
    for denominator in range(2, 15):
        for numerator in range(1, denominator):
            lam_grid = Fraction(numerator, denominator)
            for w_num in range(0, 8):
                w_grid = Fraction(w_num, 7)
                for r_num in range(0, 5):
                    if time.perf_counter() > deadline:
                        raise TimeoutError("deadline reached during rational grid")
                    r_grid = Fraction(r_num, 4)
                    c_grid, _ = one_type_fixed_point(
                        r_grid, Fraction(0), [(w_grid, lam_grid)]
                    )
                    assert c_grid >= r_grid
                    assert c_grid >= w_grid + lam_grid * c_grid
                    if c_grid > 0:
                        lower = max(r_grid, w_grid + lam_grid * (c_grid - Fraction(1, 10**6)))
                        assert lower > c_grid - Fraction(1, 10**6)
                    t_grid, _ = iterate_successor(
                        Fraction(50), Fraction(0), r_grid, Fraction(0),
                        [(w_grid, lam_grid)], 300,
                    )
                    assert c_grid <= t_grid
                    assert t_grid - c_grid <= lam_grid**300 * (Fraction(50) - c_grid)
                    grid_checks += 1
    checks += grid_checks * 4

    # A two-type return cycle may contain one same-scale edge when the whole
    # directed cycle contracts.
    typed_local = [Fraction(0), Fraction(0)]
    typed_edges = [
        (0, 1, Fraction(1, 10), Fraction(1)),
        (1, 0, Fraction(1, 5), Fraction(2, 5)),
    ]
    typed_values = bellman_iterate(typed_local, typed_edges, 500)
    typed_fixed = [Fraction(1, 2), Fraction(2, 5)]
    assert typed_fixed[0] == Fraction(1, 10) + typed_fixed[1]
    assert typed_fixed[1] == Fraction(1, 5) + Fraction(2, 5) * typed_fixed[0]
    assert all(abs(float(x - y)) < 1e-50 for x, y in zip(typed_values, typed_fixed))
    assert Fraction(1) * Fraction(2, 5) < 1
    checks += 4

    # In contrast, a positive-weight unit-product cycle has no finite budget.
    hostile_edges = [
        (0, 1, Fraction(1, 10), Fraction(1)),
        (1, 0, Fraction(1, 5), Fraction(1)),
    ]
    hostile_20 = bellman_iterate(typed_local, hostile_edges, 20)
    hostile_40 = bellman_iterate(typed_local, hostile_edges, 40)
    assert hostile_40[0] > hostile_20[0]
    assert hostile_40[1] > hostile_20[1]
    checks += 2

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "FINAL-LINK-ARC",
        "status": "COMPUTATIONAL exponent-ledger audit only",
        "williams_gamma": gamma,
        "candidate_explicit_cells": candidates,
        "route_b_prf3_0079": {
            "k": fs(k),
            "C": fs(target_c),
            "lambda": fs(lam),
            "beta_example": fs(beta_old),
            "one_child_exponent": fs(one_child),
            "all_block_exponent": fs(all_block),
            "correct_all_block_constraint": "1-lambda+beta+lambda*k < C",
            "at_k_2_C_4_over_3": "lambda < 1/3-beta",
        },
        "williams_half_scale": {
            "explicit_beta_threshold_decimal": beta_threshold,
            "beta_1_over_7": {
                "C_star": fs(explicit_c),
                "S_star": fs(explicit_s),
                "sum": fs(explicit_c + explicit_s),
                "passes": True,
            },
            "beta_1_over_6_explicit": {
                "sum": fs(boundary_c + boundary_s),
                "passes": False,
            },
            "beta_1_over_6_virtual_if_access_is_free_in_exponent": {
                "C_star": fs(virtual_c),
                "S_star": fs(virtual_s),
                "sum": fs(virtual_c + virtual_s),
                "passes": True,
                "warning": "conditional on a proved source-query interface charging all access and retained state",
            },
        },
        "finite_crossings_for_explicit_beta_1_over_7": crossings,
        "typed_cycle": {
            "edge_scales": ["1/1", "2/5"],
            "cycle_product": "2/5",
            "least_time_budgets": [fs(x) for x in typed_fixed],
            "same_scale_edge_is_safe_only_inside_contracting_cycle": True,
        },
        "hostile_unit_product_cycle": {
            "values_after_20": [fs(x) for x in hostile_20],
            "values_after_40": [fs(x) for x in hostile_40],
            "diverges": True,
        },
        "rational_grid_cases": grid_checks,
        "assertions": checks,
        "elapsed_seconds": elapsed,
        "proof_claim": False,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    signal.alarm(0)


if __name__ == "__main__":
    main()
