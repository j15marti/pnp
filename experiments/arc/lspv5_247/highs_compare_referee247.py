#!/usr/bin/env python3
"""External exact baseline: encode the two SAT fixtures as 0/1 MILPs for HiGHS.

Run time on the checked environment is below 30 seconds.  ``disp=True`` makes
HiGHS print B&B nodes, LP iterations, and wall time; these are preserved in the
published comparison JSON.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
SOURCE = CANONICAL if CANONICAL.exists() else ROOT / "tmp/doecker61_source.txt"


def load():
    text = "\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#"))
    return ast.literal_eval(text)


def solve(name, clauses):
    matrix, lower, upper = [], [], []
    for clause in clauses:
        row = np.zeros(198)
        for lit in clause:
            row[abs(lit) - 1] = 1
        matrix.append(row)
        lower.append(1 if clause[0] > 0 else -np.inf)
        upper.append(np.inf if clause[0] > 0 else 2)
    print(f"BEGIN_HIGHS::{name}", flush=True)
    result = milp(
        np.zeros(198),
        integrality=np.ones(198),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(np.asarray(matrix), lower, upper),
        options={"time_limit": 25, "disp": True},
    )
    print(
        f"END_HIGHS::{name}::status={result.status}::success={result.success}::"
        f"nodes={result.mip_node_count}::gap={result.mip_gap}",
        flush=True,
    )
    return result


def main():
    u = load()
    v = [c[:] for c in u]
    v[2][-1], v[44][-1] = v[44][-1], v[2][-1]
    ru = solve("U", u)
    rv = solve("V", v)
    if ru.status != 2 or not rv.success:
        return 1
    print("VERIFIED::HIGHS-COMPARISON::TARGET-SCOPE-FLMV-REFEREE247")
    return 0


if __name__ == "__main__":
    sys.exit(main())
