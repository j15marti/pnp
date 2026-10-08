#!/usr/bin/env python3
"""Exact arithmetic audit for FINAL-LINK2-ARC.

This program checks exponent ledgers for typed max-affine wrappers, mixed
VALUE/recursive exits, and potential-collapsed epochs.  It does not construct
a SAT compiler and it does not prove a complexity-class separation.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import random
import signal
import time


OUT = Path(__file__).with_name("final_link2_typed_audit_results.json")


def frac(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def solve_linear(a: list[list[F]], b: list[F]) -> list[F] | None:
    """Solve Ax=b over Q, returning None when A is singular."""
    n = len(b)
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col]), None)
        if pivot is None:
            return None
        m[col], m[pivot] = m[pivot], m[col]
        q = m[col][col]
        m[col] = [x / q for x in m[col]]
        for row in range(n):
            if row == col or not m[row][col]:
                continue
            q = m[row][col]
            m[row] = [x - q * y for x, y in zip(m[row], m[col])]
    return [m[i][-1] for i in range(n)]


def bellman_exact(
    local: list[F], edges: list[list[tuple[int, F, F]]]
) -> list[F] | None:
    """Least finite fixed point of V_i=max(local_i,w+theta V_j).

    Enumeration is deliberately used only on the small hostile-control
    systems in this audit.  An option -1 means that the local floor is active.
    """
    n = len(local)
    options = [list(range(-1, len(edges[i]))) for i in range(n)]
    candidates: list[list[F]] = []
    for policy in product(*options):
        a = [[F(int(i == j)) for j in range(n)] for i in range(n)]
        b = [F(0) for _ in range(n)]
        for i, choice in enumerate(policy):
            if choice == -1:
                b[i] = local[i]
            else:
                dst, weight, scale = edges[i][choice]
                a[i][dst] -= scale
                b[i] = weight
        v = solve_linear(a, b)
        if v is None:
            continue
        valid = True
        for i in range(n):
            rhs = max([local[i]] + [w + q * v[j] for j, w, q in edges[i]])
            if v[i] != rhs:
                valid = False
                break
        if valid:
            candidates.append(v)
    if not candidates:
        return None
    least = min(candidates, key=lambda v: sum(v))
    assert all(all(least[i] <= v[i] for i in range(n)) for v in candidates)
    return least


def double_closed(
    ra: F, rb: F, x: F, y: F, alpha: F, beta: F
) -> tuple[F, F]:
    assert alpha * beta < 1
    ca = max(ra, x + alpha * rb, (x + alpha * y) / (1 - alpha * beta))
    cb = max(rb, y + beta * ra, (y + beta * x) / (1 - alpha * beta))
    return ca, cb


def cycle_weight(weights: list[F], scales: list[F]) -> tuple[F, F]:
    prefix = F(1)
    total = F(0)
    for w, q in zip(weights, scales):
        total += prefix * w
        prefix *= q
    return total, prefix


def main() -> None:
    signal.signal(
        signal.SIGALRM,
        lambda *_: (_ for _ in ()).throw(TimeoutError("25-second budget")),
    )
    signal.alarm(25)
    started = time.perf_counter()
    deadline = started + 24.0
    gamma = 2.0 * math.cos(math.pi / 7.0)
    checks = 0

    # Exact two-wrapper candidate with a same-scale outer phase.
    ra = rb = F(1)
    alpha, beta = F(1), F(1, 2)
    x, y = F(1, 5), F(2, 5)
    ca, cb = double_closed(ra, rb, x, y, alpha, beta)
    time_exact = bellman_exact(
        [ra, rb],
        [[(1, x, alpha)], [(0, y, beta)]],
    )
    assert time_exact == [ca, cb] == [F(6, 5), F(1)]
    ha = hb = F(1, 2)
    space_exact = bellman_exact(
        [ha, hb],
        [[(1, F(0), alpha)], [(0, F(0), beta)]],
    )
    assert space_exact == [F(1, 2), F(1, 2)]
    assert float(ca + space_exact[0]) < gamma
    checks += 4

    # Exhaustive small-rational comparison of the closed form and policy
    # enumeration, including one same-scale phase.
    grid = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    positive_scales = [F(1, 4), F(1, 2), F(3, 4), F(1)]
    exhaustive = 0
    for ra0 in grid:
        for rb0 in grid:
            for x0 in grid:
                for y0 in grid:
                    for a0 in positive_scales:
                        for b0 in positive_scales:
                            if time.perf_counter() > deadline:
                                raise TimeoutError("rational grid exceeded deadline")
                            if a0 * b0 >= 1:
                                continue
                            closed = list(double_closed(ra0, rb0, x0, y0, a0, b0))
                            exact = bellman_exact(
                                [ra0, rb0],
                                [[(1, x0, a0)], [(0, y0, b0)]],
                            )
                            assert exact == closed
                            exhaustive += 1
    checks += exhaustive

    # Random finite typed systems with an acyclic spine plus one contracting
    # return edge.  Compare the exact policy solution with long value iteration.
    rng = random.Random(1776)
    random_systems = 0
    for _ in range(200):
        n = 3
        local = [F(rng.randrange(0, 5), 4) for _ in range(n)]
        q01 = F(rng.randrange(1, 5), 5)
        q12 = F(rng.randrange(1, 5), 5)
        q20 = F(rng.randrange(1, 5), 5)
        weights = [F(rng.randrange(0, 5), 5) for _ in range(n)]
        edges = [
            [(1, weights[0], q01)],
            [(2, weights[1], q12)],
            [(0, weights[2], q20)],
        ]
        exact = bellman_exact(local, edges)
        assert exact is not None
        value = local[:]
        for _step in range(700):
            value = [
                max([local[i]] + [w + q * value[j] for j, w, q in edges[i]])
                for i in range(n)
            ]
        assert all(abs(float(a - b)) < 1e-30 for a, b in zip(exact, value))
        random_systems += 1
    checks += random_systems

    # A positive-weight unit-product cycle has no finite Bellman solution.
    hostile_positive = bellman_exact(
        [F(0), F(0)],
        [[(1, F(1, 10), F(1))], [(0, F(1, 5), F(1))]],
    )
    assert hostile_positive is None
    checks += 1

    # A zero-weight, unit-product cycle preserves the inherited unknown K.  It
    # can have fixed points, but it cannot suppress the starting solver exponent.
    k = F(7)
    unit_value = [k, k]
    for _ in range(100):
        unit_value = [unit_value[1], unit_value[0]]
    assert unit_value == [k, k]
    checks += 1

    # Same-realization guard.  Pointwise time+space may pass while maxima taken
    # over different input types violate the uniform theorem endpoint.
    typed_pairs = [(F(17, 10), F(1, 20)), (F(4, 5), F(1))]
    assert all(float(t + s) < gamma for t, s in typed_pairs)
    global_time = max(t for t, _ in typed_pairs)
    global_space = max(s for _, s in typed_pairs)
    assert global_time + global_space == F(27, 10)
    assert float(global_time + global_space) > gamma
    checks += 3

    # Potential-collapsed epoch ledger.  The potential mass bounds the number
    # of same-input administrative nodes and recursive exits.
    kappa, xi, depth, per_node = F(1, 6), F(1, 12), F(0), F(3, 4)
    beta_access, replay = F(0), F(0)
    internal = kappa + xi + depth + per_node
    recursive_weight = kappa + xi + beta_access + replay
    assert internal == F(1)
    assert recursive_weight == F(1, 4)
    child_scale = F(3, 4)
    epoch_time = max(internal, recursive_weight / (1 - child_scale))
    explicit_child = child_scale
    source_summary = F(1, 2)
    frame, stack_depth = F(1, 2), F(0)
    epoch_space = max(source_summary, frame + stack_depth, explicit_child)
    assert epoch_time == F(1) and epoch_space == F(3, 4)
    assert float(epoch_time + epoch_space) < gamma
    checks += 4

    # Hostile controls for omitted fanout and omitted live-stack depth.
    binary_depth_exponent = F(1, 4)
    actual_exit_exponent = binary_depth_exponent
    claimed_exit_exponent = F(0)
    assert actual_exit_exponent > claimed_exit_exponent
    frame, polynomial_depth = F(3, 10), F(1, 5)
    actual_stack = frame + polynomial_depth
    assert actual_stack == F(1, 2) and actual_stack > frame
    checks += 3

    # Mixed VALUE terminals help only when their total acquisition cost is
    # already favorable.  A parent-scale SAT VALUE query is still scale one.
    value_good = max(F(1), F(3, 4))
    value_bad = max(F(1), F(2))
    assert value_good == F(1) and value_bad == F(2)
    parent_value_edge = (F(0), F(1))  # weight, scale
    inherited = F(9)
    assert parent_value_edge[0] + parent_value_edge[1] * inherited == inherited
    checks += 3

    # Type potentials reweight edges but do not change a closed cycle budget.
    weights = [F(1, 5), F(2, 5), F(1, 10)]
    scales = [F(1), F(1, 2), F(2, 3)]
    potentials = [F(3, 7), F(-1, 5), F(4, 9)]
    reweighted = [
        weights[i] + scales[i] * potentials[(i + 1) % 3] - potentials[i]
        for i in range(3)
    ]
    old_w, theta = cycle_weight(weights, scales)
    new_w, theta2 = cycle_weight(reweighted, scales)
    assert theta == theta2
    assert new_w == old_w - (1 - theta) * potentials[0]
    assert new_w / (1 - theta) + potentials[0] == old_w / (1 - theta)
    checks += 3

    # OR and AND short circuiting cannot be booked in worst-case exponents:
    # UNSAT for OR and SAT for AND force all q branches.
    branch_exponents = [F(1, 5), F(1, 4), F(1, 3)]
    aggregate = max(branch_exponents)
    assert aggregate == F(1, 3)
    checks += 1

    signal.alarm(0)
    elapsed = time.perf_counter() - started
    result = {
        "run_id": "FINAL-LINK2-ARC",
        "scope": "exponent bookkeeping only; no SAT compiler and no separation proof",
        "runtime_seconds": elapsed,
        "gamma": gamma,
        "checks": checks,
        "two_wrapper_candidate": {
            "alpha": frac(alpha),
            "beta": frac(beta),
            "x": frac(x),
            "y": frac(y),
            "R_A": frac(ra),
            "R_B": frac(rb),
            "C_A": frac(ca),
            "C_B": frac(cb),
            "rho_A": frac(space_exact[0]),
            "root_sum": frac(ca + space_exact[0]),
            "passes_numeric_endpoint": float(ca + space_exact[0]) < gamma,
            "status": "CONDITIONAL on a source-checkable SAT realization",
        },
        "grid_cases": exhaustive,
        "random_typed_systems": random_systems,
        "hostile_controls": {
            "positive_unit_cycle_has_no_finite_budget": hostile_positive is None,
            "zero_unit_cycle_preserves_inherited_K": unit_value == [k, k],
            "cross_type_same_realization_sum": frac(global_time + global_space),
            "omitted_binary_fanout_exponent": frac(actual_exit_exponent),
            "charged_stack_exponent": frac(actual_stack),
            "parent_value_query_preserves_K": True,
        },
        "potential_epoch_candidate": {
            "internal_work": frac(internal),
            "recursive_weight": frac(recursive_weight),
            "child_scale": frac(child_scale),
            "time_fixed_point": frac(epoch_time),
            "live_space": frac(epoch_space),
            "sum": frac(epoch_time + epoch_space),
            "status": "CONDITIONAL on an actual all-input potential certificate",
        },
        "type_potential_cycle_invariant": True,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
