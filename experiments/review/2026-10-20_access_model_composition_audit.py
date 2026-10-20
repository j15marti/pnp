#!/usr/bin/env python3
"""Exact audit for ACCESS-MODEL-COMPOSITION17.

Checks the geometric exponent composition and finite toy controls only.  It
does not construct the missing all-input ARC successor or SAT-to-MKTP map.
"""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


TAU = Fraction(241, 200)
U = Fraction(3, 5)
V = Fraction(1, 2)
TIME_FLOOR = Fraction(11, 10)
SPACE_FLOOR = Fraction(1, 2)


def geometric_generator_exponent(g, v, depth):
    """Base-input exponent to answer one bit at virtual depth `depth`."""
    q = Fraction(0)
    for level in range(depth):
        q += g * v**level
    return q


def arc_step(t, s, g, h=SPACE_FLOOR):
    return max(TIME_FLOOR, U + g + V * t), max(SPACE_FLOOR, h, V * s)


def local_sat_query(bit):
    """A constant-size ordinary SAT instance whose answer is `bit`."""
    return ("z",) if bit else ("z", "not-z")


def sat(query):
    return not ("z" in query and "not-z" in query)


def main():
    failures = []
    assertions = 0

    # Closed form q_j = g(1-v^j)/(1-v), with limit g/(1-v).
    composition_cases = 0
    composition_samples = []
    for v in [Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)]:
        for g in [Fraction(1, 1000), Fraction(1, 400), Fraction(1, 20)]:
            for depth in range(1, 65):
                got = geometric_generator_exponent(g, v, depth)
                want = g * (1 - v**depth) / (1 - v)
                assertions += 2
                composition_cases += 1
                if got != want:
                    failures.append(["composition_closed_form", str(v), str(g), depth])
                if not got < g / (1 - v):
                    failures.append(["composition_limit", str(v), str(g), depth])
                if len(composition_samples) < 8 and depth in (1, 2, 8, 64):
                    composition_samples.append({
                        "v": str(v), "g": str(g), "depth": depth,
                        "exponent": str(got), "limit": str(g / (1 - v)),
                    })

    # The per-stage ARC recurrence already charges the same geometric series.
    arc_cases = 0
    for g in [Fraction(0), Fraction(1, 1600), Fraction(1, 800), Fraction(3, 1600)]:
        for t0 in range(1, 65):
            t, s = Fraction(t0), Fraction(t0)
            for depth in range(1, 65):
                t, s = arc_step(t, s, g)
                closed_unfloored = V**depth * t0 + (U + g) * (1 - V**depth) / (1 - V)
                assertions += 2
                arc_cases += 1
                if t != max(TIME_FLOOR, closed_unfloored):
                    failures.append(["arc_closed_form", str(g), t0, depth, str(t)])
                if s != max(SPACE_FLOOR, V**depth * t0):
                    failures.append(["arc_space", str(g), t0, depth, str(s)])
            assertions += 1
            if not t < TAU:
                failures.append(["arc_no_entry_by_64", str(g), t0, str(t)])

    # Random access carries every source bit through one constant-size query.
    local_query_checks = 0
    for n in range(1, 9):
        for bits in product((0, 1), repeat=n):
            for bit in bits:
                assertions += 1
                local_query_checks += 1
                if sat(local_sat_query(bit)) != bool(bit):
                    failures.append(["local_query", n, bits, bit])

    # Exhaust all 4^8 maps from 3-bit strings to a 2-bit post-pass synopsis.
    # Every such map collides, so some later coordinate cannot be replayed.
    replay_encoders = 0
    min_collision_pairs = None
    domain = list(product((0, 1), repeat=3))
    for table in product(range(4), repeat=8):
        buckets = {}
        for x, state in zip(domain, table):
            buckets.setdefault(state, []).append(x)
        collisions = sum(len(bucket) * (len(bucket) - 1) // 2 for bucket in buckets.values())
        assertions += 1
        replay_encoders += 1
        if collisions == 0:
            failures.append(["injective_short_synopsis", table])
        if min_collision_pairs is None or collisions < min_collision_pairs:
            min_collision_pairs = collisions

    result = {
        "run": "ACCESS-MODEL-COMPOSITION17",
        "status": "PASS" if not failures else "FAIL",
        "scope": "exact exponent composition plus finite random-access/replay controls; missing constructions remain open",
        "generator_composition_formula": "q_j=g(1-v^j)/(1-v)",
        "generator_composition_limit_at_v_half": "2g",
        "arc_time_limit": "6/5+2g",
        "arc_strict_generator_threshold": "1/400",
        "random_access_local_query_cost": "one source read and O(1)-size ordinary SAT instance per bit",
        "one_way_exact_replay_lower_bound": "N bits for arbitrary post-pass coordinate access",
        "composition_cases": composition_cases,
        "arc_cases": arc_cases,
        "local_query_checks": local_query_checks,
        "replay_encoders": replay_encoders,
        "minimum_collision_pairs_for_3_to_2_bit_synopsis": min_collision_pairs,
        "assertions": assertions,
        "composition_samples": composition_samples,
        "failures": failures,
        "global_status": "P versus NP OPEN",
    }
    out = Path("results/raw/synthesis/2026-10-20_1448_ACCESS_MODEL_COMPOSITION17.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
