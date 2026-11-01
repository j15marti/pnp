#!/usr/bin/env python3
"""Independent finite referee for positive-defect affine-row scope.

The script deliberately does not import any producer from another LSPV role.  It
authenticates the Y6 source, enumerates all source assignments, reconstructs the
eight cost-one affine descriptions under x5=0,x6=1, and exhibits a certificate-
DAG cache-key collision when skipped sites are omitted from proof dependencies.

The XOR traces are offline diagnostics.  Nothing here is a native FLMV machine.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations, product
from pathlib import Path


Y6 = (
    (1, 2, 3),
    (1, 4, 5),
    (2, 4, 6),
    (3, 5, 6),
    (-1, -2, -4),
    (-1, -3, -6),
    (-2, -3, -5),
    (-4, -5, -6),
)
SAT_PINS = {5: 0, 6: 1}
UNSAT_PINS = {3: 1, 4: 0, 5: 0, 6: 1}


def literal_value(lit: int, assignment: dict[int, int]) -> int:
    value = assignment[abs(lit)]
    return value if lit > 0 else 1 - value


def clause_true_count(clause: tuple[int, ...], assignment: dict[int, int]) -> int:
    return sum(literal_value(lit, assignment) for lit in clause)


def formula_satisfied(assignment: dict[int, int]) -> bool:
    return all(clause_true_count(clause, assignment) >= 1 for clause in Y6)


def authenticate_source() -> dict[str, object]:
    assert len(Y6) == 8
    assert len(set(Y6)) == len(Y6)
    supports = []
    occurrence = {v: {1: 0, -1: 0} for v in range(1, 7)}
    reads = 0
    for clause in Y6:
        assert len(clause) == 3
        assert len({abs(lit) for lit in clause}) == 3
        assert all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)
        support = tuple(sorted(abs(lit) for lit in clause))
        supports.append((1 if clause[0] > 0 else -1, support))
        for lit in clause:
            occurrence[abs(lit)][1 if lit > 0 else -1] += 1
            reads += 1
    assert len(set(supports)) == len(supports)
    assert all(counts == {1: 2, -1: 2} for counts in occurrence.values())
    return {
        "valid_duplicate_free_proper_monotone_3sat_22": True,
        "variables": 6,
        "clauses": 8,
        "literal_reads": reads,
    }


def valid_target(formula: tuple[tuple[int, ...], ...], variables: int) -> bool:
    if 3 * len(formula) != 4 * variables:
        return False
    seen = set()
    occurrence = {(v, sign): 0 for v in range(1, variables + 1) for sign in (-1, 1)}
    for clause in formula:
        if len(clause) != 3 or len({abs(lit) for lit in clause}) != 3:
            return False
        if not (all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)):
            return False
        if any(abs(lit) < 1 or abs(lit) > variables for lit in clause):
            return False
        key = tuple(sorted(clause))
        if key in seen:
            return False
        seen.add(key)
        for lit in clause:
            occurrence[(abs(lit), 1 if lit > 0 else -1)] += 1
    return all(count == 2 for count in occurrence.values())


def malformed_controls() -> dict[str, object]:
    cases = [
        Y6[:-1],
        ((1, 1, 2),) + Y6[1:],
        ((1, -2, 3),) + Y6[1:],
        (Y6[0],) + Y6[:-1],
        ((1, 2, 6),) + Y6[1:],
        ((1, 2, 7),) + Y6[1:],
    ]
    rejected = [not valid_target(tuple(case), 6) for case in cases]
    assert all(rejected)
    assert valid_target(Y6, 6)
    return {"cases": len(cases), "rejected": sum(rejected)}


def enumerate_extensions(pins: dict[int, int]) -> tuple[list[dict[int, int]], int]:
    free = [v for v in range(1, 7) if v not in pins]
    models: list[dict[int, int]] = []
    literal_tests = 0
    for bits in product((0, 1), repeat=len(free)):
        assignment = dict(pins)
        assignment.update(zip(free, bits))
        ok = True
        for clause in Y6:
            count = 0
            for lit in clause:
                count += literal_value(lit, assignment)
                literal_tests += 1
            if count == 0:
                ok = False
        if ok:
            models.append(assignment)
    return models, literal_tests


def residual(pins: dict[int, int]) -> dict[str, object]:
    rows = []
    uncovered = []
    empty = []
    satisfied = []
    for clause_id, clause in enumerate(Y6):
        pinned_truth = [
            literal_value(lit, pins) for lit in clause if abs(lit) in pins
        ]
        free_literals = tuple(lit for lit in clause if abs(lit) not in pins)
        if 1 in pinned_truth:
            satisfied.append(clause_id)
        elif not free_literals:
            empty.append(clause_id)
        else:
            uncovered.append(clause_id)
            rows.append((clause_id, free_literals))
    return {
        "uncovered": uncovered,
        "satisfied": satisfied,
        "empty": empty,
        "free_variables": [v for v in range(1, 7) if v not in pins],
        "residual_clauses": rows,
    }


def default_row(clause_id: int, pins: dict[int, int], free: list[int]) -> tuple[int, int]:
    """Return mask,rhs for XOR of residual literal truth values equal to one."""
    mask = 0
    rhs = 1
    for lit in Y6[clause_id]:
        if abs(lit) in pins:
            assert literal_value(lit, pins) == 0
            continue
        mask ^= 1 << free.index(abs(lit))
        if lit < 0:
            rhs ^= 1
    return mask, rhs


def row_holds(row: tuple[int, int], free: list[int], assignment: dict[int, int]) -> bool:
    mask, rhs = row
    lhs = 0
    for i, variable in enumerate(free):
        if (mask >> i) & 1:
            lhs ^= assignment[variable]
    return lhs == rhs


def solve_rows(
    rows: list[tuple[int, int]], free: list[int], pins: dict[int, int]
) -> list[dict[int, int]]:
    solutions = []
    for bits in product((0, 1), repeat=len(free)):
        assignment = dict(pins)
        assignment.update(zip(free, bits))
        if all(row_holds(row, free, assignment) for row in rows):
            solutions.append(assignment)
    return solutions


def unit_row(lit: int, truth: int, free: list[int]) -> tuple[int, int]:
    variable_value = truth if lit > 0 else 1 - truth
    return 1 << free.index(abs(lit)), variable_value


def build_profiles() -> tuple[list[dict[str, object]], dict[int, tuple[int, int]], int]:
    state = residual(SAT_PINS)
    free = state["free_variables"]
    assert free == [1, 2, 3, 4]
    uncovered = state["uncovered"]
    assert uncovered == [0, 1, 4, 5]
    default_rows = {j: default_row(j, SAT_PINS, free) for j in uncovered}
    profiles = []
    row_evaluations = 0
    for chosen_clause in uncovered:
        residual_literals = [
            lit for lit in Y6[chosen_clause] if abs(lit) not in SAT_PINS
        ]
        for true_positions in combinations(range(len(residual_literals)), 2):
            rows = [default_rows[j] for j in uncovered if j != chosen_clause]
            exact_truth = []
            for position, lit in enumerate(residual_literals):
                truth = int(position in true_positions)
                exact_truth.append(truth)
                rows.append(unit_row(lit, truth, free))
            affine_solutions = solve_rows(rows, free, SAT_PINS)
            row_evaluations += (2 ** len(free)) * len(rows)
            source_models = [a for a in affine_solutions if formula_satisfied(a)]
            assert affine_solutions == source_models
            profiles.append(
                {
                    "profile_id": len(profiles),
                    "chosen_clause": chosen_clause,
                    "residual_literals": residual_literals,
                    "exact_truth": exact_truth,
                    "default_clause_ids": [j for j in uncovered if j != chosen_clause],
                    "rows": [[mask, rhs] for mask, rhs in rows],
                    "solutions": [assignment_bits(a) for a in affine_solutions],
                    "consistent": bool(affine_solutions),
                }
            )
    return profiles, default_rows, row_evaluations


def assignment_bits(assignment: dict[int, int]) -> list[int]:
    return [assignment[v] for v in range(1, 7)]


def xor_rows(rows: list[tuple[int, int]]) -> tuple[int, int]:
    mask = 0
    rhs = 0
    for row_mask, row_rhs in rows:
        mask ^= row_mask
        rhs ^= row_rhs
    return mask, rhs


def su_controls() -> dict[str, object]:
    checked = 0
    mismatches = []
    for left in range(len(Y6)):
        for right in range(left + 1, len(Y6)):
            for left_mode in ("S", "U"):
                for right_mode in ("S", "U"):
                    predicted = True
                    demands: dict[int, int] = {}
                    for clause_id, mode in ((left, left_mode), (right, right_mode)):
                        for lit in Y6[clause_id]:
                            want_truth = mode == "S"
                            value = int(want_truth) if lit > 0 else int(not want_truth)
                            variable = abs(lit)
                            if variable in demands and demands[variable] != value:
                                predicted = False
                            demands[variable] = value
                    observed = False
                    for bits in product((0, 1), repeat=6):
                        assignment = dict(zip(range(1, 7), bits))
                        left_truth = int(left_mode == "S")
                        right_truth = int(right_mode == "S")
                        left_ok = all(
                            literal_value(lit, assignment) == left_truth
                            for lit in Y6[left]
                        )
                        right_ok = all(
                            literal_value(lit, assignment) == right_truth
                            for lit in Y6[right]
                        )
                        observed |= left_ok and right_ok
                    checked += 1
                    if predicted != observed:
                        mismatches.append([left, right, left_mode + right_mode])
    assert not mismatches
    return {"pair_modes_checked": checked, "mismatches": mismatches}


def logical_state(assignment: dict[int, int]) -> tuple[int, ...]:
    bits = assignment_bits(assignment)
    for clause in Y6:
        count = clause_true_count(clause, assignment)
        bits.extend((count & 1, (count >> 1) & 1))
    return tuple(bits)


def xor_trace(gray: bool) -> dict[str, object]:
    order = []
    for i in range(16):
        code = i ^ (i >> 1) if gray else i
        assignment = dict(SAT_PINS)
        for offset, variable in enumerate((1, 2, 3, 4)):
            assignment[variable] = (code >> offset) & 1
        order.append(logical_state(assignment))
    adjacent = [
        sum(x != y for x, y in zip(left, right))
        for left, right in zip(order, order[1:])
    ]
    endpoint = sum(x != y for x, y in zip(order[0], order[-1]))
    return {
        "encoding": "gray" if gray else "binary",
        "state_bits": len(order[0]),
        "adjacent_d_logic": adjacent,
        "sum_adjacent_d_logic": sum(adjacent),
        "endpoint_d_logic": endpoint,
        "classification": "offline diagnostic; not physical tape work",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    grammar = authenticate_source()
    sat_models, sat_tests = enumerate_extensions(SAT_PINS)
    unsat_models, unsat_tests = enumerate_extensions(UNSAT_PINS)
    assert len(sat_models) == 6
    assert len(unsat_models) == 0
    sat_residual = residual(SAT_PINS)
    unsat_residual = residual(UNSAT_PINS)
    assert not sat_residual["empty"] and not unsat_residual["empty"]

    profiles, default_rows, row_evaluations = build_profiles()
    assert len(profiles) == 8
    assert sum(p["consistent"] for p in profiles) == 6
    profile_solutions = [tuple(bits) for p in profiles for bits in p["solutions"]]
    assert len(profile_solutions) == len(set(profile_solutions)) == 6
    assert set(profile_solutions) == {tuple(assignment_bits(a)) for a in sat_models}

    row_xor = xor_rows(list(default_rows.values()))
    assert row_xor == (0, 1)
    row_domains = {}
    for clause_id, row in default_rows.items():
        obey = [assignment_bits(a) for a in sat_models if row_holds(row, [1, 2, 3, 4], a)]
        violate = [assignment_bits(a) for a in sat_models if not row_holds(row, [1, 2, 3, 4], a)]
        chosen_profiles = [
            p["profile_id"] for p in profiles if p["chosen_clause"] == clause_id
        ]
        row_domains[str(clause_id)] = {
            "row": list(row),
            "models_obeying": obey,
            "models_violating": violate,
            "profiles_replacing_row": chosen_profiles,
            "universal_at_root": not violate,
        }
        assert violate

    root_profiles = [p["profile_id"] for p in profiles]
    skip_zero_profiles = [
        p["profile_id"] for p in profiles if p["chosen_clause"] != 0
    ]
    unsafe_key_root = {"selected": [], "remaining_budget": 1}
    unsafe_key_skip = {"selected": [], "remaining_budget": 1}
    assert unsafe_key_root == unsafe_key_skip
    assert all(0 in profiles[i]["default_clause_ids"] for i in skip_zero_profiles)
    assert any(0 not in profiles[i]["default_clause_ids"] for i in root_profiles)

    # The UNSAT child contains x1 and not-x1 as residual units.  This is an
    # independently checked opposite-label source cube, not evidence that the
    # SAT parent is UNSAT.
    assert unsat_residual["residual_clauses"] == [(1, (1,)), (5, (-1,))]

    endpoint_zero_but_sat = {
        "all_zero_satisfies": formula_satisfied({v: 0 for v in range(1, 7)}),
        "all_one_satisfies": formula_satisfied({v: 1 for v in range(1, 7)}),
        "source_model_count": len(enumerate_extensions({})[0]),
    }
    assert endpoint_zero_but_sat == {
        "all_zero_satisfies": False,
        "all_one_satisfies": False,
        "source_model_count": 20,
    }

    result = {
        "run": "LSPV5_POSITIVE_SCOPE_DAG_REFEREE264",
        "classification": {
            "proved": "finite exact row-domain and cache-key collision lemma on authenticated Y6",
            "computational": "complete enumeration of all Y6 assignments and eight affine profiles",
            "not_claimed": [
                "uniform polynomial SAT algorithm",
                "hereditary canonical target children",
                "arbitrary A to Phi(A)",
                "numerical FLMV transfer",
                "P=NP or P!=NP",
            ],
        },
        "grammar": grammar,
        "sat_cube": {
            "pins": {str(k): v for k, v in SAT_PINS.items()},
            "residual": sat_residual,
            "model_count": len(sat_models),
            "models": [assignment_bits(a) for a in sat_models],
        },
        "unsat_same_source_child": {
            "pins": {str(k): v for k, v in UNSAT_PINS.items()},
            "residual": unsat_residual,
            "model_count": 0,
            "certificate": ["x1=1 from original clause 1", "x1=0 from original clause 5"],
        },
        "default_rows": {str(j): list(row) for j, row in default_rows.items()},
        "premature_default_row_xor": list(row_xor),
        "profiles": profiles,
        "row_domains": row_domains,
        "dag_cache_collision": {
            "unsafe_key_root": unsafe_key_root,
            "unsafe_key_after_skip_clause_0": unsafe_key_skip,
            "root_profile_ids": root_profiles,
            "after_skip_clause_0_profile_ids": skip_zero_profiles,
            "row_0_valid_after_skip": True,
            "row_0_valid_at_root": False,
            "required_dependency": "closed/skipped site set or exact allowed-completion family",
        },
        "theorem_check": {
            "root_rows_are_universal": False,
            "all_four_rows_intersection_profiles": [],
            "exact_affine_profile_count": 8,
            "consistent_affine_profile_count": 6,
            "disjoint_model_union_count": 6,
        },
        "adversarial_controls": {
            "both_endpoints_fail_but_source_sat": endpoint_zero_but_sat,
            "signed_su": su_controls(),
            "opposite_sign_occurrences_present": all(
                any(lit == v for clause in Y6 for lit in clause)
                and any(lit == -v for clause in Y6 for lit in clause)
                for v in range(1, 7)
            ),
            "malformed_target_strings": malformed_controls(),
        },
        "xor_offline": {
            "binary": xor_trace(False),
            "gray": xor_trace(True),
            "delay_control": {
                "native_steps": 100,
                "data_bit_changes": 0,
                "lesson": "time can be positive while adjacent data XOR is zero",
            },
            "copy_control": {
                "logical_state_change": 0,
                "possible_shadow_writes": len(logical_state(sat_models[0])),
                "lesson": "physical copying can write while the source-indexed logical state is unchanged",
            },
            "recompute_control": {
                "retained_clause_status_bits": 0,
                "source_literal_reads_per_full_recompute": 24,
                "lesson": "virtual clause-status changes need not be materialized writes",
            },
        },
        "resource_ledger": {
            "grammar_literal_reads": grammar["literal_reads"],
            "sat_cube_fullscan_literal_tests": sat_tests,
            "unsat_cube_fullscan_literal_tests": unsat_tests,
            "affine_row_evaluations": row_evaluations,
            "failed_affine_profiles": 2,
            "successful_affine_profiles": 6,
            "profile_output_records": 8,
            "native_index_head_source_guest_peak_space": "not measured; remains charged",
        },
        "p_vs_np": "OPEN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "run": result["run"],
        "sat_models": 6,
        "unsat_models": 0,
        "profiles": 8,
        "consistent_profiles": 6,
        "premature_xor": "0=1",
        "unsafe_cache_key_collision": True,
        "p_vs_np": "OPEN",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
