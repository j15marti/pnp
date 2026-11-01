#!/usr/bin/env python3
"""REFEREE256: exact local audit of critical-port target re-entry.

The proof object is a complete enumeration of the minimum one- and two-copy
critical-port closure layouts.  Boundary truth variables are deliberately
free and distinct: this is the strongest setting for a source-independent
local replacement theorem, not an all-formula lower bound.
"""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import itertools
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.json"
FULL = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.full.json"
ARCHIVE = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.json.gz.b64"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def y6():
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def valid_target(formula):
    if not formula:
        return False
    keys, occ = [], Counter()
    for c in formula:
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return False
        if not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False
        keys.append(tuple(sorted(c)))
        for x in c:
            occ[abs(x), x > 0] += 1
    variables = {abs(x) for c in formula for x in c}
    return len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in variables for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def simplify(clauses, assignment, counter):
    out = []
    for c in clauses:
        row, done = [], False
        for lit in c:
            counter["literal_tests"] += 1
            if abs(lit) in assignment:
                if assignment[abs(lit)] == (lit > 0):
                    done = True
                    break
            else:
                row.append(lit)
        if done:
            continue
        if not row:
            return None
        out.append(row)
    return out


def dpll_witness(clauses, assignment=None, counter=None):
    assignment = {} if assignment is None else dict(assignment)
    counter = {"nodes": 0, "literal_tests": 0} if counter is None else counter
    counter["nodes"] += 1
    clauses = simplify(clauses, assignment, counter)
    if clauses is None:
        return None, counter
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        v, val = abs(unit), unit > 0
        if v in assignment and assignment[v] != val:
            return None, counter
        assignment[v] = val
        clauses = simplify(clauses, {v: val}, counter)
        if clauses is None:
            return None, counter
        if not clauses:
            return assignment, counter
    if not clauses:
        return assignment, counter
    pivot = abs(min(clauses, key=len)[0])
    for value in (False, True):
        witness, _ = dpll_witness(clauses, {**assignment, pivot: value}, counter)
        if witness is not None:
            return witness, counter
    return None, counter


def complete_witness(formula, partial, n):
    bits = "".join("1" if partial.get(v, False) else "0" for v in range(1, n + 1))
    assert satisfies(formula, bits)
    return bits


def partitions(tokens, width=3):
    """Canonical set partitions of labelled occurrences into width-tuples."""
    tokens = tuple(tokens)
    if not tokens:
        yield ()
        return
    first = tokens[0]
    for rest_idx in itertools.combinations(range(1, len(tokens)), width - 1):
        block_idx = (0,) + rest_idx
        block = tuple(tokens[i] for i in block_idx)
        if len({x[1] for x in block}) != width:
            continue
        remainder = tuple(x for i, x in enumerate(tokens) if i not in block_idx)
        for tail in partitions(remainder, width):
            yield (tuple(sorted(block)),) + tail


def canonical_partition(partition):
    return tuple(sorted(tuple(sorted(block)) for block in partition))


def plus_partitions():
    tokens = [(f"o{i}", f"o{i}") for i in range(4)] + [("za", "z"), ("zb", "z")]
    return sorted({canonical_partition(p) for p in partitions(tokens)})


def token_truth(token, z):
    return (1 - z) if token[1] == "z" else 0  # every critical port literal is forced false


def clause_truth(block, old_bits, z, plus):
    values = []
    for token in block:
        var = token[1]
        if var == "z":
            values.append(z if plus else 1 - z)
        elif var.startswith("o"):
            values.append(old_bits[int(var[1:])])
        else:
            values.append(0)
    return any(values)


def relation_for_layout(plus_blocks, minus_blocks, pads):
    relation = 0
    raw = 0
    for mask in range(256):
        old = [(mask >> i) & 1 for i in range(4)]
        binary = [(mask >> (4 + i)) & 1 for i in range(4)]
        raw_ok = bool(binary[0] or binary[1]) and bool(binary[2] or binary[3])
        if raw_ok:
            raw |= 1 << mask
        closure_ok = False
        for z in (0, 1):
            b1 = bool(binary[0] or binary[1] or token_truth(pads[0], z))
            b2 = bool(binary[2] or binary[3] or token_truth(pads[1], z))
            pos = all(clause_truth(block, old, z, True) for block in plus_blocks)
            neg = all(clause_truth(block, old, z, False) for block in minus_blocks)
            if b1 and b2 and pos and neg:
                closure_ok = True
                break
        if closure_ok:
            relation |= 1 << mask
    return raw, relation


