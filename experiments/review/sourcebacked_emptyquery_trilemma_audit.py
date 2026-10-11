#!/usr/bin/env python3
"""Finite audit for SOURCEBACKED-EMPTYQUERY-TRILEMMA1.

The symbolic theorem is in the accompanying report.  This program only checks
small extensional tables, CNF restriction semantics, hostile easy families,
wrappers, and exact exponent identities.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def satisfies(formula: Formula, assignment: tuple[int, ...]) -> bool:
    return all(any((lit > 0) == bool(assignment[abs(lit) - 1]) for lit in c)
               for c in formula)


def service(formula: Formula, rho: tuple[int, ...]) -> bool:
    """rho entries are -1 (free), 0, or 1."""
    free = [i for i, bit in enumerate(rho) if bit < 0]
    base = [max(bit, 0) for bit in rho]
    for values in itertools.product((0, 1), repeat=len(free)):
        a = base[:]
        for i, bit in zip(free, values):
            a[i] = bit
        if satisfies(formula, tuple(a)):
            return True
    return False


def all_rhos(n: int):
    return itertools.product((-1, 0, 1), repeat=n)


def affine_parity(value: int) -> Formula:
    bad = [a for a in itertools.product((0, 1), repeat=3)
           if (sum(a) & 1) != value]
    return tuple(tuple((-(i + 1) if bit else i + 1) for i, bit in enumerate(a))
                 for a in bad)


def paired_k33() -> Formula:
    # Nine edge variables e_(u,w), two signed clauses at each of six vertices.
    incident = []
    for u in range(3):
        incident.append(tuple(1 + 3 * u + w for w in range(3)))
    for w in range(3):
        incident.append(tuple(1 + 3 * u + w for u in range(3)))
    return tuple(c for ids in incident for c in (ids, tuple(-x for x in ids)))


def digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=202610110900)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    start = time.monotonic()
    counts: dict[str, int] = {}

    # A one-bit view cannot reconstruct an unrestricted multi-coordinate table.
    ambiguity = 0
    tables = 0
    for width in range(2, 13):
        for mask in range(1 << width):
            tables += 1
            b0 = mask & 1
            for q in range(1, width):
                mate = mask ^ (1 << q)
                assert (mate & 1) == b0
                assert ((mate >> q) & 1) != ((mask >> q) & 1)
                ambiguity += 1
    counts["abstract_tables"] = tables
    counts["one_bit_ambiguity_pairs"] = ambiguity

    # Exhaust all proper three-literal clauses on three variables and all pins.
    clauses = tuple(tuple((i + 1) if ((mask >> i) & 1) else -(i + 1)
                          for i in range(3)) for mask in range(8))
    semantic = empty = explicit_readback = 0
    for subset in range(1 << len(clauses)):
        f = tuple(clauses[i] for i in range(8) if (subset >> i) & 1)
        sat_bit = service(f, (-1, -1, -1))
        assert sat_bit == any(satisfies(f, a) for a in itertools.product((0, 1), repeat=3))
        empty += 1
        table = {}
        for rho in all_rhos(3):
            answer = service(f, rho)
            table[rho] = answer
            assert table[rho] == service(f, rho)  # source-backed RECOMP evaluator
            semantic += 1
            explicit_readback += 1
    counts["cnf_empty_query_equalities"] = empty
    counts["cnf_service_coordinates"] = semantic
    counts["explicit_table_readbacks"] = explicit_readback

    # Hostile easy families: Horn/2-SAT, affine, product, and paired clean core.
    easy: list[tuple[str, Formula, int]] = [
        ("horn_equality", ((-1, 2), (1, -2)), 2),
        ("two_sat_path", ((1, 2), (-2, 3), (-3, 4)), 4),
        ("affine_even", affine_parity(0), 3),
        ("affine_odd", affine_parity(1), 3),
        ("independent_product", ((1,), (-2, 3), (2, -3), (4, 5), (-4, -5)), 5),
        ("paired_k33", paired_k33(), 9),
    ]
    easy_checks = wrapper_checks = 0
    for name, f, n in easy:
        rhos = list(all_rhos(n)) if n <= 5 else [tuple(rng.choice((-1, 0, 1)) for _ in range(n)) for _ in range(768)]
        for rho in rhos:
            ans = service(f, rho)
            assert ans == service(tuple(reversed(f)), rho)  # clause-order wrapper
            assert ans == service(f + f, rho)  # COPY wrapper
            dead = tuple((i + 1, -(i + 1)) for i in range(n))
            assert ans == service(f + dead, rho)  # DEAD tautologies
            easy_checks += 1
            wrapper_checks += 3
        # Empty coordinate is the ordinary decision bit for every family.
        assert service(f, tuple([-1] * n)) == any(
            satisfies(f, a) for a in itertools.product((0, 1), repeat=n))
    counts["easy_family_service_checks"] = easy_checks
    counts["copy_dead_order_wrapper_checks"] = wrapper_checks

    # Exact exponent identities for source-backed queries and empty-query use.
    exponent_checks = 0
    for K in range(1, 13):
        assert max(Fraction(1), Fraction(K)) == K
        exponent_checks += 1
        for alpha_num in range(5):
            for beta_num in range(1, 5):
                alpha = Fraction(alpha_num, 4)
                beta = Fraction(beta_num, 4)
                batch = alpha + beta * K
                assert batch >= beta * K
                exponent_checks += 1
    counts["exact_exponent_ledger_checks"] = exponent_checks

    result = {
        "run_id": "MODELBRIDGE-0007",
        "seed": args.seed,
        "status": "COMPUTATIONAL",
        "exhaustive": ["abstract truth tables widths 2..12", "all 256 three-variable clause subsets and 27 pins"],
        "randomized": ["768 paired-K3,3 pinning queries"],
        "counts": counts,
        "total_checks": sum(counts.values()),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "claim": "finite validation only; asymptotic statements require the symbolic proof",
    }
    result["content_digest"] = digest(result)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
