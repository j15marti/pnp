#!/usr/bin/env python3
"""REFEREE254: exact action-log escape from full snapshot XOR scans.

Given an authenticated occurrence index and a materialized aligned logical
state, a variable-flip action reconstructs the complete next state and all
changed record IDs.  The result charges the index/state/action log and is not
a SAT runtime theorem.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import itertools
import json
import math
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREV_PATH = ROOT / "experiments/arc/lspv5_251/xor_activity_identity_referee251.py"
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1848_LSPV5_XOR_DELTA_EVENT_REFEREE254_raw.json"


def load_previous():
    spec = importlib.util.spec_from_file_location("ref251", PREV_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_u():
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def occurrence_index(formula, n):
    idx = [[] for _ in range(n)]
    for j, clause in enumerate(formula):
        for lit in clause:
            idx[abs(lit) - 1].append((j, int(lit > 0)))
    return idx


def state_from_counts(assignment, counts, encoding):
    out = list(assignment)
    for count in counts:
        code = count if encoding == "binary" else count ^ (count >> 1)
        out.extend((code & 1, (code >> 1) & 1, int(count > 0)))
    return out


def event_step(formula, idx, assignment, counts, variable, encoding, prev):
    before_state = state_from_counts(assignment, counts, encoding)
    after_assignment = assignment[:]
    after_assignment[variable] ^= 1
    after_counts = counts[:]
    for clause_id, sign in idx[variable]:
        old_true = assignment[variable] == sign
        after_counts[clause_id] += -1 if old_true else 1
    after_state = state_from_counts(after_assignment, after_counts, encoding)
    direct = prev.state(formula, after_assignment, encoding)
    assert after_state == direct
    ids = []
    for pos, (left, right) in enumerate(zip(before_state, after_state)):
        if left == right:
            continue
        if pos < len(assignment):
            ids.append(f"assignment:{pos}")
        else:
            q, field = divmod(pos - len(assignment), 3)
            ids.append(f"clause:{q}:" + (f"count_bit:{field}" if field < 2 else "sat"))
    assert len(ids) == len(set(ids))
    return after_assignment, after_counts, {
        "variable_zero_based": variable,
        "event_code": format(variable, f"0{max(1, math.ceil(math.log2(len(assignment))))}b"),
        "incident_clause_ids_zero_based": [j for j, _ in idx[variable]],
        "changed_record_ids": ids,
        "d_logic": len(ids),
    }


def trace(formula, start, variables, prev):
    n = len(start)
    idx = occurrence_index(formula, n)
    assert all(len(row) == 4 for row in idx)
    event_bits = max(1, math.ceil(math.log2(n)))
    out = {}
    for encoding in ("binary", "gray"):
        assignment = start[:]
        counts = [prev.tcount(c, assignment) for c in formula]
        initial = state_from_counts(assignment, counts, encoding)
        rows = []
        for variable in variables:
            assignment, counts, row = event_step(formula, idx, assignment, counts, variable, encoding, prev)
            rows.append(row)
        final = state_from_counts(assignment, counts, encoding)
        out[encoding] = {
            "state_length_L": len(initial),
            "event_code_bits": event_bits,
            "steps": len(rows),
            "event_log_bits": event_bits * len(rows),
            "posthoc_two_snapshot_probe_budget": 2 * len(initial) * len(rows),
            "sum_adjacent_d_logic": sum(r["d_logic"] for r in rows),
            "endpoint_d_logic": sum(a != b for a, b in zip(initial, final)),
            "changed_record_ids_total": sum(len(r["changed_record_ids"]) for r in rows),
            "rows": rows,
        }
    return out


def exhaustive_y6(formula, prev):
    checks = 0
    distributions = {"binary": {}, "gray": {}}
    for bits in itertools.product((0, 1), repeat=6):
        idx = occurrence_index(formula, 6)
        for variable in range(6):
            for encoding in ("binary", "gray"):
                counts = [prev.tcount(c, list(bits)) for c in formula]
                _, _, row = event_step(formula, idx, list(bits), counts, variable, encoding, prev)
                key = str(row["d_logic"])
                distributions[encoding][key] = distributions[encoding].get(key, 0) + 1
                checks += 5
    return {"assignments": 64, "single_flips": 384, "checks": checks, "distribution": distributions}


def renaming_controls(formula, prev, seed=2541848):
    rng = random.Random(seed)
    checks = 0
    for _ in range(64):
        perm = list(range(6))
        rng.shuffle(perm)
        renamed = [[(1 if x > 0 else -1) * (perm[abs(x) - 1] + 1) for x in c] for c in formula]
        old_a = [rng.randrange(2) for _ in range(6)]
        new_a = [0] * 6
        for old, new in enumerate(perm):
            new_a[new] = old_a[old]
        idx = occurrence_index(renamed, 6)
        for v in range(6):
            counts = [prev.tcount(c, new_a) for c in renamed]
            for enc in ("binary", "gray"):
                event_step(renamed, idx, new_a, counts, v, enc, prev)
                checks += 1
    return {"seed": seed, "renamings": 64, "event_replays": checks}


def malformed_controls(y6, base):
    bad = {
        "missing_clause": y6[:-1],
        "duplicate_clause": y6 + [y6[0]],
        "mixed_sign": [[1, -2, 3]] + y6[1:],
        "repeated_variable": [[1, 1, 2]] + y6[1:],
        "wrong_occurrence_count": [c[:] for c in y6[:-1]] + [[1, 2, 6]],
    }
    rows = {name: base.valid_target(f) for name, f in bad.items()}
    assert all(not row["valid"] for row in rows.values())
    return rows


def hostile_controls(prev):
    formulas = {
        "Horn": [[-1, -2, -3], [1]],
        "two_SAT": [[1, 2], [-1, 2], [1, -2]],
        "easy_XOR3": [[1, 2, 3], [1, -2, -3], [-1, 2, -3], [-1, -2, 3]],
        "bounded_treewidth": [[1, 2], [-2, 3], [-3, 4]],
    }
    rows = {}
    for name, formula in formulas.items():
        n = max(abs(x) for c in formula for x in c)
        idx = occurrence_index(formula, n)
        checks = 0
        for a in itertools.product((0, 1), repeat=n):
            counts = [prev.tcount(c, list(a)) for c in formula]
            for v in range(n):
                for enc in ("binary", "gray"):
                    event_step(formula, idx, list(a), counts, v, enc, prev)
                    checks += 1
        rows[name] = checks
    rows["wrappers"] = {
        "DELAY": "arbitrary read-only steps add no delta events",
        "COPY": "copying state is charged physical work but does not change the logical transition",
        "RECOMP": "recomputes the event consequences without a retained incidence index at charged source-query time",
        "changed_then_restored": "two equal event codes can have zero endpoint delta and positive adjacent activity",
        "unaligned": "event replay requires a declared canonical record map",
    }
    return rows


def main():
    started = time.perf_counter()
    prev = load_previous()
    base = prev.load_base()
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = prev.y6()
    assert all(base.valid_target(f)["valid"] for f in (Y, U, V))
    cert = base.module_certificate(U)
    witness = base.replay(V, base.SAT_WITNESS)
    models = sum(base.replay(Y, "".join(map(str, a)))["satisfied"] for a in itertools.product((0, 1), repeat=6))
    assert cert["proved_unsat_254_clause_subformula"] and cert["joint_rows"] == []
    assert witness["satisfied"] and models == 20

    rng = random.Random(2541848)
    shared = [rng.randrange(198) for _ in range(256)]
    traces = {
        "Y6_binary_order": trace(Y, [0] * 6, list(range(6)), prev),
        "Y6_gray_order": trace(Y, [0] * 6, [0, 1, 3, 2, 4, 5], prev),
        "Y6_restored": trace(Y, [0] * 6, [0, 0] * 8, prev),
        "U198_shared": trace(U, [0] * 198, shared, prev),
        "V198_shared": trace(V, [0] * 198, shared, prev),
        "U198_restored": trace(U, [0] * 198, [0, 0] * 16, prev),
        "V198_restored": trace(V, [0] * 198, [0, 0] * 16, prev),
    }
    raw = {
        "run_id": "XOR-DELTA-EVENT-REFEREE254",
        "timestamp": "2026-10-31 18:48 America/Los_Angeles",
        "obstruction": "post-hoc full-snapshot scans are not unavoidable when the controller already knows its flip action and retains an authenticated incidence index plus current counts",
        "theorem": {
            "quantifiers": "every valid target formula F, every complete assignment a, every variable v, and binary or Gray aligned assignment/count/status state",
            "upper": "given current materialized state and authenticated four-occurrence index I(v), the variable ID reconstructs the complete next state and changed-record set",
            "event_bits": "ceil(log2 n) fixed-length bits per promised single-variable flip",
            "lower": "ceil(log2 n) fixed-length bits are necessary because the next assignment delta has n distinct possibilities",
            "sequence": "T actions replay exactly by induction using T*ceil(log2 n) event bits, plus retained state/index or charged reacquisition",
            "scope": "logical event replay; not native FLMV runtime or arbitrary SAT hardness",
        },
        "falsifiers": {
            "F1": "the flip variable ID and prior state/index do not determine the complete logical delta",
            "F2": "a fixed-length exact single-flip event code can use fewer than ceil(log2 n) bits for all variables",
            "F3": "the event-log escape makes tracing free",
            "F4": "compact event replay proves a hereditary Phi(A) contraction or SAT lower bound",
        },
        "same_target_labels": {
            "Y6": {"status": "SAT", "models": models, "n": 6, "m": 8},
            "U198": {"status": "UNSAT", "joint_rows": cert["joint_rows"], "certificate_nodes": cert["dpll_nodes"], "n": 198, "m": 264},
            "V198": {"status": "SAT", "witness_sha256": hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest(), "n": 198, "m": 264},
        },
        "state_index_costs": {
            "Y6": {"logical_state_bits": 30, "event_bits": 3, "fixed_incidence_index_upper_bits": 4 * 6 * (3 + 1)},
            "U198_V198": {"logical_state_bits": 990, "event_bits": 8, "fixed_incidence_index_upper_bits": 4 * 198 * (9 + 1)},
            "formula": "L=n+3m=5n; index upper bound 4n*(ceil(log2 m)+1) bits for clause ID plus sign",
        },
        "traces": traces,
        "exhaustive_Y6": exhaustive_y6(Y, prev),
        "renaming_controls": renaming_controls(Y, prev),
        "malformed_rejections": malformed_controls(Y, base),
        "actual_search_baseline": {"Y6": base.dpll(Y, {}, cap=None), "U198": base.dpll(U, {}, cap=300), "V198": base.dpll(V, {}, cap=300)},
        "signed_clause_extremes": {"U198": base.clause_extreme_control(U), "V198": base.clause_extreme_control(V)},
        "hostile_controls": hostile_controls(prev),
        "search_record": {
            "web_queries": [
                "primary paper SAT local search incremental make break counts variable flip clause updates GSAT WalkSAT",
                "primary paper incremental SAT clause state update variable occurrence lists watched literals",
                "dynamic Hamming distance cell probe event updates exact primary paper",
                "Döcker Monotone 3-SAT-(2,2) original paper",
            ],
            "primary_urls": [
                "https://www.satisfiability.org/SAT04/programme/106.pdf",
                "https://doi.org/10.3233/SAT190039",
                "https://doi.org/10.1137/1.9781611973105.48",
                "https://arxiv.org/abs/1912.08032",
            ],
            "classification": "incremental occurrence-list updates are directly analogous and model-compatible at the logical-record level; cell-probe online Hamming is a different streaming problem and does not transfer a SAT lower bound",
            "github_project_queries": ["delta event", "changed record XOR", "occurrence index flip"],
            "github_openai_queries": ["SAT occurrence list", "state diff XOR"],
            "github_findings": "project hits included REF249/253 and prior occurrence-index work; OpenAI hits were unrelated PCP occurrence code or absent; no novelty inference",
            "access_failures": "none in the final searches",
        },
        "resource_ledger": {
            "discovery_policy_switching_failed_trials": "not supplied by event replay and remain charged",
            "initialization": "grammar validation, source scan, occurrence-index construction and initial counts are charged",
            "update": "four incident logical clause records per target flip; bit addresses/head motion remain model-dependent",
            "storage": "materialized 5n-bit logical state plus an explicit O(n log n)-bit incidence index in the displayed implementation",
            "reacquisition": "omitting the index/state invokes charged source reread/recomputation",
            "output": "the compact variable event reconstructs changed record IDs; explicitly printing all IDs is optional charged output",
            "physical": "logical replay does not identify native writes; eager/lazy/DELAY and index-erasure controls remain",
            "child_guest_retained": "no child or guest is produced; all live parent/index/event state would count at peak in an ARC implementation",
        },
        "proof_status": {
            "delta_event_replay": "PROVED/EXACT",
            "fixed_length_event_code": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "mandatory_full_snapshot_scan_online": "FALSIFIED/RETIRED",
            "free_trace_or_universal_runtime_inference": "FALSIFIED/RETIRED",
            "arbitrary_A_to_Phi_A_ARC": "OPEN",
            "numerical_FLMV_transport": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    assert raw["actual_search_baseline"]["Y6"]["status"] == "SAT"
    assert raw["actual_search_baseline"]["U198"]["status"] == "UNKNOWN"
    assert raw["actual_search_baseline"]["V198"]["status"] == "UNKNOWN"
    raw["elapsed_seconds"] = time.perf_counter() - started
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"run": raw["run_id"], "elapsed_seconds": raw["elapsed_seconds"], "Y6": raw["exhaustive_Y6"], "costs": raw["state_index_costs"]}, indent=2))
    print("VERIFIED::XOR-DELTA-EVENT-REFEREE254")
    return 0


if __name__ == "__main__":
    sys.exit(main())
