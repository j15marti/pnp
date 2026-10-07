#!/usr/bin/env python3
"""Exact arithmetic checks for COFINAL-SEED-HITTING1.

The theorem is logical.  This model demonstrates a cofinal diagonal seed set
with K-dependent contraction rates tending to one and finite route lengths
tending to infinity.  It also exercises bounded-seed, current-scale, and
coordinate-borrowing controls.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import signal
import time


SEED = 20261007
BUDGET_SECONDS = 25


def next_power_of_two_at_least(x: Fraction) -> int:
    target = max(2, (x.numerator + x.denominator - 1) // x.denominator)
    cap = 2
    while cap < target:
        cap *= 2
    return cap


def finite_route(cap: int) -> dict[str, int | str]:
    """Iterate z <- ((cap-1)/cap) z from z=(cap,cap) until sum(z)<1."""
    contraction = Fraction(cap - 1, cap)
    coordinate = Fraction(cap, 1)
    steps = 0
    while 2 * coordinate >= 1:
        coordinate *= contraction
        steps += 1
    exact_coordinate = f"{coordinate.numerator}/{coordinate.denominator}"
    return {
        "cap": cap,
        "lambda": f"{contraction.numerator}/{contraction.denominator}",
        "steps": steps,
        "final_coordinate_numerator_bits": coordinate.numerator.bit_length(),
        "final_coordinate_denominator_bits": coordinate.denominator.bit_length(),
        "final_coordinate_sha256": hashlib.sha256(exact_coordinate.encode()).hexdigest(),
        "final_sum_below_one": 2 * coordinate < 1,
    }


def same_realization(pair: tuple[tuple[Fraction, str], tuple[Fraction, str]]) -> bool:
    """Time and space coordinates are joint only when witness IDs agree."""
    return pair[0][1] == pair[1][1]


def main() -> None:
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25-second cooperative budget exceeded")))
    signal.alarm(BUDGET_SECONDS)
    started = time.monotonic()
    rng = random.Random(SEED)

    caps = [2**power for power in range(1, 9)]
    routes = [finite_route(cap) for cap in caps]
    assert all(bool(route["final_sum_below_one"]) for route in routes)
    assert all(routes[i]["steps"] < routes[i + 1]["steps"] for i in range(len(routes) - 1))

    padded_points = []
    for _ in range(64):
        t = Fraction(rng.randrange(0, 10000), rng.randrange(1, 31))
        s = Fraction(rng.randrange(0, 10000), rng.randrange(1, 31))
        cap = next_power_of_two_at_least(max(t, s))
        assert Fraction(cap) >= t and Fraction(cap) >= s
        padded_points.append({"t": str(t), "s": str(s), "cap": cap})

    bounded_seed_max = 16
    bounded_control_point = Fraction(17)
    bounded_seed_is_cofinal = any(
        Fraction(cap) >= bounded_control_point for cap in (2, 4, 8, bounded_seed_max)
    )
    assert not bounded_seed_is_cofinal

    no_shrink_coordinate = Fraction(32)
    for _ in range(2048):
        no_shrink_coordinate *= 1
    current_scale_control_crosses = 2 * no_shrink_coordinate < 1
    assert not current_scale_control_crosses

    joint_pair = ((Fraction(3, 2), "machine-A"), (Fraction(1, 4), "machine-A"))
    borrowed_pair = ((Fraction(3, 2), "machine-A"), (Fraction(1, 4), "machine-B"))
    assert same_realization(joint_pair)
    assert not same_realization(borrowed_pair)

    elapsed = time.monotonic() - started
    signal.alarm(0)
    result = {
        "claim_id": "COFINAL-SEED-HITTING1",
        "status": "COMPUTATIONAL check of a symbolic conditional lemma",
        "seed": SEED,
        "cooperative_budget_seconds": float(BUDGET_SECONDS),
        "elapsed_seconds": round(elapsed, 6),
        "cofinal_seed_set": "powers of two",
        "routes": routes,
        "padding_checks": len(padded_points),
        "maximum_selected_cap": max(point["cap"] for point in padded_points),
        "bounded_seed_control": {
            "largest_seed": bounded_seed_max,
            "undominated_point": str(bounded_control_point),
            "cofinal": bounded_seed_is_cofinal,
        },
        "current_scale_no_shrink_control": {
            "iterations": 2048,
            "crosses_sum_below_one": current_scale_control_crosses,
        },
        "same_realization_control": {
            "joint_pair_accepted": same_realization(joint_pair),
            "coordinate_borrowing_rejected": not same_realization(borrowed_pair),
        },
        "growing_depth_guard": (
            "Route lengths grow with the fixed cap K. The theorem selects one fixed finite K after "
            "a P=NP witness exists; it does not authorize K=K(N) or a depth growing with input length."
        ),
        "passed": True,
        "scope": (
            "Exact rational checks of cofinal padding and K-dependent finite arithmetic routes. "
            "They do not construct a SAT successor, erase current-scale calls, or establish the Williams model transfer."
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
