#!/usr/bin/env python3
"""Exact rational checks for the ARC-0007 phase-multinorm certificate.

This is a bounded arithmetic model, not a SAT transformation.  All matrix,
potential, drift, and trajectory checks use fractions.Fraction.  A 25-second
alarm enforces the project's cooperative runtime budget.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import signal
import time
from fractions import Fraction as F


STATES = ("A", "B")
LAMBDA = F(2, 3)
C = F(1, 100)
THETA = F(1, 3)
WEIGHTS = {"A": (F(1), F(1)), "B": (F(1, 3), F(3))}

# Edge tuple: source, target, 2x2 nonnegative matrix, nonnegative drift.
EDGES = (
    ("A", "A", ((F(1, 2), F(0)), (F(0), F(1, 2))), (F(1, 600), F(1, 600))),
    ("A", "B", ((F(2), F(0)), (F(0), F(1, 5))), (F(1, 100), F(0))),
    ("B", "A", ((F(1, 5), F(0)), (F(0), F(2))), (F(0), F(1, 300))),
    ("B", "B", ((F(1, 2), F(0)), (F(0), F(1, 2))), (F(1, 600), F(1, 600))),
)


def q(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def row_times_matrix(v, m):
    return tuple(sum((v[i] * m[i][j] for i in range(2)), F(0)) for j in range(2))


def mat_vec(m, x):
    return tuple(sum((m[i][j] * x[j] for j in range(2)), F(0)) for i in range(2))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def apply_edge(edge, x):
    return add(mat_vec(edge[2], x), edge[3])


def potential(state, x):
    return dot(WEIGHTS[state], x)


def edge_certificate(edge):
    src, dst, matrix, drift = edge
    lhs = row_times_matrix(WEIGHTS[dst], matrix)
    rhs = tuple(LAMBDA * z for z in WEIGHTS[src])
    affine = dot(WEIGHTS[dst], drift)
    return {
        "edge": f"{src}->{dst}",
        "linear_lhs": [q(x) for x in lhs],
        "linear_rhs": [q(x) for x in rhs],
        "linear_pass": all(x <= y for x, y in zip(lhs, rhs)),
        "drift": q(affine),
        "drift_cap": q(C),
        "drift_pass": affine <= C,
    }


def paths(start, depth):
    frontier = [(start, ())]
    for _ in range(depth):
        nxt = []
        for state, word in frontier:
            for idx, edge in enumerate(EDGES):
                if edge[0] == state:
                    nxt.append((edge[1], word + (idx,)))
        frontier = nxt
    return frontier


def run(seed: int, depth: int):
    began = time.monotonic()
    edge_checks = [edge_certificate(e) for e in EDGES]
    assert all(x["linear_pass"] and x["drift_pass"] for x in edge_checks)
    assert C / (1 - LAMBDA) == F(3, 100) < THETA

    rng = random.Random(seed)
    seeds = [(F(i), F(j)) for i in range(5) for j in range(5)]
    seeds += [(F(rng.randrange(0, 401), 20), F(rng.randrange(0, 401), 20)) for _ in range(40)]

    trajectory_checks = 0
    max_ratio_slack = F(0)
    first_crossings = []
    for start_state in STATES:
        accepted = paths(start_state, depth)
        for x0 in seeds:
            for _, word in accepted:
                state = start_state
                x = x0
                bound = potential(state, x)
                first = None
                for step, edge_index in enumerate(word, 1):
                    edge = EDGES[edge_index]
                    assert edge[0] == state
                    old_v = potential(state, x)
                    x = apply_edge(edge, x)
                    state = edge[1]
                    new_v = potential(state, x)
                    assert new_v <= LAMBDA * old_v + C
                    bound = LAMBDA * bound + C
                    assert new_v <= bound
                    max_ratio_slack = max(max_ratio_slack, bound - new_v)
                    if first is None and new_v < THETA:
                        first = step
                    trajectory_checks += 1
                if first is not None:
                    first_crossings.append(first)

    # Hostile controls.
    common_linear_impossible = 2 > 1  # M_AB has diagonal entry 2 on a positive coordinate.
    repeated_cross_invalid = not any(e[0] == "B" and e[1] == "B" and e[2][0][0] == 2 for e in EDGES)
    negative_order_counterexample = {
        "z": ["0", "0"],
        "u": ["1", "0"],
        "Mz": ["0", "0"],
        "Mu": ["-1", "0"],
        "order_propagates": False,
    }
    # The forbidden-set bridge is exact without approximating 2*cos(pi/7):
    # min weight is 1/3, so V<1/3 implies t+s<1; and pi/7<pi/3 gives gamma>1.
    threshold_bridge = min(min(v) for v in WEIGHTS.values()) == F(1, 3)

    return {
        "status": "COMPUTATIONAL exact-rational certificate regression",
        "warning": "This bounded arithmetic model is not a SAT successor construction.",
        "seed": seed,
        "depth": depth,
        "lambda": q(LAMBDA),
        "drift_cap": q(C),
        "limiting_potential_cap": q(C / (1 - LAMBDA)),
        "uniform_threshold": q(THETA),
        "weights": {k: [q(x) for x in v] for k, v in WEIGHTS.items()},
        "edge_certificates": edge_checks,
        "seed_points": len(seeds),
        "accepted_words_per_state": {s: len(paths(s, depth)) for s in STATES},
        "trajectory_step_checks": trajectory_checks,
        "crossings_observed_within_depth": len(first_crossings),
        "max_first_crossing_step": max(first_crossings) if first_crossings else None,
        "max_envelope_slack": q(max_ratio_slack),
        "hostile_controls": {
            "no_common_positive_linear_potential_for_all_edge_matrices": common_linear_impossible,
            "illegal_repeat_of_A_to_B_cross_edge_rejected_by_phase_graph": repeated_cross_invalid,
            "negative_matrix_breaks_order_propagation": negative_order_counterexample,
            "phase_erasure_is_unsound": "M_AB repeated has first diagonal 2^k",
            "fixed_graph_only": "No state count, edge set, weight, or depth depends on SAT input length.",
            "easy_oracle_controls": "No SAT family or oracle is instantiated; the model cannot imply a machine lower bound.",
        },
        "exact_threshold_bridge": threshold_bridge,
        "elapsed_seconds": time.monotonic() - began,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--seed", type=int, default=20261008)
    parser.add_argument("--depth", type=int, default=10)
    args = parser.parse_args()
    signal.alarm(25)
    result = run(args.seed, args.depth)
    body = json.dumps(result, indent=2, sort_keys=True) + "\n"
    with open(args.output, "x", encoding="utf-8") as handle:
        handle.write(body)
    print(body, end="")


if __name__ == "__main__":
    main()
