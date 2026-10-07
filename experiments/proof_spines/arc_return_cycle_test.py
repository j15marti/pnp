#!/usr/bin/env python3
"""Bounded exact-arithmetic tests for ARC finite return-cycle accounting."""

from __future__ import annotations

from fractions import Fraction
import json
import math
import random
import time

DEADLINE_SECONDS = 25.0
SEED = 20261007


def mat_vec(a, x):
    return tuple(sum(a[i][j] * x[j] for j in range(2)) for i in range(2))


def vec_add(x, y):
    return tuple(x[i] + y[i] for i in range(2))


def mat_mul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def affine(a, d, x):
    return vec_add(mat_vec(a, x), d)


def frac_pair(x):
    return [f"{v.numerator}/{v.denominator}" for v in x]


def main():
    started = time.monotonic()
    gamma = 2.0 * math.cos(math.pi / 7.0)
    m0 = ((Fraction(2), Fraction(0)), (Fraction(0), Fraction(1, 5)))
    d0 = (Fraction(1, 20), Fraction(1, 20))
    m1 = ((Fraction(1, 5), Fraction(0)), (Fraction(0), Fraction(2)))
    d1 = (Fraction(1, 20), Fraction(1, 20))
    product = mat_mul(m1, m0)
    offset = vec_add(mat_vec(m1, d0), d1)
    fixed = (
        offset[0] / (1 - product[0][0]),
        offset[1] / (1 - product[1][1]),
    )

    rng = random.Random(SEED)
    starts = [(Fraction(8), Fraction(1))]
    for _ in range(64):
        starts.append((Fraction(rng.randint(1, 40), 2), Fraction(rng.randint(1, 40), 2)))

    checks = 0
    crossing_cycles = []
    first_trace = []
    for start in starts:
        x = start
        crossed = float(sum(x)) < gamma
        for cycle in range(1, 80):
            if time.monotonic() - started > DEADLINE_SECONDS:
                raise TimeoutError("cooperative 25-second budget exceeded")
            phase0 = affine(m0, d0, x)
            phase1 = affine(m1, d1, phase0)
            direct = affine(product, offset, x)
            assert phase1 == direct
            checks += 1
            if start == starts[0] and cycle <= 8:
                first_trace.append({
                    "cycle": cycle,
                    "before": frac_pair(x),
                    "after_phase0": frac_pair(phase0),
                    "after_phase1": frac_pair(phase1),
                    "phase0_sum_expands": sum(phase0) > sum(x),
                })
            x = phase1
            if float(sum(x)) < gamma:
                crossing_cycles.append(cycle)
                crossed = True
                break
        assert crossed

    assert product == ((Fraction(2, 5), Fraction(0)), (Fraction(0), Fraction(2, 5)))
    assert offset == (Fraction(3, 50), Fraction(3, 20))
    assert fixed == (Fraction(1, 10), Fraction(1, 4))
    assert float(sum(fixed)) < gamma
    assert any(row["phase0_sum_expands"] for row in first_trace)

    asymptote_margins = [Fraction(1, 2**r) for r in range(1, 65)]
    assert all(v > 0 for v in asymptote_margins)
    checks += len(asymptote_margins)

    time_witness = (1.2, 10.0)
    space_witness = (10.0, 0.1)
    borrowed = (min(time_witness[0], space_witness[0]), min(time_witness[1], space_witness[1]))
    assert sum(borrowed) < gamma
    assert borrowed not in (time_witness, space_witness)
    checks += 1

    padding = []
    original_k = 12.0
    for p in (2, 4, 8):
        padding.append({"padding_power": p, "apparent_exponent": original_k / p})
        checks += 1

    growing_depth = []
    initial = 10.0
    for logn in (16, 32, 64, 128, 256):
        lam = 1.0 - 1.0 / logn
        steps = math.ceil(math.log(gamma / initial) / math.log(lam))
        growing_depth.append({"log2_N": logn, "lambda_N": lam, "steps_to_threshold": steps})
        checks += 1
    assert all(growing_depth[i]["steps_to_threshold"] < growing_depth[i + 1]["steps_to_threshold"] for i in range(len(growing_depth) - 1))

    non_downward = {"u": [1.0, 1.0], "z": [0.5, 0.5], "set": "t+s>1.5"}
    assert sum(non_downward["u"]) > 1.5 and sum(non_downward["z"]) <= 1.5
    checks += 1

    elapsed = time.monotonic() - started
    result = {
        "run_id": "ARC-0001",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "deadline_seconds": DEADLINE_SECONDS,
        "elapsed_seconds": elapsed,
        "checks": checks,
        "gamma": gamma,
        "two_phase_example": {
            "M0": [[str(v) for v in row] for row in m0],
            "d0": frac_pair(d0),
            "M1": [[str(v) for v in row] for row in m1],
            "d1": frac_pair(d1),
            "composite_M": [[str(v) for v in row] for row in product],
            "composite_d": frac_pair(offset),
            "fixed_point": frac_pair(fixed),
            "fixed_point_sum": float(sum(fixed)),
            "max_crossing_cycles_over_test_starts": max(crossing_cycles),
            "first_trace": first_trace,
        },
        "negative_controls": {
            "strict_decrease_without_crossing": {"smallest_exact_positive_margin": str(min(asymptote_margins)), "all_symbolically_above_gamma": True},
            "coordinate_borrowing": {"time_witness": time_witness, "space_witness": space_witness, "invalid_componentwise_min": borrowed},
            "padding": padding,
            "non_downward_endpoint": non_downward,
            "input_dependent_depth": growing_depth,
        },
        "limitations": [
            "Synthetic exponent dynamics only; no SAT-specific successor theorem is implemented.",
            "Finite tests do not establish asymptotic ARC closure.",
            "The two-phase example validates the algebra and hostile controls, not P versus NP.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()