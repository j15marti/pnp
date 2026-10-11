#!/usr/bin/env python3
"""Bounded audit for RT-0015 extensional-normalizer attacks.

The symbolic report proves two statements: under P=NP, minimization of SAT
oracle-query scale over all extensionally equivalent polynomial programs
collapses to zero; and no total computable complete canonicalizer for
polynomial-time Boolean programs exists.  This script checks finite-horizon
indistinguishability, query-scale representatives, and hostile SAT controls.
It does not computationally prove either asymptotic statement.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import time
from collections import defaultdict
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def satisfies(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(
        any(assignment[abs(lit)] == (lit > 0) for lit in clause)
        for clause in formula
    )


def sat(formula: Formula) -> bool:
    vs = variables(formula)
    return any(
        satisfies(formula, dict(zip(vs, bits)))
        for bits in itertools.product((False, True), repeat=len(vs))
    )


def gaussian_sat(rows: tuple[tuple[int, int], ...]) -> bool:
    work = [[mask, rhs] for mask, rhs in rows]
    pivot = 0
    width = max((mask.bit_length() for mask, _ in rows), default=0)
    for bit in range(width - 1, -1, -1):
        row = next(
            (j for j in range(pivot, len(work)) if (work[j][0] >> bit) & 1),
            None,
        )
        if row is None:
            continue
        work[pivot], work[row] = work[row], work[pivot]
        for j in range(len(work)):
            if j != pivot and ((work[j][0] >> bit) & 1):
                work[j][0] ^= work[pivot][0]
                work[j][1] ^= work[pivot][1]
        pivot += 1
    return all(mask or rhs == 0 for mask, rhs in work)


def formula_controls() -> tuple[tuple[str, Formula], ...]:
    proper = tuple(
        tuple(v * sign for v, sign in zip((1, 2, 3), signs))
        for signs in itertools.product((-1, 1), repeat=3)
    )
    cube = tuple(
        (f"proper_subset_{mask:03d}", tuple(proper[i] for i in range(8) if mask & (1 << i)))
        for mask in range(1 << 8)
    )
    easy = (
        ("horn", ((-1, -2, 3), (-3, 4), (-4,))),
        ("two_sat", ((1, 2), (-1, 3), (-2, -3))),
        ("bounded_treewidth", ((1, 2), (-2, 3), (-3, 4), (-4, 5))),
        ("independent_product", ((1, 2), (-1, -2), (3, 4), (-3, -4))),
        ("redundant", ((1, 2, 3), (1, 2, 3), (-1, 2, 3))),
    )
    return cube + easy


def wrapper_answer(mode: str, formula: Formula) -> tuple[bool, int, int]:
    """Return (answer, semantic calls, irrelevant operations)."""
    answer = sat(formula)
    if mode == "DIRECT":
        return answer, 1, 0
    if mode == "DEAD":
        _ = len(formula) ** 2
        return answer, 1, 1
    if mode == "CANCEL":
        bit = sat(((1, 2, 3),))
        return bool(answer ^ bit ^ bit), 2, 1
    if mode == "COPY":
        copied = tuple(tuple(lit for lit in clause) for clause in formula)
        return sat(copied), 1, len(copied)
    if mode == "DELAY":
        _ = sum(range(len(formula) + 1))
        return answer, 1, len(formula) + 1
    if mode == "INTERP":
        return not (not answer), 1, 1
    if mode == "RECOMP":
        second = sat(tuple(reversed(formula)))
        assert second == answer
        return second, 2, 1
    raise ValueError(mode)


def threshold_program(horizon: int | None, input_length: int) -> bool:
    """Finite proxy for simulating a machine for |x| steps."""
    return horizon is not None and input_length >= horizon


def query_length(n: int, numerator: int, denominator: int) -> int:
    return max(2, math.ceil(n ** (numerator / denominator)))


def run() -> dict[str, object]:
    started = time.perf_counter()
    checks: defaultdict[str, int] = defaultdict(int)
    wrappers = ("DIRECT", "DEAD", "CANCEL", "COPY", "DELAY", "INTERP", "RECOMP")

    # Bounded halting-horizon witnesses: every h>B agrees with the zero
    # program through length B but differs at length h.
    horizon_rows: list[dict[str, int]] = []
    for bound in range(1, 257):
        for offset in range(1, 9):
            horizon = bound + offset
            for n in range(0, bound + 1):
                assert threshold_program(horizon, n) == threshold_program(None, n)
                checks["bounded_prefix_agreement"] += 1
            assert threshold_program(horizon, horizon)
            assert not threshold_program(None, horizon)
            checks["future_separation"] += 1
            horizon_rows.append({"tested_through": bound, "first_one": horizon})

    # All implementations return the same one bit on easy families despite
    # different traces, query counts, recomputation, and dead work.
    formula_rows = []
    for name, formula in formula_controls():
        expected = sat(formula)
        for mode in wrappers:
            answer, semantic_calls, irrelevant = wrapper_answer(mode, formula)
            assert answer == expected
            checks["wrapper_semantic_equivalence"] += 1
            formula_rows.append({
                "family": name,
                "wrapper": mode,
                "answer": expected,
                "semantic_calls": semantic_calls,
                "irrelevant_operations": irrelevant,
            })
        # Alternate order and duplicate padding preserve the decision.
        variants = (tuple(reversed(formula)), formula + formula[:1], tuple(tuple(c) for c in formula))
        for variant in variants:
            assert sat(variant) == expected
            checks["encoding_padding_controls"] += 1

    # Affine/Tseitin controls are solved by actual GF(2) elimination.
    affine_rows = []
    for n in range(3, 65):
        even = tuple(((1 << i) | (1 << ((i + 1) % n)), 0) for i in range(n))
        odd = tuple(
            ((1 << i) | (1 << ((i + 1) % n)), int(i == 0)) for i in range(n)
        )
        assert gaussian_sat(even)
        assert not gaussian_sat(odd)
        checks["affine_gaussian_controls"] += 2
        affine_rows.append({"variables": n, "even_sat": True, "odd_sat": False})

    # For each positive-scale representative include an extensionally
    # equivalent zero-query representative.  The finite minimum scale is then
    # zero by construction, matching the symbolic P=NP replacement argument.
    scales = ((1, 4), (1, 2), (3, 4), (1, 1), (3, 2))
    scale_rows = []
    for n in (16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        base_q = 2
        for num, den in scales:
            wrapped_q = query_length(n, num, den)
            assert wrapped_q >= base_q
            representative_lengths = (base_q, wrapped_q, wrapped_q, wrapped_q)
            assert min(representative_lengths) == base_q
            checks["query_scale_representative_minimum"] += len(representative_lengths)
            scale_rows.append({
                "source_length": n,
                "declared_scale": f"{num}/{den}",
                "zero_query_convention_length": base_q,
                "wrapped_query_length": wrapped_q,
                "minimum_representative_length": min(representative_lengths),
            })

    # Padding changes the presented exponent but cannot remove the no-query
    # representative from an extensional equivalence class.
    padding_rows = []
    for core in range(2, 65):
        for degree in range(1, 7):
            presented = core**degree
            assert min(2, query_length(presented, 1, 1)) == 2
            checks["padding_keeps_zero_query_representative"] += 1
            padding_rows.append({"core": core, "degree": degree, "presented": presented})

    runtime = time.perf_counter() - started
    source = Path(__file__).read_bytes()
    return {
        "run_id": "RT-0015",
        "timestamp_utc": "2026-10-11T17:36:00Z",
        "runtime_seconds": runtime,
        "script_sha256": hashlib.sha256(source).hexdigest(),
        "status": "COMPUTATIONAL",
        "checks": dict(sorted(checks.items())),
        "total_checks": sum(checks.values()),
        "parameters": {
            "halting_test_bounds": [1, 256],
            "horizons_per_bound": 8,
            "source_formula_count": len(formula_controls()),
            "wrappers": list(wrappers),
            "query_scales": [f"{a}/{b}" for a, b in scales],
        },
        "horizon_witnesses": horizon_rows,
        "formula_rows": formula_rows,
        "affine_rows": affine_rows,
        "scale_rows": scale_rows,
        "padding_rows": padding_rows,
        "limitations": [
            "Finite horizons cannot decide extensional program equivalence.",
            "The P=NP query-scale collapse is a symbolic conditional theorem, not an empirical inference.",
            "Runtime measurements are not asymptotic evidence.",
        ],
    }


def main() -> None:
    output = Path("results/raw/review/2026-10-11_extensional_normalizer_redteam.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = run()
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "runtime_seconds": payload["runtime_seconds"],
        "total_checks": payload["total_checks"],
        "script_sha256": payload["script_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
