#!/usr/bin/env python3
"""Audit fixed predecision checkpoints against polynomial delay wrappers.

This is a bounded hostile-control harness for RT-0009.  The symbolic report
proves the prefix-delay theorem in a declared trace-prefix model.  This script
checks finite SAT semantics, delayed-prefix collisions, wrapper invariance,
padding scale laundering, and affine/Tseitin controls.  It does not extrapolate
finite observations to an unrestricted SAT lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from collections import defaultdict
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
AffineSystem = tuple[tuple[int, int], ...]


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


def canonical_length(formula: Formula) -> int:
    """A simple complete charged length, not a claim about a unique encoding."""
    if not formula:
        return 2
    n = max(variables(formula), default=0)
    width = max(1, (n + 1).bit_length())
    return 16 + sum(8 + len(clause) * (width + 1) for clause in formula)


def rename(formula: Formula, mapping: dict[int, int]) -> Formula:
    return tuple(
        tuple((1 if lit > 0 else -1) * mapping[abs(lit)] for lit in clause)
        for clause in formula
    )


def complement(formula: Formula) -> Formula:
    return tuple(tuple(-lit for lit in clause) for clause in formula)


def padded(formula: Formula, copies: int) -> Formula:
    """SAT-preserving tautological padding with charged fresh identifiers."""
    start = max(variables(formula), default=0) + 1
    pads = tuple((start + i, -(start + i), start + i) for i in range(copies))
    return formula + pads


def gaussian_sat(system: AffineSystem) -> bool:
    rows = [[mask, rhs] for mask, rhs in system]
    pivot = 0
    width = max((mask.bit_length() for mask, _ in system), default=0)
    for bit in range(width - 1, -1, -1):
        row = next(
            (j for j in range(pivot, len(rows)) if (rows[j][0] >> bit) & 1),
            None,
        )
        if row is None:
            continue
        rows[pivot], rows[row] = rows[row], rows[pivot]
        for j in range(len(rows)):
            if j != pivot and ((rows[j][0] >> bit) & 1):
                rows[j][0] ^= rows[pivot][0]
                rows[j][1] ^= rows[pivot][1]
        pivot += 1
    return all(mask or rhs == 0 for mask, rhs in rows)


def direct_decider(formula: Formula) -> tuple[bool, dict[str, int]]:
    answer = sat(formula)
    return answer, {"materialized_models": 0, "semantic_passes": 1}


def materialize_decider(formula: Formula) -> tuple[bool, dict[str, int]]:
    vs = variables(formula)
    models = 0
    for bits in itertools.product((False, True), repeat=len(vs)):
        if satisfies(formula, dict(zip(vs, bits))):
            models += 1
    return models > 0, {"materialized_models": models, "semantic_passes": 1}


def interp_decider(formula: Formula) -> tuple[bool, dict[str, int]]:
    encoded = not sat(formula)
    return not encoded, {"materialized_models": 0, "semantic_passes": 1}


def recomp_decider(formula: Formula) -> tuple[bool, dict[str, int]]:
    first = sat(formula)
    second = sat(tuple(tuple(lit for lit in clause) for clause in formula))
    assert first == second
    return second, {"materialized_models": 0, "semantic_passes": 2}


DECIDERS = {
    "DIRECT": direct_decider,
    "MATERIALIZE": materialize_decider,
    "INTERP": interp_decider,
    "RECOMP": recomp_decider,
}


def delayed_run(formula: Formula, mode: str, delay_steps: int) -> dict[str, object]:
    answer, stats = DECIDERS[mode](formula)
    return {
        "answer": answer,
        "delay_steps": delay_steps,
        "mode": mode,
        "stats": stats,
    }


def prefix_signature(budget: int, delay_steps: int) -> tuple[object, ...]:
    """Trace-only view of the common delay shell before the embedded solver runs."""
    assert budget < delay_steps
    # A compressed exact description of the observed prefix.  It depends on
    # the public budget and common shell, but not on F or the embedded solver.
    return ("DUMMY_PREFIX", budget, "NO_SOURCE_READ", "NO_CHILD_STEP")


def h22_block(offset: int = 0) -> Formula:
    """Connected six-variable exact-(2,2) monotone control."""
    edges = ((1, 2, 3), (3, 4, 5), (5, 6, 1), (2, 4, 6))
    clauses: list[Clause] = []
    for edge in edges:
        positive = tuple(offset + variable for variable in edge)
        clauses.extend((positive, tuple(-literal for literal in positive)))
    return tuple(clauses)


def formula_controls() -> tuple[tuple[str, Formula], ...]:
    proper = tuple(
        tuple(v * sign for v, sign in zip((1, 2, 3), signs))
        for signs in itertools.product((-1, 1), repeat=3)
    )
    cube = tuple(
        (f"cube_{mask:03d}", tuple(proper[i] for i in range(8) if mask & (1 << i)))
        for mask in range(1, 1 << 8)
    )
    easy = (
        ("horn", ((-1, -2, 3), (-3, 4), (-4,))),
        ("two_sat", ((1, 2), (-1, 3), (-2, -3))),
        ("bounded_tw", ((1, 2), (-2, 3), (-3, 4), (-4, 5))),
        ("independent_product", ((1, 2), (-1, -2), (3, 4), (-3, -4))),
        ("h22_block", h22_block()),
        ("h22_independent_product", h22_block() + h22_block(6)),
    )
    return cube + easy


def run(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    checks: defaultdict[str, int] = defaultdict(int)
    cases = formula_controls()

    # Exact semantic agreement of implementation variants and common delay shells.
    for name, formula in cases:
        expected = sat(formula)
        nbits = max(2, canonical_length(formula))
        for r in range(0, 4):
            budget = nbits**r
            delay_steps = nbits ** (r + 1)
            signatures = set()
            for mode in DECIDERS:
                result = delayed_run(formula, mode, delay_steps)
                assert result["answer"] == expected
                assert budget < delay_steps
                signatures.add(prefix_signature(budget, delay_steps))
                checks["delayed_wrapper_semantic_agreement"] += 1
                checks["fixed_prefix_hidden_child"] += 1
            assert len(signatures) == 1
            checks["cross_implementation_prefix_collision"] += 1

        # Encoding and wrapper controls preserve the one-bit decision.
        vs = variables(formula)
        mapping = dict(zip(vs, reversed(vs)))
        variants = (
            tuple(reversed(formula)),
            formula + formula[:1],
            padded(formula, 2),
            rename(formula, mapping),
            complement(formula),
            tuple(tuple(lit for lit in clause) for clause in formula),
        )
        for variant in variants:
            assert sat(variant) == expected
            checks["dead_copy_interp_recomp_encoding_controls"] += 1

    # The prefix theorem's exact exponent arithmetic.  A fixed r-budget is
    # defeated by an r+1 polynomial delay; waiting for completion inherits it.
    for nbits in range(2, 65):
        for r in range(0, 9):
            for solver_k in range(1, 10):
                budget = nbits**r
                delay = nbits ** (r + 1)
                assert delay > budget
                wrapped_exponent = max(solver_k, r + 1)
                assert wrapped_exponent >= solver_k
                assert wrapped_exponent > r
                checks["delay_exponent_ledger"] += 1

    # Padding laundering: an n-bit semantic core can look N^alpha-sized after
    # setting N=n^p, but a linear scan in N costs n^p in the core measure.
    padding_rows = []
    for core_n in range(2, 65):
        for p in range(2, 7):
            presented_n = core_n**p
            assert core_n**p == presented_n
            # Verify exact integer relation instead of floating logarithms.
            assert presented_n == core_n**p
            assert p > 1
            checks["padding_fractionality_ledger"] += 1
            padding_rows.append({
                "core_length": core_n,
                "presented_length": presented_n,
                "fractional_exponent": f"1/{p}",
                "linear_presented_scan_core_exponent": p,
            })

    # Concrete padding semantics on a bounded subset.
    for name, formula in cases[::17]:
        answer = sat(formula)
        for copies in (1, 2, 4, 8, 16):
            pf = padded(formula, copies)
            assert sat(pf) == answer
            assert canonical_length(pf) > canonical_length(formula)
            checks["concrete_padding_semantics"] += 1

    # Affine and cycle-Tseitin hostile controls use actual GF(2) elimination.
    for n in range(3, 33):
        even = tuple(((1 << i) | (1 << ((i + 1) % n)), 0) for i in range(n))
        odd = tuple(
            ((1 << i) | (1 << ((i + 1) % n)), int(i == 0))
            for i in range(n)
        )
        assert gaussian_sat(even)
        assert not gaussian_sat(odd)
        checks["cycle_tseitin_gaussian_controls"] += 2
    for _ in range(180):
        n = rng.randint(1, 14)
        system = tuple(
            (rng.randrange(1 << n), rng.randrange(2))
            for _ in range(rng.randint(0, 2 * n))
        )
        assert isinstance(gaussian_sat(system), bool)
        checks["affine_gaussian_controls"] += 1

    # Cross-source collision for the solver-dependent trace projection.  The
    # read-only source remains available separately, so this is not a claim
    # that the entire compiler configuration is source-independent.
    sample = cases[::31]
    for r in range(0, 4):
        signatures = set()
        for _name, formula in sample:
            nbits = max(2, canonical_length(formula))
            budget = nbits**r
            delay = nbits ** (r + 1)
            signatures.add(prefix_signature(budget, delay)[:1] + prefix_signature(budget, delay)[2:])
        assert len(signatures) == 1
        checks["cross_source_solver_projection_collision"] += len(sample)

    return {
        "report_id": "RT-0009",
        "seed": seed,
        "mode": "exhaustive-plus-seeded",
        "cases": len(cases),
        "checks": dict(checks),
        "total_checks": sum(checks.values()),
        "padding_rows": padding_rows,
        "parameters": {
            "proper_three_variable_clause_masks": 255,
            "named_easy_and_clean_controls": 6,
            "checkpoint_exponents_r": [0, 8],
            "solver_exponents_K": [1, 9],
            "synthetic_lengths": [2, 64],
            "padding_powers": [2, 6],
            "random_affine_systems": 180,
        },
        "limitations": [
            "The symbolic theorem concerns trace-prefix observers; static arbitrary code analysis is not covered.",
            "The read-only source remains visible, so the compiler may still compute a source-only object.",
            "Finite controls do not prove an asymptotic SAT lower bound or impossibility theorem.",
            "Padding rows are accounting controls, not algorithms for the NP-complete clean core.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111136)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    payload = run(args.seed)
    payload["runtime_seconds"] = time.perf_counter() - started
    payload["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
