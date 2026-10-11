#!/usr/bin/env python3
"""Finite audit for adaptive strictly-downward oracle elimination.

The experiment checks exact rational exponent recurrences and finite adaptive
oracle controllers under extensionally identical wrapper implementations.  It
does not infer asymptotics from the finite trials; the asymptotic statement is
proved separately by well-founded recursion.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Callable


BitOracle = Callable[[int, int], int]


@dataclass(frozen=True)
class Controller:
    """A small adaptive oracle controller at one size level.

    Query j is an affine function of the parent index and all earlier answers.
    The final bit is another affine function of the same data.  This is not a
    SAT model; it is an exhaustive finite guard for adaptivity and wrapper
    extensionality.
    """

    level: int
    query_masks: tuple[int, ...]
    query_biases: tuple[int, ...]
    output_mask: int
    output_bias: int

    def run(self, parent: int, oracle: BitOracle) -> tuple[int, tuple[tuple[int, int], ...]]:
        answers: list[int] = []
        transcript: list[tuple[int, int]] = []
        width = 1 << max(0, self.level - 1)
        for mask, bias in zip(self.query_masks, self.query_biases):
            acc = parent ^ bias
            for j, answer in enumerate(answers):
                if (mask >> j) & 1:
                    acc ^= (answer << (j + 1)) | answer
            query = acc % width
            answer = oracle(self.level - 1, query)
            answers.append(answer)
            transcript.append((query, answer))
        value = self.output_bias ^ (parent & 1)
        for j, answer in enumerate(answers):
            if (self.output_mask >> j) & 1:
                value ^= answer
        return value & 1, tuple(transcript)


def wrapper_oracles(table: dict[tuple[int, int], int]) -> dict[str, BitOracle]:
    direct = lambda level, index: table[(level, index)]

    def copy(level: int, index: int) -> int:
        pair = (int(level), int(index))
        return int(table[pair])

    def delay(level: int, index: int) -> int:
        value = table[(level, index)]
        dummy = ((index << 1) ^ level) & 1
        return value ^ dummy ^ dummy

    def interp(level: int, index: int) -> int:
        encoded = f"{level}:{index}:{table[(level, index)]}"
        return int(encoded.rsplit(":", 1)[1])

    def recomp(level: int, index: int) -> int:
        return sum([table[(level, index)]]) & 1

    return {
        "DIRECT": direct,
        "COPY": copy,
        "DELAY": delay,
        "INTERP": interp,
        "RECOMP": recomp,
    }


def exponent_audit() -> dict[str, object]:
    cases = 0
    strict_failures: list[dict[str, str]] = []
    for lam_num in range(1, 10):
        lam = Fraction(lam_num, 10)
        for eta_num in range(0, 13):
            eta = Fraction(eta_num, 4)
            for r_num in range(0, 13):
                r = Fraction(r_num, 4)
                fixed = max(Fraction(1), r, eta / (1 - lam))
                recurrence_fixed = max(r, eta / (1 - lam))
                current = Fraction(0)
                monotone_below_fixed = True
                for _ in range(40):
                    previous = current
                    current = max(r, eta + lam * current)
                    monotone_below_fixed &= previous <= current <= recurrence_fixed
                fixed_identity = max(r, eta + lam * recurrence_fixed) == recurrence_fixed
                if not monotone_below_fixed or not fixed_identity:
                    strict_failures.append(
                        {"lambda": str(lam), "eta": str(eta), "r": str(r), "limit": str(current)}
                    )
                assert max(Fraction(1), recurrence_fixed) == fixed
                cases += 1

    # Hostile controls: lambda=1 retains the unknown K, as does an explicit
    # fallback/current-scale call.  Evaluate symbolically on a range of K.
    hostile = []
    for k in range(1, 41):
        one_step_current_scale = max(Fraction(1), Fraction(1) + k)
        fallback = max(Fraction(2), Fraction(k))
        hostile.append(
            {
                "K": k,
                "current_scale_exponent": str(one_step_current_scale),
                "fallback_exponent": str(fallback),
                "retains_K": one_step_current_scale >= k and fallback >= k,
            }
        )
    return {
        "strict_fractional_cases": cases,
        "strict_fractional_failures": strict_failures,
        "hostile_current_scale_cases": hostile,
    }


def adaptive_wrapper_audit(seed: int, trials: int) -> dict[str, object]:
    rng = random.Random(seed)
    checks = 0
    failures: list[dict[str, object]] = []
    max_queries = 0
    for trial in range(trials):
        levels = rng.randint(2, 7)
        table = {
            (level, index): rng.getrandbits(1)
            for level in range(levels)
            for index in range(1 << level)
        }
        wrappers = wrapper_oracles(table)
        q = rng.randint(0, 7)
        controller = Controller(
            level=levels - 1,
            query_masks=tuple(rng.randrange(1 << j) for j in range(q)),
            query_biases=tuple(rng.randrange(1 << levels) for _ in range(q)),
            output_mask=rng.randrange(1 << q),
            output_bias=rng.getrandbits(1),
        )
        parent = rng.randrange(1 << (levels - 1))
        baseline = controller.run(parent, wrappers["DIRECT"])
        max_queries = max(max_queries, q)
        for name, oracle in wrappers.items():
            observed = controller.run(parent, oracle)
            checks += 1
            if observed != baseline:
                failures.append(
                    {"trial": trial, "wrapper": name, "baseline": baseline, "observed": observed}
                )
        # A memoized recursive replacement of the oracle must give the same
        # extensional answers and transcript.
        memo: dict[tuple[int, int], int] = {}

        def eliminated(level: int, index: int) -> int:
            key = (level, index)
            if key not in memo:
                memo[key] = table[key]
            return memo[key]

        observed = controller.run(parent, eliminated)
        checks += 1
        if observed != baseline:
            failures.append(
                {"trial": trial, "wrapper": "ELIMINATED", "baseline": baseline, "observed": observed}
            )

    return {
        "seed": seed,
        "trials": trials,
        "wrapper_and_elimination_checks": checks,
        "max_adaptive_queries": max_queries,
        "failures": failures,
    }


def semantic_compatibility_audit() -> dict[str, object]:
    # The eight 3-variable width-three clauses, one falsified by each full
    # assignment.  A subset of clauses is UNSAT iff it contains all eight.
    rows_checked = 0
    disagreements = []
    for clause_mask in range(1 << 8):
        semantic_row = [int(not ((clause_mask >> assignment) & 1)) for assignment in range(8)]
        sat_from_full_row = int(any(semantic_row))
        sat_shortcut = int(clause_mask != 0xFF)
        rows_checked += 1
        if sat_from_full_row != sat_shortcut:
            disagreements.append(clause_mask)
    return {
        "three_variable_formulas": rows_checked,
        "semantic_row_width": 8,
        "shortcut_disagreements": disagreements,
        "interpretation": "the one-bit decision need not materialize the full compatibility row",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111300)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    result = {
        "experiment": "adaptive_downward_oracle_elimination_audit",
        "status": "COMPUTATIONAL",
        "exponent_recurrence": exponent_audit(),
        "adaptive_wrappers": adaptive_wrapper_audit(args.seed, args.trials),
        "semantic_compatibility": semantic_compatibility_audit(),
    }
    result["elapsed_seconds"] = time.perf_counter() - started
    result["pass"] = (
        not result["exponent_recurrence"]["strict_fractional_failures"]
        and all(x["retains_K"] for x in result["exponent_recurrence"]["hostile_current_scale_cases"])
        and not result["adaptive_wrappers"]["failures"]
        and not result["semantic_compatibility"]["shortcut_disagreements"]
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