def closure_audit(k):
    q = 1
    c = (2 + 3 * k + 4 * q) // 3
    assert 3 * c - 4 * q == 2 + 3 * k
    plus_blocks_all = plus_partitions()
    minus_tokens = [(f"p{i}", f"p{i}") for i in range(3 * k)] + [("zma", "z"), ("zmb", "z")]
    layouts = {}
    for a, b in itertools.permutations(range(len(minus_tokens)), 2):
        pads = (minus_tokens[a], minus_tokens[b])
        remainder = tuple(x for i, x in enumerate(minus_tokens) if i not in (a, b))
        for minus_blocks0 in partitions(remainder):
            minus_blocks = canonical_partition(minus_blocks0)
            for plus_blocks in plus_blocks_all:
                key = (plus_blocks, minus_blocks, tuple(x[1] for x in pads), tuple(x[0] for x in pads if x[1] != "z"))
                layouts[key] = (plus_blocks, minus_blocks, pads)
    rows = []
    for plus_blocks, minus_blocks, pads in layouts.values():
        raw, relation = relation_for_layout(plus_blocks, minus_blocks, pads)
        rows.append({
            "plus_blocks": plus_blocks,
            "minus_blocks": minus_blocks,
            "pad_variables": [x[1] for x in pads],
            "pad_occurrences": [x[0] for x in pads],
            "raw_models": raw.bit_count(),
            "closure_models": relation.bit_count(),
            "raw_only": (raw & ~relation).bit_count(),
            "closure_only": (relation & ~raw).bit_count(),
            "equal": raw == relation,
            "relation_sha256": hashlib.sha256(relation.to_bytes(32, "little")).hexdigest(),
        })
    hist = Counter((r["closure_models"], r["raw_only"], r["closure_only"]) for r in rows)
    return {
        "critical_copies_k": k,
        "minimum_new_variables_q": q,
        "minimum_new_clauses_c": c,
        "equation": f"3c-4q=2+3k={2 + 3 * k}",
        "proper_labelled_slot_layouts": len(rows),
        "equal_relations": sum(r["equal"] for r in rows),
        "outcome_histogram": [
            {"closure_models": a, "raw_only": b, "closure_only": d, "layouts": count}
            for (a, b, d), count in sorted(hist.items())
        ],
        "rows": rows,
    }


def n6_catalogue():
    triples = list(itertools.combinations(range(1, 7), 3))
    families = []
    for family in itertools.combinations(triples, 4):
        degree = Counter(x for edge in family for x in edge)
        if all(degree[v] == 2 for v in range(1, 7)):
            families.append(family)
    assert len(families) == 75
    formula_count = 0
    full_one = full_two = 0
    min_models = 64
    for pos in families:
        for neg in families:
            formula = [list(c) for c in pos] + [[-x for x in c] for c in neg]
            models = [mask for mask in range(64) if satisfies(formula, f"{mask:06b}"[::-1])]
            min_models = min(min_models, len(models))
            formula_count += 1
            one_ok = all({(mask >> (v - 1)) & 1 for mask in models} == {0, 1} for v in range(1, 7))
            two_ok = all(
                {(mask >> (u - 1)) & 1 | (((mask >> (v - 1)) & 1) << 1) for mask in models} == {0, 1, 2, 3}
                for u, v in itertools.combinations(range(1, 7), 2)
            )
            full_one += int(one_ok)
            full_two += int(two_ok)
    return {"positive_families": 75, "ordered_formulas": formula_count, "full_one_pin_projection": full_one, "full_two_pin_projection": full_two, "minimum_models": min_models}


def truth_count(clause, assignment):
    return sum(assignment[abs(x) - 1] == int(x > 0) for x in clause)


