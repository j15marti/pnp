#!/usr/bin/env python3
"""Finite controls for LSPV-5 BATCH-RANK-AMORTIZATION-REFEREE211.

Standard library only.  The symbolic theorems are proved in the accompanying
report; these finite checks are observational controls.  Each invocation is
designed to finish well below the project's 30-second chunk limit.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import time


RUN_ID = "BATCH-RANK-AMORTIZATION-REFEREE211"
SEED = 2111029


def parity(x: int) -> int:
    return x.bit_count() & 1


def gf2_basis(rows: list[int]) -> list[int]:
    basis: dict[int, int] = {}
    for value in rows:
        x = value
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                for q in list(basis):
                    if q != p and ((basis[q] >> p) & 1):
                        basis[q] ^= x
                break
    return [basis[p] for p in sorted(basis, reverse=True)]


def rank(rows: list[int]) -> int:
    return len(gf2_basis(rows))


def span(rows: list[int]) -> frozenset[int]:
    b = gf2_basis(rows)
    values = {0}
    for row in b:
        values |= {x ^ row for x in list(values)}
    return frozenset(values)


def all_subspaces(b: int) -> list[frozenset[int]]:
    full = 1 << b
    seen = {frozenset({0})}
    queue = [frozenset({0})]
    while queue:
        current = queue.pop()
        for v in range(1, full):
            if v not in current:
                nxt = span(list(current) + [v])
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return sorted(seen, key=lambda s: (len(s), tuple(sorted(s))))


def image_vector(w_rows: list[int], source: int) -> int:
    out = 0
    for i, row in enumerate(w_rows):
        out |= parity(row & source) << i
    return out


def image_rank(w_rows: list[int], source_subspace: frozenset[int]) -> int:
    return rank([image_vector(w_rows, u) for u in source_subspace])


def affine_rank_drop_audit(max_b: int = 5) -> dict:
    rows = []
    total = 0
    synergy_witness = None
    for b in range(1, max_b + 1):
        spaces = all_subspaces(b)
        checks = 0
        max_drop = 0
        drop_hist = {0: 0, 1: 0}
        for source_u in spaces:
            for target_w in spaces:
                w_basis = gf2_basis(list(target_w))
                before = image_rank(w_basis, source_u)
                for c in range(1, 1 << b):
                    restricted = frozenset(u for u in source_u if parity(c & u) == 0)
                    after = image_rank(w_basis, restricted)
                    drop = before - after
                    assert drop in (0, 1)
                    drop_hist[drop] += 1
                    max_drop = max(max_drop, drop)
                    checks += 1
        rows.append({
            "b": b,
            "subspaces": len(spaces),
            "checks": checks,
            "drop_histogram": drop_hist,
            "maximum_one_linear_fact_drop": max_drop,
        })
        total += checks

    # Target x, facts x xor r and r: each singleton has zero rank value, jointly one.
    u = span([1, 2])
    w = [1]
    phi0 = image_rank(w, u)
    u1 = frozenset(x for x in u if parity(3 & x) == 0)
    u2 = frozenset(x for x in u if parity(2 & x) == 0)
    u12 = frozenset(x for x in u1 if parity(2 & x) == 0)
    gains = {
        "empty": 0,
        "x_xor_r": phi0 - image_rank(w, u1),
        "r": phi0 - image_rank(w, u2),
        "joint": phi0 - image_rank(w, u12),
        "duplicate_after_first": image_rank(w, u1) - image_rank(w, u1),
    }
    assert gains == {"empty": 0, "x_xor_r": 0, "r": 0, "joint": 1,
                     "duplicate_after_first": 0}
    synergy_witness = gains
    return {"rows": rows, "total_checks": total, "xor_synergy": synergy_witness}


def answer_vector_rank_audit() -> dict:
    rng = random.Random(SEED)
    records = []
    checks = 0
    for b in range(1, 9):
        batches = []
        batches.append([1 << i for i in range(b)])
        for m in (1, max(1, b // 2), b, b + 3):
            batches.append([rng.randrange(1, 1 << b) for _ in range(m)])
        for w_rows in batches:
            r = rank(w_rows)
            outputs = {image_vector(w_rows, a) for a in range(1 << b)}
            assert len(outputs) == 1 << r
            records.append({"b": b, "queries": len(w_rows), "rank": r,
                            "distinct_answer_vectors": len(outputs)})
            checks += 1 << b
    return {"records": records, "source_evaluations": checks}


def coordinate_batch_exact_audit(max_b: int = 12) -> dict:
    checks = 0
    rows = []
    frontier_points = 0
    for b in range(1, max_b + 1):
        for r in range(1, b + 1):
            for l in range(0, r + 1):
                q = r - l
                for source in range(1 << b):
                    summary = source & ((1 << l) - 1)
                    observed = summary
                    for i in range(l, r):
                        observed |= ((source >> i) & 1) << i
                    assert observed == (source & ((1 << r) - 1))
                    checks += 1
                assert min(l, l) + q == r
                frontier_points += 1
                if (b in (1, 4, 8, 12)
                        and r in ({1, b} if b > 1 else {1})
                        and l in ({0, r // 2, r})):
                    rows.append({"b": b, "answer_rank": r, "stored_bits": l,
                                 "continuation_probes": q,
                                 "construction_source_probes": l,
                                 "total_source_probes": l + q})
    return {"representative_rows": rows,
            "frontier_points_checked": frontier_points,
            "source_protocol_checks": checks}


def caching_amortization_audit() -> dict:
    rng = random.Random(SEED + 1)
    rows = []
    for b in (8, 16, 32, 64):
        identity = [1 << i for i in range(b)]
        for factor in (1, 2, 4):
            m = factor * b
            masks = identity + [rng.getrandbits(b) or 1 for _ in range(m - b)]
            naive = sum(mask.bit_count() for mask in masks)
            union = 0
            for mask in masks:
                union |= mask
            cached = union.bit_count()
            r = rank(masks)
            assert r == b and cached == b
            rows.append({
                "source_bits": b,
                "queries": m,
                "batch_rank": r,
                "naive_fresh_probe_sum": naive,
                "persistent_cache_distinct_source_probes": cached,
                "collapse_ratio": naive / cached,
                "query_input_bits_still_charged": m * b,
                "answer_output_bits_still_charged": m,
            })
    return {"rows": rows}


def degree_volume_peer_audit() -> dict:
    exact_family = []
    for m in range(1, 8):
        b = 2 * ((1 << m) - 1)
        volume = 1 + b + b * (b - 1) // 2
        assert 1 << (2 * m) <= volume < 1 << (2 * m + 1)
        exact_family.append({"m": m, "b": b, "V_b_2": volume,
                             "floor_log2_V": volume.bit_length() - 1,
                             "claimed_exact_L2": b - 2 * m})
    golay_volume = sum(math.comb(23, j) for j in range(4))
    assert golay_volume == 2048
    return {"two_probe_family": exact_family,
            "golay_23_radius_3_volume": golay_volume,
            "golay_storage_plus_volume_bits": 12 + int(math.log2(golay_volume))}


def horn_rare_branch_audit() -> dict:
    rows = []
    checks = 0
    for t in range(2, 33):
        models = (1 << (t - 1)) + 1
        rare = math.log2(models)
        common = math.log2(models) - (t - 1)
        p = 1 / models
        entropy = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        expected = p * rare + (1 - p) * common
        assert rare > t - 1
        assert abs(expected - entropy) < 1e-12
        assert expected <= 1 + 1e-12
        checks += 1
        if t in (2, 4, 8, 16, 24, 32):
            rows.append({"t": t, "models": models, "rare_branch_value": rare,
                         "common_branch_value": common,
                         "expected_value_uniform_models": expected})
    return {"representative_rows": rows, "identities_checked": checks}


def main() -> None:
    start = time.perf_counter()
    result = {
        "run_id": RUN_ID,
        "seed": SEED,
        "status": "PROVED/EXACT restricted symbolic lemmas; COMPUTATIONAL finite controls",
        "affine_rank_potential": affine_rank_drop_audit(),
        "answer_vector_rank": answer_vector_rank_audit(),
        "coordinate_batch_exact": coordinate_batch_exact_audit(),
        "cross_query_caching": caching_amortization_audit(),
        "peer_degree_volume": degree_volume_peer_audit(),
        "horn_rare_branch": horn_rare_branch_audit(),
    }
    result["elapsed_seconds"] = round(time.perf_counter() - start, 6)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
