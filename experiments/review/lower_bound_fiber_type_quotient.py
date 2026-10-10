#!/usr/bin/env python3
"""Finite audit for LB-0004's fiber-type quotient and binding gates.

This is exhaustive over all relations on four endpoints by four witnesses.
It validates the implementation of elementary counting identities; it is
not an asymptotic SAT lower bound or proof-assistant verification.
"""

from __future__ import annotations

import argparse
import json
import signal
import time
from collections import Counter
from pathlib import Path

START = time.monotonic()
DEADLINE = START + 25.0


class BudgetExceeded(RuntimeError):
    pass


def tick() -> None:
    if time.monotonic() >= DEADLINE:
        raise BudgetExceeded("25-second cooperative budget")


def alarm_handler(signum: int, frame: object) -> None:
    raise BudgetExceeded("25-second alarm")


def pc(mask: int) -> int:
    return mask.bit_count()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoints", type=int, default=4)
    parser.add_argument("--witnesses", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.endpoints != 4 or args.witnesses != 4:
        raise ValueError("the declared exhaustive audit is fixed at 4 by 4")

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    failures: list[dict[str, object]] = []
    relation_count = 1 << (args.endpoints * args.witnesses)
    quotient_checks = collision_checks = padding_checks = 0
    tight_quotient = 0

    for relation in range(relation_count):
        tick()
        fibers = tuple(
            (relation >> (w * args.endpoints)) & ((1 << args.endpoints) - 1)
            for w in range(args.witnesses)
        )
        union = 0
        for fiber in fibers:
            union |= fiber
        b = max(map(pc, fibers), default=0)
        counts = Counter(fibers)
        types = len(counts)
        collision = sum(value * value for value in counts.values())
        quotient_checks += 1
        collision_checks += 1
        if pc(union) > b * types:
            failures.append({"kind": "quotient", "relation": relation})
        if types * collision < args.witnesses * args.witnesses:
            failures.append({"kind": "cauchy", "relation": relation})
        if pc(union) == b * types:
            tight_quotient += 1

        # Ignored witness padding is modeled by duplicating every witness.
        padded = fibers + fibers
        padded_counts = Counter(padded)
        padded_union = 0
        for fiber in padded:
            padded_union |= fiber
        padding_checks += 1
        if padded_union != union or len(padded_counts) != types:
            failures.append({"kind": "padding_quotient", "relation": relation})
        if sum(padded_counts.values()) != 2 * args.witnesses:
            failures.append({"kind": "padding_paths", "relation": relation})

    # No selector of fewer than all accepted endpoints can preserve an
    # otherwise-undistinguished singleton truth endpoint for every binding.
    selector_binding_checks = 0
    selector_counterexamples = []
    accepted = 0b11
    for selected in range(1 << 2):
        if selected & ~accepted or selected == accepted:
            continue
        for truth_index in range(2):
            truth = 1 << truth_index
            selector_binding_checks += 1
            if not selected & truth:
                selector_counterexamples.append(
                    {"accepted": accepted, "selected": selected, "truth": truth}
                )
                break

    # Equal collision counts can coexist with different numbers of types:
    # partitions 3+1+1+1 and 2+2+2 of six witnesses both have collision 12.
    collision_direction_control = {
        "partition_a": [3, 1, 1, 1],
        "types_a": 4,
        "partition_b": [2, 2, 2],
        "types_b": 3,
        "collision_both": 12,
    }
    if sum(x * x for x in collision_direction_control["partition_a"]) != 12:
        failures.append({"kind": "collision_control_a"})
    if sum(x * x for x in collision_direction_control["partition_b"]) != 12:
        failures.append({"kind": "collision_control_b"})

    payload = {
        "status": "PASS" if not failures else "FAIL",
        "method": "exhaustive 4-endpoint by 4-witness relations plus exact synthetic controls",
        "relation_count": relation_count,
        "quotient_checks": quotient_checks,
        "collision_checks": collision_checks,
        "padding_checks": padding_checks,
        "tight_quotient_cases": tight_quotient,
        "selector_binding_checks": selector_binding_checks,
        "selector_counterexamples": selector_counterexamples,
        "collision_direction_control": collision_direction_control,
        "failures": failures,
        "elapsed_seconds": round(time.monotonic() - START, 6),
        "limitation": "Finite validation of counting identities; not an all-algorithm lower bound or an endpoint-cover construction.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in (
        "status", "relation_count", "quotient_checks", "collision_checks",
        "padding_checks", "tight_quotient_cases", "selector_binding_checks",
        "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
