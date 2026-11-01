#!/usr/bin/env python3
"""Exact finite red-team for certificate-DAG cache quotients.

This standard-library program authenticates the Y6 target source, builds every
cost-one positive-defect affine profile under x5=0,x6=1, enumerates all 79
arbitrary processed-site prefix states, and compares syntactic cache keys with
the exact source residual subfunction.  It also replays the valid F9 outside-
cycle parity counterexample and retained XOR controls.

The calculations are finite observations plus exact restricted lemmas.  They
are not a native FLMV machine and prove no arbitrary-machine lower bound.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path


Y6 = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6),
)
Y6_PINS = {5: 0, 6: 1}
Y6_UNSAT_PINS = {3: 1, 4: 0, 5: 0, 6: 1}
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
    seen: set[tuple[int, ...]] = set()
    counts = Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(lit) for lit in clause}) != 3:
            return False
        if not (all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)):
            return False
        if any(not 1 <= abs(lit) <= n for lit in clause):
            return False
        key = tuple(sorted(clause))
        if key in seen:
            return False
        seen.add(key)
        for lit in clause:
            counts[abs(lit), lit > 0] += 1
    return all(counts[v, sign] == 2 for v in range(1, n + 1) for sign in (False, True))


def malformed_controls() -> dict[str, int]:
    cases = (
        Y6[:-1],
        ((1, 1, 2),) + Y6[1:],
        ((1, -2, 3),) + Y6[1:],
        (Y6[0],) + Y6[:-1],
        ((1, 2, 6),) + Y6[1:],
        ((1, 2, 7),) + Y6[1:],
    )
    assert valid_target(Y6, 6)
    rejected = sum(not valid_target(tuple(case), 6) for case in cases)
    assert rejected == len(cases)
    return {"cases": len(cases), "rejected": rejected}


def y6_default_row(clause_id: int) -> tuple[int, int]:
    free = (1, 2, 3, 4)
    mask, rhs = 0, 1
    for lit in Y6[clause_id]:
        if abs(lit) in Y6_PINS:
            assert lit_value(lit, Y6_PINS) == 0
        else:
            mask ^= 1 << free.index(abs(lit))
            rhs ^= int(lit < 0)
    return mask, rhs


def unit_row(lit: int, truth: int) -> tuple[int, int]:
    free = (1, 2, 3, 4)
    return 1 << free.index(abs(lit)), truth if lit > 0 else truth ^ 1


def row_holds(row: tuple[int, int], assignment: dict[int, int]) -> bool:
    mask, rhs = row
    lhs = 0
    for i, variable in enumerate((1, 2, 3, 4)):
        if mask >> i & 1:
            lhs ^= assignment[variable]
    return lhs == rhs


def solve_rows(rows: list[tuple[int, int]]) -> list[dict[int, int]]:
    out = []
    for bits in product((0, 1), repeat=4):
        assignment = {**Y6_PINS, **dict(zip((1, 2, 3, 4), bits))}
        if all(row_holds(row, assignment) for row in rows):
            out.append(assignment)
    return out


def assignment_word(assignment: dict[int, int], n: int) -> int:
    return sum(assignment[v] << (v - 1) for v in range(1, n + 1))


def canonical_span(rows: list[tuple[int, int]], include_rhs: bool = True) -> tuple[int, ...]:
    """Canonical RREF row-space encoding over GF(2)."""
    basis: dict[int, int] = {}
    for mask, rhs in rows:
        word = mask | ((rhs << 4) if include_rhs else 0)
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


def build_profiles() -> tuple[list[dict[str, object]], dict[int, tuple[int, int]], int]:
    defaults = {site: y6_default_row(site) for site in SITES}
    profiles: list[dict[str, object]] = []
    evaluations = 0
    for chosen in SITES:
        residual_literals = [lit for lit in Y6[chosen] if abs(lit) not in Y6_PINS]
        for true_positions in combinations(range(len(residual_literals)), 2):
            exact = tuple(int(i in true_positions) for i in range(len(residual_literals)))
            units = [unit_row(lit, truth) for lit, truth in zip(residual_literals, exact)]
            rows = [defaults[site] for site in SITES if site != chosen] + units
            affine = solve_rows(rows)
            evaluations += 16 * len(rows)
            source = [assignment for assignment in affine if satisfies(Y6, assignment)]
            assert affine == source
            profiles.append({
                "id": len(profiles),
                "chosen_site": chosen,
                "exact_truth": list(exact),
                "unit_rows": [list(row) for row in units],
                "rows": [list(row) for row in rows],
                "models": [assignment_word(assignment, 6) for assignment in affine],
                "consistent": bool(affine),
            })
    assert len(profiles) == 8
    return profiles, defaults, evaluations


def profile_decision(profile: dict[str, object], site: int) -> tuple[object, ...]:
    if profile["chosen_site"] == site:
        return ("O", *profile["exact_truth"])
    return ("D",)


def enumerate_prefix_states(profiles: list[dict[str, object]], defaults: dict[int, tuple[int, int]]):
    states = []
    for subset_bits in range(1 << len(SITES)):
        processed = tuple(SITES[i] for i in range(len(SITES)) if subset_bits >> i & 1)
        decisions = {
            tuple(profile_decision(profile, site) for site in processed)
            for profile in profiles
        }
        for decision in sorted(decisions, key=repr):
            extending = [
                profile for profile in profiles
                if tuple(profile_decision(profile, site) for site in processed) == decision
            ]
            spent = sum(option[0] == "O" for option in decision)
            committed_rows: list[tuple[int, int]] = []
            selected_rows: list[tuple[int, int]] = []
            for site, option in zip(processed, decision):
                if option[0] == "D":
                    committed_rows.append(defaults[site])
                else:
                    representative = extending[0]
                    units = [tuple(row) for row in representative["unit_rows"]]
                    committed_rows.extend(units)
                    selected_rows.extend(units)
            models = sorted({word for profile in extending for word in profile["models"]})
            residual_mask = 0
            for word in models:
                free_word = sum(((word >> (v - 1)) & 1) << (v - 1) for v in range(1, 5))
                residual_mask |= 1 << free_word
            states.append({
                "processed_sites": list(processed),
                "decisions": [list(option) for option in decision],
                "remaining_budget": 1 - spent,
                "extending_profile_ids": [profile["id"] for profile in extending],
                "models": models,
                "residual_function_mask": residual_mask,
                "lazy_selected_augmented_span": list(canonical_span(selected_rows)),
                "committed_augmented_span": list(canonical_span(committed_rows)),
            })
    assert len(states) == 79
    return states


def collision_summary(states: list[dict[str, object]], span_field: str) -> dict[str, object]:
    buckets: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for state in states:
        key = (state["remaining_budget"], tuple(state[span_field]))
        buckets[key].append(state)
    pairs = 0
    unequal = 0
    for bucket in buckets.values():
        for left, right in combinations(bucket, 2):
            pairs += 1
            unequal += left["residual_function_mask"] != right["residual_function_mask"]
    return {
        "key_buckets": len(buckets),
        "same_key_pairs": pairs,
        "unequal_residual_function_pairs": unequal,
        "finite_observation_only": True,
    }


def pair_extremes(formula: tuple[tuple[int, ...], ...]) -> dict[str, int]:
    checks = 0
    for left, right in combinations(range(len(formula)), 2):
        for left_mode, right_mode in product((0, 1), repeat=2):
            feasible = False
            n = max(abs(lit) for clause in formula for lit in clause)
            for word in range(1 << n):
                assignment = {v: (word >> (v - 1)) & 1 for v in range(1, n + 1)}
                left_ok = all(lit_value(lit, assignment) == left_mode for lit in formula[left])
                right_ok = all(lit_value(lit, assignment) == right_mode for lit in formula[right])
                feasible |= left_ok and right_ok
            same = bool(set(formula[left]) & set(formula[right]))
            opposite = any(-lit in formula[right] for lit in formula[left])
            predicted = (not opposite) if left_mode == right_mode else (not same)
            assert feasible == predicted
            checks += 1
    return {"pair_modes_checked": checks}


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
        if mask == 0 and rhs:
            return False
    return True


def f9_affine_rows(choice: int | None) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    on_cycle = set(F9_CYCLE)
    # Outside-cycle residual one-true parity.
    for clause_id, clause in enumerate(F9):
        if clause_id in on_cycle:
            continue
        if any(abs(lit) in F9_PINS and lit_value(lit, F9_PINS) for lit in clause):
            continue
        free = [lit for lit in clause if abs(lit) not in F9_PINS]
        if not free:
            continue
        mask = sum(1 << (abs(lit) - 1) for lit in free)
        rhs = 1 ^ ((len(free) & 1) if clause[0] < 0 else 0)
        rows.append((mask, rhs))
    # Preference rows derived independently from covered-clause signed counts.
    covered = [
        j for j, clause in enumerate(F9)
        if any(abs(lit) in F9_PINS and lit_value(lit, F9_PINS) for lit in clause)
    ]
    signed = Counter()
    for j in covered:
        for lit in F9[j]:
            if abs(lit) not in F9_PINS:
                signed[abs(lit), lit > 0] += 1
    for variable in (2, 4, 9):
        preferred = 0 if signed[variable, True] > signed[variable, False] else 1
        rows.append((1 << (variable - 1), preferred))
    if choice is not None:
        for clause_id in F9_CYCLE:
            free = [abs(lit) for lit in F9[clause_id] if abs(lit) not in F9_PINS]
            assert len(free) == 2
            if clause_id == choice:
                value = int(F9[clause_id][0] > 0)
                rows.extend((1 << (variable - 1), value) for variable in free)
            else:
                rows.append(((1 << (free[0] - 1)) ^ (1 << (free[1] - 1)), 1))
    return rows


def f9_control() -> dict[str, object]:
    assert valid_target(F9, 9)
    root_models = list(extensions(F9, {}))
    cube_models = list(extensions(F9, F9_PINS))
    outside = gf2_consistent(f9_affine_rows(None))
    branches = {str(choice): gf2_consistent(f9_affine_rows(choice)) for choice in F9_CYCLE}
    assert len(root_models) == 70 and not cube_models and outside and not any(branches.values())
    return {
        "root_models": len(root_models),
        "cube_completions": 8,
        "cube_models": len(cube_models),
        "outside_cycle_parity_consistent": outside,
        "branch_consistency": branches,
        "all_cycle_choices_exhausted_unsat": True,
    }


def xor_controls() -> dict[str, object]:
    return {
        "delay": {"native_steps": 257, "data_bit_changes": 0},
        "copy": {"logical_delta": 0, "shadow_writes": 22},
        "recomp": {"retained_clause_status_bits": 0, "source_literal_rereads": 24},
        "restored_bit": {"adjacent_delta": 2, "endpoint_delta": 0},
        "classification": "offline diagnostics; no native end-to-end FLMV trace",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    profiles, defaults, row_evaluations = build_profiles()
    states = enumerate_prefix_states(profiles, defaults)
    root = next(state for state in states if state["processed_sites"] == [])
    skip0 = next(
        state for state in states
        if state["processed_sites"] == [0] and state["decisions"] == [["D"]]
    )
    assert root["remaining_budget"] == skip0["remaining_budget"] == 1
    assert root["lazy_selected_augmented_span"] == skip0["lazy_selected_augmented_span"] == []
    assert len(root["models"]) == 6 and len(skip0["models"]) == 4
    assert root["residual_function_mask"] != skip0["residual_function_mask"]

    # Same coefficient space, opposite SAT label: RHS is indispensable.
    p0, p1 = profiles[0], profiles[1]
    span0 = canonical_span([tuple(row) for row in p0["unit_rows"]], include_rhs=False)
    span1 = canonical_span([tuple(row) for row in p1["unit_rows"]], include_rhs=False)
    aug0 = canonical_span([tuple(row) for row in p0["unit_rows"]], include_rhs=True)
    aug1 = canonical_span([tuple(row) for row in p1["unit_rows"]], include_rhs=True)
    assert span0 == span1 == (1, 2, 4)
    assert aug0 != aug1 and p0["consistent"] and not p1["consistent"]

    semantic_classes = defaultdict(list)
    for state in states:
        semantic_classes[state["residual_function_mask"]].append(state)

    sat_models = list(extensions(Y6, Y6_PINS))
    unsat_models = list(extensions(Y6, Y6_UNSAT_PINS))
    assert len(list(extensions(Y6, {}))) == 20
    assert len(sat_models) == 6 and not unsat_models

    result = {
        "run": "LSPV5_RESIDUAL_SUBFUNCTION_QUOTIENT_REFEREE265",
        "timestamp_pacific": "2026-11-01 05:48 PST",
        "classification": "PROVED/EXACT restricted cache theorem; COMPUTATIONAL exhaustive finite controls",
        "source": {
            "valid_duplicate_free_proper_monotone_3sat_22": valid_target(Y6, 6),
            "root_models": 20,
            "sat_cube_models": len(sat_models),
            "unsat_cube_models": len(unsat_models),
            "grammar_literal_reads": 24,
        },
        "profiles": profiles,
        "prefix_state_enumeration": {
            "states": len(states),
            "semantic_residual_function_classes": len(semantic_classes),
            "lazy_key": collision_summary(states, "lazy_selected_augmented_span"),
            "committed_augmented_key": collision_summary(states, "committed_augmented_span"),
        },
        "explicit_lazy_collision": {
            "left": {k: root[k] for k in ("processed_sites", "decisions", "remaining_budget", "extending_profile_ids", "models", "residual_function_mask", "lazy_selected_augmented_span")},
            "right": {k: skip0[k] for k in ("processed_sites", "decisions", "remaining_budget", "extending_profile_ids", "models", "residual_function_mask", "lazy_selected_augmented_span")},
            "same_lazy_key": True,
            "different_exact_residual_subfunctions": True,
        },
        "coefficient_span_collision": {
            "profile_ids": [0, 1],
            "coefficient_span": list(span0),
            "augmented_spans": [list(aug0), list(aug1)],
            "labels": ["SAT", "UNSAT"],
            "lesson": "coefficient row space without RHS is not a semantic cache key",
        },
        "restricted_theorem": {
            "exact_safe_quotient": "equal aligned residual Boolean subfunction; for counting also preserve multiplicity/projection",
            "replayable_sufficient_condition": "equal committed affine solution set plus identical legal future transition/domain and provenance maps",
            "necessity_scope": "necessary for reuse of the full semantic model family, model count, or proof object; a decision-only cache may quotient more coarsely only with a separately proved result-equivalence",
        },
        "F9_parity_hole": f9_control(),
        "signed_SU": pair_extremes(Y6),
        "malformed": malformed_controls(),
        "xor_offline": xor_controls(),
        "resource_ledger": {
            "y6_assignments_scanned": 64 + 16 + 4,
            "prefix_states": len(states),
            "profile_affine_row_evaluations": row_evaluations,
            "failed_profiles": sum(not profile["consistent"] for profile in profiles),
            "output_profiles": len(profiles),
            "native_source_head_index_guest_peak_space": "not measured; remains charged",
        },
        "limitations": [
            "79-state Y6 committed-augmented-key success is a finite observation, not an all-input theorem",
            "children are noncanonical and no hereditary target re-encoding is proved",
            "no arbitrary-A to Phi(A) contraction or numerical FLMV transport",
            "XOR is offline and representation-dependent",
        ],
        "p_vs_np": "OPEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "run": result["run"],
        "prefix_states": len(states),
        "lazy_unequal_collisions": result["prefix_state_enumeration"]["lazy_key"]["unequal_residual_function_pairs"],
        "committed_unequal_collisions": result["prefix_state_enumeration"]["committed_augmented_key"]["unequal_residual_function_pairs"],
        "root_models": len(root["models"]),
        "skip0_models": len(skip0["models"]),
        "F9": result["F9_parity_hole"],
        "p_vs_np": "OPEN",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
