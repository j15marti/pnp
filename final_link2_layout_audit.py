#!/usr/bin/env python3
"""Finite audit for the child-layout bottleneck in source-backed wrappers.

The symbolic theorem is elementary.  The finite model checks the accounting
on deterministic regular incidence matrices and searches a rational exponent
grid.  It is not a lower bound for arbitrary SAT algorithms.
"""

from __future__ import annotations

import argparse
import json
import math
import signal
import time
from fractions import Fraction
from pathlib import Path


GAMMA = 2.0 * math.cos(math.pi / 7.0)


def layout_objective(a: Fraction, b: Fraction, delta: Fraction) -> Fraction:
    """C+S for the optimistic block-transpose schedule.

    A block contains N^delta children.  Each source rescan handles one block,
    giving acquisition exponent 1+a-delta.  Recursive evaluation gives the
    fixed-point constraint C >= a/(1-b).  Retaining one block of explicit
    N^b children gives S=delta+b.
    """

    if not (Fraction(0) <= delta <= a and Fraction(0) <= b < Fraction(1)):
        raise ValueError((a, b, delta))
    c = max(Fraction(1) + a - delta, a / (Fraction(1) - b))
    return c + delta + b


def closed_form_layout(a: Fraction, b: Fraction) -> Fraction:
    """Minimum of layout_objective on 0 <= delta <= a."""

    if b <= Fraction(1, 1) / (Fraction(1) + a):
        return Fraction(1) + a + b
    return b + a / (Fraction(1) - b)


def explicit_builder_objective(a: Fraction, b: Fraction, h: Fraction = Fraction(1)) -> Fraction:
    """C+S if a child-major builder already emits one child at a time."""

    return max(h, a / (Fraction(1) - b)) + b


def regular_incidence(n: int, q: int, ell: int) -> list[list[int]]:
    """A deterministic q-by-n incidence family with ell entries per child."""

    if ell > n:
        raise ValueError((n, ell))
    stride = max(1, n // max(1, q))
    return [[(child * stride + j) % n for j in range(ell)] for child in range(q)]


def audit_block_schedule(n: int, q: int, ell: int, block: int) -> dict[str, int]:
    children = regular_incidence(n, q, ell)
    source_passes = 0
    emitted = 0
    peak_entries = 0
    recovered: list[list[int]] = [[] for _ in range(q)]
    for lo in range(0, q, block):
        hi = min(q, lo + block)
        source_passes += 1
        active = [list(children[j]) for j in range(lo, hi)]
        peak_entries = max(peak_entries, sum(map(len, active)))
        for offset, row in enumerate(active):
            recovered[lo + offset] = row
            emitted += len(row)
    if recovered != children:
        raise AssertionError("block layout changed a child")
    return {
        "n": n,
        "q": q,
        "child_entries": ell,
        "block_children": block,
        "source_passes": source_passes,
        "optimistic_source_scan_units": source_passes * n,
        "emitted_entries": emitted,
        "peak_retained_entries": peak_entries,
    }


def rational_grid_audit() -> dict[str, object]:
    checked = 0
    mismatches = []
    points = []
    for den in range(2, 33):
        for ai in range(1, den):
            a = Fraction(ai, den)
            for bi in range(1, den):
                b = Fraction(bi, den)
                if b >= 1:
                    continue
                candidates = {Fraction(0), a}
                crossing = Fraction(1) + a - a / (Fraction(1) - b)
                if 0 <= crossing <= a:
                    candidates.add(crossing)
                brute = min(layout_objective(a, b, d) for d in candidates)
                exact = closed_form_layout(a, b)
                checked += 1
                if brute != exact:
                    mismatches.append({"a": str(a), "b": str(b), "brute": str(brute), "exact": str(exact)})
    for a, b in [
        (Fraction(1, 3), Fraction(2, 3)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1, 4), Fraction(1, 2)),
        (Fraction(1, 5), Fraction(1, 2)),
        (Fraction(1, 7), Fraction(1, 2)),
    ]:
        layout = closed_form_layout(a, b)
        explicit = explicit_builder_objective(a, b)
        points.append(
            {
                "a": str(a),
                "b": str(b),
                "layout_sum": float(layout),
                "layout_exact": str(layout),
                "layout_below_williams": float(layout) < GAMMA,
                "child_major_sum": float(explicit),
                "child_major_exact": str(explicit),
                "child_major_below_williams": float(explicit) < GAMMA,
            }
        )
    boundary = []
    for den in range(3, 65):
        for bi in range(1, den):
            b = Fraction(bi, den)
            a = Fraction(1) - b
            value = closed_form_layout(a, b)
            boundary.append(float(value))
            if value != 2:
                mismatches.append({"boundary_a": str(a), "boundary_b": str(b), "value": str(value)})
    return {
        "rational_cells_checked": checked,
        "boundary_cells_checked": len(boundary),
        "boundary_min": min(boundary),
        "boundary_max": max(boundary),
        "mismatches": mismatches,
        "selected_points": points,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="final_link2_layout_results.json")
    args = parser.parse_args()
    signal.alarm(25)
    started = time.perf_counter()

    schedules = []
    for n in (64, 256, 1024, 4096):
        q = max(2, round(n ** (1 / 3)))
        ell = max(1, round(n ** (2 / 3)))
        for block in sorted({1, max(1, round(q ** 0.5)), q}):
            schedules.append(audit_block_schedule(n, q, ell, block))

    grid = rational_grid_audit()
    if grid["mismatches"]:
        raise AssertionError(grid["mismatches"][:3])

    result = {
        "claim": "BATCH-LAYOUT-GATE1",
        "status": "PROVED/EXACT accounting for the declared block-transpose schedule; COMPUTATIONAL finite checks; arbitrary wrapper lower bound OPEN",
        "gamma": GAMMA,
        "model": {
            "fanout": "q=N^(a+o(1))",
            "child_size": "L=N^(b+o(1))",
            "block_size": "B=N^(delta+o(1))",
            "time": "C(delta)=max(1+a-delta, a/(1-b))",
            "space": "S(delta)=b+delta",
            "minimum": "1+a+b if b<=1/(1+a), otherwise b+a/(1-b)",
            "boundary": "a+b=1 implies min(C+S)=2",
        },
        "grid": grid,
        "finite_schedules": schedules,
        "limitations": [
            "The source-pass cost is optimistic and assumes output-sensitive routing within a selected child block.",
            "The result does not lower-bound a child-major generator, a semantic compiler, or an arbitrary SAT algorithm.",
            "It identifies the extra theorem needed: child-major online acquisition, not merely aggregate-linear output.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": args.output,
        "checks": grid["rational_cells_checked"] + grid["boundary_cells_checked"] + len(schedules),
        "mismatches": len(grid["mismatches"]),
        "boundary_sum": [grid["boundary_min"], grid["boundary_max"]],
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
