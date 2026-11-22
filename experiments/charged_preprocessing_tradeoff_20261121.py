#!/usr/bin/env python3
"""Exact finite audit of the charged all-checkpoint accounting envelope.

This checks arithmetic, the discrete crossing-credit optimization, and the
potential identity. It does not simulate a SAT solver, compute Kolmogorov
complexity, verify the splicing premises, or prove an asymptotic theorem.
Only the Python standard library is required. Each audit invocation is small.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import platform
import time


def phi_direct(z: int | Fraction, ell: int) -> Fraction:
    z = Fraction(z)
    answer = Fraction(0)
    j = 1
    while z - ell * j > 0:
        answer += z - ell * j
        j += 1
    return answer


def phi_closed(z: int | Fraction, ell: int) -> Fraction:
    z = Fraction(z)
    if z <= 0:
        return Fraction(0)
    q = z // ell
    return q * z - Fraction(ell * q * (q + 1), 2)


def balanced_bound(delta: int, h: int, ell: int, paid: int) -> Fraction:
    q, rem = divmod(paid, delta)
    return (delta - rem) * phi_closed(h - ell * q, ell) + rem * phi_closed(
        h - ell * (q + 1), ell
    )


@lru_cache(maxsize=None)
def compositions(total: int, slots: int) -> tuple[tuple[int, ...], ...]:
    if slots == 1:
        return ((total,),)
    return tuple(
        (first,) + tail
        for first in range(total + 1)
        for tail in compositions(total - first, slots - 1)
    )


def exact(value: int | Fraction) -> int | str:
    value = Fraction(value)
    return value.numerator if value.denominator == 1 else str(value)


def layout(r: int) -> dict[str, int]:
    n = 8 * r - 1
    m = 10 * r
    w = (8 * r - 1).bit_length()
    nbits = 3 * n + 2 + 2 * ((m + 1).bit_length() - 1) + 3 * m * (w + 1) + w
    delta = 6 * (r - 2) * (w + 1) - 1
    return {"r": r, "n": n, "m": m, "w": w, "N": nbits, "delta": delta}


def audit() -> dict:
    began = time.perf_counter()
    checks = 0
    arithmetic_cases = 0
    for ell in (1, 2, 3, 7):
        for denom in (1, 2, 3, 5):
            for numerator in range(-12, 121):
                z = Fraction(numerator, denom)
                direct = phi_direct(z, ell)
                assert direct == phi_closed(z, ell)
                lower = max(Fraction(0), z - ell) ** 2 / (2 * ell)
                upper = max(Fraction(0), z) ** 2 / (2 * ell)
                assert lower <= direct <= upper
                assert phi_closed(z, ell) - phi_closed(z - ell, ell) == max(
                    Fraction(0), z - ell
                )
                checks += 3
                arithmetic_cases += 1

    allocation_rows = []
    allocations_tested = 0
    for delta in range(1, 5):
        for h in (-2, 0, 1, 2, 5, 8, 11, 17):
            for ell in (1, 2, 3, 7):
                local_cost = [phi_direct(h - ell * p, ell) for p in range(13)]
                for paid in range(13):
                    candidates = compositions(paid, delta)
                    brute = min(sum(local_cost[p] for p in allocation) for allocation in candidates)
                    claimed = balanced_bound(delta, h, ell, paid)
                    jensen = delta * phi_closed(Fraction(h) - Fraction(ell * paid, delta), ell)
                    quadratic = Fraction(delta, 2 * ell) * max(
                        Fraction(0), Fraction(h - ell) - Fraction(ell * paid, delta)
                    ) ** 2
                    assert brute == claimed
                    assert claimed >= jensen >= quadratic
                    checks += 2
                    allocations_tested += len(candidates)
                    allocation_rows.append({
                        "delta": delta, "H": h, "ell": ell, "paid": paid,
                        "exhaustive_min": exact(brute), "balanced_bound": exact(claimed),
                        "jensen_bound": exact(jensen), "quadratic_bound": exact(quadratic),
                        "allocations": len(candidates),
                    })

    # Enumerate abstract event ledgers. 0 denotes a noncrossing transition.
    # These are accounting ledgers, not claims of physically realizable TM runs.
    event_cases = 0
    complete_event_cases = 0
    checked_checkpoints = 0
    delta, h, ell, length = 2, 5, 2, 9
    required_crossings = (h + ell - 1) // ell
    for events in itertools.product(range(delta + 1), repeat=length):
        paid_per_cut = [0] * delta
        potential = delta * phi_closed(h, ell)
        drops = []
        potentials = [potential]
        for event in events:
            old = potential
            if event:
                b = event - 1
                paid_per_cut[b] += 1
                charge = max(0, h - ell * paid_per_cut[b])
            else:
                charge = 0
            potential = sum(phi_closed(h - ell * p, ell) for p in paid_per_cut)
            assert old - potential == charge
            checks += 1
            drops.append(charge)
            potentials.append(potential)
        event_cases += 1
        if min(paid_per_cut) >= required_crossings:
            complete_event_cases += 1
            assert potentials[-1] == 0
            checks += 1
            suffix = 0
            for checkpoint in range(length, -1, -1):
                if checkpoint < length:
                    suffix += drops[checkpoint]
                assert suffix == potentials[checkpoint]
                assert suffix >= balanced_bound(delta, h, ell, checkpoint)
                checks += 2
                checked_checkpoints += 1

    params = layout(1000)
    qstates = 256
    ell = qstates.bit_length()  # ceil(log2(Q+1))
    d = 40
    wcut = params["N"].bit_length()  # ceil(log2(N+1))
    log_factorial_floor = math.factorial(params["r"]).bit_length() - 1
    h = log_factorial_floor - d - 1 - wcut - ell
    time_floor = params["delta"] * max(0, (h + ell - 1) // ell)
    example_rows = []
    for fraction in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
        paid = int(fraction * time_floor)
        example_rows.append({
            "prepayment_fraction": exact(fraction), "paid_transitions": paid,
            "remaining_time_floor": max(0, time_floor - paid),
            "remaining_CM_min_floor": exact(balanced_bound(params["delta"], h, ell, paid)),
        })
    assert h == 8460
    assert time_floor == 78801140
    assert example_rows[0]["remaining_CM_min_floor"] == 332974217070
    assert example_rows[2]["remaining_CM_min_floor"] == 83154902985
    checks += 4

    return {
        "name": "CHARGED-UNSAT-PREPAYMENT1 finite accounting audit",
        "scope": "Exact arithmetic and abstract event accounting only; no SAT-machine simulation or computation of Kolmogorov complexity.",
        "python_version": platform.python_version(),
        "randomness": "none; exhaustive finite grids and event ledgers",
        "elapsed_seconds": time.perf_counter() - began,
        "assertions_passed": checks,
        "phi_rational_cases": arithmetic_cases,
        "allocation_cases": len(allocation_rows),
        "allocations_tested": allocations_tested,
        "event_ledgers": event_cases,
        "complete_event_ledgers": complete_event_cases,
        "suffix_checkpoints_checked": checked_checkpoints,
        "illustration": {
            **params, "Q": qstates, "ell": ell, "W": wcut, "d": d,
            "floor_log2_factorial": log_factorial_floor, "H": h,
            "good_fraction_lower_bound": exact(1 - Fraction(1, 2 ** d)),
            "rows": example_rows,
            "qualification": "Theorem arithmetic for any fixed correct Q-state solver under the report's injection premises and fixed prefix-universal configuration measure; not measured runtime.",
        },
        "allocation_rows": allocation_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    brief = {k: v for k, v in result.items() if k not in ("allocation_rows",)}
    brief["raw_sha256"] = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(json.dumps(brief, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
