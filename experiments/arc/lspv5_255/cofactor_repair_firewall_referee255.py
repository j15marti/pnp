#!/usr/bin/env python3
"""REFEREE255: minimum canonical repair of one-variable cofactors.

The symbolic result is proved in the report.  This program exhaustively
checks the local completion characterization on Y6, U198, and V198, finds
same-raw-residual opposite-label completions, and records the required
signed-extreme and XOR controls.  All XOR tracing is an offline diagnostic
unless a declared eager fixed-cell state is used.
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

ROOT = Path(__file__).resolve().parents[3]
BASE_PATH = ROOT / "experiments/arc/lspv5_247/target_scope_flmv_referee247.py"
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1948_LSPV5_COFACTOR_REPAIR_FIREWALL_REFEREE255_raw.json"


def load_base():
    spec = importlib.util.spec_from_file_location("ref247", BASE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_u():
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def y6():
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def normalized(formula):
    return sorted(tuple(sorted(c)) for c in formula)


def truth_count(clause, assignment):
    return sum(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause)


def assignment_satisfies(formula, bits):
    a = [int(x) for x in bits]
    counts = [truth_count(c, a) for c in formula]
    return all(counts), counts


def cofactor(formula, pivot, value):
    rows = []
    source_ids = []
    for j, clause in enumerate(formula):
        pivot_lit = next((lit for lit in clause if abs(lit) == pivot), None)
        if pivot_lit is None:
            rows.append(list(clause)); source_ids.append(j); continue
        if (pivot_lit > 0) == bool(value):
            continue
        rows.append([lit for lit in clause if abs(lit) != pivot]); source_ids.append(j)
    return rows, source_ids


PAIRINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def minimal_completion(formula, pivot, value, pairing_index):
    """Slot-aligned minimum occurrence-preserving completion.

    Pairing 0 restores the parent exactly.  Pairings 1 and 2 are the two
    degree-preserving switches of the four co-occurrences in the clauses
    satisfied by the selected pivot value.
    """
    satisfied_ids, false_ids, co = [], [], []
    out = [list(c) for c in formula]
    for j, clause in enumerate(formula):
        pivot_lit = next((lit for lit in clause if abs(lit) == pivot), None)
        if pivot_lit is None:
            continue
        if (pivot_lit > 0) == bool(value):
            satisfied_ids.append(j)
            co.extend(lit for lit in clause if abs(lit) != pivot)
        else:
            false_ids.append(j)
    assert len(satisfied_ids) == len(false_ids) == 2 and len(co) == 4
    pairs = PAIRINGS[pairing_index]
    pivot_sign = 1 if formula[satisfied_ids[0]][0] > 0 else -1
    for clause_id, (left, right) in zip(satisfied_ids, pairs):
        old = formula[clause_id]
        pivot_position = next(i for i, lit in enumerate(old) if abs(lit) == pivot)
        new = [None, None, None]
        new[pivot_position] = pivot_sign * pivot
        free = [i for i in range(3) if i != pivot_position]
        new[free[0]], new[free[1]] = co[left], co[right]
        out[clause_id] = new
    return out, {
        "pivot": pivot,
        "value": value,
        "pairing_index": pairing_index,
        "satisfied_clause_ids": satisfied_ids,
        "binary_clause_ids": false_ids,
        "missing_cooccurrences": co,
        "changed_clause_ids": [j for j, (a, b) in enumerate(zip(formula, out)) if a != b],
    }


def diophantine_solutions(limit=20):
    rows = []
    for z in range(limit + 1):
        for c in range(limit + 1):
            if 3 * c - 4 * z == 2:
                rows.append({"new_or_reintroduced_variables_z": z, "added_clauses_c": c})
    return rows


def exhaustive_completion_audit(formula, name, base):
    n = max(abs(lit) for c in formula for lit in c)
    rows, checks = [], 0
    for pivot in range(1, n + 1):
        for value in (0, 1):
            raw, ids = cofactor(formula, pivot, value)
            assert len(raw) == len(formula) - 2
            assert sorted(map(len, raw)).count(2) == 2
            for pairing in range(3):
                repaired, meta = minimal_completion(formula, pivot, value, pairing)
                valid = base.valid_target(repaired)
                restored = normalized(repaired) == normalized(formula)
                if pairing == 0:
                    assert restored and valid["valid"]
                rows.append({
                    **meta,
                    "raw_clause_count": len(raw),
                    "raw_source_clause_ids_sha256": hashlib.sha256(json.dumps(ids).encode()).hexdigest(),
                    "valid_target": valid["valid"],
                    "restores_parent": restored,
                })
                checks += 9
    return {"name": name, "pivots": n, "completion_rows": rows, "checks": checks}


def extreme_rows(formula):
    occurrence = []
    for j, clause in enumerate(formula):
        for p, lit in enumerate(clause):
            s = int(lit > 0); u = 1 - s
            occurrence.append([j, p, lit, s, u, u, s])
    pairs = []
    for j in range(len(formula)):
        left = {abs(l): l > 0 for l in formula[j]}
        for k in range(j + 1, len(formula)):
            right = {abs(l): l > 0 for l in formula[k]}
            common = left.keys() & right.keys()
            same = any(left[v] == right[v] for v in common)
            opposite = any(left[v] != right[v] for v in common)
            pairs.append([j, k, int(not opposite), int(not same), int(not same), int(not opposite)])
    n = max(abs(l) for c in formula for l in c)
    endpoints = {}
    for label, bits in (("zero", "0" * n), ("one", "1" * n)):
        ok, counts = assignment_satisfies(formula, bits)
        endpoints[label] = {"satisfied": ok, "histogram": {str(r): counts.count(r) for r in range(4)}}
    trail = []
    for q in sorted(set([0, 1, 2, 4, 8, 16, 32, 64, 128, n])):
        if q > n: continue
        _, counts = assignment_satisfies(formula, "1" * q + "0" * (n - q))
        trail.append({"flipped_prefix": q, "histogram": {str(r): counts.count(r) for r in range(4)}})
    return {
        "occurrence_columns": ["clause", "position", "literal", "S_value", "invert_S_equals_U", "U_value", "invert_U_equals_S"],
        "occurrence_rows": occurrence,
        "pair_columns": ["source_clause_j", "source_clause_k", "SS", "SU", "US", "UU"],
        "pair_rows": pairs,
        "endpoints": endpoints,
        "flip_trail_from_zero": trail,
    }


def state(formula, assignment, encoding):
    out = list(assignment)
    for clause in formula:
        count = truth_count(clause, assignment)
        code = count if encoding == "binary" else count ^ (count >> 1)
        out.extend([code & 1, (code >> 1) & 1, int(count > 0)])
    return out


def xor_trace(formula, flips):
    n = max(abs(l) for c in formula for l in c)
    out = {}
    for encoding in ("binary", "gray"):
        assignment = [0] * n
        initial = state(formula, assignment, encoding)
        previous = initial
        rows = []
        for pivot0 in flips:
            assignment[pivot0] ^= 1
            current = state(formula, assignment, encoding)
            changed = []
            for pos, (a, b) in enumerate(zip(previous, current)):
                if a == b: continue
                if pos < n: changed.append(f"assignment:{pos}")
                else:
                    clause, field = divmod(pos - n, 3)
                    changed.append(f"clause:{clause}:" + (f"count_bit:{field}" if field < 2 else "sat"))
            rows.append({"pivot_zero_based": pivot0, "d_logic": len(changed), "changed_record_ids": changed})
            previous = current
        out[encoding] = {
            "state_length": len(initial),
            "steps": len(rows),
            "sum_adjacent_d_logic": sum(r["d_logic"] for r in rows),
            "endpoint_d_logic": sum(a != b for a, b in zip(initial, previous)),
            "eager_fixed_cell_d_phys": sum(r["d_logic"] for r in rows),
            "lazy_assignment_only_d_phys": len(flips),
            "rows": rows,
        }
    return out


def fixed_source_xor(left, right):
    n = max(abs(l) for f in (left, right) for c in f for l in c)
    width = math.ceil(math.log2(n + 1))
    rows = []
    total_binary = total_gray = 0
    for j, (ca, cb) in enumerate(zip(left, right)):
        for p, (a, b) in enumerate(zip(ca, cb)):
            if a == b: continue
            aid, bid = abs(a), abs(b)
            db = (aid ^ bid).bit_count() + int((a > 0) != (b > 0))
            ga, gb = aid ^ (aid >> 1), bid ^ (bid >> 1)
            dg = (ga ^ gb).bit_count() + int((a > 0) != (b > 0))
            total_binary += db; total_gray += dg
            rows.append({"clause": j, "position": p, "before": a, "after": b, "binary_word_delta": db, "gray_word_delta": dg})
    return {"word_id_bits": width, "changed_record_ids": rows, "binary_endpoint_delta": total_binary, "gray_endpoint_delta": total_gray,
            "semantics": "offline aligned read-only source comparison, not native execution d_phys"}


def main():
    started = time.perf_counter()
    base = load_base()
    U = load_u()
    V = [list(c) for c in U]
    assert V[2][-1] == 197 and V[44][-1] == 196
    V[2][-1], V[44][-1] = 196, 197
    Y = y6()
    cert = base.module_certificate(U)
    assert cert["joint_rows"] == []
    assert base.replay(V, base.SAT_WITNESS)["satisfied"]

    audits = {name: exhaustive_completion_audit(f, name, base) for name, f in (("Y6", Y), ("U198", U), ("V198", V))}
    selected = []
    for pivot in (2, 197):
        raw, raw_ids = cofactor(U, pivot, 1)
        for pairing in (1, 2):
            repaired, meta = minimal_completion(U, pivot, 1, pairing)
            witness_ok, counts = assignment_satisfies(repaired, base.SAT_WITNESS)
            assert witness_ok and base.valid_target(repaired)["valid"]
            selected.append({
                **meta,
                "raw_residual_clause_count": len(raw),
                "raw_residual_width_histogram": dict(Counter(map(len, raw))),
                "raw_residual_source_clause_ids": raw_ids,
                "raw_residual_status": "UNSAT by restriction of independently certified UNSAT U198",
                "repair_status": "SAT",
                "repair_witness": base.SAT_WITNESS,
                "repair_witness_histogram": {str(r): counts.count(r) for r in range(4)},
                "repair_sha256": hashlib.sha256(json.dumps(repaired, separators=(",", ":")).encode()).hexdigest(),
                "source_xor": fixed_source_xor(U, repaired),
                "repair_formula": repaired,
            })

    shared_flips = [0, 0, 1, 2, 3, 3, 4, 5] + list(range(8, 32))
    traces = {
        "Y6": xor_trace(Y, [x % 6 for x in shared_flips]),
        "U198": xor_trace(U, shared_flips),
        "V198": xor_trace(V, shared_flips),
    }
    capped = {"U198": base.dpll(U, {}, cap=300), "V198": base.dpll(V, {}, cap=300)}
    first_repair = selected[0]["repair_formula"]
    capped["SAT_repair_x2_pair1"] = base.dpll(first_repair, {}, cap=300)

    result = {
        "run_id": "COFACTOR-REPAIR-FIREWALL-REFEREE255",
        "timestamp": "2026-10-31T19:48:00-07:00",
        "claim_status": {"counting_and_minimum_form": "PROVED/EXACT", "finite_controls": "COMPUTATIONAL", "universal_ARC_FLMV": "OPEN", "P_vs_NP": "OPEN"},
        "falsifiers": {
            "F1": "one-variable raw cofactor has a smaller occurrence-preserving canonical repair",
            "F2": "minimum quota repair preserves the selected cofactor semantics",
            "F3": "quota-preserving two-switches preserve SAT label",
            "F4": "small source XOR delta or grammar validity yields arbitrary-machine hardness",
        },
        "diophantine": {"equation": "3c-4z=2", "solutions_through_20": diophantine_solutions(), "minimum": {"z": 1, "c": 2, "final_variables": "n", "final_clauses": "m"}},
        "completion_audits": audits,
        "same_raw_residual_opposite_label_completions": selected,
        "same_target_labels": {
            "U198": {"status": "UNSAT", "certificate": cert},
            "V198": {"status": "SAT", "witness": base.SAT_WITNESS, "witness_replay": base.replay(V, base.SAT_WITNESS)},
            "Y6": {"status": "SAT", "models": sum(assignment_satisfies(Y, ''.join(map(str, bits)))[0] for bits in itertools.product((0, 1), repeat=6))},
        },
        "actual_search_baseline": capped,
        "xor_adjunct": {"traces": traces, "note": "logical traces are offline; eager/lazy d_phys values apply only to the declared fixed-cell realizations"},
        "original_clause_controls": {"U198": extreme_rows(U), "SAT_repair_x2_pair1": extreme_rows(first_repair), "Y6": extreme_rows(Y)},
        "resource_ledger": {
            "source_records": "minimum repair has exactly the parent n variables and m clauses",
            "output": "Theta(N) physical bits if materialized; virtual access still presents length N",
            "index": "retain four occurrences per variable in O(n log m) bits or pay source rescans",
            "selection": "pivot, value, and one of three pairings must be acquired and authenticated",
            "failed_trials": "all invalid/label-wrong pairings remain charged",
            "guest": "a target guest sees parent-scale input; no lambda<1 exponent contraction",
            "space": "source/index/output/ancestor/guest peak remains simultaneous and charged",
        },
        "runtime_note": "wall time is printed by the producer but excluded from immutable raw data",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, separators=(",", ":"), sort_keys=True) + "\n")
    elapsed = time.perf_counter() - started
    print(json.dumps({
        "out": str(OUT), "elapsed_seconds": elapsed,
        "completion_checks": sum(v["checks"] for v in audits.values()),
        "opposite_label_repairs": len(selected),
        "raw_bytes": OUT.stat().st_size,
        "dpll": capped,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
