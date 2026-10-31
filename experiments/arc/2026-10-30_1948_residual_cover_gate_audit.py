#!/usr/bin/env python3
"""ARC residual-cover gate 231.

Pairwise-overlapping exact residual cubes do not certify a global SAT/UNSAT
composition.  The producer uses the seven-clause proper-3CNF with unique model
111 and its same-support eight-clause UNSAT completion.  Three residual cubes
x1=0, x2=0, x3=0 pairwise overlap and are all UNSAT on both sources, but leave
111 uncovered.  The missing eighth source clause is exactly the blocker that
certifies the uncovered point only on the UNSAT source.

Selected event counters are reproducible Python-level logical operations, not
native FLMV transition counts.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "clause_extremes" / "2026-10-30_0548_HITTING-CUBE-FIREWALL-REFEREE221_repro.py"


def load_old():
    spec = importlib.util.spec_from_file_location("hit221", OLD)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {OLD}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load_old()


def assignment_dict(mask, n):
    return {i + 1: (mask >> i) & 1 for i in range(n)}


def cube_holds(cube, mask):
    return all(((mask >> (v - 1)) & 1) == value for v, value in cube.items())


def cubes_compatible(a, b):
    return all(v not in b or b[v] == value for v, value in a.items())


def restrict(formula, cube):
    out = []
    source_literal_visits = 0
    for clause in formula:
        residual = []
        satisfied = False
        for lit in clause:
            source_literal_visits += 1
            var = abs(lit)
            if var not in cube:
                residual.append(lit)
            elif cube[var] == int(lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return out, source_literal_visits


def eval_formula(formula, mask):
    return all(any((((mask >> (abs(l) - 1)) & 1) == 1) == (l > 0)
                   for l in clause) for clause in formula)


def residual_row(formula, cube):
    child, construction = restrict(formula, cube)
    solved = P.dpll(child, trace_memory=False)
    return {
        "cube": {str(k): v for k, v in cube.items()},
        "child": [list(c) for c in child],
        "child_sat": solved["sat"],
        "child_dpll_selected_events": solved["selected_events"],
        "child_construction_literal_visits": construction,
    }


def pairwise_cube_matrix(cubes, n):
    rows = []
    for i, j in itertools.combinations(range(len(cubes)), 2):
        compatible = cubes_compatible(cubes[i], cubes[j])
        witnesses = [m for m in range(1 << n)
                     if cube_holds(cubes[i], m) and cube_holds(cubes[j], m)]
        assert compatible == bool(witnesses)
        rows.append({"cube_indices": [i, j], "compatible": compatible,
                     "overlap_size": len(witnesses),
                     "first_overlap_assignment": witnesses[0] if witnesses else None})
    return rows


def source_case(name, formula, cubes):
    n = 3
    models = [m for m in range(1 << n) if eval_formula(formula, m)]
    covered = [m for m in range(1 << n) if any(cube_holds(c, m) for c in cubes)]
    uncovered = [m for m in range(1 << n) if m not in covered]
    rows = [residual_row(formula, c) for c in cubes]
    all_children_unsat = all(not r["child_sat"] for r in rows)
    cover_clause = tuple(-(i + 1) for i in range(n))  # not x1 or not x2 or not x3
    scan_visits = 0
    blocker_present = False
    for clause in formula:
        scan_visits += len(clause)
        if tuple(clause) == cover_clause:
            blocker_present = True
    baseline = P.dpll(formula, trace_memory=False)
    assert baseline["sat"] == bool(models)

    # The restricted certified controller: solve the three cubes; if all are
    # UNSAT, use the exact source blocker if present, otherwise solve the one
    # uncovered complete assignment.  This is exact for this declared cover.
    completion_checks = 0
    completion_sat = False
    if all_children_unsat and not blocker_present:
        for m in uncovered:
            completion_checks += sum(len(c) for c in formula)
            completion_sat |= eval_formula(formula, m)
    certified_answer = (not all_children_unsat) or completion_sat
    if all_children_unsat and blocker_present:
        certified_answer = False
    assert certified_answer == bool(models)

    residual_work = sum(r["child_dpll_selected_events"] +
                        r["child_construction_literal_visits"] for r in rows)
    total_work = residual_work + scan_visits + completion_checks
    return {
        "name": name,
        "source_formula": [list(c) for c in formula],
        "models": models,
        "model_count": len(models),
        "parent_sat": bool(models),
        "pairwise_overlap_matrix": pairwise_cube_matrix(cubes, n),
        "covered_assignments": covered,
        "uncovered_assignments": uncovered,
        "residuals": rows,
        "all_three_children_unsat": all_children_unsat,
        "unsound_pairwise_policy_answer": False if all_children_unsat else True,
        "unsound_pairwise_policy_correct": (False if all_children_unsat else True) == bool(models),
        "source_cover_blocker": {
            "clause": list(cover_clause),
            "present_verbatim": blocker_present,
            "meaning": "F entails x1=0 OR x2=0 OR x3=0 when this source clause is present",
            "falsifying_cube": {"1": 1, "2": 1, "3": 1},
            "source_scan_literal_visits": scan_visits,
        },
        "certified_controller_answer": certified_answer,
        "certified_controller_correct": certified_answer == bool(models),
        "certified_controller_selected_work": total_work,
        "baseline_up_dpll_selected_work": baseline["selected_events"],
        "baseline_up_dpll_nodes": baseline["events"]["nodes"],
        "local_clause_targets": P.local_targets(formula),
        "source_clause_pair_extremes": P.pair_extremes(formula),
        "global_endpoints": {"0^n": P.status(formula, 0), "1^n": P.status(formula, 7)},
        "intermediate_flip_trails": P.flip_trails(formula),
    }


def hostile_control_table():
    rows = []
    for name, formula in P.CASES:
        d = P.dpll(formula, trace_memory=False)
        rows.append({"name": name, "n": P.nvars(formula), "m": len(formula),
                     "sat": d["sat"], "dpll_nodes": d["events"]["nodes"],
                     "dpll_selected_events": d["selected_events"]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    # P.HIT7 omits the clause falsified by 001 in its historical orientation.
    # Build the orientation required here directly: omit the 111 blocker.
    blocker = (-1, -2, -3)
    sat7 = [c for c in P.ALL8 if tuple(c) != blocker]
    unsat8 = list(P.ALL8)
    cubes = [{1: 0}, {2: 0}, {3: 0}]
    sat = source_case("SEVEN_CLAUSE_UNIQUE_111_SAT", sat7, cubes)
    unsat = source_case("EIGHT_CLAUSE_FULL_CUBE_UNSAT", unsat8, cubes)
    assert sat["models"] == [7] and unsat["models"] == []
    assert not sat["unsound_pairwise_policy_correct"]
    assert unsat["unsound_pairwise_policy_correct"]
    assert not sat["source_cover_blocker"]["present_verbatim"]
    assert unsat["source_cover_blocker"]["present_verbatim"]
    assert sat["certified_controller_correct"] and unsat["certified_controller_correct"]

    result = {
        "id": "ARC-RESIDUAL-COVER-GATE231",
        "date": "2026-10-30 19:48 America/Los_Angeles",
        "status": {
            "source_relative_cover_lemma": "PROVED/EXACT restricted composition criterion",
            "pairwise_overlap_implies_global_cover": "FALSIFIED/RETIRED",
            "finite_controls": "COMPUTATIONAL",
            "arbitrary_A_to_Phi_A": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "theorem_checked": (
            "For cubes rho_i, OR_i SAT(F|rho_i) always implies SAT(F). "
            "The converse is guaranteed by the source-relative certificate "
            "F entails OR_i cube(rho_i). Pairwise cube overlap does not imply it."
        ),
        "cubes": [{str(k): v for k, v in c.items()} for c in cubes],
        "same_support_opposite_label_sources": {"SAT": sat, "UNSAT": unsat},
        "hostile_controls": hostile_control_table(),
        "limitations": [
            "The verbatim blocker is a convenient source certificate for this family; general entailment needs a charged proof.",
            "Pairwise overlap failure is an architecture counterexample, not an arbitrary-SAT lower bound.",
            "The certified controller is exact only for the declared three-cube plus singleton-completion cover.",
            "Selected Python logical events are not native FLMV transitions or peak tape measurements.",
        ],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
