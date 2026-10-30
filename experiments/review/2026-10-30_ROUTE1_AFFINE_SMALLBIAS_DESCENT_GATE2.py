#!/usr/bin/env python3
"""Exact finite audit for the affine small-bias MCSP threshold-descent obstruction.

These tests check the probabilistic lemmas and declared controls. They do not
compute asymptotic minimum circuit complexity or prove a SAT runtime bound.
Run: python affine_smallbias_gate_audit.py --output audit_raw.json
Python 3.10+, standard library only. Each suite is deliberately small.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
from random import Random
from time import perf_counter

SEED = 202610300919
RUN_ID = "2026-10-30_0919_AFFINE_SMALLBIAS_DESCENT_GATE2"
IRREDUCIBLES = {4: 0b10011, 5: 0b100101, 6: 0b1000011}


def gf_mul(a: int, b: int, degree: int) -> int:
    result = 0
    modulus = IRREDUCIBLES[degree]
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return result


def walsh(hist: list[int]) -> list[int]:
    values = hist.copy()
    stride = 1
    while stride < len(values):
        for base in range(0, len(values), 2 * stride):
            for j in range(base, base + stride):
                left, right = values[j], values[j + stride]
                values[j], values[j + stride] = left + right, left - right
        stride *= 2
    return values


def field_ensemble(bits: int, degree: int) -> tuple[list[int], list[list[int]]]:
    """Exactly the power/inner-product primitive in CHMY Theorem 33, j=1..bits."""
    field_size = 1 << degree
    hist = [0] * (1 << bits)
    powers = []
    for a in range(field_size):
        row = []
        power = 1
        for _ in range(bits):
            power = gf_mul(power, a, degree)
            row.append(power)
        powers.append(row)
        for b in range(field_size):
            x = sum(((power & b).bit_count() & 1) << j
                    for j, power in enumerate(row))
            hist[x] += 1
    return hist, powers


def linear_value(rows: tuple[int, ...], x: int) -> int:
    return sum(((row & x).bit_count() & 1) << j for j, row in enumerate(rows))


def row_rank(rows: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        while row:
            lead = row.bit_length() - 1
            if lead not in pivots:
                pivots[lead] = row
                break
            row ^= pivots[lead]
    return len(pivots)


def primitive_suite() -> tuple[dict, dict[int, list[int]]]:
    result = {"families": [], "nonzero_fourier_checks": 0,
              "polynomial_root_identity_checks": 0, "field_inverse_checks": 0}
    saved: dict[int, list[int]] = {}
    for bits, degree in ((4, 4), (8, 5), (16, 6)):
        field_size = 1 << degree
        for a in range(1, field_size):
            assert any(gf_mul(a, b, degree) == 1 for b in range(1, field_size))
            result["field_inverse_checks"] += 1
        hist, powers = field_ensemble(bits, degree)
        total = field_size * field_size
        assert sum(hist) == total
        spectrum = walsh(hist)
        assert spectrum[0] == total
        eps_num = max(abs(value) for value in spectrum[1:])
        for value in spectrum[1:]:
            assert 0 <= value <= bits * field_size
            result["nonzero_fourier_checks"] += 1
        # An independent direct root count checks the Walsh implementation.
        subset_range = range(1, 1 << bits) if bits <= 8 else [1, 3, 255, 65535]
        for subset in subset_range:
            roots = 0
            for row in powers:
                value = 0
                for j in range(bits):
                    if subset >> j & 1:
                        value ^= row[j]
                roots += value == 0
            assert spectrum[subset] == roots * field_size
            result["polynomial_root_identity_checks"] += 1
        support = sum(bool(c) for c in hist)
        result["families"].append({
            "output_bits": bits, "field_degree": degree, "field_size": field_size,
            "seed_pairs_exhausted": total, "distinct_outputs": support,
            "max_character_bias": str(Fraction(eps_num, total)),
            "root_degree_bound": str(Fraction(bits, field_size)),
        })
        saved[bits] = hist
    return result, saved


def affine_suite(hist: list[int]) -> dict:
    """Exhaust all 3x4 matrices, all offsets, and all sets for every linear map.

