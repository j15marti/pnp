#!/usr/bin/env python3
"""REFEREE257: all-k minimum critical-port closure firewall.

This is a restricted architecture theorem.  It does not rule out nonminimum
closures, different gadgets, global re-encoding, or arbitrary SAT algorithms.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_2148_LSPV5_ALL_K_CRITICAL_PORT_FIREWALL_REFEREE257_raw.json"
PREV = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.json"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def y6():
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def valid_target(formula):
    keys, occ = [], Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            return False
        keys.append(tuple(sorted(clause)))
        for lit in clause:
            occ[abs(lit), lit > 0] += 1
    variables = {abs(x) for clause in formula for x in clause}
    return bool(formula) and len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in variables for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in clause) for clause in formula)


def simplify(clauses, assignment):
    out = []
    for clause in clauses:
        row, done = [], False
        for lit in clause:
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


def sat(clauses, assignment=None):
    assignment = {} if assignment is None else dict(assignment)
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return None
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        v, val = abs(unit), unit > 0
        if v in assignment and assignment[v] != val:
            return None
        assignment[v] = val
        clauses = simplify(clauses, {v: val})
        if clauses is None:
            return None
        if not clauses:
            return assignment
    if not clauses:
        return assignment
    pivot = abs(min(clauses, key=len)[0])
    for value in (False, True):
        witness = sat(clauses, {**assignment, pivot: value})
        if witness is not None:
            return witness
    return None


def complete_witness(formula, partial, n):
    bits = "".join("1" if partial.get(v, False) else "0" for v in range(1, n + 1))
    assert satisfies(formula, bits)
    return bits


def unsat_boundary_certificate(U):
    boundary = list(range(193, 199))
    allowed = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        rows = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if sat(module, a) is not None:
                rows.add(mask)
        allowed.append(rows)
    globals_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in U[:2]):
            globals_ok.add(mask)
    return sorted(globals_ok.intersection(*allowed))


def all_k_row(k, a):
    # a is the number of the two negative z-occurrences used as binary pads.
    q, c = 1, k + 2
    assert 3 * c - 4 * q == 2 + 3 * k
    remaining_z = 2 - a
    forced_port_only_lower_bound = max(0, k - remaining_z)
    return {
        "k": k,
        "negative_z_pads_a": a,
        "minimum_q": q,
        "minimum_c": c,
        "remaining_negative_z_occurrences": remaining_z,
        "negative_closure_clauses": k,
        "forced_port_only_clause_lower_bound": forced_port_only_lower_bound,
        "minimum_closure_unsat": forced_port_only_lower_bound > 0,
    }


def exact_pair_extremes(formula):
    counts = Counter()
    checked = 0
    for i, j in itertools.combinations(range(len(formula)), 2):
        c1, c2 = formula[i], formula[j]
        variables = sorted({abs(x) for x in c1 + c2})
        observed = set()
        for bits in itertools.product((False, True), repeat=len(variables)):
            a = dict(zip(variables, bits))
            t1 = sum(a[abs(x)] == (x > 0) for x in c1)
            t2 = sum(a[abs(x)] == (x > 0) for x in c2)
            if t1 in (0, 3) and t2 in (0, 3):
                observed.add(("S" if t1 == 3 else "U") + ("S" if t2 == 3 else "U"))
        same = any(x in c2 for x in c1)
        opposite = any(-x in c2 for x in c1)
        predicted = set()
        if not opposite:
            predicted.update(("SS", "UU"))
        if not same:
            predicted.update(("SU", "US"))
        assert observed == predicted
        counts["".join(sorted(observed)) or "none"] += 1
        checked += 1
    return {"pairs_checked": checked, "compatibility_signature_counts": dict(sorted(counts.items()))}


def truth_count(clause, assignment):
    return sum(assignment[abs(x) - 1] == int(x > 0) for x in clause)


def endpoint_hist(formula):
    n = max(abs(x) for c in formula for x in c)
    out = {}
    for name, a in (("zero", [0] * n), ("one", [1] * n)):
        counts = [truth_count(c, a) for c in formula]
        out[name] = {str(i): counts.count(i) for i in range(4)}
    return out


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
            changed = [i for i, (x, y) in enumerate(zip(previous, current)) if x != y]
            rows.append({"pivot_zero_based": pivot, "d_logic": len(changed), "changed_cell_ids": changed})
            previous = current
        result[encoding] = {
            "state_bits": len(first),
            "sum_adjacent_d_logic": sum(x["d_logic"] for x in rows),
            "endpoint_d_logic": sum(x != y for x, y in zip(first, previous)),
            "rows": rows,
            "actual_solver_d_phys": "NOT MEASURED",
            "offline_lazy_assignment_writes": len(flips),
        }
    return result


def main():
    started = time.perf_counter()
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = y6()
    assert valid_target(U) and valid_target(V) and valid_target(Y)
    assert unsat_boundary_certificate(U) == []
    assert satisfies(V, V_WITNESS)
    y_models = [f"{mask:06b}"[::-1] for mask in range(64) if satisfies(Y, f"{mask:06b}"[::-1])]
    assert y_models

    D = U[:1] + U[2:]
    d_witness = complete_witness(D, sat(D), 198)
    assert all(d_witness[abs(x) - 1] == "0" for x in U[1])

    table = [all_k_row(k, a) for k in range(1, 257) for a in range(3)]
    assert all(r["minimum_closure_unsat"] for r in table if r["k"] >= 3)
    previous = json.loads(PREV.read_text())
    assert previous["closure_summary"]["1"]["equal_relations"] == 0
    assert previous["closure_summary"]["2"]["equal_relations"] == 0

    flips = [0, 0, 1, 2, 3, 3, 4, 5]
    result = {
        "run_id": "ALL-K-CRITICAL-PORT-FIREWALL-REFEREE257",
        "timestamp": "2026-10-31T21:48:00-07:00",
        "claim_status": {"all_k_minimum_architecture": "PROVED/EXACT", "finite_controls": "COMPUTATIONAL", "nonminimum_or_global_closure": "OPEN", "ARC_FLMV": "OPEN", "P_vs_NP": "OPEN"},
        "falsifiers": {
            "F1": "some k>=3 minimum critical-port closure has no all-forced-false negative closure clause",
            "F2": "the minimum balance solution has q!=1 or c!=k+2",
            "F3": "the already enumerated k=1 or k=2 minimum closure realizes the raw boundary relation",
            "F4": "offline logical XOR alone proves a lower bound for an arbitrary SAT machine",
        },
        "theorem": {
            "scope": "slot-faithful minimum closure of the REF256 one-pivot cofactor plus k disjoint polarity-oriented copies of D=U198\\C; two binary clauses are padded by negative ports or the two negative z occurrences",
            "balance_equation": "3c-4q=2+3k; modulo 3 gives q=1 mod 3, hence minimum q=1 and c=k+2",
            "positive_slots": "four old positive deficits plus two positive z occurrences form two clauses",
            "negative_slots": "3k forced-false ports plus two negative z occurrences; two pad the binary clauses; 3k slots remain in k clauses",
            "pigeonhole": "if a negative z occurrences pad binaries, at most 2-a of k negative closure clauses contain z, so at least k-(2-a) are all forced-false",
            "conclusion": "all k>=3 minimum closures are UNSAT; REF256 independently enumerated k=1,2 and found zero exact boundary relations",
            "excluded_scope": "q>=4 nonminimum closure, other gadgets, source-aware correlations, global re-encoding, and arbitrary algorithms",
            "symbolic_table_k_1_to_256": table,
        },
        "critical_source": {
            "critical_clause": U[1],
            "D_status": "SAT",
            "D_witness": d_witness,
            "D_witness_sha256": hashlib.sha256(d_witness.encode()).hexdigest(),
            "forced_false_proof": "U=D AND C is UNSAT; therefore every D model falsifies every literal of C",
            "U198_status": "UNSAT by replayed boundary certificate",
            "V198_status": "SAT",
            "V198_witness_sha256": hashlib.sha256(V_WITNESS.encode()).hexdigest(),
        },
        "prior_exact_audits": {
            "source": str(PREV.relative_to(ROOT)),
            "sha256": hashlib.sha256(PREV.read_bytes()).hexdigest(),
            "k1": previous["closure_summary"]["1"],
            "k2": previous["closure_summary"]["2"],
        },
        "same_target_controls": {
            "U198": {"status": "UNSAT", "endpoint_histograms": endpoint_hist(U), "extreme_pairs": exact_pair_extremes(U)},
            "V198": {"status": "SAT", "endpoint_histograms": endpoint_hist(V), "extreme_pairs": exact_pair_extremes(V)},
            "Y6": {"status": "SAT", "models": len(y_models), "witness": y_models[0], "endpoint_histograms": endpoint_hist(Y), "extreme_pairs": exact_pair_extremes(Y)},
        },
        "xor_adjunct": {
            "U198": xor_trace(U, flips), "V198": xor_trace(V, flips), "Y6": xor_trace(Y, flips),
            "delay": {"native_steps": 100, "data_bit_changes": 0},
            "source_reread": {"reads": 1000, "writes": 0, "data_bit_changes": 0},
            "restoration": "repeated flips make endpoint delta smaller than adjacent-delta sum",
            "unaligned_variable_length": "not comparable without a declared canonical physical layout",
            "physical_semantics": "offline logical diagnostic only; d_phys and native tape time not measured",
        },
        "resource_ledger": {
            "discovery": "literature and repository searches charged separately",
            "policy_selection_switching": "k, q, polarity, pad choice a, partitions, and failed layouts are charged",
            "source_tape_query": "source clauses, deleted-clause certificate, and child indices require declared access",
            "child_output": "materializing k copies is linear in k times source size; output is not free",
            "retained_space": "source, copies, indices, witness/certificate, and workspace count at simultaneous peak",
            "proof_checking": "balance, properness, forced-port certificate, k=1,2 archive, and SAT/UNSAT controls all charged",
            "guest_FLMV": "no power-short child or admissible FLMV exponent pair follows",
        },
        "search_record": {
            "web_queries": [
                "bounded occurrence SAT enforcer gadget forced literals ports exact occurrence primary paper",
                "Monotone 3-SAT-(2,2) enforcer gadget duplicate-free proper primary paper Döcker",
                "minimal unsatisfiable critical clause deletion forced literals primary paper",
                "bounded degree CSP gadgets perfect implementation pp-definitions primary paper",
            ],
            "primary_findings": [
                "Döcker 2019/2021 proves the canonical target NP-complete and explicitly constructs false-literal enforcers; it does not state this all-k minimum-closure theorem",
                "Berman-Karpinski-Scott 2003 studies bounded-occurrence SAT enforcers; no model-matched all-k closure transfer found",
                "minimal-unsatisfiable literature supports clause-deletion forcing, but not the target quota conclusion",
                "pp-definability describes gadget relations abstractly; exact occurrence and FLMV accounting still require a new bridge",
            ],
            "github_queries": [
                "repo:j15marti/pnp critical port closure",
                "repo:j15marti/pnp 3c-4q",
                "repo:j15marti/pnp minimum closure",
                "repo:j15marti/pnp forced-false ports",
                "org:openai SAT gadget forced false ports",
            ],
            "github_findings": "exact critical-port terminology occurs in REF256; 3c-4q occurs in REF256 and LSPV-1 slack292; no 'minimum closure' hit; broader forced-false hits are prior project port work; OpenAI results were unrelated",
            "access_failures": "none for the primary and GitHub searches used; generic web GitHub indexing was noisy, so GitHub code-search API was used separately",
            "novelty_claim": "none outside the project corpus",
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(OUT), "bytes": OUT.stat().st_size, "runtime_seconds": result["runtime_seconds"], "symbolic_rows": len(table)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
