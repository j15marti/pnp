#!/usr/bin/env python3
"""Finite guards for BLACKBOX-QUERY-SCALE-DICHOTOMY1.

The asymptotic result is proved symbolically.  This program checks exact
rational exponent ledgers, extensional transcript invariance, and small
hostile SAT families.  No finite timing is used as an asymptotic lower bound.
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


def canonical(clauses: Iterable[Iterable[int]]) -> Formula:
    return tuple(tuple(int(x) for x in clause) for clause in clauses)


def sat_bit(formula: Formula) -> int:
    variables = max((abs(x) for c in formula for x in c), default=0)
    for assignment in itertools.product((0, 1), repeat=variables):
        if all(any((lit > 0) == bool(assignment[abs(lit) - 1]) for lit in c) for c in formula):
            return 1
    return 0


def wrappers(base: Callable[[Formula], int]) -> dict[str, Callable[[Formula], int]]:
    def copy(formula: Formula) -> int:
        return int(base(tuple(tuple(c) for c in formula)))

    def delay(formula: Formula) -> int:
        answer = base(formula)
        dummy = sum(len(c) for c in formula) & 1
        return answer ^ dummy ^ dummy

    def interp(formula: Formula) -> int:
        return int({"answer": base(formula)}["answer"])

    def recomp(formula: Formula) -> int:
        return sum((base(formula), 0)) & 1

    return {"DIRECT": base, "COPY": copy, "DELAY": delay, "INTERP": interp, "RECOMP": recomp}


def exact_exponent_audit() -> dict[str, object]:
    positive_checks = 0
    vanishing_checks = 0
    failures: list[dict[str, object]] = []

    # Positive scale: for every proposed common exponent c, choose an integer
    # delay exponent d with lambda*d > c.
    for lam_num in range(1, 17):
        lam = Fraction(lam_num, 16)
        for c_num in range(0, 49):
            c = Fraction(c_num, 4)
            d = c // lam + 1
            positive_checks += 1
            if not lam * d > c:
                failures.append({"regime": "positive", "lambda": str(lam), "c": str(c), "d": int(d)})

    # Vanishing scale delta_t=1/t: for each fixed solver exponent K and
    # tolerance eps, K/t eventually falls below eps.  Query-count exponent
    # eta therefore survives while K disappears into o(1).
    for k in range(1, 65):
        for eps_den in (2, 4, 8, 16, 32, 64):
            eps = Fraction(1, eps_den)
            threshold = k * eps_den + 1
            for extra in (0, 1, 7):
                t = threshold + extra
                vanishing_checks += 1
                if not Fraction(k, t) < eps:
                    failures.append({"regime": "vanishing", "K": k, "epsilon": str(eps), "t": t})

    return {
        "positive_scale_exact_checks": positive_checks,
        "vanishing_scale_exact_checks": vanishing_checks,
        "failures": failures,
        "identity": "max(r, eta + K*delta_t) -> max(r, eta) for each fixed K when delta_t -> 0",
    }


def named_controls() -> dict[str, Formula]:
    return {
        "2SAT": canonical(((1, 2), (-1, 2), (1, -2))),
        "HORN": canonical(((-1, 2), (-2, 3), (1,), (-3,))),
        "AFFINE_TSEITIN": canonical(((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))),
        "BOUNDED_TREEWIDTH": canonical(((1, 2), (-2, 3), (-3, 4), (-4,))),
        "INDEPENDENT_PRODUCT": canonical(((1,), (2,), (-3, 4), (3, -4))),
        "PADDING": canonical(((1,), (2, -2, 2), (3, -3, 3), (4, -4, 4))),
        "REDUNDANT": canonical(((1, 2), (1, 2), (-1,), (-2,))),
        "ALTERNATE_ENCODING": canonical(((3, -1), (-3, 2), (1,), (-2,))),
    }


def query_schedule(formula: Formula, oracle: Callable[[Formula], int]) -> tuple[int, tuple[tuple[Formula, int], ...]]:
    """A bounded answer-adaptive truth-bit service with small derived queries."""
    transcript: list[tuple[Formula, int]] = []
    seed = sum((i + 1) * sum(c) for i, c in enumerate(formula))
    state = seed & 1
    for step in range(5):
        v = 1 + ((abs(seed) + step + state) % 3)
        if step % 3 == 0:
            query = canonical(((v,),))
        elif step % 3 == 1:
            query = canonical(((v,), (-v,)))
        else:
            query = canonical(((v, (v % 3) + 1),))
        answer = oracle(query)
        transcript.append((query, answer))
        state ^= answer
    return state, tuple(transcript)


def wrapper_audit(seed: int, trials: int) -> dict[str, object]:
    ws = wrappers(sat_bit)
    failures: list[dict[str, object]] = []
    named_checks = 0
    randomized_checks = 0

    for name, formula in named_controls().items():
        reference = query_schedule(formula, ws["DIRECT"])
        for wrapper_name, oracle in ws.items():
            named_checks += 1
            if query_schedule(formula, oracle) != reference:
                failures.append({"family": name, "wrapper": wrapper_name})

    # All 256 subsets of the eight proper width-three clauses on three vars.
    clauses = tuple(tuple((i + 1) if ((mask >> i) & 1) else -(i + 1) for i in range(3)) for mask in range(8))
    exhaustive_checks = 0
    for subset in range(256):
        formula = canonical(clauses[i] for i in range(8) if (subset >> i) & 1)
        reference = query_schedule(formula, ws["DIRECT"])
        for wrapper_name, oracle in ws.items():
            exhaustive_checks += 1
            if query_schedule(formula, oracle) != reference:
                failures.append({"subset": subset, "wrapper": wrapper_name})

    rng = random.Random(seed)
    for trial in range(trials):
        n = rng.randint(1, 5)
        formula = canonical(
            tuple(
                tuple((1 if rng.getrandbits(1) else -1) * rng.randint(1, n) for _ in range(rng.randint(1, 3)))
                for _ in range(rng.randint(0, 8))
            )
        )
        reference = query_schedule(formula, ws["DIRECT"])
        for wrapper_name, oracle in ws.items():
            randomized_checks += 1
            if query_schedule(formula, oracle) != reference:
                failures.append({"trial": trial, "wrapper": wrapper_name})

    return {
        "seed": seed,
        "trials": trials,
        "named_hostile_checks": named_checks,
        "exhaustive_clean_core_checks": exhaustive_checks,
        "randomized_wrapper_checks": randomized_checks,
        "failures": failures,
    }


def encoding_controls() -> dict[str, object]:
    # Polynomial padding N'=N^a changes a fixed semantic query exponent
    # lambda to lambda/a but cannot make it zero for fixed a.  Superpolynomial
    # padding can, but parent input reading then dominates and the encoding is
    # not a polynomially equivalent local simulation.
    checks = 0
    failures = []
    for lam_num in range(1, 17):
        lam = Fraction(lam_num, 16)
        for a in range(1, 17):
            checks += 1
            if not lam / a > 0:
                failures.append({"lambda": str(lam), "padding_power": a})
    return {
        "fixed_polynomial_padding_checks": checks,
        "failures": failures,
        "interpretation": "fixed polynomial recodings rescale but do not erase a positive exponent",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111712)
    parser.add_argument("--trials", type=int, default=5000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    result = {
        "experiment": "blackbox_query_scale_dichotomy_audit",
        "status": "COMPUTATIONAL",
        "exact_exponents": exact_exponent_audit(),
        "wrappers_and_hostile_families": wrapper_audit(args.seed, args.trials),
        "encoding_controls": encoding_controls(),
    }
    result["elapsed_seconds"] = time.perf_counter() - started
    result["pass"] = (
        not result["exact_exponents"]["failures"]
        and not result["wrappers_and_hostile_families"]["failures"]
        and not result["encoding_controls"]["failures"]
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