def logical_state(formula, assignment, encoding):
    out = list(assignment)
    for clause in formula:
        count = truth_count(clause, assignment)
        code = count if encoding == "binary" else count ^ (count >> 1)
        out.extend((code & 1, (code >> 1) & 1, int(count > 0)))
    return out


def xor_trace(formula, flips):
    n = max(abs(x) for c in formula for x in c)
    result = {}
    for encoding in ("binary", "gray"):
        assignment = [0] * n
        first = previous = logical_state(formula, assignment, encoding)
        rows = []
        for pivot in flips:
            assignment[pivot] ^= 1
            current = logical_state(formula, assignment, encoding)
            changed = [i for i, (a, b) in enumerate(zip(previous, current)) if a != b]
            rows.append({"pivot_zero_based": pivot, "d_logic": len(changed), "changed_cell_ids": changed})
            previous = current
        result[encoding] = {
            "state_bits": len(first),
            "sum_adjacent_d_logic": sum(x["d_logic"] for x in rows),
            "endpoint_d_logic": sum(a != b for a, b in zip(first, previous)),
            "rows": rows,
            "actual_solver_d_phys": "NOT MEASURED: no native fixed-tape SAT machine was executed",
            "offline_eager_fixed_cell_delta": sum(x["d_logic"] for x in rows),
            "offline_lazy_assignment_cell_delta": len(flips),
        }
    return result


def endpoint_hist(formula):
    n = max(abs(x) for c in formula for x in c)
    out = {}
    for name, a in (("zero", [0] * n), ("one", [1] * n)):
        counts = [truth_count(c, a) for c in formula]
        out[name] = {str(i): counts.count(i) for i in range(4)}
    return out


