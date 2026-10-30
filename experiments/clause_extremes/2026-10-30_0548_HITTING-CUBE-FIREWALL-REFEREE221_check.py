#!/usr/bin/env python3
"""Independent checker for HITTING-CUBE-FIREWALL-REFEREE221 raw JSON."""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter


def lit_true(lit, assignment):
    return (((assignment >> (abs(lit) - 1)) & 1) == 1) == (lit > 0)


def nvars(formula):
    return max(abs(lit) for clause in formula for lit in clause)


def status(formula, assignment):
    values = [sum(lit_true(lit, assignment) for lit in clause) for clause in formula]
    return values, [values.count(r) for r in range(4)]


def conflict(clause_a, clause_b):
    return any(-lit in clause_b for lit in clause_a)


def requirements(clause, mode):
    return {abs(lit): int((lit > 0) == (mode == "S")) for lit in clause}


def compatible(formula, indices, modes):
    partial = {}
    for j, mode in zip(indices, modes):
        for var, value in requirements(formula[j], mode).items():
            if var in partial and partial[var] != value:
                return False
            partial[var] = value
    return True


def check_case(case):
    formula = [tuple(c) for c in case["source_formula"]]
    n = nvars(formula)
    checks = Counter()

    assert case["proper_width_three"] == all(
        len(c) == 3 and len(set(map(abs, c))) == 3 for c in formula)

    for row in case["local_clause_targets"]:
        j = row["clause_index"]
        assert row["original_clause"] == list(formula[j])
        for occ in row["occurrences"]:
            lit = occ["literal"]
            s = int(lit > 0)
            assert occ["preferred_S_value"] == s
            assert occ["S_local_all_literals_true"] == s
            assert occ["U_local_all_literals_false"] == 1 - s
            assert occ["invert_S_is_U"] == 1 - s
            assert occ["invert_U_is_S"] == s
            checks["occurrence_targets"] += 1

    pair_lookup = {tuple(row["clause_indices"]): row
                   for row in case["pair_extreme_compatibility"]}
    for j, k in itertools.combinations(range(len(formula)), 2):
        row = pair_lookup[(j, k)]
        assert row["is_conflict_graph_edge"] == conflict(formula[j], formula[k])
        shared = set(map(abs, formula[j])) & set(map(abs, formula[k]))
        same, opposite = set(), set()
        for var in shared:
            sj = next(l > 0 for l in formula[j] if abs(l) == var)
            sk = next(l > 0 for l in formula[k] if abs(l) == var)
            (same if sj == sk else opposite).add(var)
        assert set(row["same_polarity_shared"]) == same
        assert set(row["opposite_polarity_shared"]) == opposite
        for mode in ("SS", "SU", "US", "UU"):
            expected = compatible(formula, (j, k), mode)
            assert row["modes"][mode]["feasible"] == expected
            assert expected == (not opposite if mode in ("SS", "UU") else not same)
            union = sorted(set(map(abs, formula[j])) | set(map(abs, formula[k])))
            brute = 0
            for bits in itertools.product((0, 1), repeat=len(union)):
                a = dict(zip(union, bits))
                t = [sum(a[abs(lit)] == int(lit > 0) for lit in formula[q])
                     for q in (j, k)]
                brute += int(all(t[z] == (3 if mode[z] == "S" else 0)
                                 for z in range(2)))
            assert row["modes"][mode]["coherent_witness_count"] == brute
            checks["pair_modes"] += 1

    triples = case["triple_extreme_compatibility"]
    feasible = infeasible = 0
    for indices in itertools.combinations(range(len(formula)), 3):
        for modes in itertools.product("SU", repeat=3):
            ok = compatible(formula, indices, modes)
            feasible += int(ok)
            infeasible += int(not ok)
            checks["triple_modes"] += 1
    assert triples["feasible_modes"] == feasible
    assert triples["infeasible_modes"] == infeasible

    edges = [(j, k) for j, k in itertools.combinations(range(len(formula)), 2)
             if conflict(formula[j], formula[k])]
    assert case["conflict_graph"]["edges"] == [list(e) for e in edges]
    hitting = len(edges) == len(formula) * (len(formula) - 1) // 2
    assert case["conflict_graph"]["complete"] == hitting

    models = []
    false_hist = Counter()
    profile_hist = Counter()
    minimum_middle = None
    for assignment in range(1 << n):
        values, hist = status(formula, assignment)
        false_hist[hist[0]] += 1
        profile_hist[tuple(hist)] += 1
        complement_values, complement_hist = status(formula, ((1 << n) - 1) ^ assignment)
        assert complement_values == [3 - x for x in values]
        assert complement_hist == list(reversed(hist))
        if hist[0] == 0:
            models.append(assignment)
            middle = hist[1] + hist[2]
            minimum_middle = middle if minimum_middle is None else min(minimum_middle, middle)
        if hitting:
            assert hist[0] <= 1
        checks["assignments_and_complements"] += 1
    exact = case["exact_enumeration"]
    assert exact["model_count"] == len(models)
    assert exact["first_model_mask"] == (models[0] if models else None)
    assert exact["minimum_middle_clauses_over_models"] == minimum_middle
    assert exact["false_clause_multiplicity_histogram"] == {
        str(k): v for k, v in sorted(false_hist.items())}
    assert exact["profile_histogram"] == [
        {"N0_N1_N2_N3": list(p), "assignments": z}
        for p, z in sorted(profile_hist.items())]

    for key, assignment in (("0^n", 0), ("1^n", (1 << n) - 1)):
        values, hist = status(formula, assignment)
        row = case["global_endpoints"][key]
        assert row["per_original_clause_true_literal_counts"] == values
        assert row["N0_N1_N2_N3"] == hist
        assert row["formula_SAT"] == (hist[0] == 0)
        checks["endpoints"] += 1

    if hitting:
        predicted = (1 << n) - sum(1 << (n - len(c)) for c in formula)
        assert case["hitting_closed_form_model_count"] == predicted == len(models)
        checks["hitting_count_formula"] += 1
    else:
        assert case["hitting_closed_form_model_count"] is None

    for proof in case["source_resolvent_prohibited_cubes"]:
        j, k = proof["parent_clause_indices"]
        pivot = proof["pivot_variable"]
        assert any(abs(lit) == pivot and -lit in formula[k] for lit in formula[j])
        cube = {int(var): value for var, value in proof["prohibited_partial_cube"].items()}
        count = 0
        for assignment in range(1 << n):
            if all(((assignment >> (var - 1)) & 1) == value
                   for var, value in cube.items()):
                count += 1
                assert not (any(lit_true(lit, assignment) for lit in formula[j]) and
                            any(lit_true(lit, assignment) for lit in formula[k]))
                checks["resolvent_cube_extensions"] += 1
        assert count == proof["checked_cube_completions"]

    baseline = case["baseline_UP_DPLL"]
    controller = case["hitting_prepass_then_fallback"]
    assert baseline["sat"] == controller["sat"] == bool(models)
    if hitting:
        assert controller["used_hitting_shortcut"]
        if models:
            witness = controller["hitting_witness"]
            assert all(any(witness[str(abs(lit))] == int(lit > 0) if isinstance(next(iter(witness)), str)
                               else witness[abs(lit)] == int(lit > 0) for lit in clause)
                       for clause in formula)
    else:
        assert not controller["used_hitting_shortcut"]
        assert controller["fallback"] is not None
    checks["solver_answers"] += 2
    return checks


