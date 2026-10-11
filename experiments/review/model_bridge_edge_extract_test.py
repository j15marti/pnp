#!/usr/bin/env python3
"""Finite audit of external SAT search-to-decision and interface guards.

The theorem in MODELBRIDGE-0003 is symbolic.  This program checks the exact
pinning construction on bounded 3-CNF instances, including repeated-literal
encodings, duplicate-clause padding, easy structural families, random controls,
and extensionally equivalent decider wrappers.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import signal
import time
from pathlib import Path


Clause = tuple[int, int, int]


class BudgetExceeded(RuntimeError):
    pass


def _alarm(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


def gamma_len(z: int) -> int:
    assert z >= 1
    return 2 * (z.bit_length() - 1) + 1


def encoded_bits(nvars: int, clauses: tuple[Clause, ...]) -> int:
    """Declared canonical binary length used by the report.

    Header: Elias-gamma(nvars), Elias-gamma(m+1).  Every literal uses one
    sign bit and a fixed-width variable index.  Exact 3-clause boundaries are
    implicit.  The +1 permits the empty formula.
    """
    width = max(1, math.ceil(math.log2(nvars + 1)))
    return gamma_len(nvars) + gamma_len(len(clauses) + 1) + 3 * len(clauses) * (1 + width)


def pin(var: int, value: int) -> Clause:
    lit = var if value else -var
    return (lit, lit, lit)


def satisfies(clauses: tuple[Clause, ...], assignment: tuple[int, ...]) -> bool:
    for clause in clauses:
        if not any((lit > 0) == bool(assignment[abs(lit) - 1]) for lit in clause):
            return False
    return True


def brute_decider(nvars: int, clauses: tuple[Clause, ...]) -> bool:
    return any(satisfies(clauses, bits) for bits in itertools.product((0, 1), repeat=nvars))


def wrapped_decider(mode: str):
    def decide(nvars: int, clauses: tuple[Clause, ...]) -> bool:
        if mode == "DIRECT":
            return brute_decider(nvars, clauses)
        if mode == "DEAD":
            _junk = sum(abs(lit) for clause in clauses for lit in clause) & 1
            return brute_decider(nvars, clauses)
        if mode == "COPY":
            first = brute_decider(nvars, clauses)
            _second = brute_decider(nvars, clauses)
            return first
        if mode == "DELAY":
            return not (not brute_decider(nvars, clauses))
        if mode == "RECOMP":
            return brute_decider(nvars, clauses) and brute_decider(nvars, clauses)
        raise AssertionError(mode)
    return decide


def extract_one(nvars: int, clauses: tuple[Clause, ...], decide):
    calls = 1
    query_lengths = [encoded_bits(nvars, clauses)]
    if not decide(nvars, clauses):
        return None, calls, query_lengths
    prefix: list[int] = []
    for var in range(1, nvars + 1):
        trial = clauses + tuple(pin(i + 1, bit) for i, bit in enumerate(prefix)) + (pin(var, 0),)
        calls += 1
        query_lengths.append(encoded_bits(nvars, trial))
        prefix.append(0 if decide(nvars, trial) else 1)
    witness = tuple(prefix)
    assert satisfies(clauses, witness)
    return witness, calls, query_lengths


def eq_family(k: int) -> tuple[int, tuple[Clause, ...]]:
    clauses: list[Clause] = []
    for i in range(1, k + 1):
        j = k + i
        clauses.extend([(-i, j, j), (i, -j, -j)])
    return 2 * k, tuple(clauses)


def affine_complement(k: int) -> tuple[int, tuple[Clause, ...]]:
    clauses: list[Clause] = []
    for i in range(1, k + 1):
        j = k + i
        clauses.extend([(i, j, j), (-i, -j, -j)])
    return 2 * k, tuple(clauses)


def horn_chain(n: int) -> tuple[int, tuple[Clause, ...]]:
    clauses: list[Clause] = [(1, 1, 1)]
    for i in range(1, n):
        clauses.append((-i, i + 1, i + 1))
    return n, tuple(clauses)


def random_formula(rng: random.Random, n: int, m: int) -> tuple[int, tuple[Clause, ...]]:
    clauses = []
    for _ in range(m):
        lits = []
        for _ in range(3):
            v = rng.randint(1, n)
            lits.append(v if rng.randrange(2) else -v)
        clauses.append(tuple(lits))
    return n, tuple(clauses)  # type: ignore[arg-type]


def run(max_k: int, random_cases: int, seed: int) -> dict:
    started = time.perf_counter()
    rng = random.Random(seed)
    cases: list[tuple[str, int, tuple[Clause, ...]]] = []
    for k in range(1, max_k + 1):
        n, f = eq_family(k)
        cases.append(("equality_2sat_treewidth1", n, f))
        cases.append(("independent_product", n, f + f[:2]))
        n, f = affine_complement(k)
        cases.append(("affine_xor_pairs", n, f))
        n, f = horn_chain(k + 1)
        cases.append(("horn_chain", n, f))
        cases.append(("redundant_clause_padding", n, f + tuple(f[:1]) * (k + 1)))
    for i in range(random_cases):
        n = rng.randint(2, min(7, 2 * max_k))
        nv, f = random_formula(rng, n, rng.randint(1, 2 * n + 2))
        cases.append((f"random_{i}", nv, f))
    # Explicit inconsistent unit pins supply UNSAT controls.
    for n in range(1, max_k + 1):
        cases.append(("contradictory_pins", n, (pin(1, 0), pin(1, 1))))

    wrappers = ["DIRECT", "DEAD", "COPY", "DELAY", "RECOMP"]
    formula_checks = 0
    wrapper_checks = 0
    witness_checks = 0
    query_bound_checks = 0
    wrapper_witness_checks = 0
    total_oracle_calls = 0
    max_query_growth = 0
    rows = []

    for label, nvars, formula in cases:
        truth = brute_decider(nvars, formula)
        witness, calls, lengths = extract_one(nvars, formula, brute_decider)
        formula_checks += 1
        total_oracle_calls += calls
        if truth:
            assert witness is not None and satisfies(formula, witness)
            assert calls == nvars + 1
            witness_checks += 1
        else:
            assert witness is None and calls == 1
        base_len = encoded_bits(nvars, formula)
        width = max(1, math.ceil(math.log2(nvars + 1)))
        declared = base_len + (gamma_len(len(formula) + nvars + 1) - gamma_len(len(formula) + 1)) + 3 * nvars * (1 + width)
        assert max(lengths) <= declared
        query_bound_checks += 1
        max_query_growth = max(max_query_growth, max(lengths) - base_len)

        for mode in wrappers:
            decide = wrapped_decider(mode)
            assert decide(nvars, formula) == truth
            wrapper_checks += 1
            w2, c2, _ = extract_one(nvars, formula, decide)
            assert c2 == calls
            assert (w2 is None) == (witness is None)
            if w2 is not None:
                assert satisfies(formula, w2)
                wrapper_witness_checks += 1
        rows.append({
            "family": label,
            "nvars": nvars,
            "clauses": len(formula),
            "encoded_bits": base_len,
            "sat": truth,
            "oracle_calls": calls,
            "max_query_bits": max(lengths),
        })

    return {
        "status": "PASS",
        "scope": {
            "max_k": max_k,
            "random_cases": random_cases,
            "seed": seed,
            "wrappers": wrappers,
            "encoding": "gamma(n), gamma(m+1), then three signed fixed-width literals per clause",
            "warning": "Finite checks validate the construction, not an asymptotic lower bound.",
        },
        "checks": {
            "formulas": formula_checks,
            "wrapper_answer_checks": wrapper_checks,
            "direct_witness_checks": witness_checks,
            "wrapper_witness_checks": wrapper_witness_checks,
            "query_length_bound_checks": query_bound_checks,
            "total_direct_oracle_calls": total_oracle_calls,
        },
        "max_query_growth_bits": max_query_growth,
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=4)
    parser.add_argument("--random-cases", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    result = run(args.max_k, args.random_cases, args.seed)
    signal.alarm(0)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["checks"], sort_keys=True))
    print(f"elapsed_seconds={result['elapsed_seconds']:.6f}")


if __name__ == "__main__":
    main()
