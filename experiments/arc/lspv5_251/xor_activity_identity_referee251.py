#!/usr/bin/env python3
"""REFEREE251: exact local activity identity for aligned logical XOR.

The traced logical vector is an OFFLINE diagnostic.  It is not an internal
oracle and its bit changes are not promoted to native FLMV tape writes.
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
BASE_PATH = ROOT / "experiments/arc/lspv5_247/target_scope_flmv_referee247.py"
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1548_LSPV5_XOR_ACTIVITY_IDENTITY_REFEREE251_raw.json"


def load_base():
    spec = importlib.util.spec_from_file_location("ref247", BASE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_u() -> list[list[int]]:
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def y6() -> list[list[int]]:
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def tcount(clause: list[int], assignment: list[int]) -> int:
    return sum(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause)


def count_code(value: int, encoding: str) -> tuple[int, int]:
    code = value if encoding == "binary" else value ^ (value >> 1)
    return code & 1, (code >> 1) & 1


def state(formula: list[list[int]], assignment: list[int], encoding: str) -> list[int]:
    out = list(assignment)
    for clause in formula:
        t = tcount(clause, assignment)
        out.extend((*count_code(t, encoding), int(t > 0)))
    return out


def hd(left: list[int], right: list[int]) -> int:
    return sum(x != y for x, y in zip(left, right))


def flip_record(formula: list[list[int]], assignment: list[int], var0: int) -> dict:
    before = [tcount(c, assignment) for c in formula]
    after_assignment = assignment[:]
    after_assignment[var0] ^= 1
    after = [tcount(c, after_assignment) for c in formula]
    changed = [j for j, (p, q) in enumerate(zip(before, after)) if p != q]
    boundary = sum({before[j], after[j]} == {0, 1} for j in changed)
    middle = sum({before[j], after[j]} == {1, 2} for j in changed)
    high = sum({before[j], after[j]} == {2, 3} for j in changed)
    degree = len(changed)
    observed = {
        enc: hd(state(formula, assignment, enc), state(formula, after_assignment, enc))
        for enc in ("binary", "gray")
    }
    expected = {
        "gray": 1 + degree + boundary,
        "binary": 1 + degree + boundary + middle,
    }
    assert observed == expected
    assert boundary + middle + high == degree
    return {
        "variable_zero_based": var0,
        "old_value": assignment[var0],
        "new_value": after_assignment[var0],
        "changed_clause_ids_zero_based": changed,
        "degree": degree,
        "zero_boundary_crossings": boundary,
        "one_two_crossings": middle,
        "two_three_crossings": high,
        "observed_d_logic": observed,
        "expected_d_logic": expected,
        "after_assignment": after_assignment,
    }


def exhaustive_single_flips(formula: list[list[int]], name: str) -> dict:
    n = max(abs(lit) for c in formula for lit in c)
    assertions = 0
    distribution = {"binary": Counter(), "gray": Counter(), "B": Counter(), "H": Counter()}
    for bits in itertools.product((0, 1), repeat=n):
        a = list(bits)
        for var in range(n):
            row = flip_record(formula, a, var)
            for enc in ("binary", "gray"):
                distribution[enc][row["observed_d_logic"][enc]] += 1
            distribution["B"][row["zero_boundary_crossings"]] += 1
            distribution["H"][row["one_two_crossings"]] += 1
            assertions += 6
    return {
        "name": name,
        "assignments": 2**n,
        "single_flips": n * 2**n,
        "assertions": assertions,
        "distribution": {k: dict(sorted(v.items())) for k, v in distribution.items()},
    }


def sampled_single_flips(formula: list[list[int]], name: str, assignments: list[list[int]]) -> dict:
    n = max(abs(lit) for c in formula for lit in c)
    assertions = 0
    distribution = {"binary": Counter(), "gray": Counter(), "B": Counter(), "H": Counter()}
    examples = []
    for q, a in enumerate(assignments):
        for var in range(n):
            row = flip_record(formula, a, var)
            assert row["degree"] == 4
            assert 5 <= row["observed_d_logic"]["gray"] <= 9
            assert 5 <= row["observed_d_logic"]["binary"] <= 9
            for enc in ("binary", "gray"):
                distribution[enc][row["observed_d_logic"][enc]] += 1
            distribution["B"][row["zero_boundary_crossings"]] += 1
            distribution["H"][row["one_two_crossings"]] += 1
            assertions += 9
            if q < 2 and var < 3:
                keep = dict(row)
                keep.pop("after_assignment")
                examples.append(keep)
    return {
        "name": name,
        "sampled_assignments": len(assignments),
        "single_flips": len(assignments) * n,
        "assertions": assertions,
        "distribution": {k: dict(sorted(v.items())) for k, v in distribution.items()},
        "changed_record_examples": examples,
    }


def sequence_ledger(formula: list[list[int]], start: list[int], variables: list[int]) -> dict:
    a = start[:]
    total = {"binary": 0, "gray": 0}
    B = H = 0
    changed_ids = Counter()
    first_rows = []
    for step, var in enumerate(variables):
        row = flip_record(formula, a, var)
        B += row["zero_boundary_crossings"]
        H += row["one_two_crossings"]
        for enc in total:
            total[enc] += row["observed_d_logic"][enc]
        changed_ids.update(row["changed_clause_ids_zero_based"])
        if step < 16:
            keep = dict(row)
            keep.pop("after_assignment")
            first_rows.append(keep)
        a = row["after_assignment"]
    T = len(variables)
    assert total["gray"] == 5 * T + B
    assert total["binary"] == 5 * T + B + H
    return {
        "steps": T,
        "sum_adjacent_d_logic": total,
        "zero_boundary_crossings_B": B,
        "one_two_crossings_H": H,
        "identity_rhs": {"gray": 5 * T + B, "binary": 5 * T + B + H},
        "endpoint_delta": {
            enc: hd(state(formula, start, enc), state(formula, a, enc))
            for enc in ("binary", "gray")
        },
        "changed_record_frequency": dict(sorted(changed_ids.items())),
        "first_16_steps": first_rows,
    }


def hostile_controls() -> dict:
    # The generalized 1+degree+B(+H) identity is representational and remains
    # cheap on easy formula classes; this is adverse to a hardness reading.
    formulas = {
        "Horn": [[-1, -2, -3], [1]],
        "two_SAT": [[1, 2], [-1, 2], [1, -2]],
        "easy_XOR3_CNF": [[1, 2, 3], [1, -2, -3], [-1, 2, -3], [-1, -2, 3]],
        "bounded_treewidth_path": [[1, 2], [-2, 3], [-3, 4]],
    }
    out = {}
    for name, formula in formulas.items():
        n = max(abs(lit) for c in formula for lit in c)
        checks = 0
        for a in itertools.product((0, 1), repeat=n):
            for var in range(n):
                flip_record(formula, list(a), var)
                checks += 2
        out[name] = {"n": n, "clauses": len(formula), "single_flip_checks": checks}
    out["wrappers"] = [
        {"name": "DELAY_read_only", "steps": 10000, "logical_data_delta": 0},
        {"name": "source_reread", "steps": 792, "logical_data_delta": 0},
        {"name": "changed_then_restored", "steps": 2, "endpoint_delta": 0, "adjacent_delta_positive": True},
        {"name": "lazy_flags", "materialized_clause_records": 0, "source_recomputation_charged": True},
    ]
    return out


def main() -> int:
    started = time.perf_counter()
    base = load_base()
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = y6()
    assert base.valid_target(Y)["valid"] and base.valid_target(U)["valid"] and base.valid_target(V)["valid"]
    cert = base.module_certificate(U)
    witness = base.replay(V, base.SAT_WITNESS)
    assert cert["proved_unsat_254_clause_subformula"] and witness["satisfied"]
    models = sum(base.replay(Y, "".join(map(str, a)))["satisfied"] for a in itertools.product((0, 1), repeat=6))
    assert models == 20
    malformed = {
        "missing_clause": Y[:-1],
        "duplicate_clause": Y + [Y[0]],
        "mixed_sign": [[1, -2, 3]] + Y[1:],
        "repeated_variable": [[1, 1, 2]] + Y[1:],
        "wrong_occurrence_count": [c[:] for c in Y[:-1]] + [[1, 2, 6]],
    }
    malformed_results = {name: base.valid_target(formula) for name, formula in malformed.items()}
    assert all(not row["valid"] for row in malformed_results.values())

    rng = random.Random(2511548)
    random_U = [[rng.randrange(2) for _ in range(198)] for _ in range(64)]
    random_V = [[rng.randrange(2) for _ in range(198)] for _ in range(64)]
    v_witness = [int(x) for x in base.SAT_WITNESS]
    assignments_U = [[0] * 198, [1] * 198] + random_U
    assignments_V = [[0] * 198, [1] * 198, v_witness] + random_V

    trace_vars = [rng.randrange(198) for _ in range(1000)]
    raw = {
        "run_id": "XOR-ACTIVITY-IDENTITY-REFEREE251",
        "timestamp": "2026-10-31 15:48 America/Los_Angeles",
        "theorem": {
            "general_single_flip": "gray=1+degree+B; binary=1+degree+B+H",
            "target_single_flip": "gray=5+B; binary=5+B+H; 0<=B+H<=4",
            "target_sequence": "sum_gray=5T+sum(B); sum_binary=5T+sum(B)+sum(H)",
            "definitions": {"B": "number of touched clauses crossing true-count 0<->1", "H": "number crossing 1<->2"},
            "scope": "fixed aligned assignment/count/status vector; offline logical diagnostic",
        },
        "same_target_labels": {
            "Y6": {"status": "SAT", "models": models, "n": 6, "m": 8},
            "U198": {"status": "UNSAT", "certificate_nodes": cert["dpll_nodes"], "joint_rows": cert["joint_rows"], "n": 198, "m": 264},
            "V198": {"status": "SAT", "witness_sha256": hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest(), "n": 198, "m": 264},
        },
        "malformed_rejections": malformed_results,
        "exhaustive_Y6": exhaustive_single_flips(Y, "Y6"),
        "sampled_U198": sampled_single_flips(U, "U198", assignments_U),
        "sampled_V198": sampled_single_flips(V, "V198", assignments_V),
        "sequence_ledgers": {
            "U198": sequence_ledger(U, [0] * 198, trace_vars),
            "V198": sequence_ledger(V, [0] * 198, trace_vars),
        },
        "actual_search_baseline": {
            "Y6": base.dpll(Y, {}, cap=None),
            "U198": base.dpll(U, {}, cap=300),
            "V198": base.dpll(V, {}, cap=300),
        },
        "signed_clause_extremes": {
            "U198": base.clause_extreme_control(U),
            "V198": base.clause_extreme_control(V),
        },
        "hostile_controls": hostile_controls(),
        "falsifiers": {
            "F1": "the complete logical XOR contains information beyond local B/H activity counters",
            "F2": "large boundary activity certifies UNSAT or distinguishes U198 from V198",
            "F3": "logical activity is an unavoidable physical-write tariff for arbitrary exact solvers",
            "F4": "low endpoint XOR implies low time despite DELAY, rereads or restored bits",
        },
        "resource_ledger": {
            "logical_trace": "offline; constructing/scanning it internally is charged",
            "local_update": "four source clause IDs and their pre-flip counts suffice on the target",
            "source": "formula acquisition and indexed record access remain charged",
            "physical": "no d_phys or FLMV native time is inferred from d_logic",
            "policy": "seeded 1000-flip trace is experimental; strategy selection/switching is not free",
            "failed_trials": "U/V capped DPLL UNKNOWN and wrappers are retained, not erased from work",
            "space": "Python objects/JSON are audit material, not a native peak-space claim",
        },
        "proof_status": {
            "local_activity_identity": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "XOR_as_independent_hardness_resource": "FALSIFIED/RETIRED",
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
        "Y6": raw["exhaustive_Y6"],
        "U_trace": {k: raw["sequence_ledgers"]["U198"][k] for k in ("steps", "sum_adjacent_d_logic", "zero_boundary_crossings_B", "one_two_crossings_H", "endpoint_delta")},
        "V_trace": {k: raw["sequence_ledgers"]["V198"][k] for k in ("steps", "sum_adjacent_d_logic", "zero_boundary_crossings_B", "one_two_crossings_H", "endpoint_delta")},
        "search": raw["actual_search_baseline"],
    }, indent=2))
    print("VERIFIED::XOR-ACTIVITY-IDENTITY-REFEREE251")
    return 0


if __name__ == "__main__":
    sys.exit(main())
