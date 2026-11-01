#!/usr/bin/env python3
"""REFEREE253: charge acquisition of complete checkpoint XOR diagnostics.

The theorems concern deterministic bit probes and a restricted one-pass
toggle-stream tracer.  They are tracing-cost results, not SAT lower bounds.
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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREV_PATH = ROOT / "experiments/arc/lspv5_251/xor_activity_identity_referee251.py"
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1748_LSPV5_XOR_TRACE_ACQUISITION_REFEREE253_raw.json"


def load_previous():
    spec = importlib.util.spec_from_file_location("ref251", PREV_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_u() -> list[list[int]]:
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def snapshot_probe_certificate(max_length: int = 20) -> dict:
    rows = []
    checks = 0
    for length in range(1, max_length + 1):
        zero = [0] * length
        baseline = 0
        for bit in range(2 * length):
            left, right = zero[:], zero[:]
            if bit < length:
                left[bit] = 1
            else:
                right[bit - length] = 1
            assert baseline != sum(a != b for a, b in zip(left, right))
            checks += 1
        for bit in range(length):
            right = zero[:]
            right[bit] = 1
            assert baseline != sum(a != b for a, b in zip(zero, right))
            checks += 1
        rows.append({
            "length": length,
            "two_unknown_snapshots_exact_worst_case_queries": 2 * length,
            "previous_snapshot_retained_exact_worst_case_queries": length,
            "unread_bit_adversary_witnesses": 3 * length,
        })
    return {
        "model": "deterministic adaptive bit probes to arbitrary aligned binary snapshots",
        "theorem": "exact Hamming distance requires 2L worst-case probes; if the previous snapshot is already retained, L current-snapshot probes",
        "upper_bound": "read every relevant bit",
        "lower_bound": "on the all-zero transcript, any unread bit can be flipped without changing the transcript but changes the answer 0 to 1",
        "rows": rows,
        "checks": checks,
    }


def parity_after(stream: list[int]) -> int:
    mask = 0
    for index in stream:
        mask ^= 1 << index
    return mask


def canonical_length_l_stream(mask: int, length: int) -> list[int]:
    stream = [i for i in range(length) if (mask >> i) & 1]
    assert (length - len(stream)) % 2 == 0
    stream.extend([0, 0] * ((length - len(stream)) // 2))
    assert len(stream) == length and parity_after(stream) == mask
    return stream


def toggle_cut_certificate(max_length: int = 14) -> dict:
    rows = []
    checks = 0
    for length in range(1, max_length + 1):
        masks = [m for m in range(1 << length) if m.bit_count() % 2 == length % 2]
        assert len(masks) == 1 << (length - 1)
        for mask in masks:
            canonical_length_l_stream(mask, length)
            checks += 1
        pairs = itertools.combinations(masks, 2)
        limit = None if length <= 10 else 5000
        pair_checks = 0
        for p, q in pairs:
            # Common suffix toggles support(p): p reaches zero, q reaches q xor p.
            suffix = [i for i in range(length) if (p >> i) & 1]
            assert parity_after(canonical_length_l_stream(p, length) + suffix) == 0
            assert parity_after(canonical_length_l_stream(q, length) + suffix) == (p ^ q) != 0
            pair_checks += 1
            checks += 2
            if limit is not None and pair_checks >= limit:
                break
        rows.append({
            "cut_events": length,
            "reachable_parity_masks": len(masks),
            "required_persistent_bits_no_reread": length - 1,
            "distinguishability_pair_checks": pair_checks,
        })
    return {
        "model": "deterministic one-pass stream of cell-toggle indices; no prefix reread; exact final changed-cell count after every continuation",
        "theorem": "after an L-event cut, at least L-1 persistent bits are required",
        "reason": "2^(L-1) parity masks of parity L are reachable; a common suffix separates every pair",
        "scope": "restricted streaming tracer only; source reread, recomputation, or a charged event log evades the state bound",
        "rows": rows,
        "checks": checks,
    }


def changed_record_ids(formula: list[list[int]], left: list[int], right: list[int], encoding: str, prev) -> list[str]:
    ids = []
    n = len(left)
    for i, (a, b) in enumerate(zip(left, right)):
        if a != b:
            ids.append(f"assignment:{i}")
    for j, clause in enumerate(formula):
        before, after = prev.tcount(clause, left), prev.tcount(clause, right)
        cb, ca = prev.count_code(before, encoding), prev.count_code(after, encoding)
        for k in range(2):
            if cb[k] != ca[k]:
                ids.append(f"clause:{j}:count_bit:{k}")
        if int(before > 0) != int(after > 0):
            ids.append(f"clause:{j}:sat")
    return ids


def trace_ledger(formula: list[list[int]], start: list[int], variables: list[int], prev) -> dict:
    out = {}
    for encoding in ("binary", "gray"):
        assignment = start[:]
        start_state = prev.state(formula, assignment, encoding)
        last_state = start_state
        rows = []
        dsum = 0
        for step, var in enumerate(variables):
            nxt = assignment[:]
            nxt[var] ^= 1
            next_state = prev.state(formula, nxt, encoding)
            ids = changed_record_ids(formula, assignment, nxt, encoding, prev)
            delta = prev.hd(last_state, next_state)
            assert delta == len(ids)
            dsum += delta
            rows.append({
                "step": step,
                "variable_zero_based": var,
                "d_logic": delta,
                "changed_record_ids": ids,
                "posthoc_two_snapshot_bit_probes": 2 * len(next_state),
                "posthoc_previous_retained_bit_probes": len(next_state),
                "eager_fixed_slot_d_phys": delta,
                "lazy_assignment_only_d_phys": 1,
                "lazy_incident_source_reads_with_supplied_occurrence_index": 12,
            })
            assignment, last_state = nxt, next_state
        out[encoding] = {
            "state_length_bits": len(start_state),
            "steps": len(rows),
            "sum_adjacent_d_logic": dsum,
            "endpoint_d_logic": prev.hd(start_state, last_state),
            "sum_posthoc_two_snapshot_bit_probes": sum(r["posthoc_two_snapshot_bit_probes"] for r in rows),
            "sum_posthoc_previous_retained_bit_probes": sum(r["posthoc_previous_retained_bit_probes"] for r in rows),
            "sum_eager_fixed_slot_d_phys": dsum,
            "sum_lazy_assignment_only_d_phys": len(rows),
            "rows": rows,
        }
    return out


def malformed_controls(y6: list[list[int]], base) -> dict:
    bad = {
        "missing_clause": y6[:-1],
        "duplicate_clause": y6 + [y6[0]],
        "mixed_sign": [[1, -2, 3]] + y6[1:],
        "repeated_variable": [[1, 1, 2]] + y6[1:],
        "wrong_occurrence_count": [c[:] for c in y6[:-1]] + [[1, 2, 6]],
    }
    rows = {name: base.valid_target(formula) for name, formula in bad.items()}
    assert all(not row["valid"] for row in rows.values())
    return rows


def main() -> int:
    started = time.perf_counter()
    prev = load_previous()
    base = prev.load_base()
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = prev.y6()
    assert all(base.valid_target(f)["valid"] for f in (Y, U, V))
    u_cert = base.module_certificate(U)
    v_witness = base.replay(V, base.SAT_WITNESS)
    y_models = sum(base.replay(Y, "".join(map(str, a)))["satisfied"] for a in itertools.product((0, 1), repeat=6))
    assert u_cert["proved_unsat_254_clause_subformula"] and u_cert["joint_rows"] == []
    assert v_witness["satisfied"] and y_models == 20

    rng = random.Random(2531748)
    shared = [rng.randrange(198) for _ in range(32)]
    traces = {
        "Y6_binary_variable_order": trace_ledger(Y, [0] * 6, list(range(6)), prev),
        "Y6_gray_flip_order": trace_ledger(Y, [0] * 6, [0, 1, 3, 2, 4, 5], prev),
        "U198_shared": trace_ledger(U, [0] * 198, shared, prev),
        "V198_shared": trace_ledger(V, [0] * 198, shared, prev),
        "U198_changed_then_restored": trace_ledger(U, [0] * 198, [0, 0] * 8, prev),
        "V198_changed_then_restored": trace_ledger(V, [0] * 198, [0, 0] * 8, prev),
    }

    raw = {
        "run_id": "XOR-TRACE-ACQUISITION-REFEREE253",
        "timestamp": "2026-10-31 17:48 America/Los_Angeles",
        "obstruction": "complete aligned XOR tracing is not a free internal oracle: snapshots must be acquired or change parity retained/reacquired",
        "falsifiers": {
            "F1": "two arbitrary snapshots admit exact deterministic post-hoc Hamming distance with o(L) bit probes",
            "F2": "retaining the previous snapshot removes the need to inspect an arbitrary current snapshot",
            "F3": "a no-reread online toggle tracer remains exact with o(L) persistent state at an L-event cut",
            "F4": "charging the optional tracer yields an arbitrary-SAT-machine lower bound",
        },
        "snapshot_probe_theorem": snapshot_probe_certificate(),
        "toggle_stream_theorem": toggle_cut_certificate(),
        "same_target_labels": {
            "Y6": {"status": "SAT", "models": y_models, "n": 6, "m": 8},
            "U198": {"status": "UNSAT", "certificate_nodes": u_cert["dpll_nodes"], "joint_rows": u_cert["joint_rows"], "n": 198, "m": 264},
            "V198": {"status": "SAT", "witness_sha256": hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest(), "n": 198, "m": 264},
        },
        "malformed_rejections": malformed_controls(Y, base),
        "trace_ledgers": traces,
        "actual_search_baseline": {
            "Y6": base.dpll(Y, {}, cap=None),
            "U198": base.dpll(U, {}, cap=200),
            "V198": base.dpll(V, {}, cap=200),
        },
        "signed_clause_extremes": {
            "U198": base.clause_extreme_control(U),
            "V198": base.clause_extreme_control(V),
        },
        "hostile_controls": {
            "DELAY_read_only": {"native_steps": 10000, "data_bit_delta": 0},
            "source_reread": "evades retained-state lower bound but all query/address/head-motion time is charged",
            "lazy_flags": "one assignment-cell write can induce many virtual logical changes",
            "changed_then_restored": "positive adjacent activity with zero endpoint activity",
            "unaligned_variable_length": "cellwise XOR is undefined until an alignment/decoding convention and its cost are declared",
            "same_value_writes_and_moves": "positive native work can have zero data-bit XOR",
            "offline_trace": "experimental diagnostic only; its scan and output are not charged to the measured SAT solver",
        },
        "search_record": {
            "web_queries": [
                "deterministic decision tree query complexity exact Hamming distance two strings lower bound",
                "exact Hamming streaming communication lower bound",
                "asymmetric read write memory primary paper",
                "Döcker duplicate-free proper Monotone 3-SAT-(2,2) NP-complete",
            ],
            "primary_findings": [
                "Pang--El Gamal determine deterministic communication complexity of exact Hamming distance; communication is a different model",
                "Blelloch et al. formalize asymmetric read/write costs; exact model transfer only, no SAT lower-bound transfer",
                "Döcker supplies the canonical NP-complete target language",
            ],
            "github_project_queries": [
                "exact Hamming distance bit probe query lower bound",
                "XOR tracing scan materialization",
                "transition log XOR changed cells",
            ],
            "github_openai_queries": ["exact Hamming distance bit probe", "XOR tracing state diff"],
            "github_findings": "project searches surfaced REF249--252 and older ledgers; OpenAI hits were unrelated; absence is not novelty evidence",
            "access_failures": "one GitHub search request returned HTTP 429; the searches were retried successfully later",
        },
        "resource_ledger": {
            "discovery": "choosing whether and where to trace is not supplied",
            "policy_selection_switching_failed_trials": "all are outside XOR and remain charged",
            "source_tape_queries": "snapshot probes or event-prefix reacquisition are explicit costs",
            "index_tapes_and_heads": "addresses, head positions, resets, and random-access semantics must be declared and charged",
            "child_guest_retained": "child encodings, guest work, ancestors, snapshots, and parity masks count at peak",
            "output": "writing all changed record IDs is charged to a tracer; raw JSON is offline audit output",
            "space": "one-pass no-reread exact change parity needs L-1 bits at the L-event cut; arbitrary reread can trade space for charged time",
            "physical": "eager fixed slots instantiate d_phys=d_logic; lazy assignment-only checkpoints instantiate one data-bit change per flip",
        },
        "proof_status": {
            "snapshot_bit_probe_theorem": "PROVED/EXACT",
            "toggle_stream_state_theorem": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "free_internal_XOR_oracle": "FALSIFIED/RETIRED",
            "XOR_only_universal_runtime_lower_bound": "FALSIFIED/RETIRED",
            "arbitrary_A_to_Phi_A_ARC": "OPEN",
            "numerical_FLMV_transport": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    assert raw["actual_search_baseline"]["Y6"]["status"] == "SAT"
    assert raw["actual_search_baseline"]["U198"]["status"] == "UNKNOWN"
    assert raw["actual_search_baseline"]["V198"]["status"] == "UNKNOWN"
    raw["elapsed_seconds"] = time.perf_counter() - started
    OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "run": raw["run_id"],
        "elapsed_seconds": raw["elapsed_seconds"],
        "snapshot_checks": raw["snapshot_probe_theorem"]["checks"],
        "toggle_checks": raw["toggle_stream_theorem"]["checks"],
        "labels": raw["same_target_labels"],
    }, indent=2))
    print("VERIFIED::XOR-TRACE-ACQUISITION-REFEREE253")
    return 0


if __name__ == "__main__":
    sys.exit(main())
