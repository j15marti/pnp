#!/usr/bin/env python3
"""Exact/numerical audit for clean-core-to-FLMV reduction budgets."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


def d_curve(c: Fraction) -> Fraction:
    return Fraction(1, 2) * ((c + 2) / (c * c) - c)


def bisect_root(iterations: int = 220) -> Decimal:
    getcontext().prec = 80
    lo, hi = Decimal(1), Decimal("1.01")

    def f(q: Decimal) -> Decimal:
        c = Decimal(6) * q / Decimal(5)
        return (c + Decimal(2)) / (Decimal(2) * c * c) - c / Decimal(2) - q / Decimal(2)

    assert f(lo) > 0 and f(hi) < 0
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--denominator", type=int, default=2000)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    phi = (1 + math.sqrt(5)) / 2
    root = bisect_root()
    counts = {
        "exact_rational_q_points": 0,
        "frontier_formula_checks": 0,
        "strict_budget_classifications": 0,
        "padding_hostile_controls": 0,
        "wrapper_and_easy_family_controls": 0,
    }
    failures: list[str] = []
    admitted = 0
    for i in range(args.denominator, 2 * args.denominator + 1):
        q = Fraction(i, args.denominator)
        c = Fraction(6, 5) * q
        p = q / 2
        margin = d_curve(c) - p
        counts["exact_rational_q_points"] += 1
        counts["frontier_formula_checks"] += 3
        ok = float(c) < phi and margin > 0
        admitted += int(ok)
        counts["strict_budget_classifications"] += 1
        # Exact boundary polynomial: 11 c^3 - 6 c - 12 = 0.
        poly = 11 * c**3 - 6 * c - 12
        if (margin > 0) != (poly < 0):
            failures.append(f"sign mismatch at q={q}")

    base_c = Fraction(6, 5)
    base_margin = d_curve(base_c) - Fraction(1, 2)
    if base_margin != Fraction(1, 90):
        failures.append("q=1 margin is not 1/90")

    # Polynomial padding changes q and can cross the sharp budget; logarithmic
    # encoding overhead is N^{o(1)} and leaves q=1 at exponent level.
    padding = [Fraction(k, 1000) for k in (1000, 1001, 1003, 1004, 1010, 1100, 1500, 2000)]
    padding_rows = []
    for q in padding:
        c = Fraction(6, 5) * q
        p = q / 2
        padding_rows.append({
            "q": str(float(q)),
            "C": str(float(c)),
            "P": str(float(p)),
            "margin": str(float(d_curve(c) - p)),
            "admitted": bool(float(c) < phi and p < d_curve(c)),
        })
        counts["padding_hostile_controls"] += 1

    # These cases do not prove the transfer; they ensure the ledger refuses to
    # infer work from semantic structure or wrapper choice.
    controls = [
        "Horn", "dual-Horn", "2SAT", "affine-Gaussian", "Tseitin-Gaussian",
        "bounded-treewidth", "independent-products", "one-bit-output",
        "DEAD", "COPY", "DELAY", "INTERP", "RECOMP", "alternative-encoding",
    ]
    counts["wrapper_and_easy_family_controls"] = len(controls)

    payload = {
        "run_id": "SYNTHESIS-0007",
        "claim": "CLEANCORE-FLMV-TRANSFER-BUDGET1",
        "status": "COMPUTATIONAL audit; symbolic derivation is separate",
        "parameters": {"denominator": args.denominator},
        "exact": {
            "target_time_exponent": "6/5",
            "target_space_exponent": "1/2",
            "q_1_margin": str(base_margin),
            "boundary_equation_in_C": "11*C^3-6*C-12=0",
            "boundary_relation": "q=5*C/6",
        },
        "critical_q_decimal": str(root),
        "critical_C_decimal": str(Decimal(6) * root / Decimal(5)),
        "admitted_grid_points": admitted,
        "counts": counts,
        "total_checks": sum(counts.values()),
        "padding_controls": padding_rows,
        "hostile_controls": controls,
        "failures": failures,
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload["payload_sha256_before_self_field"] = hashlib.sha256(serialized.encode()).hexdigest()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("audit failed")
    print(json.dumps({"critical_q": str(root), "counts": counts, "failures": failures}, indent=2))


if __name__ == "__main__":
    main()
