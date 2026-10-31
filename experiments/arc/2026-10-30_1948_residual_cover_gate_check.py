#!/usr/bin/env python3
"""Independent checker for ARC-RESIDUAL-COVER-GATE231 raw output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def lit_true(lit, mask):
    return ((((mask >> (abs(lit) - 1)) & 1) == 1) == (lit > 0))


def formula_sat(formula, mask):
    return all(any(lit_true(l, mask) for l in c) for c in formula)


def cube_holds(cube, mask):
    return all(((mask >> (int(v) - 1)) & 1) == value for v, value in cube.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = json.loads(args.raw.read_text(encoding="utf-8"))
    assert data["id"] == "ARC-RESIDUAL-COVER-GATE231"
    checks = 1
    cubes = data["cubes"]
    controls = data["same_support_opposite_label_sources"]
    for side, expected in (("SAT", True), ("UNSAT", False)):
        c = controls[side]
        formula = c["source_formula"]
        models = [m for m in range(8) if formula_sat(formula, m)]
        assert models == c["models"]
        assert bool(models) == expected == c["parent_sat"]
        covered = [m for m in range(8) if any(cube_holds(cu, m) for cu in cubes)]
        assert covered == c["covered_assignments"] == list(range(7))
        assert c["uncovered_assignments"] == [7]
        checks += 5
        for row in c["pairwise_overlap_matrix"]:
            i, j = row["cube_indices"]
            overlap = [m for m in range(8) if cube_holds(cubes[i], m) and cube_holds(cubes[j], m)]
            assert row["compatible"] and overlap
            assert len(overlap) == row["overlap_size"]
            checks += 2
        for residual in c["residuals"]:
            cu = residual["cube"]
            # Directly check no parent model lies in the residual cube.
            assert not any(cube_holds(cu, m) for m in models)
            assert residual["child_sat"] is False
            checks += 2
        assert c["all_three_children_unsat"]
        assert c["certified_controller_correct"]
        checks += 2

        # Recheck all local occurrence S/U target inversions.
        for clause in c["local_clause_targets"]:
            for occ in clause["occurrences"]:
                assert occ["invert_S_is_U"] == occ["U_local_all_literals_false"]
                assert occ["invert_U_is_S"] == occ["S_local_all_literals_true"]
                checks += 2
        # Recheck complement identity for the explicit endpoint records.
        zero = c["global_endpoints"]["0^n"]["per_original_clause_true_literal_counts"]
        one = c["global_endpoints"]["1^n"]["per_original_clause_true_literal_counts"]
        assert all(a + b == 3 for a, b in zip(zero, one))
        checks += len(zero)

    sat, no = controls["SAT"], controls["UNSAT"]
    assert not sat["source_cover_blocker"]["present_verbatim"]
    assert no["source_cover_blocker"]["present_verbatim"]
    assert sat["unsound_pairwise_policy_correct"] is False
    assert no["unsound_pairwise_policy_correct"] is True
    assert sat["certified_controller_answer"] is True
    assert no["certified_controller_answer"] is False
    checks += 6
    names = {r["name"]: r for r in data["hostile_controls"]}
    assert names["W1_STRICT22_UNSAT"]["sat"] is False
    assert names["SWAP6_STRICT22_SAT"]["sat"] is True
    assert names["TSEITIN_K4_ODD_UNSAT"]["sat"] is False
    assert names["DENSE_PLANTED_SAT"]["sat"] is True
    checks += 4
    result = {"id": data["id"], "status": "PASS", "independent_checks": checks}
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
