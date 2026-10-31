#!/usr/bin/env python3
"""ARC source-blocker compression firewall 232.

Source-derived blockers are globally valid and useful for pruning, but there
are two different physical objects:

  (1) F plus its learned blockers, which is exact but retains the full source;
  (2) the blockers alone, which is only a relaxation unless a separately
      checked completeness/equivalence proof is supplied.

The matched proper-3CNF controls have identical unsigned clause-support
multisets and equal clause counts.  The SAT source has the unique all-one
model.  The UNSAT source replaces one duplicate clause in the first block by
the missing eighth sign pattern.  Both sources entail every positive unit, so
the same blocker-only formula is satisfiable on both labels.

Selected event counters are Python logical-operation proxies, not native FLMV
Turing-machine transition or peak-space measurements.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from collections import Counter
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


def falsified_clause(values, offset):
    return tuple((offset + i + 1) if bit == 0 else -(offset + i + 1)
                 for i, bit in enumerate(values))


def block_clauses(offset, unsat=False):
    patterns = list(itertools.product((0, 1), repeat=3))
    clauses = [falsified_clause(u, offset) for u in patterns if u != (1, 1, 1)]
    if unsat:
        clauses.append(falsified_clause((1, 1, 1), offset))
    else:
        clauses.append(falsified_clause((0, 0, 0), offset))  # duplicate support/sign
    return clauses


def pair_sources(blocks):
    sat = []
    unsat = []
    for j in range(blocks):
        sat.extend(block_clauses(3 * j, unsat=False))
        unsat.extend(block_clauses(3 * j, unsat=(j == 0)))
    return sat, unsat


def eval_clause(clause, mask):
    return any((((mask >> (abs(lit) - 1)) & 1) == 1) == (lit > 0)
               for lit in clause)


def eval_formula(formula, mask):
    return all(eval_clause(c, mask) for c in formula)


def restrict(formula, cube):
    out = []
    visits = 0
    for clause in formula:
        residual = []
        satisfied = False
        for lit in clause:
            visits += 1
            v = abs(lit)
            if v not in cube:
                residual.append(lit)
            elif cube[v] == int(lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return out, visits


def unsigned_supports(formula):
    return Counter(tuple(sorted(abs(l) for l in c)) for c in formula)


def blocker_case(name, formula, blocks, include_details=False):
    n = 3 * blocks
    models = [m for m in range(1 << n) if eval_formula(formula, m)]
    units = [(i,) for i in range(1, n + 1)]
    all_one = (1 << n) - 1
    assert all(eval_formula(units, m) for m in range(1 << n)
               if eval_formula(formula, m))

    residual_rows = []
    residual_work = 0
    for i in range(1, n + 1):
        child, visits = restrict(formula, {i: 0})
        solved = P.dpll(child, trace_memory=False)
        assert not solved["sat"]
        residual_rows.append({
            "cube": {str(i): 0},
            "learned_source_blocker": [i],
            "child_clause_count": len(child),
            "construction_literal_visits": visits,
            "child_dpll_nodes": solved["events"]["nodes"],
            "child_dpll_selected_events": solved["selected_events"],
        })
        residual_work += visits + solved["selected_events"]

    baseline = P.dpll(formula, trace_memory=False)
    blockers_only = P.dpll(units, trace_memory=False)
    source_preserving = list(formula) + units
    preserved = P.dpll(source_preserving, trace_memory=False)
    assert baseline["sat"] == bool(models)
    assert blockers_only["sat"]
    assert preserved["sat"] == baseline["sat"]

    # Exact completion of the uncovered all-one point.
    completion_visits = sum(len(c) for c in formula)
    completion_answer = eval_formula(formula, all_one)
    assert completion_answer == bool(models)
    selected_controller = residual_work + completion_visits

    row = {
        "name": name,
        "blocks": blocks,
        "n": n,
        "source_clause_count": len(formula),
        "source_literal_tokens": sum(len(c) for c in formula),
        "source_formula": [list(c) for c in formula],
        "model_count": len(models),
        "models": models,
        "sat": bool(models),
        "common_source_blockers": [list(c) for c in units],
        "blockers_only_sat": blockers_only["sat"],
        "blockers_only_model_count": 1,
        "blockers_only_unique_model": all_one,
        "source_preserving_clause_count": len(source_preserving),
        "source_preserving_literal_tokens": sum(len(c) for c in source_preserving),
        "source_preserving_sat": preserved["sat"],
        "residuals": residual_rows,
        "uncovered_assignment": all_one,
        "uncovered_assignment_source_sat": completion_answer,
        "baseline_dpll_nodes": baseline["events"]["nodes"],
        "baseline_dpll_selected_events": baseline["selected_events"],
        "certified_controller_selected_events": selected_controller,
        "global_endpoints": {
            "0^n": P.status(formula, 0),
            "1^n": P.status(formula, all_one),
        },
    }
    if include_details:
        row.update({
            "local_clause_targets": P.local_targets(formula),
            "source_clause_pair_extremes": P.pair_extremes(formula),
            "intermediate_flip_trails": P.flip_trails(formula),
        })
    return row


def hostile_controls():
    rows = []
    for name, formula in P.CASES:
        d = P.dpll(formula, trace_memory=False)
        rows.append({
            "name": name,
            "n": P.nvars(formula),
            "m": len(formula),
            "sat": d["sat"],
            "dpll_nodes": d["events"]["nodes"],
            "dpll_selected_events": d["selected_events"],
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    cases = []
    for blocks in range(1, 6):
        sat, unsat = pair_sources(blocks)
        assert len(sat) == len(unsat) == 8 * blocks
        assert unsigned_supports(sat) == unsigned_supports(unsat)
        sat_row = blocker_case(f"SAT_UNIQUE_ALL_ONE_B{blocks}", sat, blocks,
                               include_details=(blocks == 1))
        unsat_row = blocker_case(f"UNSAT_FIRST_BLOCK_COMPLETE_B{blocks}", unsat,
                                 blocks, include_details=(blocks == 1))
        assert sat_row["models"] == [(1 << (3 * blocks)) - 1]
        assert unsat_row["models"] == []
        assert sat_row["common_source_blockers"] == unsat_row["common_source_blockers"]
        assert sat_row["blockers_only_sat"] and unsat_row["blockers_only_sat"]
        cases.append({
            "blocks": blocks,
            "same_unsigned_support_multiset": True,
            "same_clause_count": True,
            "SAT": sat_row,
            "UNSAT": unsat_row,
        })

    result = {
        "id": "ARC-SOURCE-BLOCKER-COMPRESSION-FIREWALL232",
        "date": "2026-10-30 20:48 America/Los_Angeles",
        "status": {
            "append_only_source_blocker_theorem": "PROVED/EXACT restricted explicit encoding",
            "blockers_alone_are_exact_child": "FALSIFIED/RETIRED",
            "finite_controls": "COMPUTATIONAL",
            "arbitrary_A_to_Phi_A": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "theorem_checked": [
            "If every D_i is entailed by F, then F AND all D_i is equivalent to F but an explicit append-only encoding retains all N source bits.",
            "The blocker-only conjunction is a relaxation: F implies B. UNSAT(B) certifies UNSAT(F), but SAT(B) does not certify SAT(F).",
            "A source-derived blocker or proof can be globally valid without being a power-short exact ordinary-SAT child.",
        ],
        "matched_same_support_cases": cases,
        "hostile_controls": hostile_controls(),
        "limitations": [
            "The lower bound is for the declared explicit source-preserving append-only representation, not arbitrary semantic re-encoding.",
            "An UNSAT blocker conjunction is a valid proof endpoint; the falsifier concerns using a satisfiable blocker relaxation as an exact SAT child.",
            "The unique-model family is deliberately easy and is an adverse representation control, not SAT hardness.",
            "Selected Python events are not native FLMV transitions or simultaneous tape-space measurements.",
        ],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
