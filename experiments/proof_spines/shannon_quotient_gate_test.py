#!/usr/bin/env python3
"""Bounded checks for the Shannon-then-quotient wrapper candidate.

The script tests the exact family F_m = AND_i (x_i OR y_i).  Restricting
designated x variables exposes an OR of residual CNFs.  On this family the
residuals are pairwise distinct both syntactically and as Boolean functions,
so exact equality quotienting does not reduce the frontier.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import time
from pathlib import Path


SEED = 20261007
BUDGET_SECONDS = 25.0


def residual_signature(m: int, h: int, bits: tuple[int, ...]):
    """Canonical CNF signature after assigning x_0,...,x_{h-1}."""
    clauses: list[tuple[str, ...]] = []
    for i in range(m):
        if i < h:
            if bits[i] == 0:
                clauses.append((f"y{i}",))
        else:
            clauses.append((f"x{i}", f"y{i}"))
    return tuple(clauses)


def truth_signature(m: int, h: int, bits: tuple[int, ...]) -> tuple[int, ...]:
    """Truth table over the remaining x variables and all y variables."""
    variables = [f"x{i}" for i in range(h, m)] + [f"y{i}" for i in range(m)]
    residual = residual_signature(m, h, bits)
    table = []
    for values in itertools.product((0, 1), repeat=len(variables)):
        assignment = dict(zip(variables, values))
        table.append(int(all(any(assignment[v] for v in clause) for clause in residual)))
    return tuple(table)


def encoded_length(m: int) -> int:
    """A fixed self-delimiting token model, Theta(m log m) bits."""
    index_bits = max(1, math.ceil(math.log2(2 * m + 1)))
    return m * (2 * index_bits + 5)


def run() -> dict:
    started = time.monotonic()
    rng = random.Random(SEED)
    checks = 0
    small_cases = []

    for m in range(1, 7):
        for h in range(m + 1):
            assignments = list(itertools.product((0, 1), repeat=h))
            syntactic = {residual_signature(m, h, a) for a in assignments}
            assert len(syntactic) == 2**h
            checks += 1
            if m <= 4:
                semantic = {truth_signature(m, h, a) for a in assignments}
                assert len(semantic) == 2**h
                checks += 1
            small_cases.append(
                {
                    "m": m,
                    "h": h,
                    "frontier": 2**h,
                    "syntactic_classes": len(syntactic),
                }
            )
            assert time.monotonic() - started < BUDGET_SECONDS

    asymptotic_samples = []
    for m in (16, 64, 256, 1024, 4096, 16384):
        M = encoded_length(m)
        h_poly = int(math.log2(M))
        residual_lower = encoded_length(max(1, m - h_poly))
        ratio = residual_lower / M
        asymptotic_samples.append(
            {
                "m": m,
                "encoded_M": M,
                "h_floor_log2_M": h_poly,
                "frontier_le_M": 2**h_poly <= M,
                "residual_length_lower": residual_lower,
                "residual_over_parent": ratio,
                "residual_gt_M_pow_0_9": residual_lower > M**0.9,
                "half_restriction_frontier_over_M_squared_log2":
                    (m // 2) - 2 * math.log2(M),
            }
        )
        checks += 3

    # Seeded spot checks exercise arbitrary frontier assignments.
    for _ in range(64):
        m = rng.randint(2, 12)
        h = rng.randint(0, m)
        a = tuple(rng.randint(0, 1) for _ in range(h))
        sig = residual_signature(m, h, a)
        expected_units = sum(bit == 0 for bit in a)
        assert sum(len(c) == 1 for c in sig) == expected_units
        assert sum(len(c) == 2 for c in sig) == m - h
        checks += 2

    M = encoded_length(4096)
    padding_control = {
        "original_M": M,
        "padded_length_M_squared": M * M,
        "original_source_exponent_in_padded_measure": 0.5,
        "interpretation": (
            "The apparent square-root child retains the original source unless a "
            "standalone ordinary-SAT encoding and charged decoder are supplied."
        ),
    }
    current_scale_control = {
        "canonicalizer_calls_A_on_parent": True,
        "charged_local_exponent": "at least K",
        "interpretation": "A current-scale semantic query preserves the unknown exponent K.",
    }
    oracle_control = {
        "sat_answer_quotient_classes": 1,
        "interpretation": (
            "Collapsing by the SAT answer uses the answer being computed; treating it as "
            "free changes the model to an oracle model."
        ),
    }

    elapsed = time.monotonic() - started
    assert elapsed < BUDGET_SECONDS
    return {
        "claim": "SHANNON-QUOTIENT-GATE1",
        "status": "COMPUTATIONAL support for an exact analytic obstruction",
        "seed": SEED,
        "budget_seconds": BUDGET_SECONDS,
        "elapsed_seconds": elapsed,
        "checks": checks,
        "small_cases": small_cases,
        "asymptotic_samples": asymptotic_samples,
        "padding_control": padding_control,
        "current_scale_call_control": current_scale_control,
        "oracle_replacement_control": oracle_control,
        "scope": (
            "Finite checks only. The theorem concerns Shannon restriction followed by "
            "exact equality quotienting in the ordinary residual-CNF representation; "
            "it is not a lower bound against arbitrary SAT algorithms or representations."
        ),
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
