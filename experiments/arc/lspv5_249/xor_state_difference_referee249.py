#!/usr/bin/env python3
"""XOR state-difference red-team controls for REFEREE249.

The exact theorem under test is deliberately narrow: on k fixed binary
writable tapes, a native step can change at most k currently scanned cells, so
the sum of checkpoint-to-checkpoint physical tape Hamming distances lower-bounds
native time after division by k.  Logical residual vectors, variable-length
encodings, head addresses, and offline traces are kept separate.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
SOURCE = CANONICAL if CANONICAL.exists() else ROOT / "tmp/doecker61_source.txt"
BASE = ROOT / "experiments/arc/lspv5_247/target_scope_flmv_referee247.py"
OUT = ROOT / "results/raw/arc/2026-10-31_1348_LSPV5_XOR_STATE_DIFFERENCE_REFEREE249_raw.json"


def load_base():
    spec = importlib.util.spec_from_file_location("ref247", BASE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_source() -> list[list[int]]:
    text = "\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#"))
    return ast.literal_eval(text)


def y6() -> list[list[int]]:
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def hamming(a: list[int], b: list[int]) -> int:
    assert len(a) == len(b)
    return sum(x != y for x, y in zip(a, b))


def count_clause(clause: list[int], assignment: list[int]) -> int:
    return sum(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause)


def logical_state(clauses: list[list[int]], assignment: list[int]):
    """Canonical aligned logical state: a | two-bit t_j | satisfied_j."""
    bits = list(assignment)
    ids = [f"assignment:x{i + 1}" for i in range(len(assignment))]
    counts = []
    for j, clause in enumerate(clauses):
        t = count_clause(clause, assignment)
        counts.append(t)
        bits.extend((t & 1, (t >> 1) & 1, int(t > 0)))
        ids.extend((f"clause:C{j}:count_bit0", f"clause:C{j}:count_bit1", f"clause:C{j}:sat"))
    return bits, ids, counts


def changed_ids(old: list[int], new: list[int], ids: list[str]) -> list[str]:
    return [name for x, y, name in zip(old, new, ids) if x != y]


def assignment_cycle(n: int, width: int, gray: bool) -> list[list[int]]:
    out = []
    for i in range(1 << width):
        z = i ^ (i >> 1) if gray else i
        out.append([(z >> j) & 1 if j < width else 0 for j in range(n)])
    out.append(out[0][:])
    return out


def trail_audit(clauses: list[list[int]], assignments: list[list[int]], keep_rows: bool) -> dict:
    states = [logical_state(clauses, a) for a in assignments]
    rows = []
    sum_logic = sum_lazy = 0
    lazy_reads = 0
    changed_record_counter: Counter[str] = Counter()
    for q in range(len(assignments) - 1):
        old_bits, ids, _ = states[q]
        new_bits, _, new_counts = states[q + 1]
        dl = hamming(old_bits, new_bits)
        dp_lazy = hamming(assignments[q], assignments[q + 1])
        changed = changed_ids(old_bits, new_bits, ids)
        sum_logic += dl
        sum_lazy += dp_lazy
        lazy_reads += 3 * len(clauses)
        for rid in changed:
            changed_record_counter[rid.split(":")[0]] += 1
        if keep_rows:
            rows.append({
                "transition": q,
                "d_logic": dl,
                "d_phys_eager_materialized": dl,
                "d_phys_lazy_assignment_only": dp_lazy,
                "changed_record_ids": changed,
                "new_false_clause_ids": [j for j, t in enumerate(new_counts) if t == 0],
            })
    endpoint = hamming(states[0][0], states[-1][0])
    compact = json.dumps(rows if keep_rows else [
        [q, hamming(states[q][0], states[q + 1][0]), hamming(assignments[q], assignments[q + 1])]
        for q in range(len(assignments) - 1)
    ], separators=(",", ":")).encode()
    return {
        "checkpoints": len(assignments),
        "transitions": len(assignments) - 1,
        "logic_state_bits": len(states[0][0]),
        "sum_adjacent_d_logic": sum_logic,
        "endpoint_d_logic": endpoint,
        "sum_adjacent_d_phys_eager": sum_logic,
        "sum_adjacent_d_phys_lazy": sum_lazy,
        "lazy_full_formula_literal_reads": lazy_reads,
        "changed_record_class_counts": dict(changed_record_counter),
        "rows": rows,
        "transition_sha256": hashlib.sha256(compact).hexdigest(),
    }


def witness_path(bits: str, reverse: bool = False) -> list[list[int]]:
    current = [0] * len(bits)
    out = [current[:]]
    order = [i for i, bit in enumerate(bits) if bit == "1"]
    if reverse:
        order.reverse()
    for i in order:
        current = current[:]
        current[i] = 1
        out.append(current)
    return out


def physical_interval_theorem_exhaustive() -> dict:
    checks = traces = 0
    # Exhaust every sequence of <=4 native two-tape writes on four fixed cells.
    masks = [m for m in range(16) if m.bit_count() <= 2]
    for length in range(5):
        for trace in itertools.product(masks, repeat=length):
            traces += 1
            state = 0
            for mask in trace:
                state ^= mask
            d = state.bit_count()
            assert d <= 2 * length
            assert length >= math.ceil(d / 2)
            checks += 2
    # Checkpoint sums on all ways to split all traces of four steps.
    split_checks = 0
    for trace in itertools.product(masks, repeat=4):
        for cut in range(5):
            s0 = 0
            for mask in trace[:cut]:
                s0 ^= mask
            s1 = s0
            for mask in trace[cut:]:
                s1 ^= mask
            dsum = s0.bit_count() + (s0 ^ s1).bit_count()
            assert 4 >= math.ceil(dsum / 2)
            split_checks += 1
    return {"k_tapes": 2, "fixed_cells": 4, "traces": traces, "checks": checks + split_checks, "split_checks": split_checks}


def wrapper_controls() -> dict:
    rows = []
    for delay in (0, 1, 10, 1000, 10000):
        rows.append({"wrapper": "read_only_DELAY", "native_steps": delay, "start_end_d_phys": 0, "writes": 0})
    for repeats in (1, 10, 1000):
        rows.append({"wrapper": "toggle_then_restore", "native_steps": 2 * repeats, "start_end_d_phys": 0, "writes": 2 * repeats})
        rows.append({"wrapper": "unchanged_writes", "native_steps": repeats, "start_end_d_phys": 0, "writes": repeats})
    return {"rows": rows, "conclusion": "zero checkpoint XOR does not imply zero work; skipped checkpoints hide restored changes"}


def counter_encoding_controls(width: int) -> dict:
    binary = [list(map(int, f"{i:0{width}b}")) for i in range(1 << width)]
    gray = [list(map(int, f"{(i ^ (i >> 1)):0{width}b}")) for i in range(1 << width)]
    binary.append(binary[0][:])
    gray.append(gray[0][:])
    return {
        "width": width,
        "states": 1 << width,
        "binary_cycle_delta": sum(hamming(binary[i], binary[i + 1]) for i in range(len(binary) - 1)),
        "gray_cycle_delta": sum(hamming(gray[i], gray[i + 1]) for i in range(len(gray) - 1)),
        "same_abstract_counter_sequence": True,
    }


def unaligned_control() -> dict:
    records = ["00101", "110", "000111", "10"]
    aligned = "".join(records).ljust(32, "0")
    shifted = ("1" + "".join(records)).ljust(32, "0")[:32]
    semantic_edit_records = 1
    positional_xor = sum(a != b for a, b in zip(aligned, shifted))
    return {
        "aligned_bits": aligned,
        "prefix_inserted_bits": shifted,
        "semantic_records_edited": semantic_edit_records,
        "positionwise_hamming": positional_xor,
        "status": "FAILED TRANSFER: cell identities changed, so fixed-location lemma is inapplicable",
    }


def brute_models(clauses: list[list[int]]) -> int:
    n = max(abs(x) for c in clauses for x in c)
    return sum(all(any(bits[abs(l) - 1] == int(l > 0) for l in c) for c in clauses)
               for bits in itertools.product((0, 1), repeat=n))


def highs(name: str, clauses: list[list[int]]) -> dict:
    n = max(abs(x) for c in clauses for x in c)
    matrix, lo, hi = [], [], []
    for c in clauses:
        row = np.zeros(n)
        for lit in c:
            row[abs(lit) - 1] = 1
        matrix.append(row)
        lo.append(1 if c[0] > 0 else -np.inf)
        hi.append(np.inf if c[0] > 0 else 2)
    started = time.perf_counter()
    result = milp(np.zeros(n), integrality=np.ones(n), bounds=Bounds(0, 1),
                  constraints=LinearConstraint(np.asarray(matrix), lo, hi),
                  options={"time_limit": 8, "disp": False})
    return {"name": name, "status": int(result.status), "success": bool(result.success),
            "mip_nodes": None if result.mip_node_count is None else int(result.mip_node_count),
            "mip_gap": None if result.mip_gap is None else float(result.mip_gap),
            "classification": "UNSAT" if result.status == 2 else ("SAT" if result.success else "UNRESOLVED_AT_CAP"),
            "wall_seconds": time.perf_counter() - started}


def main() -> int:
    started = time.perf_counter()
    base = load_base()
    u = load_source()
    v = [c[:] for c in u]
    v[2][-1], v[44][-1] = v[44][-1], v[2][-1]
    y = y6()

    cert = base.module_certificate(u)
    assert cert["proved_unsat_254_clause_subformula"]
    witness_replay = base.replay(v, base.SAT_WITNESS)
    assert witness_replay["satisfied"]
    assert brute_models(y) == 20

    cycles = {}
    for name, clauses, width in (("Y6", y, 6), ("U198", u, 10), ("V198", v, 10)):
        n = max(abs(x) for c in clauses for x in c)
        cycles[name] = {
            "binary_cycle": trail_audit(clauses, assignment_cycle(n, width, False), name == "Y6"),
            "gray_cycle": trail_audit(clauses, assignment_cycle(n, width, True), name == "Y6"),
        }

    paths = {
        "U198_on_V_witness_forward": trail_audit(u, witness_path(base.SAT_WITNESS), False),
        "U198_on_V_witness_reverse": trail_audit(u, witness_path(base.SAT_WITNESS, True), False),
        "V198_witness_forward": trail_audit(v, witness_path(base.SAT_WITNESS), False),
        "V198_witness_reverse": trail_audit(v, witness_path(base.SAT_WITNESS, True), False),
    }
    assert paths["V198_witness_forward"]["endpoint_d_logic"] == paths["V198_witness_reverse"]["endpoint_d_logic"]
    # For this one-way 0-to-witness path on a monotone formula, reversing the
    # order changes the transition sequence but not the total aligned ledger.
    assert paths["V198_witness_forward"]["sum_adjacent_d_logic"] == paths["V198_witness_reverse"]["sum_adjacent_d_logic"]
    assert paths["V198_witness_forward"]["transition_sha256"] != paths["V198_witness_reverse"]["transition_sha256"]

    standard_solver = {"U198": highs("U198", u), "V198": highs("V198", v)}
    assert standard_solver["U198"]["status"] in (1, 2)
    assert standard_solver["V198"]["success"]

    raw = {
        "run_id": "XOR-STATE-DIFFERENCE-REFEREE249",
        "timestamp": "2026-10-31 13:48 America/Los_Angeles",
        "claim": "fixed-location physical tape XOR gives a write lower bound; logical XOR does not transfer to arbitrary SAT runtime",
        "exact_theorem_controls": physical_interval_theorem_exhaustive(),
        "same_source_labels": {
            "U198": {"status": "UNSAT", "variables": 198, "clauses": 264,
                     "module_joint_rows": cert["joint_rows"], "certificate_dpll_nodes": cert["dpll_nodes"]},
            "V198": {"status": "SAT", "variables": 198, "clauses": 264,
                     "witness_sha256": hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest(),
                     "witness_histogram": witness_replay["true_literal_histogram"]},
            "Y6": {"status": "SAT", "variables": 6, "clauses": 8, "model_count": 20},
        },
        "binary_gray_assignment_cycles": cycles,
        "same_endpoint_flip_order_paths": paths,
        "counter_encoding": {"width6": counter_encoding_controls(6), "width10": counter_encoding_controls(10)},
        "wrapper_controls": wrapper_controls(),
        "unaligned_encoding": unaligned_control(),
        "signed_clause_extremes": {
            "U198": base.clause_extreme_control(u),
            "V198": base.clause_extreme_control(v),
        },
        "standard_solver": standard_solver,
        "resource_ledger": {
            "offline_diagnostic": "all XOR traces are external instrumentation and not a free solver oracle",
            "eager_materialized": "fixed aligned assignment/count/status cells; each differing bit is explicitly rewritten",
            "lazy": "only assignment bits are stored; clause counts/status are recomputed by 3m reads per checkpoint",
            "heads_and_control": "not included in d_phys; their moves/control transitions remain charged native time",
            "source": "read-only source retained; source rereads cost time without d_phys",
            "failed_trials": "DELAY, unchanged writes, restored scratch, binary/Gray and unaligned controls are separately charged",
            "peak_space": "experiment materializes traces in Python; no Python heap measurement is promoted to FLMV space",
            "standard_solver": "HiGHS work is external baseline; no XOR trace is supplied to it",
        },
        "proof_status": {
            "physical_interval_lemma": "PROVED/EXACT",
            "target_trace_results": "COMPUTATIONAL",
            "logical_xor_universal_lower_bound": "FALSIFIED/RETIRED",
            "arbitrary_A_to_Phi_A_ARC": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    summary = {
        "theorem_controls": raw["exact_theorem_controls"],
        "Y6_binary_vs_gray": {k: cycles["Y6"][k]["sum_adjacent_d_logic"] for k in cycles["Y6"]},
        "V_witness_forward_reverse": {k: paths[k]["sum_adjacent_d_logic"] for k in ("V198_witness_forward", "V198_witness_reverse")},
        "standard_solver": standard_solver,
        "elapsed_seconds": raw["elapsed_seconds"],
        "output": str(OUT.relative_to(ROOT)),
    }
    print(json.dumps(summary, indent=2))
    print("VERIFIED::XOR-STATE-DIFFERENCE-REFEREE249")
    return 0


if __name__ == "__main__":
    sys.exit(main())
