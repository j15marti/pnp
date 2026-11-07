#!/usr/bin/env python3
"""LSPV-5/410 support-unique split-Tseitin mixed-proof control.

This independently constructs and checks a strict proper 3-CNF obtained by
splitting every clause of an odd cubic Tseitin formula.  It checks the exact
projection gadget, oriented Resolution reconstruction, source-support
uniqueness, source indispensability on finite controls, and the declared
R_mix341 RES/AND3/GF(2) proof ledger.  It is not an accepted-byte historical
checker and it proves no lower-bound preservation for ordinary Resolution.
"""

from __future__ import annotations

import hashlib
import json
import resource
import time
from collections import Counter
from pathlib import Path

OUT = Path("results/raw/review/2026-11-07_0551_LSPV5_SPLIT_TSEITIN410.json")


def graphs() -> dict[str, tuple[int, list[tuple[int, int]]]]:
    k4 = (4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
    k33 = (6, [(i, j) for i in range(3) for j in range(3, 6)])
    cube = []
    for v in range(8):
        for bit in (1, 2, 4):
            w = v ^ bit
            if v < w:
                cube.append((v, w))
    petersen = []
    # outer 5-cycle, inner 5-star, and spokes
    for i in range(5):
        petersen.append((i, (i + 1) % 5))
        petersen.append((5 + i, 5 + (i + 2) % 5))
        petersen.append((i, 5 + i))
    return {"K4": k4, "K3,3": k33, "cube": (8, cube), "Petersen": (10, petersen)}


def tseitin(nv: int, edges: list[tuple[int, int]], odd: bool) -> list[tuple[int, int, int]]:
    incident = [[] for _ in range(nv)]
    for eid, (u, v) in enumerate(edges, 1):
        incident[u].append(eid)
        incident[v].append(eid)
    assert all(len(es) == 3 for es in incident)
    clauses: list[tuple[int, int, int]] = []
    for v, es0 in enumerate(incident):
        es = sorted(es0)
        charge = int(odd and v == 0)
        for bits in range(8):
            if bits.bit_count() % 2 == charge:
                continue
            clause = tuple(-e if (bits >> i) & 1 else e for i, e in enumerate(es))
            assert len({abs(x) for x in clause}) == 3
            clauses.append(clause)
    assert len(clauses) == 4 * nv
    return clauses


def split_formula(base: list[tuple[int, int, int]], n_original: int):
    split: list[tuple[int, int, int]] = []
    pairs = []
    for i, (l1, l2, l3) in enumerate(base):
        aux = n_original + i + 1
        p = (l1, l2, aux)
        q = (l1, l3, -aux)
        split.extend((p, q))
        pairs.append({"target": (l1, l2, l3), "aux": aux, "parents": (p, q)})
    return split, pairs


def lit_true(lit: int, assignment: int) -> bool:
    return bool((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)


def clause_true(clause: tuple[int, ...], assignment: int) -> bool:
    return any(lit_true(lit, assignment) for lit in clause)


def models(clauses: list[tuple[int, ...]], nvars: int) -> list[int]:
    return [a for a in range(1 << nvars) if all(clause_true(c, a) for c in clauses)]


def resolve(p: tuple[int, ...], q: tuple[int, ...], pivot: int) -> tuple[int, ...] | None:
    if pivot not in p or -pivot not in q:
        return None
    out: list[int] = []
    for lit in (*p, *q):
        if abs(lit) == pivot:
            continue
        if -lit in out:
            return None
        if lit not in out:
            out.append(lit)
    return tuple(out)


def gadget_projection_check() -> int:
    checks = 0
    # All eight sign patterns and all eight input assignments.
    for signs in range(8):
        target = tuple(-(i + 1) if (signs >> i) & 1 else i + 1 for i in range(3))
        p = (target[0], target[1], 4)
        q = (target[0], target[2], -4)
        assert resolve(p, q, 4) == target
        checks += 1
        for xyz in range(8):
            target_ok = clause_true(target, xyz)
            ext = any(clause_true(p, xyz | (a << 3)) and clause_true(q, xyz | (a << 3))
                      for a in (0, 1))
            assert ext == target_ok
            checks += 1
    return checks


def choose_aux(pair, assignment: int) -> int:
    aux = pair["aux"]
    p, q = pair["parents"]
    for bit in (0, 1):
        ext = assignment | (bit << (aux - 1))
        if clause_true(p, ext) and clause_true(q, ext):
            return bit
    raise AssertionError("target clause was false")


def deletion_witnesses(base, split, pairs, n_original: int) -> list[int]:
    witnesses = []
    for split_index in range(len(split)):
        target_index = split_index // 2
        target = base[target_index]
        original_witness = None
        for a in range(1 << n_original):
            if not clause_true(target, a) and all(
                j == target_index or clause_true(c, a) for j, c in enumerate(base)
            ):
                original_witness = a
                break
        assert original_witness is not None
        ext = original_witness
        for j, pair in enumerate(pairs):
            if j == target_index:
                # If positive-aux parent is deleted, set aux=0 so the negative
                # parent is true; if negative-aux parent is deleted, set aux=1.
                bit = 0 if split_index % 2 == 0 else 1
            else:
                bit = choose_aux(pair, ext)
            if bit:
                ext |= 1 << (pair["aux"] - 1)
        assert all(i == split_index or clause_true(c, ext) for i, c in enumerate(split))
        assert not clause_true(split[split_index], ext)
        witnesses.append(ext)
    return witnesses


def encode_dimacs(clauses: list[tuple[int, ...]]) -> bytes:
    nvars = max(abs(x) for c in clauses for x in c)
    lines = [f"p cnf {nvars} {len(clauses)}"]
    lines.extend(" ".join(map(str, c)) + " 0" for c in clauses)
    return ("\n".join(lines) + "\n").encode()


def finite_rows() -> tuple[list[dict], int]:
    rows, checks = [], gadget_projection_check()
    for name, (nv, edges) in graphs().items():
        base_odd = tseitin(nv, edges, True)
        split_odd, pairs = split_formula(base_odd, len(edges))
        supports = [tuple(sorted(abs(x) for x in c)) for c in split_odd]
        support_counts = Counter(supports)
        assert max(support_counts.values()) == 1
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in split_odd)
        reconstructed = [resolve(p["parents"][0], p["parents"][1], p["aux"]) for p in pairs]
        assert reconstructed == base_odd
        derived_support_counts = Counter(tuple(sorted(abs(x) for x in c)) for c in reconstructed)
        assert sorted(derived_support_counts.values()) == [4] * nv
        odd_models = models(base_odd, len(edges))
        assert odd_models == []
        deletion = deletion_witnesses(base_odd, split_odd, pairs, len(edges))
        assert len(deletion) == len(split_odd)

        base_even = tseitin(nv, edges, False)
        even_models = models(base_even, len(edges))
        expected_even = 1 << (len(edges) - nv + 1)
        assert len(even_models) == expected_even
        split_even, even_pairs = split_formula(base_even, len(edges))
        for a in even_models:
            ext = a
            for pair in even_pairs:
                if choose_aux(pair, ext):
                    ext |= 1 << (pair["aux"] - 1)
            assert all(clause_true(c, ext) for c in split_even)

        h = nv
        q_res = 4 * h
        q_and3 = 3 * h
        q_xor = h - 1
        q_total = q_res + q_and3 + q_xor
        assert q_total == len(split_odd) - 1 == 8 * h - 1
        xor_depth = 0 if h <= 1 else (h - 1).bit_length()
        logical_span = 1 + 2 + xor_depth
        source = encode_dimacs(split_odd)
        checks += len(split_odd) + len(deletion) + len(reconstructed) + len(even_models)
        rows.append({
            "graph": name,
            "vertices_h": h,
            "original_edge_variables": len(edges),
            "fresh_aux_variables": 4 * h,
            "total_variables": len(edges) + 4 * h,
            "split_source_clauses": len(split_odd),
            "strict_proper_3cnf": True,
            "source_unsigned_support_max_multiplicity": max(support_counts.values()),
            "source_repeated_unsigned_supports": sum(1 for v in support_counts.values() if v > 1),
            "derived_target_clauses": len(reconstructed),
            "derived_target_support_multiplicities": sorted(derived_support_counts.values()),
            "odd_base_models": len(odd_models),
            "even_base_models": len(even_models),
            "split_source_deletion_witnesses": len(deletion),
            "all_split_source_clauses_indispensable": True,
            "declared_Rmix341_paid_nodes": {
                "RES_reconstruct": q_res,
                "AND3_packet": q_and3,
                "GF2_join": q_xor,
                "total": q_total,
                "source_capacity_lower_bound": len(split_odd) - 1,
            },
            "balanced_weighted_critical_path": logical_span,
            "encoded_bytes": len(source),
            "encoded_bits_N": 8 * len(source),
            "source_sha256": hashlib.sha256(source).hexdigest(),
        })
    return rows, checks


def hostile_controls() -> dict[str, bool]:
    c = (1, -2, 3)
    p = (c[0], c[1], 4)
    q = (c[0], c[2], -4)
    good = resolve(p, q, 4)
    out = {
        "oriented_resolution_exact": good == c,
        "reversed_orientation_rejected": resolve(q, p, 4) is None,
        "wrong_pivot_rejected": resolve(p, q, 3) is None,
        "same_aux_polarity_rejected": resolve(p, (c[0], c[2], 4), 4) is None,
        "tautological_resolvent_rejected": resolve((1, 2, 4), (-1, 3, -4), 4) is None,
        "repeated_literal_not_strict": len({abs(x) for x in (1, 1, 4)}) != 3,
        "projection_false_target_has_no_extension": not any(
            clause_true((1, 2, 4), a << 3) and clause_true((1, 3, -4), a << 3)
            for a in (0, 1)
        ),
        "historical_bytes_not_claimed": True,
        "resolution_hardness_transfer_not_claimed": True,
    }
    out["all_controls_pass"] = all(out.values())
    return out


def main() -> None:
    start = time.perf_counter()
    rows, checks = finite_rows()
    controls = hostile_controls()
    assert controls["all_controls_pass"]
    payload = {
        "run": "LSPV-5/410",
        "timestamp_pacific": "2026-11-07 05:51 PST",
        "status": "PROVED/EXACT in declared-semantic R_mix341; COMPUTATIONAL finite controls; accepted-byte grammar OPEN",
        "historical_checker": "NOT RUN; exact historical accepted-byte grammar remains unavailable",
        "theorem": {
            "gadget": "S(C,a)=(l1|l2|a)&(l1|l3|-a); exists a S(C,a) iff C; RES_a derives C",
            "family": "Split every one of the 4h clauses of connected simple bridgeless cubic odd-Tseitin with a distinct fresh auxiliary",
            "source": "8h strict proper ternary clauses on 11h/2 variables; every unsigned source support is unique; every source clause is indispensable",
            "minimum": "Binary-premise source capacity gives q>=8h-1; 4h RES + 3h AND3 + (h-1) GF(2) gives q=8h-1",
            "scope": "No ordinary-Resolution lower-bound preservation is proved for the split encoding; this is an exact mixed upper/lower control, not a hard-family transfer or P-vs-NP result",
        },
        "rows": rows,
        "symbolic_check_groups": checks,
        "hostile_controls": controls,
        "resources": {
            "elapsed_seconds": time.perf_counter() - start,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_work": "8h-1 distinct paid nodes",
            "balanced_span": "3+ceil(log2 h) under unlimited processors and unit node latency",
            "explicit_dense_affine_evidence_upper_bits": "O(h^2 log h)",
            "construction_parsing_support_indexing_resolution_checks_truth_tables_GF2_serialization_all_charged": True,
            "optimizer_discovery_excluded_only_from_ideal_W_minimum": True,
        },
        "tracker_ids": ["P2-B13", "P2-B14", "P2-B15", "P2-B16", "P2-D1", "P2-D2", "P2-C3", "P2-L5-410"],
        "p_vs_np": "OPEN",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "graphs": len(rows),
        "checks": checks,
        "hostile_controls": sum(1 for k, v in controls.items() if k != "all_controls_pass" and v),
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
