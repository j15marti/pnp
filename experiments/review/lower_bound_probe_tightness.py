#!/usr/bin/env python3
"""Bounded audit for the clause-probe guard and its linear tightness.

Designed for a 25 second cooperative budget.  The shell invocation should
also use a 30 second hard timeout.
"""
from __future__ import annotations

import argparse
import json
import signal
import time
from pathlib import Path


def force_zero(v: int, a: int, b: int):
    return [(-v, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)]


def family(r: int, flipped: int | None = None):
    x = list(range(1, r + 1))
    y, z = r + 1, r + 2
    nxt = r + 3
    clauses = []
    for v in x + [y, z]:
        clauses.extend(force_zero(v, nxt, nxt + 1))
        nxt += 2
    for j, v in enumerate(x):
        clauses.append(((v if j == flipped else -v), y, z))
    return clauses, nxt - 1


def simplify(clauses, var, value):
    sat_lit = var if value else -var
    dead_lit = -sat_lit
    out = []
    for clause in clauses:
        if sat_lit in clause:
            continue
        out.append(tuple(l for l in clause if l != dead_lit))
    return out


def dpll(clauses):
    while True:
        if any(len(c) == 0 for c in clauses):
            return False
        if not clauses:
            return True
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        clauses = simplify(clauses, abs(unit), unit > 0)
    lit = clauses[0][0]
    var = abs(lit)
    return dpll(simplify(clauses, var, True)) or dpll(simplify(clauses, var, False))


def scan_emit(signs):
    probes = 0
    for sign in signs:
        probes += 1
        if sign == 1:
            return 0, probes
    return 1, probes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-r", type=int, default=10)
    parser.add_argument("--scale-r", type=int, default=100000)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
    signal.alarm(25)
    started = time.monotonic()
    failures = []
    semantic_checks = 0
    omitted_slot_controls = 0
    for r in range(1, args.max_r + 1):
        base, _ = family(r)
        semantic_checks += 1
        if not dpll(base):
            failures.append({"r": r, "case": "base"})
        for j in range(r):
            semantic_checks += 1
            if dpll(family(r, j)[0]):
                failures.append({"r": r, "case": "flip", "j": j})
            # Any transcript omitting j is identical on the two sign vectors.
            q = [i for i in range(r) if i != j]
            zero_view = tuple(-1 for _ in q)
            flip_view = tuple((1 if i == j else -1) for i in q)
            omitted_slot_controls += 1
            if zero_view != flip_view:
                failures.append({"r": r, "case": "transcript", "j": j})
        value, probes = scan_emit([-1] * r)
        if value != 1 or probes != r:
            failures.append({"r": r, "case": "tight_scan"})
    scale_value, scale_probes = scan_emit([-1] * args.scale_r)
    elapsed = time.monotonic() - started
    result = {
        "status": "PASS" if not failures else "FAIL",
        "max_r_exact": args.max_r,
        "semantic_checks": semantic_checks,
        "omitted_slot_controls": omitted_slot_controls,
        "scale_r": args.scale_r,
        "scale_value": scale_value,
        "scale_probes": scale_probes,
        "failures": failures,
        "elapsed_seconds": elapsed,
        "interpretation": (
            "The family realizes the SAT/UNSAT switch and forces every switch "
            "probe on the satisfiable member, while a direct scan achieves the "
            "linear floor. This is finite validation, not an asymptotic SAT lower bound."
        ),
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
