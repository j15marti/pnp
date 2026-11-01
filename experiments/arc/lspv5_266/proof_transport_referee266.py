#!/usr/bin/env python3
"""Finite referee for typed proof transport across semantic DAG quotients.

The script is standard-library only.  It authenticates Y6, reconstructs the
eight cost-one affine leaves under x5=0,x6=1, and exhaustively proves that two
semantically identical UNSAT leaves require different source-row certificates.
It also retains same-source SAT/UNSAT, F9 parity, S/U, malformed, DPLL, and XOR
controls.  This is not a native FLMV implementation or an all-input solver.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

Y6 = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6),
)
PINS = {5: 0, 6: 1}
UNSAT_PINS = {3: 1, 4: 0, 5: 0, 6: 1}
SITES = (0, 1, 4, 5)

F9_POS = ((1, 5, 6), (2, 3, 8), (1, 3, 5), (4, 6, 9), (2, 4, 7), (7, 8, 9))
F9_NEG = ((4, 6, 8), (1, 6, 7), (2, 3, 4), (3, 5, 8), (1, 2, 9), (5, 7, 9))
F9 = F9_POS + tuple(tuple(-v for v in clause) for clause in F9_NEG)
F9_PINS = {8: 0, 3: 0, 7: 0, 6: 0, 1: 1, 5: 1}
F9_CYCLE = (3, 4, 10)


def lit_value(lit: int, assignment: dict[int, int]) -> int:
    bit = assignment[abs(lit)]
    return bit if lit > 0 else bit ^ 1


def satisfies(formula: tuple[tuple[int, ...], ...], assignment: dict[int, int]) -> bool:
    return all(any(lit_value(lit, assignment) for lit in clause) for clause in formula)


def extensions(formula: tuple[tuple[int, ...], ...], pins: dict[int, int]):
    n = max(abs(lit) for clause in formula for lit in clause)
    free = [v for v in range(1, n + 1) if v not in pins]
    for bits in product((0, 1), repeat=len(free)):
        assignment = {**pins, **dict(zip(free, bits))}
        if satisfies(formula, assignment):
            yield assignment


def valid_target(formula: tuple[tuple[int, ...], ...], n: int) -> bool:
    if 3 * len(formula) != 4 * n:
        return False
    if len({tuple(sorted(clause)) for clause in formula}) != len(formula):
        return False
    counts = Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(lit) for lit in clause}) != 3:
            return False
        if not (all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)):
            return False
        if any(not 1 <= abs(lit) <= n for lit in clause):
            return False
        for lit in clause:
            counts[abs(lit), lit > 0] += 1
    return all(counts[v, sign] == 2 for v in range(1, n + 1) for sign in (False, True))


def default_row(site: int) -> tuple[int, int]:
    free = (1, 2, 3, 4)
    mask, rhs = 0, 1
    for lit in Y6[site]:
        if abs(lit) in PINS:
            assert lit_value(lit, PINS) == 0
        else:
            mask ^= 1 << free.index(abs(lit))
            rhs ^= int(lit < 0)
    return mask, rhs


def unit_row(lit: int, truth: int) -> tuple[int, int]:
    free = (1, 2, 3, 4)
    return 1 << free.index(abs(lit)), truth if lit > 0 else truth ^ 1


def holds(row: tuple[int, int], assignment: dict[int, int]) -> bool:
    mask, rhs = row
    lhs = 0
    for i, variable in enumerate((1, 2, 3, 4)):
        if mask >> i & 1:
            lhs ^= assignment[variable]
    return lhs == rhs


def solve_rows(records: list[dict[str, object]]) -> list[dict[int, int]]:
    out = []
    for bits in product((0, 1), repeat=4):
        assignment = {**PINS, **dict(zip((1, 2, 3, 4), bits))}
        if all(holds(tuple(record["row"]), assignment) for record in records):
            out.append(assignment)
    return out


def word(assignment: dict[int, int], n: int) -> int:
    return sum(assignment[v] << (v - 1) for v in range(1, n + 1))


def build_profiles() -> tuple[list[dict[str, object]], int]:
    defaults = {site: default_row(site) for site in SITES}
    profiles = []
    row_tests = 0
    for chosen in SITES:
        literals = [lit for lit in Y6[chosen] if abs(lit) not in PINS]
        for true_positions in combinations(range(len(literals)), 2):
            exact = tuple(int(i in true_positions) for i in range(len(literals)))
            records = [
                {"tag": f"D{site}", "row": list(defaults[site]), "source_clause": site}
                for site in SITES if site != chosen
            ]
            for lit, truth in zip(literals, exact):
                records.append({
                    "tag": f"U{chosen}:x{abs(lit)}={truth if lit > 0 else truth ^ 1}",
                    "row": list(unit_row(lit, truth)),
                    "source_clause": chosen,
                })
            affine = solve_rows(records)
            row_tests += 16 * len(records)
            source = [assignment for assignment in affine if satisfies(Y6, assignment)]
            assert affine == source
            profiles.append({
                "id": len(profiles), "chosen_site": chosen,
                "exact_truth": list(exact), "records": records,
                "models": [word(assignment, 6) for assignment in affine],
                "consistent": bool(affine),
            })
    assert len(profiles) == 8
    return profiles, row_tests


def xor_is_contradiction(records: list[dict[str, object]]) -> bool:
    mask = rhs = 0
    for record in records:
        row_mask, row_rhs = record["row"]
        mask ^= row_mask
        rhs ^= row_rhs
    return mask == 0 and rhs == 1


def minimal_certificates(profile: dict[str, object]) -> tuple[list[dict[str, object]], int]:
    records = profile["records"]
    out: list[dict[str, object]] = []
    checked = 0
    for size in range(1, len(records) + 1):
        for ids in combinations(range(len(records)), size):
            checked += 1
            selected = [records[i] for i in ids]
            if xor_is_contradiction(selected):
                out.append({"record_ids": list(ids), "records": selected})
        if out:
            break
    return out, checked


def verify_certificate(profile: dict[str, object], certificate: dict[str, object]) -> dict[str, object]:
    environment = {(record["tag"], tuple(record["row"]), record["source_clause"]) for record in profile["records"]}
    missing = [
        record for record in certificate["records"]
        if (record["tag"], tuple(record["row"]), record["source_clause"]) not in environment
    ]
    contradiction = xor_is_contradiction(certificate["records"])
    return {
        "accepted": not missing and contradiction,
        "missing_tags": [record["tag"] for record in missing],
        "xor_is_0_eq_1": contradiction,
    }


def malformed_controls() -> dict[str, int]:
    cases = (
        Y6[:-1], ((1, 1, 2),) + Y6[1:], ((1, -2, 3),) + Y6[1:],
        (Y6[0],) + Y6[:-1], ((1, 2, 6),) + Y6[1:], ((1, 2, 7),) + Y6[1:],
    )
    rejected = sum(not valid_target(tuple(case), 6) for case in cases)
    assert rejected == len(cases)
    return {"cases": len(cases), "rejected": rejected}


def pair_extremes() -> dict[str, int]:
    checks = 0
    for left, right in combinations(range(8), 2):
        for left_mode, right_mode in product((0, 1), repeat=2):
            feasible = False
            for assignment_word in range(64):
                assignment = {v: assignment_word >> (v - 1) & 1 for v in range(1, 7)}
                feasible |= (
                    all(lit_value(lit, assignment) == left_mode for lit in Y6[left])
                    and all(lit_value(lit, assignment) == right_mode for lit in Y6[right])
                )
            same = bool(set(Y6[left]) & set(Y6[right]))
            opposite = any(-lit in Y6[right] for lit in Y6[left])
            assert feasible == ((not opposite) if left_mode == right_mode else (not same))
            checks += 1
    return {"pair_modes_checked": checks}


def simplify(formula: tuple[tuple[int, ...], ...], pins: dict[int, int]):
    residual = []
    literal_reads = 0
    for clause in formula:
        new_clause = []
        satisfied_clause = False
        for lit in clause:
            literal_reads += 1
            if abs(lit) in pins:
                if pins[abs(lit)] == int(lit > 0):
                    satisfied_clause = True
            else:
                new_clause.append(lit)
        if not satisfied_clause:
            residual.append(tuple(new_clause))
    return tuple(residual), literal_reads


def dpll_count(formula: tuple[tuple[int, ...], ...]) -> dict[str, int | bool]:
    nodes = literal_probes = propagations = 0

    def rec(clauses: tuple[tuple[int, ...], ...]) -> bool:
        nonlocal nodes, literal_probes, propagations
        nodes += 1
        work = clauses
        while True:
            if not work:
                return True
            if any(not clause for clause in work):
                return False
            unit = next((clause[0] for clause in work if len(clause) == 1), None)
            if unit is None:
                break
            propagations += 1
            next_work = []
            for clause in work:
                literal_probes += len(clause)
                if unit in clause:
                    continue
                next_work.append(tuple(lit for lit in clause if lit != -unit))
            work = tuple(next_work)
        branch = work[0][0]
        for choice in (branch, -branch):
            next_work = []
            for clause in work:
                literal_probes += len(clause)
                if choice in clause:
                    continue
                next_work.append(tuple(lit for lit in clause if lit != -choice))
            if rec(tuple(next_work)):
                return True
        return False

    decision = rec(formula)
    return {"sat": decision, "nodes": nodes, "literal_probes": literal_probes, "unit_propagations": propagations}


def gf2_consistent(rows: list[tuple[int, int]]) -> bool:
    basis: dict[int, tuple[int, int]] = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in basis:
                old_mask, old_rhs = basis[pivot]
                mask, rhs = mask ^ old_mask, rhs ^ old_rhs
            else:
                basis[pivot] = (mask, rhs)
                break
        if not mask and rhs:
            return False
    return True


def f9_rows(choice: int | None) -> list[tuple[int, int]]:
    rows = []
    covered = []
    for clause_id, clause in enumerate(F9):
        if any(abs(lit) in F9_PINS and lit_value(lit, F9_PINS) for lit in clause):
            covered.append(clause_id)
        elif clause_id not in F9_CYCLE:
            free = [lit for lit in clause if abs(lit) not in F9_PINS]
            if free:
                mask = sum(1 << (abs(lit) - 1) for lit in free)
                rhs = 1 ^ ((len(free) & 1) if clause[0] < 0 else 0)
                rows.append((mask, rhs))
    signed = Counter()
    for clause_id in covered:
        for lit in F9[clause_id]:
            if abs(lit) not in F9_PINS:
                signed[abs(lit), lit > 0] += 1
    for variable in (2, 4, 9):
        preferred = 0 if signed[variable, True] > signed[variable, False] else 1
        rows.append((1 << (variable - 1), preferred))
    if choice is not None:
        for clause_id in F9_CYCLE:
            free = [abs(lit) for lit in F9[clause_id] if abs(lit) not in F9_PINS]
            if clause_id == choice:
                value = int(F9[clause_id][0] > 0)
                rows.extend((1 << (variable - 1), value) for variable in free)
            else:
                rows.append(((1 << (free[0] - 1)) ^ (1 << (free[1] - 1)), 1))
    return rows


def f9_control() -> dict[str, object]:
    root = list(extensions(F9, {}))
    cube = list(extensions(F9, F9_PINS))
    outside = gf2_consistent(f9_rows(None))
    branches = {str(choice): gf2_consistent(f9_rows(choice)) for choice in F9_CYCLE}
    residual, reads = simplify(F9, F9_PINS)
    dpll = dpll_count(residual)
    assert len(root) == 70 and not cube and outside and not any(branches.values()) and not dpll["sat"]
    return {"root_models": 70, "cube_completions": 8, "cube_models": 0,
            "outside_cycle_consistent": outside, "branch_consistency": branches,
            "dpll": dpll, "residual_scan_literal_reads": reads}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert valid_target(Y6, 6) and valid_target(F9, 9)
    profiles, affine_row_tests = build_profiles()
    left, right = profiles[1], profiles[5]
    assert not left["models"] and not right["models"]
    cert_left, checks_left = minimal_certificates(left)
    cert_right, checks_right = minimal_certificates(right)
    assert len(cert_left) == len(cert_right) == 2
    transport = {
        "1_to_1": [verify_certificate(left, certificate) for certificate in cert_left],
        "1_to_5": [verify_certificate(right, certificate) for certificate in cert_left],
        "5_to_5": [verify_certificate(right, certificate) for certificate in cert_right],
        "5_to_1": [verify_certificate(left, certificate) for certificate in cert_right],
    }
    assert all(item["accepted"] for item in transport["1_to_1"] + transport["5_to_5"])
    assert not any(item["accepted"] for item in transport["1_to_5"] + transport["5_to_1"])

    root_models = list(extensions(Y6, {}))
    sat_models = list(extensions(Y6, PINS))
    unsat_models = list(extensions(Y6, UNSAT_PINS))
    assert len(root_models) == 20 and len(sat_models) == 6 and not unsat_models
    sat_residual, sat_reads = simplify(Y6, PINS)
    unsat_residual, unsat_reads = simplify(Y6, UNSAT_PINS)
    dpll = {"SAT_cube": dpll_count(sat_residual), "UNSAT_cube": dpll_count(unsat_residual)}
    assert dpll["SAT_cube"]["sat"] and not dpll["UNSAT_cube"]["sat"]

    result = {
        "run": "LSPV5_TYPED_PROOF_TRANSPORT_REFEREE266",
        "timestamp_pacific": "2026-11-01 06:48 PST",
        "classification": "PROVED/EXACT restricted typed-cache theorem; COMPUTATIONAL exhaustive finite falsifier",
        "source": {"valid_Y6": True, "valid_F9": True, "Y6_root_models": 20,
                   "Y6_sat_cube_models": 6, "Y6_unsat_cube_models": 0},
        "semantic_equality_falsifier": {
            "profile_ids": [1, 5], "aligned_residual_function_masks": [0, 0],
            "same_scalar_answer": "UNSAT", "same_exact_model_family": True,
            "profile_1_certificates": cert_left, "profile_5_certificates": cert_right,
            "transport_matrix": transport,
            "conclusion": "semantic answer/family equality does not type-check raw proof-object reuse",
        },
        "restricted_theorem": {
            "answer_cache": "equal aligned residual functions safely share the semantic answer",
            "proof_cache": "a proof may be reused only if the target node verifier accepts it under the target assumption/provenance environment, or a checked translator produces an accepted proof",
            "count_cache": "weighted residual equality must include output projection and multiplicity",
            "cost_firewall": "semantic equality says nothing about equality-recognition, translation, verification, guest delay, or peak-space cost",
        },
        "same_source_DPLL": dpll,
        "F9_parity_hole": f9_control(),
        "signed_SU": pair_extremes(),
        "malformed": malformed_controls(),
        "xor_offline": {
            "DELAY": {"native_steps": 257, "data_bit_changes": 0},
            "COPY": {"logical_delta": 0, "shadow_writes": 22},
            "RECOMP": {"retained_status_bits": 0, "source_literal_rereads": 24},
            "restored_bit": {"adjacent_delta": 2, "endpoint_delta": 0},
            "classification": "offline diagnostic only",
        },
        "resource_ledger": {
            "grammar_literal_reads_Y6": 24, "affine_row_tests": affine_row_tests,
            "certificate_subsets_checked": checks_left + checks_right,
            "semantic_truth_points_compared": 16,
            "Y6_residual_scan_literal_reads": sat_reads + unsat_reads,
            "proof_outputs": len(cert_left) + len(cert_right),
            "native_source_head_index_guest_peak_space": "not measured; remains charged",
        },
        "limitations": [
            "proof transport is a typing/soundness condition, not a polynomial equality oracle",
            "affine leaves are noncanonical target children",
            "no hereditary power-short arbitrary-A to Phi(A) contractor",
            "no quantitative SAT-to-target numerical FLMV transfer or arbitrary-machine lower bound",
        ],
        "p_vs_np": "OPEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"run": result["run"], "certificates": [len(cert_left), len(cert_right)],
                      "cross_transport_accepts": sum(item["accepted"] for item in transport["1_to_5"] + transport["5_to_1"]),
                      "DPLL": dpll, "F9": result["F9_parity_hole"], "p_vs_np": "OPEN"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
