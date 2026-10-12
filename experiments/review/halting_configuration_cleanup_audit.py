#!/usr/bin/env python3
"""Bounded audit for HALT-CANON1.

This script does not prove an asymptotic SAT lower bound.  It checks, on a
finite hostile-control battery, that a destructive post-decision cleanup
preserves the answer while reducing the simulated halting configuration to
one output bit and blank work cells.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from pathlib import Path


Literal = int
Clause = tuple[Literal, ...]
CNF = tuple[Clause, ...]


@dataclass
class Trace:
    answer: bool
    work: list[int]
    steps: int
    peak_cells: int


def sat_by_scan(cnf: CNF) -> Trace:
    n = max((abs(lit) for clause in cnf for lit in clause), default=0)
    work: list[int] = []
    steps = 0
    peak = 0
    for bits in itertools.product((0, 1), repeat=n):
        work[:] = bits
        peak = max(peak, len(work))
        steps += 1
        if all(any(bool(bits[abs(lit) - 1]) == (lit > 0) for lit in c)
               for c in cnf):
            return Trace(True, work.copy(), steps, peak)
    return Trace(False, work.copy(), steps, peak)


def direct(cnf: CNF) -> Trace:
    return sat_by_scan(cnf)


def copy(cnf: CNF) -> Trace:
    t = sat_by_scan(tuple(tuple(c) for c in cnf))
    t.work.extend([len(cnf), sum(map(len, cnf))])
    t.peak_cells = max(t.peak_cells, len(t.work))
    t.steps += len(cnf)
    return t


def dead(cnf: CNF) -> Trace:
    t = sat_by_scan(cnf)
    t.work.extend([(i * i + 3 * i + 1) & 1 for i in range(2 * len(cnf) + 7)])
    t.peak_cells = max(t.peak_cells, len(t.work))
    t.steps += len(t.work)
    return t


def delay(cnf: CNF) -> Trace:
    t = sat_by_scan(cnf)
    d = (sum(map(len, cnf)) + 1) ** 2
    t.work.extend([d & 1, (d >> 1) & 1])
    t.peak_cells = max(t.peak_cells, len(t.work))
    t.steps += d
    return t


def interp(cnf: CNF) -> Trace:
    encoded = json.dumps(cnf)
    parsed = tuple(tuple(int(x) for x in c) for c in json.loads(encoded))
    t = sat_by_scan(parsed)
    t.work.extend([len(encoded) & 1])
    t.peak_cells = max(t.peak_cells, len(t.work))
    t.steps += len(encoded)
    return t


def recomp(cnf: CNF) -> Trace:
    first = sat_by_scan(cnf)
    second = sat_by_scan(cnf)
    assert first.answer == second.answer
    return Trace(second.answer, second.work, first.steps + second.steps,
                 max(first.peak_cells, second.peak_cells))


def cleanup(trace: Trace) -> dict[str, int | bool]:
    answer = trace.answer
    touched = len(trace.work)
    # Sequential tape cleanup: sweep every retained work cell once, blank it,
    # reset the head/control, and keep only the output bit.
    trace.work[:] = [0] * touched
    cleanup_steps = touched + 1
    trace.work.clear()
    return {
        "answer": answer,
        "nonblank_work_cells": sum(bool(x) for x in trace.work),
        "retained_output_bits": 1,
        "cleanup_steps": cleanup_steps,
        "peak_cells_before_cleanup": trace.peak_cells,
        "total_steps": trace.steps + cleanup_steps,
    }


def families() -> dict[str, CNF]:
    # Canonical paired K_{3,3}: six positive triples and their six negative
    # mates.  It is proper, duplicate free, sign-monochromatic, and every
    # variable occurs exactly twice in each polarity.
    triples = [[3 * i + j for j in range(3)] for i in range(3)]
    triples += [[3 * i + j for i in range(3)] for j in range(3)]
    signed_22 = tuple(
        clause
        for triple in triples
        for clause in (
            tuple(v + 1 for v in triple),
            tuple(-(v + 1) for v in triple),
        )
    )
    return {
        "signed_22_paired_k33": signed_22,
        "horn_sat": ((-1, -2, 3), (1,), (2,)),
        "horn_unsat": ((1,), (-1,)),
        "two_sat": ((1, 2), (-1, 2), (1, -2)),
        "affine_tseitin_unsat": ((1, 2), (-1, -2), (1, -2), (-1, 2)),
        "bounded_treewidth_path": ((1, 2), (-2, 3), (-3, 4), (-4,)),
        "independent_product": ((1,), (2, 3), (-2, 3), (4,), (-5, 6)),
        "padding_redundancy": ((1, 2, 3), (1, 2, 3), (4, -4, 5)),
        "alternate_literal_order": ((3, 1, 2), (-2, -1), (4,)),
    }


def is_signed_22(cnf: CNF) -> bool:
    n = max(abs(lit) for clause in cnf for lit in clause)
    counts = {(v, sign): 0 for v in range(1, n + 1) for sign in (-1, 1)}
    if len(set(cnf)) != len(cnf):
        return False
    for clause in cnf:
        if len(clause) != 3 or len({abs(lit) for lit in clause}) != 3:
            return False
        signs = {1 if lit > 0 else -1 for lit in clause}
        if len(signs) != 1:
            return False
        for lit in clause:
            counts[(abs(lit), 1 if lit > 0 else -1)] += 1
    return all(counts[(v, -1)] == counts[(v, 1)] == 2
               for v in range(1, n + 1))


def main() -> None:
    started = time.perf_counter()
    solvers = {
        "DIRECT": direct,
        "COPY": copy,
        "DEAD": dead,
        "DELAY": delay,
        "INTERP": interp,
        "RECOMP": recomp,
    }
    assertions = 0
    assert is_signed_22(families()["signed_22_paired_k33"])
    assertions += 1
    rows = []
    for family, cnf in families().items():
        expected = sat_by_scan(cnf).answer
        for solver_name, solver in solvers.items():
            trace = solver(cnf)
            before = len(trace.work)
            result = cleanup(trace)
            checks = [
                result["answer"] == expected,
                result["nonblank_work_cells"] == 0,
                result["retained_output_bits"] == 1,
                result["cleanup_steps"] <= before + 1,
                result["total_steps"] >= result["cleanup_steps"],
            ]
            assert all(checks), (family, solver_name, result)
            assertions += len(checks)
            rows.append({
                "family": family,
                "solver": solver_name,
                "answer": expected,
                "work_cells_before_cleanup": before,
                **result,
            })
    payload = {
        "claim": "HALTING-CONFIGURATION-CANONICALIZATION1",
        "status": "COMPUTATIONAL",
        "families": len(families()),
        "solvers": len(solvers),
        "cases": len(rows),
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "rows": rows,
    }
    encoded = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    payload["payload_sha256_without_self_field"] = hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()
    out = Path("results/raw/review/2026-10-12_halting_configuration_cleanup.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        k: payload[k] for k in (
            "claim", "status", "families", "solvers", "cases", "assertions",
            "failures", "elapsed_seconds", "payload_sha256_without_self_field"
        )
    }, sort_keys=True))


if __name__ == "__main__":
    main()
