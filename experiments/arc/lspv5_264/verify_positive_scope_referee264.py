#!/usr/bin/env python3
"""No-producer-import verifier for LSPV5_POSITIVE_SCOPE_DAG_REFEREE264."""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path


CLAUSES = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6),
)


def truth(lit: int, word: int) -> int:
    bit = (word >> (abs(lit) - 1)) & 1
    return bit if lit > 0 else bit ^ 1


def satisfies(word: int) -> bool:
    return all(any(truth(lit, word) for lit in clause) for clause in CLAUSES)


def extends(word: int, pins: dict[int, int]) -> bool:
    return all(((word >> (variable - 1)) & 1) == value for variable, value in pins.items())


def valid_target(formula: tuple[tuple[int, ...], ...], variables: int = 6) -> bool:
    if len(formula) * 3 != variables * 4:
        return False
    if len({tuple(sorted(clause)) for clause in formula}) != len(formula):
        return False
    for clause in formula:
        if len(clause) != 3 or len({abs(lit) for lit in clause}) != 3:
            return False
        if not (all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)):
            return False
        if any(not 1 <= abs(lit) <= variables for lit in clause):
            return False
    for variable in range(1, variables + 1):
        if sum(lit == variable for clause in formula for lit in clause) != 2:
            return False
        if sum(lit == -variable for clause in formula for lit in clause) != 2:
            return False
    return True


def bits(word: int) -> list[int]:
    return [(word >> i) & 1 for i in range(6)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.input.read_text())
    assertions = 0

    # Independent source grammar authentication.
    assert len(CLAUSES) == len(set(CLAUSES)) == 8; assertions += 1
    for clause in CLAUSES:
        assert len(clause) == len({abs(lit) for lit in clause}) == 3; assertions += 1
        assert all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause); assertions += 1
    for variable in range(1, 7):
        assert sum(lit == variable for clause in CLAUSES for lit in clause) == 2; assertions += 1
        assert sum(lit == -variable for clause in CLAUSES for lit in clause) == 2; assertions += 1

    all_models = [word for word in range(64) if satisfies(word)]
    assert len(all_models) == 20; assertions += 1
    assert not satisfies(0) and not satisfies(63); assertions += 1
    malformed = [
        CLAUSES[:-1],
        ((1, 1, 2),) + CLAUSES[1:],
        ((1, -2, 3),) + CLAUSES[1:],
        (CLAUSES[0],) + CLAUSES[:-1],
        ((1, 2, 6),) + CLAUSES[1:],
        ((1, 2, 7),) + CLAUSES[1:],
    ]
    assert valid_target(CLAUSES); assertions += 1
    assert all(not valid_target(tuple(case)) for case in malformed); assertions += 1
    assert raw["adversarial_controls"]["malformed_target_strings"] == {"cases": 6, "rejected": 6}; assertions += 1

    sat_pins = {5: 0, 6: 1}
    unsat_pins = {3: 1, 4: 0, 5: 0, 6: 1}
    sat_models = [word for word in all_models if extends(word, sat_pins)]
    unsat_models = [word for word in all_models if extends(word, unsat_pins)]
    assert len(sat_models) == 6; assertions += 1
    assert not unsat_models; assertions += 1
    assert sorted(raw["sat_cube"]["models"]) == sorted(bits(word) for word in sat_models); assertions += 1

    # Rebuild the four default rows directly from their mathematical meaning.
    free = (1, 2, 3, 4)
    uncovered = (0, 1, 4, 5)
    rows = {}
    for clause_id in uncovered:
        mask, rhs = 0, 1
        for lit in CLAUSES[clause_id]:
            if abs(lit) in sat_pins:
                assert truth(lit, sum(v << (k - 1) for k, v in sat_pins.items())) == 0
                assertions += 1
            else:
                mask ^= 1 << free.index(abs(lit))
                rhs ^= int(lit < 0)
        rows[clause_id] = (mask, rhs)
    assert rows == {0: (7, 1), 1: (9, 1), 4: (11, 0), 5: (5, 1)}; assertions += 1
    assert (
        rows[0][0] ^ rows[1][0] ^ rows[4][0] ^ rows[5][0],
        rows[0][1] ^ rows[1][1] ^ rows[4][1] ^ rows[5][1],
    ) == (0, 1); assertions += 1

    def holds(row: tuple[int, int], word: int) -> bool:
        mask, rhs = row
        lhs = 0
        for index, variable in enumerate(free):
            if (mask >> index) & 1:
                lhs ^= (word >> (variable - 1)) & 1
        return lhs == rhs

    for clause_id, row in rows.items():
        violating = [word for word in sat_models if not holds(row, word)]
        assert violating; assertions += 1
        assert sorted(raw["row_domains"][str(clause_id)]["models_violating"]) == sorted(
            bits(word) for word in violating
        ); assertions += 1

    profiles = raw["profiles"]
    assert len(profiles) == 8; assertions += 1
    assert sum(bool(profile["consistent"]) for profile in profiles) == 6; assertions += 1
    profile_models = [tuple(model) for profile in profiles for model in profile["solutions"]]
    assert len(profile_models) == len(set(profile_models)) == 6; assertions += 1
    assert set(profile_models) == {tuple(bits(word)) for word in sat_models}; assertions += 1

    root = raw["dag_cache_collision"]["root_profile_ids"]
    skipped = raw["dag_cache_collision"]["after_skip_clause_0_profile_ids"]
    assert raw["dag_cache_collision"]["unsafe_key_root"] == raw["dag_cache_collision"]["unsafe_key_after_skip_clause_0"]; assertions += 1
    assert any(0 not in profiles[i]["default_clause_ids"] for i in root); assertions += 1
    assert all(0 in profiles[i]["default_clause_ids"] for i in skipped); assertions += 1

    # Independent local S/U feasibility enumeration over all 28 pairs and four modes.
    su_checks = 0
    for left in range(8):
        for right in range(left + 1, 8):
            for lm, rm in product((0, 1), repeat=2):  # 1=S, 0=U
                feasible = False
                for word in range(64):
                    l_ok = all(truth(lit, word) == lm for lit in CLAUSES[left])
                    r_ok = all(truth(lit, word) == rm for lit in CLAUSES[right])
                    feasible |= l_ok and r_ok
                same = bool(set(CLAUSES[left]) & set(CLAUSES[right]))
                opposite = any(-lit in CLAUSES[right] for lit in CLAUSES[left])
                predicted = (not opposite) if lm == rm else (not same)
                assert feasible == predicted; assertions += 1
                su_checks += 1
    assert su_checks == raw["adversarial_controls"]["signed_su"]["pair_modes_checked"] == 112; assertions += 1

    # DELAY/COPY/RECOMP are countermodels to XOR-as-total-work, not machine bounds.
    assert raw["xor_offline"]["delay_control"] == {
        "native_steps": 100,
        "data_bit_changes": 0,
        "lesson": "time can be positive while adjacent data XOR is zero",
    }; assertions += 1
    assert raw["xor_offline"]["binary"]["classification"].startswith("offline"); assertions += 1
    assert raw["xor_offline"]["gray"]["classification"].startswith("offline"); assertions += 1
    assert raw["p_vs_np"] == "OPEN"; assertions += 1

    result = {
        "run": "VERIFY_LSPV5_POSITIVE_SCOPE_DAG_REFEREE264",
        "assertions": assertions,
        "source_models": 20,
        "sat_cube_models": 6,
        "unsat_child_models": 0,
        "profiles": 8,
        "consistent_profiles": 6,
        "su_pair_modes": 112,
        "status": "PASS",
        "p_vs_np": "OPEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