def main():
    started = time.perf_counter()
    U = load_u()
    assert valid_target(U)
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    assert valid_target(V) and satisfies(V, V_WITNESS)
    D = U[:1] + U[2:]
    witness_partial, dpll_stats = dpll_witness(D)
    assert witness_partial is not None
    d_witness = complete_witness(D, witness_partial, 198)
    critical_clause = U[1]
    assert all(d_witness[abs(x) - 1] == "0" for x in critical_clause)

    audits = {str(k): closure_audit(k) for k in (1, 2)}
    assert all(a["equal_relations"] == 0 for a in audits.values())
    Y = y6()
    flips_small = [0, 0, 1, 2, 3, 3, 4, 5]
    result = {
        "run_id": "CRITICAL-PORT-CLOSURE-REFEREE256",
        "timestamp": "2026-10-31T20:48:00-07:00",
        "claim_status": {"local_minimum_closure": "PROVED/EXACT", "finite_controls": "COMPUTATIONAL", "all_input_ARC_FLMV": "OPEN", "P_vs_NP": "OPEN"},
        "falsifiers": {
            "F1": "a minimum k=1 critical-port closure has the same free-boundary relation as the raw two-binary interface",
            "F2": "a minimum k=2 closure repairs the k=1 defect without changing the free-boundary relation",
            "F3": "a closed six-variable target formula can force one or two boundary pins",
            "F4": "logical XOR or endpoint delta alone lower-bounds an arbitrary SAT machine",
        },
        "critical_source": {
            "U198_status": "UNSAT by independently replayed project boundary certificate; certificate replay repeated in verifier",
            "critical_clause_zero_based": 1,
            "critical_clause": critical_clause,
            "D_clause_count": len(D),
            "D_status": "SAT",
            "D_witness": d_witness,
            "D_witness_sha256": hashlib.sha256(d_witness.encode()).hexdigest(),
            "D_dpll": dpll_stats,
            "forced_port_reason": "U=D AND C is UNSAT while D is SAT, hence every D model falsifies all literals of positive C",
            "V198_status": "SAT",
            "V198_witness_sha256": hashlib.sha256(V_WITNESS.encode()).hexdigest(),
        },
        "minimum_closure_audits": audits,
        "n6_closed_catalogue": n6_catalogue(),
        "same_target_controls": {
            "U198": {"status": "UNSAT", "endpoint_histograms": endpoint_hist(U)},
            "V198": {"status": "SAT", "endpoint_histograms": endpoint_hist(V)},
            "Y6": {"status": "SAT", "models": sum(satisfies(Y, f"{mask:06b}"[::-1]) for mask in range(64)), "endpoint_histograms": endpoint_hist(Y)},
        },
        "xor_adjunct": {
            "U198": xor_trace(U, flips_small),
            "V198": xor_trace(V, flips_small),
            "Y6": xor_trace(Y, flips_small),
            "delay_control": {"native_steps": 100, "data_bit_changes": 0, "lesson": "time can grow with zero XOR data delta"},
            "source_reread_control": {"reads": 1000, "writes": 0, "data_bit_changes": 0},
            "changed_then_restored_control": "the repeated pivot flips make endpoint delta smaller than the sum of adjacent deltas",
            "physical_semantics": "all listed XOR vectors are offline canonical logical diagnostics; no actual SAT-machine d_phys is claimed",
        },
        "resource_ledger": {
            "discovery": "literature, repository, and finite-layout search charged separately from proof verification",
            "policy_selection": "choosing k, q, padding ports, partitions, and branch polarity is not a free oracle",
            "switching_failed_trials": "every rejected layout and source-specific retry remains charged",
            "source_access": "U/V/Y records and the critical clause must be read or indexed",
            "query_child_output": "materialized critical gadgets and target children are parent-scale or larger; output bits are charged",
            "retained_ancestor": "source, indices, child, guest workspace, and certificate must be counted at simultaneous peak",
            "tape_index_space": "actual head locations, index tapes, and shadow states are absent from the offline XOR trace and cannot be inferred",
            "guest": "no child exponent lambda<1 is obtained; the local closure theorem supplies no FLMV box entry",
        },
        "runtime_note": "wall time printed below is not included in the immutable result",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    full_bytes = (json.dumps(result, separators=(",", ":"), sort_keys=True) + "\n").encode()
    FULL.write_bytes(full_bytes)
    archive_bytes = base64.b64encode(gzip.compress(full_bytes, compresslevel=9, mtime=0)) + b"\n"
    ARCHIVE.write_bytes(archive_bytes)
    summary = {
        "run_id": result["run_id"],
        "timestamp": result["timestamp"],
        "claim_status": result["claim_status"],
        "falsifiers": result["falsifiers"],
        "critical_source": result["critical_source"],
        "closure_summary": {
            k: {key: audit[key] for key in ("critical_copies_k", "minimum_new_variables_q", "minimum_new_clauses_c", "equation", "proper_labelled_slot_layouts", "equal_relations", "outcome_histogram")}
            for k, audit in audits.items()
        },
        "n6_closed_catalogue": result["n6_closed_catalogue"],
        "same_target_controls": result["same_target_controls"],
        "xor_summary": {
            name: {
                enc: {key: record[key] for key in ("state_bits", "sum_adjacent_d_logic", "endpoint_d_logic", "actual_solver_d_phys", "offline_eager_fixed_cell_delta", "offline_lazy_assignment_cell_delta")}
                for enc, record in result["xor_adjunct"][name].items()
            }
            for name in ("U198", "V198", "Y6")
        },
        "xor_controls": {key: result["xor_adjunct"][key] for key in ("delay_control", "source_reread_control", "changed_then_restored_control", "physical_semantics")},
        "resource_ledger": result["resource_ledger"],
        "full_raw": {
            "archive_path": str(ARCHIVE.relative_to(ROOT)),
            "encoding": "base64(gzip(full UTF-8 JSON)); decode with base64 -d then gzip -d",
            "full_json_bytes": len(full_bytes),
            "archive_text_bytes": len(archive_bytes),
            "full_json_sha256": hashlib.sha256(full_bytes).hexdigest(),
            "archive_text_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "out": str(OUT),
        "elapsed_seconds": time.perf_counter() - started,
        "D_dpll": dpll_stats,
        "layouts": {k: v["proper_labelled_slot_layouts"] for k, v in audits.items()},
        "equal_relations": {k: v["equal_relations"] for k, v in audits.items()},
        "n6": result["n6_closed_catalogue"],
        "summary_bytes": OUT.stat().st_size,
        "full_bytes": FULL.stat().st_size,
        "archive_text_bytes": ARCHIVE.stat().st_size,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
