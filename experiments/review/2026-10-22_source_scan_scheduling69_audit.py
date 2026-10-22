#!/usr/bin/env python3
"""Finite accounting audit for SOURCE-SCAN-SCHEDULING69.

This checks explicit scheduling identities only.  It does not construct an
all-input ARC transformer or prove a complexity-class separation.
"""

from __future__ import annotations

import json
import math
import random


ALPHA = 0.6
BETA = 0.5
DELTA = 0.5


def iterate(c: float, base: float, alpha: float, beta: float, k: int) -> float:
    for _ in range(k):
        c = max(base, alpha + beta * c)
    return c


def explicit_levels(c0: float, base: float, alpha: float, beta: float, k: int) -> float:
    terms = [alpha * (1.0 - beta**k) / (1.0 - beta) + c0 * beta**k]
    for i in range(k):
        prefix = alpha * (1.0 - beta**i) / (1.0 - beta)
        terms.append(prefix + base * beta**i)
    return max(terms)


def main() -> None:
    rng = random.Random(691748)
    failures = []
    checks = 0
    scale_rows = []

    # Exact finite scheduling controls.
    for n in [64, 128, 256, 512, 1024, 2048, 4096]:
        q = max(1, math.ceil(n**ALPHA))
        d = max(1, math.ceil(n**DELTA))
        child_local_reads = q * n
        retained_descriptor_bits = q * d
        streamed_source_reads = n
        streamed_descriptor_work = q * d
        streamed_peak = d

        assertions = [
            child_local_reads == q * n,
            retained_descriptor_bits == q * d,
            streamed_source_reads == n,
            streamed_descriptor_work == q * d,
            streamed_peak == d,
            streamed_source_reads < child_local_reads,
            streamed_peak < retained_descriptor_bits,
        ]
        for ok in assertions:
            checks += 1
            if not ok:
                failures.append(("scale", n, q, d))
        scale_rows.append(
            {
                "n": n,
                "q": q,
                "descriptor_bits": d,
                "child_local_source_reads": child_local_reads,
                "retain_all_descriptor_bits": retained_descriptor_bits,
                "streamed_source_reads": streamed_source_reads,
                "streamed_descriptor_work": streamed_descriptor_work,
                "streamed_peak_descriptor_bits": streamed_peak,
            }
        )

    # Target exponent calculations.
    child_local_base = ALPHA + 1.0
    retain_all_space = ALPHA + DELTA
    shared_stream_base = max(1.0, ALPHA + DELTA)
    target = {
        "child_local_base_time": child_local_base,
        "retain_all_peak_space": retain_all_space,
        "shared_stream_base_time": shared_stream_base,
        "shared_stream_peak_space": DELTA,
        "shared_stream_time_fixed_point": max(
            shared_stream_base, ALPHA / (1.0 - BETA)
        ),
        "child_local_time_fixed_point": max(
            child_local_base, ALPHA / (1.0 - BETA)
        ),
    }
    expected = [1.6, 1.1, 1.1, 0.5, 1.2, 1.6]
    for got, want in zip(target.values(), expected):
        checks += 1
        if abs(got - want) > 1e-12:
            failures.append(("target", got, want))

    # Recurrence versus explicit recursion-tree levels for the viable shared
    # stream schedule and the hostile per-child-rescan schedule.
    recurrence_rows = []
    for _ in range(5000):
        alpha = rng.uniform(0.01, 0.95)
        beta = rng.uniform(0.05, 0.95)
        delta = rng.uniform(0.01, 0.95)
        c0 = rng.uniform(1.0, 20.0)
        k = rng.randint(1, 30)
        for mode, base in (
            ("shared_stream", max(1.0, alpha + delta)),
            ("child_local_rescan", alpha + 1.0),
        ):
            a = iterate(c0, base, alpha, beta, k)
            b = explicit_levels(c0, base, alpha, beta, k)
            checks += 1
            if abs(a - b) > 1e-9:
                failures.append(("recurrence", mode, alpha, beta, delta, c0, k, a, b))
        if len(recurrence_rows) < 20:
            recurrence_rows.append(
                {
                    "alpha": alpha,
                    "beta": beta,
                    "delta": delta,
                    "c0": c0,
                    "depth": k,
                    "shared_stream": iterate(c0, max(1.0, alpha + delta), alpha, beta, k),
                    "child_local_rescan": iterate(c0, alpha + 1.0, alpha, beta, k),
                }
            )

    # Fixed target, broad initial exponents/depths.
    target_rows = []
    for j in range(10, 1001):
        c0 = j / 10.0
        for k in range(1, 31):
            viable = iterate(c0, shared_stream_base, ALPHA, BETA, k)
            viable_explicit = explicit_levels(c0, shared_stream_base, ALPHA, BETA, k)
            hostile = iterate(c0, child_local_base, ALPHA, BETA, k)
            hostile_explicit = explicit_levels(c0, child_local_base, ALPHA, BETA, k)
            for got, want in ((viable, viable_explicit), (hostile, hostile_explicit)):
                checks += 1
                if abs(got - want) > 1e-9:
                    failures.append(("target_recurrence", c0, k, got, want))
        if j % 100 == 0:
            target_rows.append(
                {
                    "c0": c0,
                    "depth_30_shared_stream": iterate(c0, shared_stream_base, ALPHA, BETA, 30),
                    "depth_30_child_local_rescan": iterate(c0, child_local_base, ALPHA, BETA, 30),
                }
            )

    result = {
        "status": "restricted_scheduling_identity_only_no_class_separation",
        "checks": checks,
        "failures": len(failures),
        "failure_samples": failures[:20],
        "target_parameters": {
            "alpha": ALPHA,
            "beta": BETA,
            "delta": DELTA,
        },
        "target_exponents": target,
        "scale_rows": scale_rows,
        "recurrence_samples": recurrence_rows,
        "target_depth_samples": target_rows,
        "excluded_claim": (
            "No streamable exact ARC compiler, FLMV contradiction, MKTP hardness, "
            "or P-vs-NP/P-vs-RP result is proved."
        ),
    }
    with open("source_scan_scheduling69_raw.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: result[k] for k in ("status", "checks", "failures")}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
