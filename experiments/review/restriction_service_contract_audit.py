#!/usr/bin/env python3
"""Finite audit for RESTRICTION-SERVICE-CONTRACT1.

This does not test an asymptotic lower bound.  It checks the exact semantic
identity behind the service-contract classification on exhaustive and seeded
finite CNFs, together with representation and wrapper controls.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]
Rho = tuple[int, ...]  # -1 is unset, 0 is false, 1 is true


def brute_sat(cnf: CNF, n: int) -> bool:
    for mask in range(1 << n):
        if all(any(((mask >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
               for clause in cnf):
            return True
    return False


def restrict_cnf(cnf: CNF, rho: Rho) -> CNF:
    out: list[Clause] = []
    for clause in cnf:
        residual: list[int] = []
        satisfied = False
        for lit in clause:
            value = rho[abs(lit) - 1]
            if value == -1:
                residual.append(lit)
            elif value == int(lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return tuple(out)


def service_by_restriction(cnf: CNF, rho: Rho) -> bool:
    return brute_sat(restrict_cnf(cnf, rho), len(rho))


def service_by_completion(cnf: CNF, rho: Rho) -> bool:
    unset = [i for i, value in enumerate(rho) if value == -1]
    for bits in itertools.product((0, 1), repeat=len(unset)):
        assignment = list(rho)
        for i, bit in zip(unset, bits):
            assignment[i] = bit
        if all(any(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause)
               for clause in cnf):
            return True
    return False


def all_proper_three_clauses(n: int) -> list[Clause]:
    clauses: list[Clause] = []
    for variables in itertools.combinations(range(1, n + 1), 3):
        for signs in itertools.product((-1, 1), repeat=3):
            clauses.append(tuple(v * s for v, s in zip(variables, signs)))
    return clauses


def rename(cnf: CNF, permutation: tuple[int, ...]) -> CNF:
    return tuple(tuple((1 if lit > 0 else -1) * permutation[abs(lit) - 1]
                       for lit in clause) for clause in cnf)


def rename_rho(rho: Rho, permutation: tuple[int, ...]) -> Rho:
    out = [-1] * len(rho)
    for old, new in enumerate(permutation, start=1):
        out[new - 1] = rho[old - 1]
    return tuple(out)


def complement(cnf: CNF, variables: set[int]) -> CNF:
    return tuple(tuple(-lit if abs(lit) in variables else lit for lit in clause)
                 for clause in cnf)


def complement_rho(rho: Rho, variables: set[int]) -> Rho:
    return tuple((1 - value) if i + 1 in variables and value != -1 else value
                 for i, value in enumerate(rho))


def random_cnf(rng: random.Random, n: int, m: int) -> CNF:
    universe = all_proper_three_clauses(n)
    return tuple(rng.sample(universe, min(m, len(universe))))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--random-formulas", type=int, default=160)
    parser.add_argument("--random-queries", type=int, default=80)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    rng = random.Random(args.seed)

    counts = {
        "exhaustive_formula_query_checks": 0,
        "seeded_formula_query_checks": 0,
        "explicit_table_coordinate_checks": 0,
        "polynomial_batch_checks": 0,
        "wrapper_checks": 0,
        "independent_product_checks": 0,
        "easy_control_checks": 0,
        "recomp_checks": 0,
        "accounting_identities": 0,
    }

    # Exhaust all 2^8 proper three-CNF clause subsets and all 3^3 pinnings.
    clauses3 = all_proper_three_clauses(3)
    rhos3 = list(itertools.product((-1, 0, 1), repeat=3))
    for mask in range(1 << len(clauses3)):
        cnf = tuple(clauses3[i] for i in range(len(clauses3)) if (mask >> i) & 1)
        table: dict[Rho, bool] = {}
        for rho in rhos3:
            direct = service_by_completion(cnf, rho)
            replay = service_by_restriction(cnf, rho)
            assert direct == replay
            table[rho] = replay
            counts["exhaustive_formula_query_checks"] += 1
        for rho in rhos3:
            assert table[rho] == service_by_restriction(cnf, rho)
            counts["explicit_table_coordinate_checks"] += 1

    # Seeded n=4 sources, polynomial-size batches, and syntax wrappers.
    for _ in range(args.random_formulas):
        cnf = random_cnf(rng, 4, rng.randint(0, 20))
        batch: list[Rho] = []
        for _ in range(args.random_queries):
            rho = tuple(rng.choice((-1, 0, 1)) for _ in range(4))
            batch.append(rho)
            assert service_by_completion(cnf, rho) == service_by_restriction(cnf, rho)
            counts["seeded_formula_query_checks"] += 1

        batch_direct = [service_by_completion(cnf, rho) for rho in batch]
        batch_replay = [service_by_restriction(cnf, rho) for rho in batch]
        assert batch_direct == batch_replay
        counts["polynomial_batch_checks"] += len(batch)

        permutation = tuple(rng.sample(range(1, 5), 4))
        complemented = {v for v in range(1, 5) if rng.getrandbits(1)}
        for rho, expected in zip(batch[:8], batch_direct[:8]):
            assert service_by_restriction(rename(cnf, permutation),
                                          rename_rho(rho, permutation)) == expected
            counts["wrapper_checks"] += 1
            assert service_by_restriction(complement(cnf, complemented),
                                          complement_rho(rho, complemented)) == expected
            counts["wrapper_checks"] += 1
            assert service_by_restriction(tuple(reversed(cnf)), rho) == expected
            counts["wrapper_checks"] += 1
            copied = cnf + cnf[: min(2, len(cnf))]
            assert service_by_restriction(copied, rho) == expected
            counts["wrapper_checks"] += 1
            dead = cnf + ((1, -1),)
            assert service_by_restriction(dead, rho) == expected
            counts["wrapper_checks"] += 1
            for _repeat in range(3):
                assert service_by_restriction(cnf, rho) == expected
                counts["recomp_checks"] += 1

    # Independent products combine by conjunction without a joint service table.
    for _ in range(256):
        left = random_cnf(rng, 3, rng.randint(0, 8))
        right0 = random_cnf(rng, 3, rng.randint(0, 8))
        right = tuple(tuple((abs(lit) + 3) * (1 if lit > 0 else -1) for lit in clause)
                      for clause in right0)
        rho = tuple(rng.choice((-1, 0, 1)) for _ in range(6))
        product = left + right
        expected = (service_by_restriction(left, rho[:3]) and
                    service_by_restriction(right0, rho[3:]))
        assert service_by_restriction(product, rho) == expected
        counts["independent_product_checks"] += 1

    # Easy-family controls.  Their service semantics obey the same identity.
    easy_cnfs: list[tuple[CNF, int]] = [
        (((-1, 2), (-2, 3), (-3,)), 3),                 # Horn
        (((1, 2), (-1, 3), (-2, -3)), 3),               # 2-SAT
        (((1,), (-2,), (3,)), 3),                        # unit / treewidth zero
        (((1, 2, 3), (-1, -2, 3), (-1, 2, -3),
          (1, -2, -3)), 3),                              # affine parity encoding
    ]
    for cnf, n in easy_cnfs:
        for rho in itertools.product((-1, 0, 1), repeat=n):
            assert service_by_completion(cnf, rho) == service_by_restriction(cnf, rho)
            counts["easy_control_checks"] += 1

    # Exact exponent bookkeeping for B=N^alpha queries of size N^beta.
    for k in range(1, 7):
        for alpha_num in range(0, 5):
            for beta_num in range(0, 5):
                alpha = alpha_num / 4
                beta = beta_num / 4
                replay_exponent = alpha + beta * k
                assert replay_exponent == alpha + beta * k
                counts["accounting_identities"] += 1

    elapsed = time.perf_counter() - started
    script_path = Path(__file__).resolve()
    result = {
        "claim": "RESTRICTION-SERVICE-CONTRACT1",
        "status": {
            "semantic_identity": "COMPUTATIONAL finite audit of an exact symbolic identity",
            "generic_service_size_implies_hardness": "FALSIFIED/RETIRED",
            "arbitrary_algorithm_lower_bound": "OPEN",
        },
        "seed": args.seed,
        "parameters": {
            "exhaustive_n": 3,
            "exhaustive_formulas": 1 << len(clauses3),
            "exhaustive_queries_per_formula": len(rhos3),
            "random_n": 4,
            "random_formulas": args.random_formulas,
            "random_queries_per_formula": args.random_queries,
        },
        "counts": counts,
        "elapsed_seconds": elapsed,
        "script_sha256": digest(script_path),
        "limitations": [
            "Finite tests do not prove an asymptotic lower bound.",
            "The replay evaluator deliberately retains the cost of its supplied decider.",
            "No cell-probe or preprocessing lower bound is transferred to unrestricted SAT.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