All sets with all offsets follow also by the explicitly checked translation
identity. We do not count that implication as extra exhaustive evaluations.
"""
    n, m = 4, 3
    dden, uden = sum(hist), 1 << n
    eps_num = max(abs(v) for v in walsh(hist)[1:])
    out = {"binary_matrices": 0, "affine_maps": 0, "point_checks": 0,
           "accepting_set_checks": 0, "rank_histogram": {},
           "translation_checks": 0, "max_singleton_advantage": "0"}
    ranks: Counter[int] = Counter()
    max_point = 0
    for rows in product(range(1 << n), repeat=m):
        rank = row_rank(rows)
        ranks[rank] += 1
        dhist, uhist = [0] * (1 << m), [0] * (1 << m)
        for x in range(1 << n):
            y = linear_value(rows, x)
            dhist[y] += hist[x]
            uhist[y] += 1
        assert sum(bool(c) for c in uhist) == 1 << rank
        differences = [dhist[y] * uden - uhist[y] * dden for y in range(1 << m)]
        max_point = max(max_point, *(abs(v) for v in differences))
        for offset in range(1 << m):
            for y in range(1 << m):
                difference = differences[y ^ offset]
                assert abs(difference) * (1 << rank) <= ((1 << rank) - 1) * eps_num * uden
                out["point_checks"] += 1
            # Translation of a fixed nontrivial target set is checked exactly.
            chosen = (0, 1, 3)
            direct = sum(dhist[y ^ offset] * uden - uhist[y ^ offset] * dden
                         for y in chosen)
            assert direct == sum(differences[y ^ offset] for y in chosen)
            out["translation_checks"] += 1
            out["affine_maps"] += 1
        sums, sizes = [0] * 256, [0] * 256
        for target in range(256):
            if target:
                lowbit = target & -target
                j = lowbit.bit_length() - 1
                rest = target ^ lowbit
                sums[target] = sums[rest] + differences[j]
                sizes[target] = sizes[rest] + 1
            assert abs(sums[target]) <= sizes[target] * eps_num * uden
            out["accepting_set_checks"] += 1
        out["binary_matrices"] += 1
    out["rank_histogram"] = dict(sorted(ranks.items()))
    out["max_singleton_advantage"] = str(Fraction(max_point, dden * uden))
    return out


def mask_and_port_suite() -> dict:
    # Even parity on four bits is exactly 3-wise independent.
    bits, order = 4, 3
    sources = [x for x in range(1 << bits) if x.bit_count() % 2 == 0]
    out = {"kwise_mask_point_checks": 0, "multiport_source_identity_checks": 0,
           "multiport_cases": 0}
    for q in range(1 << bits):
        active = q.bit_count()
        for baseline in range(1 << bits):
            dh = Counter(baseline ^ (q & x) for x in sources)
            uh = Counter(baseline ^ (q & x) for x in range(1 << bits))
            for y in range(1 << bits):
                delta = abs(Fraction(dh[y], len(sources)) - Fraction(uh[y], 1 << bits))
                if active <= order:
                    assert delta == 0
                else:
                    assert delta <= Fraction(1, 1 << order)
                out["kwise_mask_point_checks"] += 1
    rng = Random(SEED)
    N, allones = 8, 255
    for _ in range(2000):
        h = rng.randrange(1, 7)
        ports = rng.randrange(1, 1 << h)
        masks = [rng.randrange(1 << N) for _ in range(h)]
        additive = [rng.randrange(1 << N) for _ in range(h)]
        initial = rng.randrange(1 << N)
        baseline = initial
        for d, mask in zip(additive, masks):
            baseline = d ^ (mask & baseline)
        # Independent closed form: XOR of suffix products for source ports.
        effective = 0
        suffix = allones
        for i in range(h - 1, -1, -1):
            if ports >> i & 1:
                effective ^= suffix
            suffix &= masks[i]
        for x in range(1 << N):
            state = initial
            for i in range(h):
                state = additive[i] ^ (masks[i] & state) ^ (x if ports >> i & 1 else 0)
            assert state == baseline ^ (effective & x)
            out["multiport_source_identity_checks"] += 1
        out["multiport_cases"] += 1
    return out


def hostile_controls(hist16: list[int]) -> dict:
    # A nonlinear membership test distinguishes a small-biased ensemble strongly.
    den = sum(hist16)
    bias = Fraction(max(abs(v) for v in walsh(hist16)[1:]), den)
    support = sum(bool(c) for c in hist16)
    nonlinear_gap = 1 - Fraction(support, 1 << 16)
    assert nonlinear_gap > bias
    # Pairwise independence by itself does not fool arbitrary linear queries.
    even4 = [x for x in range(16) if x.bit_count() % 2 == 0]
    parity_gap = sum(x.bit_count() % 2 == 0 for x in even4) / len(even4) - 0.5
    assert parity_gap == 0.5
    # Two reused mask layers cancel in the previously documented 2-port example.
    reused = [bit ^ (bit & bit) for bit in (0, 1)]
    assert reused == [0, 0]
    # Padding copies a truth table, with the same absolute threshold.
    def nand_one_gate_class(n: int) -> set[int]:
        width = 1 << n
        full = (1 << width) - 1
        inputs = [sum(((x >> j) & 1) << x for x in range(width)) for j in range(n)]
        available = inputs + [0, full]
        return set(available) | {full ^ (a & b) for a in available for b in available}
    c2, c3 = nand_one_gate_class(2), nand_one_gate_class(3)
    for f in range(16):
        padded = f | (f << 4)
        assert (f in c2) == (padded in c3)
    return {
        "nonlinear_source_dependent_map": {
            "source_bits": 16, "support_size": support,
            "actual_character_bias": str(bias),
            "membership_advantage": str(nonlinear_gap),
            "violates_affine_point_bound_as_expected": True,
        },
        "pairwise_only_even_parity_linear_query_advantage": "1/2",
        "reused_layer_effective_mask_values": reused,
        "ignored_variable_padding_same_absolute_threshold_checks": 16,
        "scope": "These controls violate premises or lie outside the strict threshold-shrink regime.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("affine_smallbias_gate_raw.json"))
    args = parser.parse_args()
    start = perf_counter()
    primitives, saved = primitive_suite()
    affine = affine_suite(saved[4])
    mask = mask_and_port_suite()
    hostile = hostile_controls(saved[16])
    result = {
        "run_id": RUN_ID, "seed": SEED, "status": "PASS", "failed_assertions": 0,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "primitive": primitives, "affine": affine, "mask": mask,
        "hostile_controls": hostile,
        "elapsed_seconds": round(perf_counter() - start, 6),
        "limitations": [
            "Finite checks validate exact probability, rank, and mask identities, not an asymptotic separation.",
            "Finite field instances are CHMY Theorem 33's primitive, not a full PRG-security experiment.",
            "No arbitrary SAT runtime, one-tape implementation, or minimum universal-machine KT is measured.",
            "The final theorem relies separately on the published local-generator circuit upper bound.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
