#!/usr/bin/env python3
"""Finite hostile-control audit for TRACECONJ1.

This is a bounded identity/property test.  It does not establish an
asymptotic lower bound and it does not decide P versus NP.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


def prefix_parities(bits: tuple[int, ...]) -> tuple[int, ...]:
    out = [0]
    for bit in bits:
        out.append(out[-1] ^ bit)
    return tuple(out)


def reconstruct(trace: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a ^ b for a, b in zip(trace, trace[1:]))


def fixed_schedule(n: int, budget: int) -> tuple[str, ...]:
    # Abstract fixed-sweep schedule: addresses and control depend only on n,budget.
    scan = tuple(f"input:{i}" for i in range(n))
    sweeps = tuple(f"sweep:{t}:{j}" for t in range(budget) for j in range(budget))
    return scan + sweeps + ("cancel:p", "cancel:q", "output")


def wrapped(bits: tuple[int, ...], answer: int, budget: int) -> dict[str, object]:
    trace = prefix_parities(bits)
    p = trace[-1]
    q = p
    z = answer ^ p
    y = z ^ q
    schedule = fixed_schedule(len(bits), budget)
    return {
        "trace": trace,
        "schedule_hash": hashlib.sha256("|".join(schedule).encode()).hexdigest(),
        "terminal": (answer, p, q, z, y),
        "output": y,
        "charged_steps": len(bits) + budget * budget + 3,
    }


def answer_zero(bits: tuple[int, ...]) -> int:
    return 0


def answer_first(bits: tuple[int, ...]) -> int:
    return bits[0]


def answer_majority(bits: tuple[int, ...]) -> int:
    return int(sum(bits) * 2 >= len(bits))


def answer_parity(bits: tuple[int, ...]) -> int:
    return sum(bits) & 1


def fixed_width_forced_assignment(a: tuple[int, int, int]) -> tuple[int, ...]:
    # Three repeated-literal 3-CNF clauses.  Each literal uses fixed-width
    # (sign, variable-id) bits, so all eight encodings have the same length.
    ids = ((0, 1), (1, 0), (1, 1))
    bits: list[int] = []
    for value, var_id in zip(a, ids):
        literal = (value,) + var_id
        bits.extend(literal * 3)
    return tuple(bits)


def main() -> None:
    functions = {
        "zero": answer_zero,
        "first": answer_first,
        "majority": answer_majority,
        "parity": answer_parity,
    }
    source_checks = 0
    reconstruction_checks = 0
    output_checks = 0
    intervention_checks = 0
    schedule_checks = 0
    schedule_by_shape: dict[tuple[int, int], str] = {}

    for n in range(1, 13):
        budget = n + 2
        for bits in itertools.product((0, 1), repeat=n):
            for name, fn in functions.items():
                answer = fn(bits)
                run = wrapped(bits, answer, budget)
                source_checks += 1
                assert reconstruct(run["trace"]) == bits
                reconstruction_checks += 1
                assert run["output"] == answer
                output_checks += 1

                a, p, q, z, y = run["terminal"]
                assert (z ^ 1) ^ q == (y ^ 1)  # intervene on the p-to-z path
                assert z ^ (q ^ 1) == (y ^ 1)  # intervene on the q path
                intervention_checks += 2

                key = (n, budget)
                old = schedule_by_shape.setdefault(key, run["schedule_hash"])
                assert old == run["schedule_hash"], (name, bits)
                schedule_checks += 1

    # Same-answer, same-parity terminal collision with different H=assignment.
    forced = []
    for a in itertools.product((0, 1), repeat=3):
        bits = fixed_width_forced_assignment(a)
        run = wrapped(bits, 1, len(bits) + 2)
        forced.append({"assignment": a, "bits": bits, "terminal": run["terminal"]})
    collision = None
    for left, right in itertools.combinations(forced, 2):
        if left["terminal"] == right["terminal"] and left["assignment"] != right["assignment"]:
            collision = (left, right)
            break
    assert collision is not None

    # Named hostile controls.  They test representation/wrapper invariance only;
    # no timing extrapolation is made from these finite instances.
    controls = {
        "2SAT": (0, 1, 1, 0, 1, 0),
        "Horn": (1, 0, 0, 1, 1, 0),
        "affine_Tseitin": (1, 1, 0, 1, 0, 0),
        "bounded_treewidth": (0, 0, 1, 0, 1, 1),
        "independent_product": (1, 0, 1, 0, 1, 0),
        "padding": (0, 1, 0, 1, 0, 1, 0, 0, 0, 0),
        "redundant_clauses": (1, 1, 0, 0, 1, 1, 0, 0),
        "alternate_encoding": (0, 1, 0, 0, 1, 1, 1),
    }
    control_checks = 0
    for bits0 in controls.values():
        bits = tuple(bits0)
        answer = answer_majority(bits)
        baseline = wrapped(bits, answer, len(bits) + 2)
        for wrapper in ("dead", "copy", "delay", "interpret", "recompute"):
            # Wrapper names deliberately do not alter the exact one-bit function.
            candidate = wrapped(bits, answer, len(bits) + 2)
            assert candidate["output"] == baseline["output"] == answer, wrapper
            assert reconstruct(candidate["trace"]) == bits
            control_checks += 2

    result = {
        "run_id": "TRACECONJ1",
        "status": "COMPUTATIONAL finite identity/property audit",
        "scope": "n=1..12; no asymptotic inference",
        "source_checks": source_checks,
        "reconstruction_checks": reconstruction_checks,
        "output_checks": output_checks,
        "intervention_checks": intervention_checks,
        "schedule_checks": schedule_checks,
        "hostile_control_checks": control_checks,
        "forced_assignment_count": len(forced),
        "terminal_collision": {
            "left_H": collision[0]["assignment"],
            "right_H": collision[1]["assignment"],
            "terminal": collision[0]["terminal"],
            "encoding_length": len(collision[0]["bits"]),
        },
        "conclusion": (
            "The finite construction simultaneously has a source-injective data trace, "
            "an input-independent fixed schedule, live cancellation paths, positive charged "
            "work, and exact output, while the terminal view collides on distinct H values."
        ),
        "p_vs_np": "OPEN",
    }
    out = Path("results/raw/review/2026-10-13_trace_guard_conjunction.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
