#!/usr/bin/env python3
"""Exact expected-rank audit for noisy witness advice without replacement.

This is a finite reproducer for REFEREE297.  It does not implement a SAT
oracle and does not claim a SAT lower bound.
"""

from __future__ import annotations

import argparse
import json
import math
import time
import tracemalloc
from decimal import Decimal, getcontext
from typing import Iterable


getcontext().prec = 100


def parse_dimacs(text: str) -> tuple[int, list[tuple[int, ...]]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("c")]
    if not lines or len(lines[0].split()) != 4 or lines[0].split()[:2] != ["p", "cnf"]:
        raise ValueError("missing or malformed header")
    try:
        nvars, nclauses = int(lines[0].split()[2]), int(lines[0].split()[3])
    except ValueError as exc:
        raise ValueError("nonnumeric header") from exc
    if nvars < 1 or nclauses < 1:
        raise ValueError("nonpositive dimensions")
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        try:
            vals = [int(x) for x in line.split()]
        except ValueError as exc:
            raise ValueError("nonnumeric literal") from exc
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError("bad clause terminator")
        clause = tuple(vals[:-1])
        if not clause or any(abs(x) > nvars for x in clause):
            raise ValueError("empty or out-of-range clause")
        if len({abs(x) for x in clause}) != len(clause):
            raise ValueError("duplicate variable")
        clauses.append(clause)
    if len(clauses) != nclauses:
        raise ValueError("clause-count mismatch")
    return nvars, clauses


def satisfies(clauses: Iterable[tuple[int, ...]], bits: int) -> bool:
    for clause in clauses:
        if not any(((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return False
    return True


def model_count(nvars: int, clauses: list[tuple[int, ...]]) -> int:
    return sum(satisfies(clauses, bits) for bits in range(1 << nvars))


def unique_unit_cnf(n: int, contradictory: bool = False) -> str:
    clauses = [f"{i} 0" for i in range(1, n + 1)]
    if contradictory:
        clauses.append("-1 0")
    return f"p cnf {n} {len(clauses)}\n" + "\n".join(clauses) + "\n"


def expected_rank(n: int, q: Decimal) -> Decimal:
    """Expected target rank in a Plackett-Luce weighted permutation.

    Each assignment a has product weight q^(n-d)(1-q)^d, where d is its
    Hamming distance from the unique target.  Exponential clocks generate
    successive weighted sampling without replacement.
    """
    if not (Decimal("0.5") <= q <= Decimal(1)):
        raise ValueError("q must lie in [1/2,1]")
    if q == 1:
        return Decimal(1)
    r = (Decimal(1) - q) / q
    total = Decimal(1)
    rd = Decimal(1)
    choose = 1
    for d in range(1, n + 1):
        rd *= r
        choose = choose * (n - d + 1) // d
        total += Decimal(choose) * rd / (Decimal(1) + rd)
    return total


def bounds(n: int, q: Decimal) -> tuple[Decimal, Decimal]:
    inv = q ** (-n)
    return (inv + Decimal(1)) / Decimal(2), inv


def first_n_over(q: Decimal, threshold: Decimal) -> int:
    # The exact expected rank is monotone in n.  Double, then binary-search.
    if q == 1:
        return -1
    lo, hi = 0, 1
    while expected_rank(hi, q) <= threshold:
        lo, hi = hi, 2 * hi
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if expected_rank(mid, q) <= threshold:
            lo = mid
        else:
            hi = mid
    return hi


def sci(x: Decimal, digits: int = 12) -> str:
    if x == 0:
        return "0"
    return f"{x:.{digits}E}"


def audit() -> dict:
    t0 = time.perf_counter_ns()
    tracemalloc.start()

    sat_text = unique_unit_cnf(12, False)
    unsat_text = unique_unit_cnf(12, True)
    n_sat, sat_clauses = parse_dimacs(sat_text)
    n_unsat, unsat_clauses = parse_dimacs(unsat_text)
    sat_models = model_count(n_sat, sat_clauses)
    unsat_models = model_count(n_unsat, unsat_clauses)
    assert sat_models == 1 and unsat_models == 0

    malformed = [
        "",
        "p cnf x 1\n1 0\n",
        "p cnf 1 1\n1\n",
        "p cnf 1 1\n2 0\n",
        "p cnf 2 1\n1 -1 0\n",
        "p cnf 2 2\n1 0\n",
    ]
    rejected = 0
    for text in malformed:
        try:
            parse_dimacs(text)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)

    rates = ["0.66", "0.75", "0.90", "0.95", "0.99"]
    ns = [9, 20, 50, 100, 500, 1000]
    rows = []
    for stated in rates:
        p = Decimal(stated)
        for interpretation, q in [
            ("direct_bit_accuracy", p),
            ("oracle_else_fair_random", (Decimal(1) + p) / Decimal(2)),
        ]:
            for n in ns:
                exact = expected_rank(n, q)
                low, high = bounds(n, q)
                assert low <= exact <= high
                rows.append(
                    {
                        "stated_rate": stated,
                        "interpretation": interpretation,
                        "effective_q": str(q),
                        "n": n,
                        "exact_expected_unique_checks": sci(exact),
                        "lower_bound": sci(low),
                        "upper_bound_iid": sci(high),
                    }
                )

    thresholds = []
    for stated in rates:
        p = Decimal(stated)
        for interpretation, q in [
            ("direct_bit_accuracy", p),
            ("oracle_else_fair_random", (Decimal(1) + p) / Decimal(2)),
        ]:
            n_cross = first_n_over(q, Decimal(1_000_000))
            thresholds.append(
                {
                    "stated_rate": stated,
                    "interpretation": interpretation,
                    "effective_q": str(q),
                    "first_n_expected_rank_over_1e6": n_cross,
                }
            )

    # Exact source-aware comparison on the fixtures.
    # The SAT unit formula is certified by its all-one witness in one source scan.
    # The UNSAT sibling has the source units x1 and ~x1 and one Resolution step.
    logical_controls = {
        "unique_sat_nvars": n_sat,
        "unique_sat_models": sat_models,
        "unique_sat_witness": (1 << n_sat) - 1,
        "unsat_sibling_models": unsat_models,
        "unsat_resolution_derived_nodes": 1,
        "malformed_rejected": rejected,
    }

    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    elapsed = time.perf_counter_ns() - t0

    return {
        "claim": "exact no-repeat unique-witness expected-rank audit",
        "sampling_model": "Plackett-Luce successive weighted sampling without replacement via exponential clocks",
        "theorem": {
            "exact": "E[R]=1+sum_{d=1}^n C(n,d) r^d/(1+r^d), r=(1-q)/q",
            "bounds": "(q^(-n)+1)/2 <= E[R] <= q^(-n)",
            "asymptotic": "Theta(q^(-n)) for every fixed q in [1/2,1)",
            "polynomial_threshold": "-n log(q)=O(log n), equivalently q=1-O(log n/n)",
        },
        "logical_controls": logical_controls,
        "rows": rows,
        "thresholds": thresholds,
        "charged_audit": {
            "elapsed_ns": elapsed,
            "peak_traced_bytes": peak,
            "includes": [
                "strict parsing",
                "complete SAT/UNSAT enumeration for 12-variable fixtures",
                "exact expected-rank sums",
                "bound checks",
                "threshold search",
                "malformed controls",
            ],
            "excludes": [
                "acquisition of witness-correlated advice",
                "proof of Valiant-Vazirani or Schoning",
                "unbounded SAT decision",
            ],
        },
        "status": {
            "expected_rank_theorem": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "B1": "OPEN for desired fixed mixed R",
            "global_B2": "OPEN",
            "B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

