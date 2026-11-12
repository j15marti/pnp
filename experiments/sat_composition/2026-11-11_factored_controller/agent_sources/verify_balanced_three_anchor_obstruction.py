#!/usr/bin/env python3
"""Balanced three-anchor controls for the four specified exact local routines.

No claim about all SAT algorithms: these instances have explicit easy witnesses.
The polynomial formulas and seed prefix bounds concern the frozen implementations.
"""
from __future__ import annotations

import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from closure_parity import solve_2cnf_affine, solve_horn_affine
from seed_parity import solve_2cnf_affine_seeds, solve_horn_affine_seeds
from verify_three_anchor_obstruction import source, check_witness


def balanced_rows(masks, base):
    m = len(masks)
    q = m // 2
    parities = [(mask & base).bit_count() % 2 for mask in masks]
    chosen = set(sorted(range(m), key=lambda i: (parities[i], i))[:q])
    bits = [int(i in chosen) for i in range(m)]
    h = sum(p != b for p, b in zip(parities, bits))
    assert sum(bits) == q and h >= q >= 1
    return list(zip(masks, bits)), q, h, parities


def prefix_products(factors):
    values = [1]
    for factor in factors:
        values.append(values[-1] * factor)
    return values


def actual_control(m, run_seed=True):
    n, anchors, triples, clauses, masks = source(m)
    base = solve_2cnf_affine(n, clauses, [])["witness"]
    rows, q, h, p = balanced_rows(masks, base)
    explicit = sum(1 << (a - 1) for a in anchors)
    for triple, (_, bit) in zip(triples, rows):
        if bit:
            explicit |= 1 << (triple[0] - 1)
    check_witness(n, clauses, rows, explicit)
    out = {"triples": m, "variables": n, "q": q, "h": h,
           "base_parities": p, "right_hand_sides": [b for _, b in rows],
           "explicit_witness": explicit}
    modes = [
        ("horn", solve_horn_affine, solve_horn_affine_seeds, q,
         [3 if b else 4 for _, b in rows]),
        ("two_cnf", solve_2cnf_affine, solve_2cnf_affine_seeds, h,
         [3 if p[i] != b else 4 for i, (_, b) in enumerate(rows)]),
    ]
    for name, polynomial, seeds, threshold, factors in modes:
        answer = polynomial(n, clauses, rows)
        assert answer["status"] == "SAT", answer
        check_witness(n, clauses, rows, answer["witness"])
        expected = prefix_products(factors)
        assert answer["counters"]["polynomial_stage_sizes"] == expected, (name, m, answer)
        lower_prefix = sum(comb(n, k) for k in range(threshold))
        row = {"polynomial_stage_sizes": expected,
               "final_terms": expected[-1], "minimum_seed_size": threshold,
               "all_smaller_seeds": lower_prefix}
        if run_seed:
            seed_answer = seeds(n, clauses, rows)
            assert seed_answer["status"] == "SAT", seed_answer
            check_witness(n, clauses, rows, seed_answer["witness"])
            assert len(seed_answer["counters"]["witness_seed"]) >= threshold
            assert seed_answer["counters"]["seeds_attempted"] > lower_prefix
            capped = seeds(n, clauses, rows, seed_cap=lower_prefix)
            assert capped["status"] == "UNRESOLVED", capped
            assert capped["counters"]["seeds_attempted"] == lower_prefix
            row["observed_seeds_attempted"] = seed_answer["counters"]["seeds_attempted"]
            row["observed_witness_seed_size"] = len(seed_answer["counters"]["witness_seed"])
            row["prefix_cap_status"] = capped["status"]
        out[name] = row
    return out


def small_base_controls(m):
    n, anchors, triples, clauses, masks = source(m)
    original_models = []
    for choices in product(range(4), repeat=m):
        selected = sum(1 << (triples[j][c - 1] - 1)
                       for j, c in enumerate(choices) if c)
        for ap in ((7,) if selected else range(8)):
            original_models.append(selected | (ap << (3 * m)))
    tested, forbidden_seed_tests = 0, 0
    full = (1 << n) - 1
    for base in original_models:
        rows, q, h, parities = balanced_rows(masks, base)
        translated = [tuple(-lit if (base >> (abs(lit) - 1)) & 1 else lit
                            for lit in clause) for clause in clauses]
        translated_rows = [(mask, b ^ parities[i]) for i, (mask, b) in enumerate(rows)]
        answer = solve_horn_affine(n, translated, translated_rows)
        assert answer["status"] == "SAT"
        assert answer["counters"]["polynomial_stage_sizes"][-1] == 3 ** h * 4 ** (m - h)
        # Independently compute each small seed's least model by intersecting
        # all semantic models extending it, without a Horn closure routine.
        translated_models = [x ^ base for x in original_models]
        for size in range(h):
            for seed in combinations(range(n), size):
                mask = sum(1 << j for j in seed)
                eligible = [x for x in translated_models if x & mask == mask]
                if eligible:
                    least = full
                    for x in eligible:
                        least &= x
                    assert not all((least & row).bit_count() % 2 == b
                                   for row, b in translated_rows), (m, base, seed)
                forbidden_seed_tests += 1
        tested += 1
    return {"valid_bases": tested, "forbidden_seed_tests": forbidden_seed_tests}


def derived_large_bound(m=20):
    n, anchors, triples, clauses, masks = source(m)
    base = solve_2cnf_affine(n, clauses, [])["witness"]
    rows, q, h, p = balanced_rows(masks, base)
    return {"triples": m, "variables": n, "q": q, "h": h,
            "horn_final_terms": 3 ** q * 4 ** (m - q),
            "two_cnf_final_terms": 3 ** h * 4 ** (m - h),
            "horn_smaller_seed_count": sum(comb(n, k) for k in range(q)),
            "two_cnf_smaller_seed_count": sum(comb(n, k) for k in range(h)),
            "execution": "Only base and arithmetic bounds computed; exponential solver runs not executed"}


def main():
    report = {"status": "PASS", "scope": "four specified exact local implementations",
              "polynomial_engine_sha256": hashlib.sha256((ROOT / "closure_parity.py").read_bytes()).hexdigest(),
              "seed_engine_sha256": hashlib.sha256((ROOT / "seed_parity.py").read_bytes()).hexdigest(),
              "actual_controls": [actual_control(m, run_seed=m <= 8) for m in range(2, 10)],
              "all_valid_small_bases": {str(m): small_base_controls(m) for m in (2, 3)},
              "derived_large_bound": derived_large_bound()}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
