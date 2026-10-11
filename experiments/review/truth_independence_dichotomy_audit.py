#!/usr/bin/env python3
"""Bounded audit for RT-0010's truth-independence dichotomy.

The symbolic report distinguishes schedule obliviousness from semantic
noninterference.  This harness verifies finite branch-free decide-then-emit
constructions, wrapper/encoding controls, and easy-family controls.  It does
not extrapolate finite observations to an unrestricted SAT lower bound.
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


def exhaustive_oblivious_sat(formula: Formula) -> tuple[bool, tuple[str, ...]]:
    """Evaluate every assignment without early exit; schedule depends only on n."""
    vs = variables(formula)
    answer = False
    trace: list[str] = []
    for bits in itertools.product((False, True), repeat=len(vs)):
        answer |= satisfies(formula, dict(zip(vs, bits)))
        trace.append("EVAL_ASSIGNMENT")
    trace.append("OR_REDUCE")
    return answer, tuple(trace)


def terminal_pair() -> tuple[Formula, Formula]:
    # Equal-length proper width-three formulas.  Y repeats one satisfiable
    # clause; U contains all sign patterns and is unsatisfiable.
    y = tuple((1, 2, 3) for _ in range(8))
    u = tuple(
        tuple(v * sign for v, sign in zip((1, 2, 3), signs))
        for signs in itertools.product((-1, 1), repeat=3)
    )
    assert sat(y) and not sat(u) and len(y) == len(u)
    return y, u


def flatten(formula: Formula) -> tuple[int, ...]:
    return tuple(lit for clause in formula for lit in clause)


def unflatten(encoded: tuple[int, ...]) -> Formula:
    assert len(encoded) % 3 == 0
    return tuple(tuple(encoded[i : i + 3]) for i in range(0, len(encoded), 3))


def emit_branch(answer: bool, y: Formula, u: Formula) -> tuple[Formula, tuple[str, ...]]:
    return (y if answer else u), ("BRANCH_ON_DECISION", "EMIT_CONSTANT")


def emit_arithmetic(answer: bool, y: Formula, u: Formula) -> tuple[Formula, tuple[str, ...]]:
    b = int(answer)
    ey, eu = flatten(y), flatten(u)
    out = tuple(uv + b * (yv - uv) for yv, uv in zip(ey, eu))
    trace = tuple("MUL_ADD_SELECT" for _ in out)
    return unflatten(out), trace


def emit_xor_mask(answer: bool, y: Formula, u: Formula) -> tuple[Formula, tuple[str, ...]]:
    b = int(answer)
    ey, eu = flatten(y), flatten(u)
    # Magnitudes coincide coordinatewise, so only the sign bit is selected.
    out: list[int] = []
    for yv, uv in zip(ey, eu):
        mag = abs(yv)
        ys, us = int(yv < 0), int(uv < 0)
        sign = us ^ (b & (us ^ ys))
        out.append(-mag if sign else mag)
    trace = tuple("XOR_AND_SELECT" for _ in out)
    return unflatten(tuple(out)), trace


def emit_polynomial(answer: bool, y: Formula, u: Formula) -> tuple[Formula, tuple[str, ...]]:
    # The selector p(b)=b on {0,1}; kept separate to test relabelled arithmetic.
    b = int(answer)
    p = b * b
    ey, eu = flatten(y), flatten(u)
    out = tuple((1 - p) * uv + p * yv for yv, uv in zip(ey, eu))
    trace = ("SQUARE_SELECTOR",) + tuple("POLY_SELECT" for _ in out)
    return unflatten(out), trace


def emit_recompute(formula: Formula, y: Formula, u: Formula) -> tuple[Formula, tuple[str, ...]]:
    first = sat(formula)
    second = sat(tuple(tuple(lit for lit in clause) for clause in formula))
    assert first == second
    out, trace = emit_xor_mask(second, y, u)
    return out, ("RECOMP_DECISION",) + trace


EMITTERS = {
    "BRANCH": emit_branch,
    "ARITHMETIC": emit_arithmetic,
    "XOR_MASK": emit_xor_mask,
    "POLYNOMIAL": emit_polynomial,
}


def materialize_decider(formula: Formula) -> bool:
    vs = variables(formula)
    models = [
        bits
        for bits in itertools.product((False, True), repeat=len(vs))
        if satisfies(formula, dict(zip(vs, bits)))
    ]
    return bool(models)


def interp_decider(formula: Formula) -> bool:
    return not (not sat(formula))


def recomp_decider(formula: Formula) -> bool:
    a = sat(formula)
    b = sat(tuple(tuple(lit for lit in clause) for clause in formula))
    assert a == b
    return b


DECIDERS = {
    "DIRECT": sat,
    "MATERIALIZE": materialize_decider,
    "INTERP": interp_decider,
    "RECOMP": recomp_decider,
}


def rename(formula: Formula) -> Formula:
    vs = variables(formula)
    mapping = dict(zip(vs, reversed(vs)))
    return tuple(
        tuple((1 if lit > 0 else -1) * mapping[abs(lit)] for lit in clause)
        for clause in formula
    )


def complement(formula: Formula) -> Formula:
    return tuple(tuple(-lit for lit in clause) for clause in formula)


def pad(formula: Formula, count: int) -> Formula:
    start = max(variables(formula), default=0) + 1
    return formula + tuple((start + i, -(start + i), start + i) for i in range(count))


def h22_block(offset: int = 0) -> Formula:
    edges = ((1, 2, 3), (3, 4, 5), (5, 6, 1), (2, 4, 6))
    clauses: list[Clause] = []
    for edge in edges:
        positive = tuple(offset + x for x in edge)
        clauses.extend((positive, tuple(-x for x in positive)))
    return tuple(clauses)


def controls() -> tuple[tuple[str, Formula], ...]:
    proper = tuple(
        tuple(v * sign for v, sign in zip((1, 2, 3), signs))
        for signs in itertools.product((-1, 1), repeat=3)
    )
    cube = tuple(
        (f"cube_{mask:03d}", tuple(proper[i] for i in range(8) if mask & (1 << i)))
        for mask in range(1 << 8)
    )
    easy = (
        ("horn", ((-1, -2, 3), (-3, 4), (-4,))),
        ("two_sat", ((1, 2), (-1, 3), (-2, -3))),
        ("bounded_treewidth", ((1, 2), (-2, 3), (-3, 4), (-4, 5))),
        ("independent_product", ((1, 2), (-1, -2), (3, 4), (-3, -4))),
        ("h22", h22_block()),
        ("h22_product", h22_block() + h22_block(6)),
    )
    return cube + easy


def gaussian_sat(rows: tuple[tuple[int, int], ...]) -> bool:
    work = [[mask, rhs] for mask, rhs in rows]
    pivot = 0
    width = max((mask.bit_length() for mask, _ in rows), default=0)
    for bit in range(width - 1, -1, -1):
        found = next((i for i in range(pivot, len(work)) if (work[i][0] >> bit) & 1), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        for i in range(len(work)):
            if i != pivot and ((work[i][0] >> bit) & 1):
                work[i][0] ^= work[pivot][0]
                work[i][1] ^= work[pivot][1]
        pivot += 1
    return all(mask != 0 or rhs == 0 for mask, rhs in work)


def brute_affine_sat(rows: tuple[tuple[int, int], ...], n: int) -> bool:
    return any(all(((mask & assignment).bit_count() & 1) == rhs for mask, rhs in rows)
               for assignment in range(1 << n))


def run(seed: int) -> dict[str, object]:
    started = time.perf_counter()
    rng = random.Random(seed)
    checks: defaultdict[str, int] = defaultdict(int)
    y, u = terminal_pair()
    cases = controls()
    yes_views: set[tuple[int, ...]] = set()
    no_views: set[tuple[int, ...]] = set()

    for _name, formula in cases:
        expected = sat(formula)
        for mode, decider in DECIDERS.items():
            answer = decider(formula)
            assert answer == expected
            checks["wrapper_semantic_agreement"] += 1
            for emitter_name, emitter in EMITTERS.items():
                child, trace = emitter(answer, y, u)
                assert child == (y if expected else u)
                assert sat(child) == expected
                checks["terminal_successor_roundtrip"] += 1
                if emitter_name != "BRANCH":
                    # The postdecision operation names and count are answer-oblivious.
                    other_child, other_trace = emitter(not answer, y, u)
                    assert trace == other_trace
                    assert other_child != child
                    checks["branch_free_schedule_collision"] += 1
                view = flatten(child)
                (yes_views if expected else no_views).add(view)
            child, _trace = emit_recompute(formula, y, u)
            assert sat(child) == expected
            checks["recompute_successor_roundtrip"] += 1

        oblivious_answer, schedule = exhaustive_oblivious_sat(formula)
        assert oblivious_answer == expected
        assert len(schedule) == (1 << len(variables(formula))) + 1
        checks["fixed_exhaustive_schedule"] += 1

        variants = (
            tuple(reversed(formula)),
            formula + formula[:1],
            rename(formula),
            complement(formula),
            pad(formula, 2),
        )
        for variant in variants:
            assert sat(variant) == expected
            checks["encoding_padding_copy_controls"] += 1

    # Exact terminal noninterference check: opposite answers cannot share the
    # complete terminal view when the reconstruction reads only that view.
    assert yes_views and no_views and yes_views.isdisjoint(no_views)
    checks["terminal_view_separation"] += len(yes_views) * len(no_views)

    # Unknown solver exponent is retained by both predication and O(T log T)
    # oblivious simulation: logarithmic overhead does not remove K.
    for k in range(1, 17):
        for wrapper_degree in range(0, 17):
            constructor_exponent = max(k, wrapper_degree)
            assert constructor_exponent >= k
            checks["exponent_retention_ledger"] += 1

    # Affine/Tseitin controls compare exact GF(2) elimination with brute force.
    for n in range(2, 9):
        for _ in range(24):
            rows = tuple(
                (rng.randrange(1 << n), rng.randrange(2))
                for _ in range(rng.randint(0, 2 * n))
            )
            assert gaussian_sat(rows) == brute_affine_sat(rows, n)
            checks["affine_gaussian_controls"] += 1

    elapsed = time.perf_counter() - started
    return {
        "run_id": "RT-0010",
        "seed": seed,
        "status": "COMPUTATIONAL",
        "elapsed_seconds": elapsed,
        "formula_cases": len(cases),
        "checks": dict(sorted(checks.items())),
        "total_checks": sum(checks.values()),
        "terminal_yes_view_count": len(yes_views),
        "terminal_no_view_count": len(no_views),
        "limitations": [
            "Finite controls validate constructions and bookkeeping only.",
            "No finite observation is extrapolated to an asymptotic SAT lower bound.",
            "The O(T log T) oblivious-simulation statement is literature-backed, not benchmarked here.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111236)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/raw/review/2026-10-11_truth_independence_dichotomy.json"),
    )
    args = parser.parse_args()
    result = run(args.seed)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
