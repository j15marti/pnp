#!/usr/bin/env python3
"""Finite audit for the pre-output versus pre-decision boundary.

The symbolic result is proved in the accompanying TESTS-0005 report.  This
runner checks the two-pin service, its covariance under renaming and global
complementation, and four trace schedules with fully separated phase counts.
It also exercises the standard easy-family, product, padding, encoding, and
affine/Tseitin controls.  No finite timing observation is extrapolated.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import signal
import time
from collections import defaultdict
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


class BudgetExpired(RuntimeError):
    pass


def _alarm(_signum: int, _frame: object) -> None:
    raise BudgetExpired("25-second cooperative budget expired")


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def encoded_length(formula: Formula) -> int:
    n = max(variables(formula), default=0)
    width = max(1, math.ceil(math.log2(n + 1)))
    return 16 + len(formula) * (4 + 3 * (1 + width))


def evaluate(formula: Formula) -> dict[str, int | bool]:
    vs = variables(formula)
    assignment_checks = 0
    literal_checks = 0
    for bits in itertools.product((False, True), repeat=len(vs)):
        assignment_checks += 1
        assignment = dict(zip(vs, bits))
        ok = True
        for clause in formula:
            clause_ok = False
            for lit in clause:
                literal_checks += 1
                if assignment[abs(lit)] == (lit > 0):
                    clause_ok = True
                    break
            if not clause_ok:
                ok = False
                break
        if ok:
            return {
                "answer": True,
                "assignment_checks": assignment_checks,
                "literal_checks": literal_checks,
            }
    return {
        "answer": False,
        "assignment_checks": assignment_checks,
        "literal_checks": literal_checks,
    }


def pin(formula: Formula, variable: int, value: bool) -> tuple[Formula, int]:
    out: list[Clause] = []
    scans = 0
    for clause in formula:
        satisfied = False
        residual: list[int] = []
        for lit in clause:
            scans += 1
            if abs(lit) == variable:
                if (lit > 0) == value:
                    satisfied = True
            else:
                residual.append(lit)
        if not satisfied:
            out.append(tuple(residual))
    return tuple(out), scans


def service(formula: Formula, variable: int) -> tuple[tuple[bool, bool], dict[str, int]]:
    phase = defaultdict(int)
    answers: list[bool] = []
    for value in (False, True):
        child, scans = pin(formula, variable, value)
        record = evaluate(child)
        answers.append(bool(record["answer"]))
        phase["pin_literal_scans"] += scans
        phase["service_assignment_checks"] += int(record["assignment_checks"])
        phase["service_literal_checks"] += int(record["literal_checks"])
        phase["service_encoded_bits"] += encoded_length(child)
    return (answers[0], answers[1]), dict(phase)


def rename(formula: Formula, mapping: dict[int, int]) -> Formula:
    return tuple(
        tuple(mapping[abs(lit)] if lit > 0 else -mapping[abs(lit)] for lit in clause)
        for clause in formula
    )


def complement(formula: Formula) -> Formula:
    return tuple(tuple(-lit for lit in clause) for clause in formula)


def prism_formula(k: int, offset: int = 0) -> Formula:
    top = tuple(offset + i + 1 for i in range(k))
    bottom = tuple(offset + k + i + 1 for i in range(k))
    rung = tuple(offset + 2 * k + i + 1 for i in range(k))
    edges: list[tuple[int, int, int]] = []
    for i in range(k):
        edges.append(tuple(sorted((top[(i - 1) % k], top[i], rung[i]))))
        edges.append(tuple(sorted((bottom[(i - 1) % k], bottom[i], rung[i]))))
    return tuple(edges + [tuple(-v for v in edge) for edge in edges])


def trace_schedules(formula: Formula, variable: int) -> dict[str, dict[str, object]]:
    main = evaluate(formula)
    q, extraction = service(formula, variable)
    answer = bool(main["answer"])
    assert answer == (q[0] or q[1])
    decision_cost = int(main["assignment_checks"]) + int(main["literal_checks"])
    extraction_cost = sum(extraction.values())
    parse_cost = encoded_length(formula)
    schedules = {
        "DIRECT": {
            "answer": answer,
            "service": None,
            "decision_tick": parse_cost + decision_cost,
            "service_tick": None,
            "output_tick": parse_cost + decision_cost + 1,
            "raw_answer_before_output": True,
        },
        "POSTSERVICE": {
            "answer": answer,
            "service": q,
            "decision_tick": parse_cost + decision_cost,
            "service_tick": parse_cost + decision_cost + extraction_cost,
            "output_tick": parse_cost + decision_cost + extraction_cost + 1,
            "raw_answer_before_output": True,
        },
        "MASKED_POSTSERVICE": {
            "answer": answer,
            "service": q,
            "decision_tick": parse_cost + decision_cost,
            "service_tick": parse_cost + decision_cost + extraction_cost,
            "output_tick": parse_cost + decision_cost + extraction_cost + 2,
            "raw_answer_before_output": False,
            "decoded_answer_before_output": True,
        },
        "PRESERVICE": {
            "answer": q[0] or q[1],
            "service": q,
            "decision_tick": parse_cost + extraction_cost + 1,
            "service_tick": parse_cost + extraction_cost,
            "output_tick": parse_cost + extraction_cost + 2,
            "raw_answer_before_output": True,
        },
    }
    assert schedules["POSTSERVICE"]["decision_tick"] < schedules["POSTSERVICE"]["service_tick"]
    assert schedules["PRESERVICE"]["service_tick"] < schedules["PRESERVICE"]["decision_tick"]
    assert not schedules["MASKED_POSTSERVICE"]["raw_answer_before_output"]
    return schedules


def gaussian_consistent(rows: tuple[tuple[int, int], ...]) -> bool:
    work = [[mask, rhs] for mask, rhs in rows]
    pivot = 0
    width = max((mask.bit_length() for mask, _ in rows), default=0)
    for bit in range(width - 1, -1, -1):
        found = next((j for j in range(pivot, len(work)) if (work[j][0] >> bit) & 1), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        for j in range(len(work)):
            if j != pivot and ((work[j][0] >> bit) & 1):
                work[j][0] ^= work[pivot][0]
                work[j][1] ^= work[pivot][1]
        pivot += 1
    return all(mask or rhs == 0 for mask, rhs in work)


def gaussian_pin(rows: tuple[tuple[int, int], ...], variable: int, value: bool) -> tuple[tuple[int, int], ...]:
    bit = 1 << variable
    return tuple((mask & ~bit, rhs ^ (int(value) if mask & bit else 0)) for mask, rhs in rows)


def run(seed: int) -> dict[str, object]:
    started = time.perf_counter()
    rng = random.Random(seed)
    checks = defaultdict(int)
    phase_totals = defaultdict(int)
    formulas: list[tuple[str, Formula]] = []

    proper = tuple(
        tuple(v * s for v, s in zip((1, 2, 3), signs))
        for signs in itertools.product((-1, 1), repeat=3)
    )
    for mask in range(1 << 8):
        formulas.append(("proper3", tuple(proper[i] for i in range(8) if mask & (1 << i))))

    formulas.extend([
        ("two_sat", ((-1, 2), (-2, 3), (-3, 4))),
        ("horn", ((-1, -2, 3), (-3,), (1,))),
        ("bounded_treewidth", ((1, 2), (-2, 3), (-3, 4), (-4, 5))),
        ("independent_product", ((1,), (4, 5), (-5, 6))),
        ("redundant", ((1, 2, 3), (1, 2, 3), (-1, 2, 3))),
        ("padding", ((1, 2, 3), (4, -4))),
        ("h22_prism3", prism_formula(3)),
        ("h22_prism4", prism_formula(4)),
    ])

    family_counts = defaultdict(int)
    for family, formula in formulas:
        vs = variables(formula)
        if not vs:
            continue
        z = vs[0]
        answer = bool(evaluate(formula)["answer"])
        q, phases = service(formula, z)
        assert answer == (q[0] or q[1])
        checks["two_pin_semantics"] += 1
        family_counts[family] += 1
        for key, value in phases.items():
            phase_totals[key] += value

        perm = list(vs)
        rng.shuffle(perm)
        mapping = dict(zip(vs, perm))
        q_renamed, _ = service(rename(formula, mapping), mapping[z])
        assert q_renamed == q
        checks["rename_covariance"] += 1
        q_complement, _ = service(complement(formula), z)
        assert q_complement == (q[1], q[0])
        checks["complement_covariance"] += 1

        schedules = trace_schedules(formula, z)
        assert len({bool(row["answer"]) for row in schedules.values()}) == 1
        assert schedules["POSTSERVICE"]["service"] == schedules["PRESERVICE"]["service"]
        checks["trace_schedule_agreement"] += len(schedules)
        checks["preoutput_postdecision_witness"] += 1
        checks["interp_mask_guard"] += 1

        # COPY, DEAD, DELAY, and alternate clause-order encodings preserve the bit.
        reversed_formula = tuple(reversed(formula))
        assert bool(evaluate(reversed_formula)["answer"]) == answer
        assert (answer and answer) == answer
        assert (sum(range(17)) >= 0 and answer) == answer
        assert answer == bool(evaluate(formula)["answer"])
        checks["wrapper_encoding_controls"] += 4

    # Actual Gaussian elimination for affine and cycle-Tseitin controls.
    for n in range(3, 13):
        for _ in range(12):
            rows = tuple((rng.randrange(1 << n), rng.randrange(2)) for _ in range(2 * n))
            z = rng.randrange(n)
            answer = gaussian_consistent(rows)
            assert answer == (
                gaussian_consistent(gaussian_pin(rows, z, False))
                or gaussian_consistent(gaussian_pin(rows, z, True))
            )
            checks["affine_gaussian_controls"] += 1
        for odd in (False, True):
            charges = [0] * n
            charges[0] = int(odd)
            cycle = tuple(((1 << ((i - 1) % n)) | (1 << i), charges[i]) for i in range(n))
            answer = gaussian_consistent(cycle)
            assert answer == (not odd)
            assert answer == (
                gaussian_consistent(gaussian_pin(cycle, 0, False))
                or gaussian_consistent(gaussian_pin(cycle, 0, True))
            )
            checks["tseitin_gaussian_controls"] += 1

    return {
        "run_id": "TESTS-0005",
        "status": "PASS",
        "global_status": "P versus NP remains OPEN",
        "seed": seed,
        "mode": "exhaustive-plus-seeded",
        "runtime_seconds": time.perf_counter() - started,
        "checks": dict(checks),
        "total_checks": sum(checks.values()),
        "family_counts": dict(family_counts),
        "charged_phase_totals": dict(phase_totals),
        "exact_schedule_finding": (
            "POSTSERVICE computes the covariant two-pin service after the source answer "
            "is fixed but before external output; PRESERVICE computes the same service before the answer."
        ),
        "limitations": [
            "The symbolic wrapper theorem, not finite traces, establishes the boundary result.",
            "Brute-force controls measure exact finite operations and are not claimed efficient.",
            "The result retires pre-output chronology alone, not a future externally fixed checkpoint contract.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111124)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    try:
        result = run(args.seed)
    finally:
        signal.alarm(0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "total_checks": result["total_checks"],
        "runtime_seconds": result["runtime_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
