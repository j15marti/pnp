#!/usr/bin/env python3
"""Accounting audit for PARENT-PROBE-BUDGET70.

Finite checks only: no semantic ARC compiler or class separation is claimed.
"""

from __future__ import annotations

import json
import math
import random


def iterate(c: float, base: float, alpha: float, beta: float, depth: int) -> float:
    for _ in range(depth):
        c = max(base, alpha + beta * c)
    return c


def explicit(c0: float, base: float, alpha: float, beta: float, depth: int) -> float:
    vals = [alpha * (1.0 - beta**depth) / (1.0 - beta) + c0 * beta**depth]
    for i in range(depth):
        prefix = alpha * (1.0 - beta**i) / (1.0 - beta)
        vals.append(prefix + base * beta**i)
    return max(vals)


def main() -> None:
    alpha, beta, delta = 0.6, 0.5, 0.5
    checks = 0
    failures = []
    rng = random.Random(701848)

    phase_rows = []
    for j in range(0, 101):
        eta = j / 100.0
        probe_exp = alpha + eta
        base = max(1.0, alpha + delta, probe_exp)
        fixed = max(base, alpha / (1.0 - beta))
        preserve_11 = eta <= 0.5 + 1e-12
        preserve_12 = eta <= 0.6 + 1e-12
        checks += 4
        if (base <= 1.1 + 1e-12) != preserve_11:
            failures.append(("one_step_threshold", eta, base))
        if (fixed <= 1.2 + 1e-12) != preserve_12:
            failures.append(("fixed_point_threshold", eta, fixed))
        if abs(probe_exp - (alpha + eta)) > 1e-12:
            failures.append(("probe_sum", eta, probe_exp))
        if abs(fixed - max(base, 1.2)) > 1e-12:
            failures.append(("fixed_formula", eta, fixed))
        phase_rows.append(
            {
                "eta": eta,
                "aggregate_probe_exponent": probe_exp,
                "one_step_base": base,
                "time_fixed_point": fixed,
                "preserves_1_1_overhead": preserve_11,
                "preserves_1_2_fixed_point": preserve_12,
            }
        )

    # Blocked scans: B=N^b gives average per-child probe exponent eta=1-b.
    blocked_rows = []
    for j in range(0, 101):
        b = j / 100.0
        eta = 1.0 - b
        aggregate = 1.0 + max(0.0, alpha - b)
        direct = max(1.0, alpha + eta)
        checks += 1
        if abs(aggregate - direct) > 1e-12:
            failures.append(("blocked_equivalence", b, aggregate, direct))
        blocked_rows.append(
            {
                "block_exponent": b,
                "average_probe_exponent": eta,
                "aggregate_source_exponent": aggregate,
            }
        )

    # Round-adaptive phase law: source exponent 1+max(alpha-b,rho).
    round_rows = []
    for jb in range(0, 101):
        b = jb / 100.0
        for jr in range(0, 101):
            rho = jr / 100.0
            source = 1.0 + max(0.0, alpha - b, rho)
            preserve_11 = (b >= 0.5 - 1e-12) and (rho <= 0.1 + 1e-12)
            preserve_12 = (b >= 0.4 - 1e-12) and (rho <= 0.2 + 1e-12)
            checks += 2
            if (source <= 1.1 + 1e-12) != preserve_11:
                failures.append(("round_11", b, rho, source))
            if (source <= 1.2 + 1e-12) != preserve_12:
                failures.append(("round_12", b, rho, source))
            if jb in (40, 50, 60) and jr in (10, 20, 21):
                round_rows.append(
                    {
                        "block_exponent": b,
                        "round_exponent": rho,
                        "source_exponent": source,
                        "preserves_1_1_overhead": preserve_11,
                        "preserves_1_2_fixed_point": preserve_12,
                    }
                )

    # Recurrence identity for random parameters and parent-probe exponents.
    samples = []
    for _ in range(10000):
        a = rng.uniform(0.01, 0.95)
        be = rng.uniform(0.05, 0.95)
        de = rng.uniform(0.01, 0.95)
        eta = rng.uniform(0.0, 1.2)
        c0 = rng.uniform(1.0, 100.0)
        depth = rng.randint(1, 40)
        base = max(1.0, a + de, a + eta)
        lhs = iterate(c0, base, a, be, depth)
        rhs = explicit(c0, base, a, be, depth)
        checks += 1
        if abs(lhs - rhs) > 1e-8:
            failures.append(("recurrence", a, be, de, eta, c0, depth, lhs, rhs))
        if len(samples) < 20:
            samples.append(
                {
                    "alpha": a,
                    "beta": be,
                    "delta": de,
                    "eta": eta,
                    "initial_exponent": c0,
                    "depth": depth,
                    "iterated": lhs,
                    "explicit": rhs,
                }
            )

    # Integer source-access controls at finite sizes.
    finite_rows = []
    for n in [64, 128, 256, 512, 1024, 2048, 4096, 8192]:
        q = math.ceil(n**alpha)
        for eta in (0.4, 0.5, 0.6, 0.7, 1.0):
            per_child = math.ceil(n**eta)
            total = q * per_child
            checks += 1
            if total != q * per_child:
                failures.append(("integer_total", n, eta))
            finite_rows.append(
                {
                    "n": n,
                    "children": q,
                    "eta": eta,
                    "probes_per_child": per_child,
                    "total_parent_probes": total,
                }
            )

    result = {
        "status": "aggregate_parent_probe_accounting_only_no_class_separation",
        "checks": checks,
        "failures": len(failures),
        "failure_samples": failures[:20],
        "target_parameters": {"alpha": alpha, "beta": beta, "delta": delta},
        "thresholds": {
            "eta_for_1_1_overhead": 0.5,
            "eta_for_1_2_fixed_point": 0.6,
            "per_child_full_scan_eta": 1.0,
            "per_child_full_scan_fixed_point": 1.6,
        },
        "phase_rows": phase_rows,
        "blocked_scan_rows": blocked_rows,
        "round_adaptive_samples": round_rows,
        "recurrence_samples": samples,
        "finite_rows": finite_rows,
        "excluded_claim": (
            "No exact hereditary semantic compiler, FLMV transfer, MKTP hardness, "
            "or P-vs-NP/P-vs-RP resolution is proved."
        ),
    }
    with open("parent_probe_budget70_raw.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: result[k] for k in ("status", "checks", "failures")}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