def main():
    path = (sys.argv[1] if len(sys.argv) > 1 else
            "2026-10-30_0548_HITTING-CUBE-FIREWALL-REFEREE221_raw.json")
    with open(path) as handle:
        raw = json.load(handle)
    total = Counter()
    for case in raw["cases"]:
        total.update(check_case(case))
    by_name = {case["name"]: case for case in raw["cases"]}
    hit7 = by_name["HIT7_BOTH_ENDPOINTS_FAIL_SAT"]
    assert hit7["conflict_graph"]["complete"]
    assert hit7["exact_enumeration"]["model_count"] == 1
    assert hit7["exact_enumeration"]["first_model_bitstring"] == "001"
    assert not hit7["global_endpoints"]["0^n"]["formula_SAT"]
    assert not hit7["global_endpoints"]["1^n"]["formula_SAT"]
    assert hit7["exact_enumeration"]["minimum_middle_clauses_over_models"] == 6
    hit8 = by_name["HIT8_UNSAT"]
    assert hit8["conflict_graph"]["complete"]
    assert hit8["exact_enumeration"]["model_count"] == 0
    result = {"run_id": raw["run_id"], "status": "PASS",
              "cases": len(raw["cases"]), "checks": dict(total),
              "total_checks": sum(total.values())}
    with open("2026-10-30_0548_HITTING-CUBE-FIREWALL-REFEREE221_check.json", "w") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
