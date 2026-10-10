#!/usr/bin/env python3
"""Bounded exact check for the MODEL_BRIDGE semantic-transport probe guard."""

from __future__ import annotations

import argparse
import json
import signal
import time
from pathlib import Path


def force_zero(v: int, a: int, b: int) -> list[tuple[int, int, int]]:
    return [
        (-v, a, b),
        (-v, a, -b),
        (-v, -a, b),
        (-v, -a, -b),
    ]


def build(r: int, flipped: int | None) -> list[tuple[int, int, int]]:
    forced = list(range(1, r + 3))  # x_1,...,x_r,y,z
    next_var = r + 3
    clauses: list[tuple[int, int, int]] = []
    for v in forced:
        clauses.extend(force_zero(v, next_var, next_var + 1))
        next_var += 2
    y, z = r + 1, r + 2
    for i in range(1, r + 1):
        clauses.append(((i if flipped == i else -i), y, z))
    return clauses


def simplify(clauses: list[tuple[int, ...]], var: int, value: bool):
    sat_lit = var if value else -var
    false_lit = -sat_lit
    out = []
    for clause in clauses:
        if sat_lit in clause:
            continue
        reduced = tuple(lit for lit in clause if lit != false_lit)
        if not reduced:
            return None
        out.append(reduced)
    return out


def dpll(clauses: list[tuple[int, ...]]) -> bool:
    while True:
        units = [c[0] for c in clauses if len(c) == 1]
        if not units:
            break
        lit = units[0]
        nxt = simplify(clauses, abs(lit), lit > 0)
        if nxt is None:
            return False
        clauses = nxt
    if not clauses:
        return True
    var = abs(clauses[0][0])
    for value in (False, True):
        nxt = simplify(clauses, var, value)
        if nxt is not None and dpll(nxt):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-r", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    signal.alarm(25)
    started = time.time()
    rows = []
    failures = []
    for r in range(1, args.max_r + 1):
        base = build(r, None)
        base_sat = dpll([tuple(c) for c in base])
        row = {
            "r": r,
            "clauses": len(base),
            "expected_clauses": 5 * r + 8,
            "base_sat": base_sat,
            "flips": [],
        }
        if not base_sat or len(base) != 5 * r + 8:
            failures.append({"r": r, "kind": "base_or_count"})
        for j in range(1, r + 1):
            alt = build(r, j)
            diff = [k for k, (a, b) in enumerate(zip(base, alt)) if a != b]
            alt_sat = dpll([tuple(c) for c in alt])
            ok = (not alt_sat) and len(diff) == 1 and diff[0] == 4 * (r + 2) + j - 1
            row["flips"].append({"j": j, "sat": alt_sat, "different_slots": diff, "ok": ok})
            if not ok:
                failures.append({"r": r, "j": j, "kind": "flip"})
        rows.append(row)
    payload = {
        "status": "PASS" if not failures else "FAIL",
        "method": "exhaustive over r and every single switch flip; exact DPLL truth check",
        "max_r": args.max_r,
        "instances_checked": sum(1 + r for r in range(1, args.max_r + 1)),
        "seed": None,
        "elapsed_seconds": round(time.time() - started, 6),
        "rows": rows,
        "failures": failures,
        "limitation": "Finite sanity check only; the asymptotic probe guard is proved symbolically in the report.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("status", "max_r", "instances_checked", "elapsed_seconds", "failures")}))


if __name__ == "__main__":
    main()
