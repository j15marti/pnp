#!/usr/bin/env python3
"""Finite guards for BLACKBOX-POSITIVE-SCALE-GATE1.

The asymptotic theorem is a symbolic delay-wrapper argument.  This script
checks its exact rational arithmetic, transcript invariance under several
extensionally equal implementations, and small hostile SAT-representation
controls.  Finite timings are not used as asymptotic evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path
from typing import Callable, Iterable


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def eval_formula(formula: Formula, assignment: tuple[int, ...]) -> int:
    for clause in formula:
        if not any((lit > 0) == bool(assignment[abs(lit) - 1]) for lit in clause):
            return 0
    return 1


def sat_bit(formula: Formula) -> int:
    variables = max((abs(lit) for clause in formula for lit in clause), default=0)
    return int(any(eval_formula(formula, a) for a in itertools.product((0, 1), repeat=variables)))


def canonical(formula: Iterable[Iterable[int]]) -> Formula:
    return tuple(tuple(int(x) for x in clause) for clause in formula)


def representations() -> dict[str, Formula]:
    """Small satisfiable/unsatisfiable controls named by structural route."""
    return {
        "2SAT": canonical(((1, 2), (-1, 2), (1, -2))),
        "HORN": canonical(((-1, 2), (-2, 3), (1,), (-3,))),
        "AFFINE_TSEITIN": canonical(((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))),
        "BOUNDED_TREEWIDTH": canonical(((1, 2), (-2, 3), (-3, 4), (-4,))),
        "INDEPENDENT_PRODUCT": canonical(((1,), (2,), (-3, 4), (3, -4))),
        "PADDING": canonical(((1,), (2, -2, 2), (3, -3, 3), (4, -4, 4))),
        "REDUNDANT_CLAUSES": canonical(((1, 2), (1, 2), (-1,), (-2,))),
        "ALTERNATE_ENCODING": canonical(((3, -1), (-3, 2), (1,), (-2,))),
    }


def wrapper_set(base: Callable[[Formula], int]) -> dict[str, Callable[[Formula], int]]:
    def copy(formula: Formula) -> int:
        return int(base(tuple(tuple(c) for c in formula)))

    def delay(formula: Formula) -> int:
        answer = base(formula)
        dummy = 0
        for i, clause in enumerate(formula):
            dummy ^= (i + len(clause)) & 1
        return answer ^ dummy ^ dummy

    def interp(formula: Formula) -> int:
        return int(f"answer={base(formula)}".split("=")[1])

    def recomp(formula: Formula) -> int:
        return sum((base(formula), 0)) & 1

    return {"DIRECT": base, "COPY": copy, "DELAY": delay, "INTERP": interp, "RECOMP": recomp}


def adaptive_transcript(seed_formula: Formula, oracle: Callable[[Formula], int]) -> tuple[int, tuple[tuple[Formula, int], ...]]:
    """Answer-dependent derived queries; exact wrappers must induce one transcript."""
    transcript: list[tuple[Formula, int]] = []
    current = seed_formula
    accumulator = 0
    for step in range(4):
        answer = oracle(current)
        transcript.append((current, answer))
        accumulator ^= answer
        if not current:
            continue
        pivot = 1 + (step % max(1, max(abs(x) for c in current for x in c)))
        unit = (pivot if answer else -pivot,)
        current = canonical((*current[1:], unit))
    return accumulator, tuple(transcript)


def transcript_audit() -> dict[str, object]:
    wrappers = wrapper_set(sat_bit)
    failures: list[dict[str, object]] = []
    checks = 0
    per_family: dict[str, object] = {}
    for name, formula in representations().items():
        reference = adaptive_transcript(formula, wrappers["DIRECT"])
        family_checks = 0
        for wrapper_name, oracle in wrappers.items():
            observed = adaptive_transcript(formula, oracle)
            checks += 1
            family_checks += 1
            if observed != reference:
                failures.append({"family": name, "wrapper": wrapper_name})
        per_family[name] = {
            "input_sat_bit": sat_bit(formula),
            "clauses": len(formula),
            "transcript_queries": len(reference[1]),
            "wrapper_checks": family_checks,
        }
    return {"families": per_family, "checks": checks, "failures": failures}


def exponent_audit() -> dict[str, object]:
    witnesses = []
    failures = []
    for c_num in range(1, 33):
        c = Fraction(c_num, 4)
        for eps_num in range(1, 17):
            epsilon = Fraction(eps_num, 16)
            d = c // epsilon + 1
            item = {
                "c": str(c),
                "epsilon": str(epsilon),
                "delay_exponent_d": int(d),
                "charged_exponent": str(epsilon * d),
            }
            witnesses.append(item)
            if not epsilon * d > c:
                failures.append(item)

    scale_table = []
    for lambda_num in range(0, 17):
        lam = Fraction(lambda_num, 16)
        for d in (1, 2, 4, 8, 16, 32, 64):
            scale_table.append(
                {
                    "lambda": str(lam),
                    "delay_exponent_d": d,
                    "charged_parent_exponent": str(lam * d),
                    "positive_scale_amplifies": bool(lam > 0 and lam * d > 0),
                }
            )
    return {
        "fixed_exponent_witnesses": len(witnesses),
        "witness_failures": failures,
        "scale_table": scale_table,
        "subpolynomial_boundary": "lambda=0 is not excluded by the delay-exponent multiplication argument",
    }


def randomized_wrapper_audit(seed: int, trials: int) -> dict[str, object]:
    rng = random.Random(seed)
    wrappers = wrapper_set(sat_bit)
    failures = []
    checks = 0
    for trial in range(trials):
        variables = rng.randint(1, 5)
        formula = canonical(
            tuple(
                tuple((1 if rng.getrandbits(1) else -1) * rng.randint(1, variables) for _ in range(rng.randint(1, 3)))
                for _ in range(rng.randint(0, 8))
            )
        )
        reference = adaptive_transcript(formula, wrappers["DIRECT"])
        for wrapper_name, oracle in wrappers.items():
            checks += 1
            if adaptive_transcript(formula, oracle) != reference:
                failures.append({"trial": trial, "wrapper": wrapper_name})
    return {"seed": seed, "trials": trials, "checks": checks, "failures": failures}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111700)
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    result = {
        "experiment": "blackbox_positive_scale_gate_audit",
        "status": "COMPUTATIONAL",
        "exponent": exponent_audit(),
        "hostile_structural_controls": transcript_audit(),
        "randomized_wrapper_controls": randomized_wrapper_audit(args.seed, args.trials),
    }
    result["elapsed_seconds"] = time.perf_counter() - started
    result["pass"] = (
        not result["exponent"]["witness_failures"]
        and not result["hostile_structural_controls"]["failures"]
        and not result["randomized_wrapper_controls"]["failures"]
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
