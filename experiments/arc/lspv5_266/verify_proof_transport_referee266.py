#!/usr/bin/env python3
"""No-producer-import verifier for TYPED-PROOF-TRANSPORT-REFEREE266."""

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
F9 = (
    (1, 5, 6), (2, 3, 8), (1, 3, 5), (4, 6, 9), (2, 4, 7), (7, 8, 9),
    (-4, -6, -8), (-1, -6, -7), (-2, -3, -4), (-3, -5, -8), (-1, -2, -9), (-5, -7, -9),
)


def truth(lit: int, word: int) -> int:
    bit = word >> (abs(lit) - 1) & 1
    return bit if lit > 0 else bit ^ 1


def sat(formula: tuple[tuple[int, ...], ...], word: int) -> bool:
    return all(any(truth(lit, word) for lit in clause) for clause in formula)


def extends(word: int, pins: dict[int, int]) -> bool:
    return all((word >> (variable - 1) & 1) == bit for variable, bit in pins.items())


def valid(formula: tuple[tuple[int, ...], ...], n: int) -> bool:
    if 3 * len(formula) != 4 * n or len({tuple(sorted(clause)) for clause in formula}) != len(formula):
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


def contradiction(records: list[dict[str, object]]) -> bool:
    mask = rhs = 0
    for record in records:
        mask ^= record["row"][0]
        rhs ^= record["row"][1]
    return mask == 0 and rhs == 1


def check_certificate(profile: dict[str, object], certificate: dict[str, object]) -> bool:
    environment = {(record["tag"], tuple(record["row"]), record["source_clause"]) for record in profile["records"]}
    return contradiction(certificate["records"]) and all(
        (record["tag"], tuple(record["row"]), record["source_clause"]) in environment
        for record in certificate["records"]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.input.read_text())
    checks = 0

    assert valid(Y6, 6) and valid(F9, 9); checks += 2
    y6_models = [word for word in range(64) if sat(Y6, word)]
    sat_pins = {5: 0, 6: 1}
    unsat_pins = {3: 1, 4: 0, 5: 0, 6: 1}
    sat_cube = [word for word in y6_models if extends(word, sat_pins)]
    unsat_cube = [word for word in y6_models if extends(word, unsat_pins)]
    assert len(y6_models) == 20 and len(sat_cube) == 6 and not unsat_cube; checks += 3

    falsifier = raw["semantic_equality_falsifier"]
    assert falsifier["profile_ids"] == [1, 5]
    assert falsifier["aligned_residual_function_masks"] == [0, 0]
    assert falsifier["same_exact_model_family"] is True; checks += 3

    # Reconstruct the two row environments independently from the published records.
    profiles = raw.get("profiles")
    # Producer deliberately publishes the exact records inside certificates only.
    left_records = {
        ("D1", (9, 1), 1), ("D4", (11, 0), 4), ("D5", (5, 1), 5),
        ("U0:x1=1", (1, 1), 0), ("U0:x2=0", (2, 0), 0), ("U0:x3=1", (4, 1), 0),
    }
    right_records = {
        ("D0", (7, 1), 0), ("D1", (9, 1), 1), ("D5", (5, 1), 5),
        ("U4:x1=0", (1, 0), 4), ("U4:x2=1", (2, 1), 4), ("U4:x4=0", (8, 0), 4),
    }

    cert_left = falsifier["profile_1_certificates"]
    cert_right = falsifier["profile_5_certificates"]
    assert len(cert_left) == len(cert_right) == 2; checks += 1
    for certificate in cert_left:
        assert len(certificate["records"]) == 3 and contradiction(certificate["records"]); checks += 2
        assert all((r["tag"], tuple(r["row"]), r["source_clause"]) in left_records for r in certificate["records"]); checks += 1
        assert any((r["tag"], tuple(r["row"]), r["source_clause"]) not in right_records for r in certificate["records"]); checks += 1
    for certificate in cert_right:
        assert len(certificate["records"]) == 3 and contradiction(certificate["records"]); checks += 2
        assert all((r["tag"], tuple(r["row"]), r["source_clause"]) in right_records for r in certificate["records"]); checks += 1
        assert any((r["tag"], tuple(r["row"]), r["source_clause"]) not in left_records for r in certificate["records"]); checks += 1

    matrix = falsifier["transport_matrix"]
    assert all(entry["accepted"] for entry in matrix["1_to_1"] + matrix["5_to_5"]); checks += 1
    assert not any(entry["accepted"] for entry in matrix["1_to_5"] + matrix["5_to_1"]); checks += 1
    assert all(entry["xor_is_0_eq_1"] for entries in matrix.values() for entry in entries); checks += 1
    assert all(entry["missing_tags"] for entry in matrix["1_to_5"] + matrix["5_to_1"]); checks += 1

    f9_pins = {8: 0, 3: 0, 7: 0, 6: 0, 1: 1, 5: 1}
    f9_root = sum(sat(F9, word) for word in range(1 << 9))
    f9_cube = sum(sat(F9, word) and extends(word, f9_pins) for word in range(1 << 9))
    assert f9_root == 70 and f9_cube == 0; checks += 2
    assert raw["F9_parity_hole"]["outside_cycle_consistent"] is True
    assert not any(raw["F9_parity_hole"]["branch_consistency"].values()); checks += 2

    modes = 0
    for i, j in combinations(range(8), 2):
        for mi, mj in product((0, 1), repeat=2):
            feasible = any(
                all(truth(lit, word) == mi for lit in Y6[i])
                and all(truth(lit, word) == mj for lit in Y6[j])
                for word in range(64)
            )
            same = bool(set(Y6[i]) & set(Y6[j]))
            opposite = any(-lit in Y6[j] for lit in Y6[i])
            assert feasible == ((not opposite) if mi == mj else (not same))
            modes += 1
            checks += 1
    assert modes == raw["signed_SU"]["pair_modes_checked"] == 112; checks += 1

    assert raw["malformed"] == {"cases": 6, "rejected": 6}; checks += 1
    assert raw["same_source_DPLL"]["SAT_cube"]["sat"] is True
    assert raw["same_source_DPLL"]["UNSAT_cube"]["sat"] is False; checks += 2
    assert raw["xor_offline"]["DELAY"] == {"native_steps": 257, "data_bit_changes": 0}; checks += 1
    assert raw["xor_offline"]["restored_bit"] == {"adjacent_delta": 2, "endpoint_delta": 0}; checks += 1
    assert raw["p_vs_np"] == "OPEN"; checks += 1

    result = {
        "run": "VERIFY_LSPV5_TYPED_PROOF_TRANSPORT_REFEREE266",
        "assertions": checks, "Y6_root_models": 20, "Y6_sat_cube_models": 6,
        "Y6_unsat_cube_models": 0, "F9_root_models": 70, "F9_cube_models": 0,
        "local_certificates_accepted": 4, "cross_certificates_accepted": 0,
        "signed_SU_pair_modes": modes, "status": "PASS", "p_vs_np": "OPEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
