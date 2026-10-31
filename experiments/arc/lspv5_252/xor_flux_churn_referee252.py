#!/usr/bin/env python3
"""REFEREE252: endpoint-plus-churn decomposition of logical XOR activity.

The logical vectors are offline aligned diagnostics.  The declared physical
checkpoint models are representation-specific and are not universal SAT costs.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import itertools
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREV_PATH = ROOT / "experiments/arc/lspv5_251/xor_activity_identity_referee251.py"
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1648_LSPV5_XOR_FLUX_CHURN_REFEREE252_raw.json"


def load_previous():
    spec = importlib.util.spec_from_file_location("ref251", PREV_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_u() -> list[list[int]]:
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def histogram(formula: list[list[int]], assignment: list[int], prev) -> list[int]:
    h = [0, 0, 0, 0]
    for clause in formula:
        h[prev.tcount(clause, assignment)] += 1
    return h


def flux_step(formula: list[list[int]], assignment: list[int], var0: int, prev) -> dict:
    before = [prev.tcount(c, assignment) for c in formula]
    row = prev.flip_record(formula, assignment, var0)
    after_assignment = row["after_assignment"]
    after = [prev.tcount(c, after_assignment) for c in formula]
    transitions = Counter()
    for j in row["changed_clause_ids_zero_based"]:
        transitions[f"{before[j]}to{after[j]}"] += 1
        assert abs(before[j] - after[j]) == 1
    assert sum(transitions.values()) == 4
    return {
        "variable_zero_based": var0,
        "changed_clause_ids_zero_based": row["changed_clause_ids_zero_based"],
        "transitions": dict(sorted(transitions.items())),
        "d_logic": row["observed_d_logic"],
        "after_assignment": after_assignment,
    }


def sequence_flux(formula: list[list[int]], start: list[int], variables: list[int], prev) -> dict:
    a = start[:]
    start_h = histogram(formula, a, prev)
    totals = Counter()
    dsum = Counter()
    changed = Counter()
    first = []
    for step, var in enumerate(variables):
        row = flux_step(formula, a, var, prev)
        totals.update(row["transitions"])
        dsum.update(row["d_logic"])
        changed.update(row["changed_clause_ids_zero_based"])
        if step < 12:
            keep = dict(row)
            keep.pop("after_assignment")
            first.append(keep)
        a = row["after_assignment"]
    end_h = histogram(formula, a, prev)
    r0, f0 = totals["0to1"], totals["1to0"]
    u1, d1 = totals["1to2"], totals["2to1"]
    delta_n0 = end_h[0] - start_h[0]
    delta_m = (end_h[0] + end_h[1]) - (start_h[0] + start_h[1])
    c0, c1 = min(r0, f0), min(u1, d1)
    b, h = r0 + f0, u1 + d1
    assert delta_n0 == f0 - r0
    assert delta_m == d1 - u1
    assert b == abs(delta_n0) + 2 * c0
    assert h == abs(delta_m) + 2 * c1
    T = len(variables)
    rhs_gray = 5 * T + abs(delta_n0) + 2 * c0
    rhs_binary = 5 * T + abs(delta_n0) + abs(delta_m) + 2 * (c0 + c1)
    assert dsum["gray"] == rhs_gray
    assert dsum["binary"] == rhs_binary
    return {
        "steps": T,
        "start_histogram_N0_N1_N2_N3": start_h,
        "end_histogram_N0_N1_N2_N3": end_h,
        "delta_N0": delta_n0,
        "delta_N0_plus_N1": delta_m,
        "directional_crossings": dict(sorted(totals.items())),
        "zero_boundary_total_B": b,
        "middle_boundary_total_H": h,
        "paired_churn_C0": c0,
        "paired_churn_C1": c1,
        "sum_adjacent_d_logic": {"gray": dsum["gray"], "binary": dsum["binary"]},
        "endpoint_d_logic": {
            enc: prev.hd(prev.state(formula, start, enc), prev.state(formula, a, enc))
            for enc in ("gray", "binary")
        },
        "identity_rhs": {"gray": rhs_gray, "binary": rhs_binary},
        "changed_record_frequency": dict(sorted(changed.items())),
        "first_12_steps": first,
    }


def exhaustive_y6_short_paths(formula: list[list[int]], prev) -> dict:
    checked = assertions = 0
    churn_loops = 0
    for bits in itertools.product((0, 1), repeat=6):
        start = list(bits)
        for length in range(4):
            for variables in itertools.product(range(6), repeat=length):
                row = sequence_flux(formula, start, list(variables), prev)
                assert row["sum_adjacent_d_logic"] == row["identity_rhs"]
                assertions += 8
                if length == 2 and variables[0] == variables[1]:
                    assert row["endpoint_d_logic"] == {"gray": 0, "binary": 0}
                    assert row["sum_adjacent_d_logic"]["gray"] >= 10
                    churn_loops += 1
                checked += 1
    return {"paths_length_0_through_3": checked, "assertions": assertions, "two_flip_restored_loops": churn_loops}


def physical_checkpoint_models(logical: dict) -> dict:
    T = logical["steps"]
    return {
        "materialized_gray_fixed_slots": {
            "complete_checkpoint_state": "assignment plus every Gray count and SAT-status bit",
            "sum_adjacent_d_phys": logical["sum_adjacent_d_logic"]["gray"],
            "endpoint_d_phys": logical["endpoint_d_logic"]["gray"],
            "lower_bound_k_tapes": "sum_i ceil(d_phys_i/k) on disjoint intervals",
        },
        "materialized_binary_fixed_slots": {
            "complete_checkpoint_state": "assignment plus every binary count and SAT-status bit",
            "sum_adjacent_d_phys": logical["sum_adjacent_d_logic"]["binary"],
            "endpoint_d_phys": logical["endpoint_d_logic"]["binary"],
        },
        "lazy_assignment_fixed_slots": {
            "complete_checkpoint_state": "assignment tape; scratch, control and index fields reset to identical zero checkpoint values; no clause-status tape",
            "sum_adjacent_d_phys": T,
            "endpoint_d_phys": sum(v & 1 for v in []),
            "checkpoint_note": "endpoint is recomputed below from flip parity; clause-state d_logic is virtual",
            "paid_but_not_visible_in_checkpoint_xor": {
                "assignment_cell_writes": T,
                "incident_literal_source_reads_after_supplied_occurrence_index": 12 * T,
                "index_head_motion_and_resets": "charged but not natively simulated here",
            },
        },
        "DELAY_read_only_loop": {"native_steps": 10000, "sum_adjacent_data_d_phys": 0, "endpoint_data_d_phys": 0},
        "scope": "representation-specific diagnostic, not an arbitrary-machine lower bound or FLMV upper bound",
    }


def add_lazy_endpoint(row: dict, variables: list[int]) -> None:
    parity = Counter(variables)
    row["lazy_assignment_fixed_slots"]["endpoint_d_phys"] = sum(v % 2 for v in parity.values())


def malformed_controls(Y: list[list[int]], base) -> dict:
    bad = {
        "missing_clause": Y[:-1],
        "duplicate_clause": Y + [Y[0]],
        "mixed_sign": [[1, -2, 3]] + Y[1:],
        "repeated_variable": [[1, 1, 2]] + Y[1:],
        "wrong_occurrence_count": [c[:] for c in Y[:-1]] + [[1, 2, 6]],
    }
    out = {name: base.valid_target(f) for name, f in bad.items()}
    assert all(not row["valid"] for row in out.values())
    return out


def hostile_controls(prev) -> dict:
    formulas = {
        "Horn": [[-1, -2, -3], [1]],
        "two_SAT": [[1, 2], [-1, 2], [1, -2]],
        "easy_XOR": [[1, 2, 3], [1, -2, -3], [-1, 2, -3], [-1, -2, 3]],
        "bounded_treewidth": [[1, 2], [-2, 3], [-3, 4]],
    }
    checked = {}
    for name, formula in formulas.items():
        n = max(abs(x) for c in formula for x in c)
        count = 0
        for a in itertools.product((0, 1), repeat=n):
            for v in range(n):
                prev.flip_record(formula, list(a), v)
                count += 1
        checked[name] = count
    checked["wrapper_falsifiers"] = {
        "lazy_flags": "large virtual clause-state delta with one assignment-cell write per checkpoint",
        "changed_then_restored": "zero endpoint with positive adjacent XOR and arbitrarily repeatable churn",
        "source_reread": "positive time with zero writable data-bit delta",
        "unaligned_encoding": "requires declared canonical alignment; variable-length insertion invalidates direct cellwise XOR",
        "DELAY": "arbitrarily many read-only steps with zero data-bit XOR",
    }
    return checked


def main() -> int:
    started = time.perf_counter()
    prev = load_previous()
    base = prev.load_base()
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = prev.y6()
    assert all(base.valid_target(F)["valid"] for F in (Y, U, V))

    cert = base.module_certificate(U)
    assert cert["proved_unsat_254_clause_subformula"] and cert["joint_rows"] == []
    witness = base.replay(V, base.SAT_WITNESS)
    assert witness["satisfied"]
    models = sum(base.replay(Y, "".join(map(str, a)))["satisfied"] for a in itertools.product((0, 1), repeat=6))
    assert models == 20

    rng = random.Random(2521648)
    shared_trace = [rng.randrange(198) for _ in range(1000)]
    loop_trace = [0] * 1000
    y_sweep = list(range(6))
    rows = {
        "Y6_binary_order_sweep": sequence_flux(Y, [0] * 6, y_sweep, prev),
        "Y6_restored_loop": sequence_flux(Y, [0] * 6, [0] * 200, prev),
        "U198_shared_random": sequence_flux(U, [0] * 198, shared_trace, prev),
        "V198_shared_random": sequence_flux(V, [0] * 198, shared_trace, prev),
        "U198_restored_loop": sequence_flux(U, [0] * 198, loop_trace, prev),
        "V198_restored_loop": sequence_flux(V, [0] * 198, loop_trace, prev),
    }
    physical = {}
    trace_map = {
        "Y6_binary_order_sweep": y_sweep,
        "Y6_restored_loop": [0] * 200,
        "U198_shared_random": shared_trace,
        "V198_shared_random": shared_trace,
        "U198_restored_loop": loop_trace,
        "V198_restored_loop": loop_trace,
    }
    for name, row in rows.items():
        physical[name] = physical_checkpoint_models(row)
        add_lazy_endpoint(physical[name], trace_map[name])

    raw = {
        "run_id": "XOR-FLUX-CHURN-REFEREE252",
        "timestamp": "2026-10-31 16:48 America/Los_Angeles",
        "obstruction": "cumulative logical XOR mixes endpoint boundary flux with arbitrarily repeatable opposite-direction churn",
        "theorem": {
            "quantifiers": "every valid canonical target formula, every complete start assignment, every finite variable-flip sequence",
            "gray": "sum d_logic = 5T + |Delta N0| + 2*C0",
            "binary": "sum d_logic = 5T + |Delta N0| + |Delta(N0+N1)| + 2*(C0+C1)",
            "C0": "min(total 0->1 crossings,total 1->0 crossings)",
            "C1": "min(total 1->2 crossings,total 2->1 crossings)",
            "scope": "aligned source-indexed assignment/count/status representation; offline diagnostic",
        },
        "falsifiers": {
            "F1": "boundary activity is monotone progress toward SAT",
            "F2": "fixed endpoints determine cumulative logical XOR",
            "F3": "XOR churn distinguishes same-target SAT from UNSAT",
            "F4": "logical XOR churn is an unavoidable physical-write/runtime tariff for arbitrary solvers",
        },
        "same_target_labels": {
            "Y6": {"status": "SAT", "models": models, "n": 6, "m": 8},
            "U198": {"status": "UNSAT", "certificate_nodes": cert["dpll_nodes"], "joint_rows": cert["joint_rows"], "n": 198, "m": 264},
            "V198": {"status": "SAT", "witness_sha256": hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest(), "n": 198, "m": 264},
        },
        "malformed_rejections": malformed_controls(Y, base),
        "exhaustive_Y6_short_paths": exhaustive_y6_short_paths(Y, prev),
        "sequence_flux_ledgers": rows,
        "physical_checkpoint_models": physical,
        "actual_search_baseline": {
            "Y6": base.dpll(Y, {}, cap=None),
            "U198": base.dpll(U, {}, cap=200),
            "V198": base.dpll(V, {}, cap=200),
        },
        "signed_clause_extremes": {
            "U198": base.clause_extreme_control(U),
            "V198": base.clause_extreme_control(V),
        },
        "hostile_controls": hostile_controls(prev),
        "search_record": {
            "web_queries": [
                "discrete coarea formula graph paths level set crossings total variation",
                "SAT local search make break score clause transitions original paper GSAT WalkSAT",
                "Döcker Monotone 3-SAT-(2,2) duplicate-free proper NP-complete paper",
                "Fortnow Lipton van Melkebeek Viglas SAT time space lower bound paper",
            ],
            "github_project_query": "XOR flux churn N0 boundary crossings",
            "github_openai_query": "SAT XOR state difference churn",
            "github_findings": "no matching project/openai implementation; absence is not novelty evidence",
            "cross_field": "graph coarea/total-variation boundary crossings are an ANALOGY/CANDIDATE only; no runtime transfer",
        },
        "resource_ledger": {
            "discovery": "the trace is supplied; discovering a useful policy remains charged",
            "policy_selection_switching": "not supplied by the identity",
            "failed_trials": "capped U/V DPLL UNKNOWN retained",
            "source_tape_query_child_retained": "all source reads, indices, children, guest tapes and ancestor state remain outside d_logic and charged",
            "logical_tracing": "offline; internal full-state XOR calculation would require scanning/materialization",
            "physical": "only declared fixed-slot checkpoint models are measured; no native FLMV upper bound",
            "output_and_space": "raw JSON/Python allocation is audit material, not same-machine writable space",
        },
        "proof_status": {
            "endpoint_plus_churn_identity": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "XOR_as_monotone_progress_or_universal_hardness": "FALSIFIED/RETIRED",
            "arbitrary_A_to_Phi_A_ARC": "OPEN",
            "numerical_FLMV_transport": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    raw["elapsed_seconds"] = time.perf_counter() - started
    assert raw["actual_search_baseline"]["Y6"]["status"] == "SAT"
    assert raw["actual_search_baseline"]["U198"]["status"] == "UNKNOWN"
    assert raw["actual_search_baseline"]["V198"]["status"] == "UNKNOWN"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "run": raw["run_id"],
        "elapsed_seconds": raw["elapsed_seconds"],
        "Y6_short_paths": raw["exhaustive_Y6_short_paths"],
        "U_random": {k: rows["U198_shared_random"][k] for k in ("steps", "delta_N0", "delta_N0_plus_N1", "paired_churn_C0", "paired_churn_C1", "sum_adjacent_d_logic", "endpoint_d_logic")},
        "V_random": {k: rows["V198_shared_random"][k] for k in ("steps", "delta_N0", "delta_N0_plus_N1", "paired_churn_C0", "paired_churn_C1", "sum_adjacent_d_logic", "endpoint_d_logic")},
        "loop_endpoint": rows["U198_restored_loop"]["endpoint_d_logic"],
        "loop_sum": rows["U198_restored_loop"]["sum_adjacent_d_logic"],
    }, indent=2))
    print("VERIFIED::XOR-FLUX-CHURN-REFEREE252")
    return 0


if __name__ == "__main__":
    sys.exit(main())
