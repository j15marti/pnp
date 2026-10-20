#!/usr/bin/env python3
"""Exact audit for AFFINE-DUAL-STREAM-OBSTRUCTION35.

An affine map from D=N+d source/advice bits to M>D target bits has a
nonzero dual parity check.  The audit exhausts small matrices and verifies the
resulting one-pass parity distinguisher, image cardinality, and the side-advice
dimension threshold.  This is not a minimum-KT computation or SAT lower bound.
"""

from hashlib import sha256
import json


def parity(x: int) -> int:
    return x.bit_count() & 1


def rank_gf2(rows, width):
    rows = list(rows)
    rank = 0
    for col in range(width - 1, -1, -1):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def dependency(rows):
    """Return a nonzero v with XOR_{i:v_i=1} rows[i] = 0, if one exists."""
    m = len(rows)
    for v in range(1, 1 << m):
        acc = 0
        for i, row in enumerate(rows):
            if (v >> i) & 1:
                acc ^= row
        if acc == 0:
            return v
    return None


def encode(rows, h, x):
    y = 0
    for i, row in enumerate(rows):
        y |= (parity(row & x) ^ ((h >> i) & 1)) << i
    return y


def canonical_masks(m):
    if m <= 4:
        return range(1 << m)
    vals = {0, (1 << m) - 1}
    vals.add(sum(1 << i for i in range(0, m, 2)))
    vals.add(sum(1 << i for i in range(1, m, 2)))
    for i in range(m):
        vals.add(1 << i)
    return sorted(vals)


def run():
    matrices = 0
    affine_instances = 0
    source_points = 0
    relation_checks = 0
    image_checks = 0
    rank_checks = 0
    advice_boundary_checks = 0
    assertions = 0

    # Exhaust all small affine maps with M>D.  The product cap keeps the audit
    # exhaustive while covering 38,268 distinct matrices.
    for d in range(1, 5):
        for m in range(d + 1, 6):
            if d * m > 16:
                continue
            for matrix_code in range(1 << (d * m)):
                rows = [(matrix_code >> (i * d)) & ((1 << d) - 1) for i in range(m)]
                matrices += 1
                v = dependency(rows)
                assert v is not None
                assertions += 1
                rank = rank_gf2(rows, d)
                assert rank < m
                assertions += 1
                rank_checks += 1
                for h in canonical_masks(m):
                    affine_instances += 1
                    rhs = parity(v & h)
                    image = set()
                    for x in range(1 << d):
                        y = encode(rows, h, x)
                        image.add(y)
                        assert parity(v & y) == rhs
                        assertions += 1
                        relation_checks += 1
                        source_points += 1
                    assert len(image) == 1 << rank
                    assert len(image) <= 1 << d
                    assertions += 2
                    image_checks += 1

    # Exact side-information threshold: avoiding dimension-forced parity
    # requires D=N+d >= M, hence d >= M-N.  Identity rows witness sufficiency
    # at the linear-algebra level when the bound holds.
    for n in range(1, 9):
        for m in range(n + 1, 13):
            for side in range(0, 13):
                total = n + side
                forced = total < m
                assert forced == (side < m - n)
                assertions += 1
                if total >= m:
                    rows = [1 << i for i in range(m)]
                    assert rank_gf2(rows, total) == m
                    assert dependency(rows) is None
                    assertions += 2
                advice_boundary_checks += 1

    # High-dual-distance positive control: the systematic [7,4,3] Hamming
    # code has dual minimum weight 4.  Weight four still needs only one parity
    # accumulator during a forward scan.
    hamming_rows = [
        0b0001, 0b0010, 0b0100, 0b1000,
        0b1011, 0b1101, 0b1110,
    ]
    dependencies = []
    for v in range(1, 1 << 7):
        acc = 0
        for i, row in enumerate(hamming_rows):
            if (v >> i) & 1:
                acc ^= row
        if acc == 0:
            dependencies.append(v)
    weights = [v.bit_count() for v in dependencies]
    assert len(dependencies) == 7
    assert min(weights) == max(weights) == 4
    assertions += 2
    for h in canonical_masks(7):
        v = dependencies[0]
        for x in range(16):
            y = encode(hamming_rows, h, x)
            assert parity(v & y) == parity(v & h)
            assertions += 1
            relation_checks += 1

    result = {
        "name": "AFFINE-DUAL-STREAM-OBSTRUCTION35",
        "status": "exact affine obstruction; nonlinear totalization and ARC contractor OPEN; P versus NP OPEN",
        "exhaustive_matrices": matrices,
        "affine_mask_instances": affine_instances,
        "source_points_checked": source_points,
        "parity_relation_checks": relation_checks,
        "image_cardinality_checks": image_checks,
        "rank_checks": rank_checks,
        "side_advice_boundary_checks": advice_boundary_checks,
        "instrumented_assertions": assertions,
        "failures": 0,
        "theorem": {
            "domain_dimension": "D=N+d",
            "forced_relation_condition": "M>D",
            "minimum_side_information_to_avoid_dimension_forcing": "d>=M-N",
            "distinguisher_memory": "one parity bit when support membership is uniformly streamable",
            "length_specific_control_states": "O(M) when the parity support is hardwired",
            "uniformity_firewall": "a uniform CHMY transfer must generate support membership within the claimed machine resources"
        },
        "hamming_7_4_control": {
            "dual_relations": len(dependencies),
            "minimum_dual_weight": min(weights),
            "maximum_dual_weight": max(weights),
            "streaming_accumulator_bits": 1
        },
        "scope_firewall": [
            "does not rule out genuinely nonlinear encoders",
            "does not turn length-specific testers into one uniform machine",
            "does not construct a SAT-to-MKTP reduction",
            "does not construct an all-input ARC successor",
            "does not prove P unequal NP"
        ]
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["audit_sha256"] = sha256(canonical.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
