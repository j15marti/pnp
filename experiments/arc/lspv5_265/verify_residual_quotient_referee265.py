#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE265."""

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
    return all((word >> (v - 1) & 1) == bit for v, bit in pins.items())


def valid(formula: tuple[tuple[int, ...], ...], n: int) -> bool:
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


def canonical(rows: list[tuple[int, int]], rhs: bool) -> tuple[int, ...]:
    basis: dict[int, int] = {}
    for mask, bit in rows:
        word = mask | ((bit << 4) if rhs else 0)
        while word:
            pivot = word.bit_length() - 1
            if pivot in basis:
                word ^= basis[pivot]
            else:
                basis[pivot] = word
                for other in tuple(basis):
                    if other != pivot and (basis[other] >> pivot) & 1:
                        basis[other] ^= word
                break
    return tuple(sorted(basis.values()))


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
    assert raw["source"]["root_models"] == 20
    assert raw["source"]["sat_cube_models"] == 6
    assert raw["source"]["unsat_cube_models"] == 0; checks += 3

    profiles = raw["profiles"]
    assert len(profiles) == 8 and sum(profile["consistent"] for profile in profiles) == 6; checks += 2
    profile_models = [word for profile in profiles for word in profile["models"]]
    assert len(profile_models) == len(set(profile_models)) == 6; checks += 1
    assert set(profile_models) == set(sat_cube); checks += 1

    left = raw["explicit_lazy_collision"]["left"]
    right = raw["explicit_lazy_collision"]["right"]
    assert left["remaining_budget"] == right["remaining_budget"] == 1; checks += 1
    assert left["lazy_selected_augmented_span"] == right["lazy_selected_augmented_span"] == []; checks += 1
    assert len(left["models"]) == 6 and len(right["models"]) == 4; checks += 1
    assert left["residual_function_mask"] != right["residual_function_mask"]; checks += 1
    assert set(right["models"]).issubset(left["models"]); checks += 1

    # Recompute profile 0/1 unit-row spaces without using producer code.
    rows0 = [tuple(row) for row in profiles[0]["unit_rows"]]
    rows1 = [tuple(row) for row in profiles[1]["unit_rows"]]
    assert canonical(rows0, False) == canonical(rows1, False) == (1, 2, 4); checks += 1
    assert canonical(rows0, True) != canonical(rows1, True); checks += 1
    assert profiles[0]["models"] and not profiles[1]["models"]; checks += 1

    enumeration = raw["prefix_state_enumeration"]
    assert enumeration["states"] == 79; checks += 1
    assert enumeration["lazy_key"]["unequal_residual_function_pairs"] > 0; checks += 1
    assert enumeration["committed_augmented_key"]["unequal_residual_function_pairs"] == 0; checks += 1
    assert enumeration["committed_augmented_key"]["finite_observation_only"] is True; checks += 1

    f9_pins = {8: 0, 3: 0, 7: 0, 6: 0, 1: 1, 5: 1}
    f9_root = sum(sat(F9, word) for word in range(1 << 9))
    f9_cube = sum(sat(F9, word) and extends(word, f9_pins) for word in range(1 << 9))
    assert f9_root == 70 and f9_cube == 0; checks += 2
    assert raw["F9_parity_hole"]["root_models"] == 70
    assert raw["F9_parity_hole"]["cube_models"] == 0
    assert raw["F9_parity_hole"]["outside_cycle_parity_consistent"] is True
    assert not any(raw["F9_parity_hole"]["branch_consistency"].values()); checks += 4

    # Independent pair-extreme enumeration.
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
    assert raw["xor_offline"]["delay"] == {"native_steps": 257, "data_bit_changes": 0}; checks += 1
    assert raw["xor_offline"]["restored_bit"] == {"adjacent_delta": 2, "endpoint_delta": 0}; checks += 1
    assert raw["p_vs_np"] == "OPEN"; checks += 1

    result = {
        "run": "VERIFY_LSPV5_RESIDUAL_SUBFUNCTION_QUOTIENT_REFEREE265",
        "assertions": checks,
        "source_models": 20,
        "sat_cube_models": 6,
        "unsat_cube_models": 0,
        "prefix_states": 79,
        "F9_root_models": 70,
        "F9_cube_models": 0,
        "signed_SU_pair_modes": modes,
        "status": "PASS",
        "p_vs_np": "OPEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
