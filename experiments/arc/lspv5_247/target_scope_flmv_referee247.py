#!/usr/bin/env python3
"""Finite referee controls for TARGET-SCOPE-FLMV-REFEREE247.

All computations are exact.  The large UNSAT certificate is a 64-row
boundary decomposition of Doecker's 198-variable instance; each row/module
entry is independently decided by unit-propagating DPLL.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANONICAL_SOURCE = ROOT / "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
# The fallback exists only in the transient referee checkout; a repository clone uses
# the canonical, already-published source artifact above.
SOURCE = CANONICAL_SOURCE if CANONICAL_SOURCE.exists() else ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1148_LSPV5_TARGET_SCOPE_FLMV_REFEREE247_raw.json"

SAT_WITNESS = (
    "001110010011110001010001110100111110011011000101000101001010100001011010"
    "101011000100000111001010110101001110001001101000110001100010100101101110"
    "010101011001001100000110111001001101001101101001010101"
)


def load_source(path: Path) -> list[list[int]]:
    text = "\n".join(line for line in path.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def valid_target(clauses: list[list[int]]) -> dict:
    if not clauses or any(len(c) != 3 for c in clauses):
        return {"valid": False, "reason": "not ternary"}
    if any(len({abs(x) for x in c}) != 3 for c in clauses):
        return {"valid": False, "reason": "repeated variable in clause"}
    if any(not (all(x > 0 for x in c) or all(x < 0 for x in c)) for c in clauses):
        return {"valid": False, "reason": "mixed-sign clause"}
    normalized = [tuple(sorted(c)) for c in clauses]
    if len(normalized) != len(set(normalized)):
        return {"valid": False, "reason": "duplicate clause"}
    occ: Counter[tuple[int, int]] = Counter()
    for c in clauses:
        for lit in c:
            occ[(abs(lit), 1 if lit > 0 else -1)] += 1
    variables = sorted({v for v, _ in occ})
    ok = all(occ[(v, 1)] == 2 and occ[(v, -1)] == 2 for v in variables)
    return {
        "valid": ok,
        "reason": "ok" if ok else "not exactly two occurrences per polarity",
        "variables": len(variables),
        "clauses": len(clauses),
        "positive_clauses": sum(c[0] > 0 for c in clauses),
        "negative_clauses": sum(c[0] < 0 for c in clauses),
    }


def eval_clause(clause: list[int], assignment: dict[int, bool]) -> int:
    return sum(assignment[abs(l)] == (l > 0) for l in clause)


def replay(clauses: list[list[int]], bits: str) -> dict:
    a = {i + 1: bit == "1" for i, bit in enumerate(bits)}
    counts = [eval_clause(c, a) for c in clauses]
    return {
        "satisfied": all(counts),
        "true_literal_histogram": {str(r): counts.count(r) for r in range(4)},
        "false_clause_indices": [i for i, x in enumerate(counts) if x == 0],
    }


def simplify(clauses: tuple[tuple[int, ...], ...], assignment: dict[int, bool]):
    out = []
    for c in clauses:
        nc = []
        satisfied = False
        for lit in c:
            v = abs(lit)
            if v in assignment:
                if assignment[v] == (lit > 0):
                    satisfied = True
                    break
            else:
                nc.append(lit)
        if satisfied:
            continue
        if not nc:
            return None
        out.append(tuple(nc))
    return tuple(out)


def dpll(clauses: list[list[int]], seed: dict[int, bool], cap: int | None = None) -> dict:
    nodes = 0
    literal_tests = 0

    def search(cs: tuple[tuple[int, ...], ...], a: dict[int, bool]):
        nonlocal nodes, literal_tests
        nodes += 1
        if cap is not None and nodes > cap:
            return "UNKNOWN"
        while True:
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            v, value = abs(unit), unit > 0
            if v in a and a[v] != value:
                return None
            a = dict(a)
            a[v] = value
            literal_tests += sum(len(c) for c in cs)
            cs = simplify(cs, {v: value})
            if cs is None:
                return None
            if not cs:
                return a
        if not cs:
            return a
        counts = Counter(abs(l) for c in cs for l in c)
        v = max(counts, key=counts.get)
        for value in (True, False):
            literal_tests += sum(len(c) for c in cs)
            nxt = simplify(cs, {v: value})
            if nxt is not None:
                aa = dict(a)
                aa[v] = value
                ans = search(nxt, aa)
                if ans == "UNKNOWN" or isinstance(ans, dict):
                    return ans
        return None

    cs0 = simplify(tuple(tuple(c) for c in clauses), seed)
    if cs0 is None:
        answer = None
    else:
        answer = search(cs0, dict(seed))
    return {
        "status": "UNKNOWN" if answer == "UNKNOWN" else ("SAT" if isinstance(answer, dict) else "UNSAT"),
        "nodes": nodes,
        "literal_tests": literal_tests,
    }


def module_certificate(u: list[list[int]]) -> dict:
    boundary = list(range(193, 199))
    modules = [u[2 + 42 * i : 2 + 42 * (i + 1)] for i in range(6)]
    allowed = []
    nodes = tests = 0
    row_hashes = []
    for mi, module in enumerate(modules):
        rows = []
        for mask in range(64):
            seed = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            result = dpll(module, seed)
            nodes += result["nodes"]
            tests += result["literal_tests"]
            if result["status"] == "SAT":
                rows.append(mask)
        allowed.append(rows)
        row_hashes.append(hashlib.sha256(bytes(rows)).hexdigest())
    global_ok = []
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(eval_clause(c, a) > 0 for c in u[:2]):
            global_ok.append(mask)
    intersection = sorted(set(global_ok).intersection(*map(set, allowed)))
    return {
        "boundary_variables": boundary,
        "module_clause_ranges_zero_based_half_open": [[2 + 42 * i, 2 + 42 * (i + 1)] for i in range(6)],
        "omitted_balancing_clause_range": [254, 264],
        "allowed_counts": [len(x) for x in allowed],
        "allowed_row_sha256": row_hashes,
        "global_rows": global_ok,
        "joint_rows": intersection,
        "proved_unsat_254_clause_subformula": not intersection,
        "dpll_nodes": nodes,
        "literal_tests": tests,
        "discovery_charge": "six 42-clause modules and boundary were supplied; only verification is charged here",
    }


def clause_extreme_control(clauses: list[list[int]]) -> dict:
    occurrence_rows = []
    for j, c in enumerate(clauses):
        for p, lit in enumerate(c):
            s = lit > 0
            occurrence_rows.append([j, p, lit, int(s), int(not s), int(not s), int(s)])
    pair_counts = Counter()
    pair_rows = []
    modes = (("S", "S"), ("S", "U"), ("U", "S"), ("U", "U"))
    for j in range(len(clauses)):
        cj = {abs(l): l > 0 for l in clauses[j]}
        for k in range(j + 1, len(clauses)):
            ck = {abs(l): l > 0 for l in clauses[k]}
            same = any(cj[v] == ck[v] for v in cj.keys() & ck.keys())
            opposite = any(cj[v] != ck[v] for v in cj.keys() & ck.keys())
            mask = []
            for x, y in modes:
                feasible = not (opposite if x == y else same)
                mask.append(int(feasible))
            pair_counts["".join(map(str, mask))] += 1
            pair_rows.append([j, k, *mask])
    endpoints = {
        "zero": replay(clauses, "0" * max(abs(l) for c in clauses for l in c)),
        "one": replay(clauses, "1" * max(abs(l) for c in clauses for l in c)),
    }
    compact = json.dumps(pair_rows, separators=(",", ":")).encode()
    return {
        "occurrence_columns": ["clause", "position", "literal", "S_value", "invert_S_equals_U", "U_value", "invert_U_equals_S"],
        "occurrence_count": len(occurrence_rows),
        "occurrence_sha256": hashlib.sha256(json.dumps(occurrence_rows, separators=(",", ":")).encode()).hexdigest(),
        "pair_columns": ["source_clause_j", "source_clause_k", "SS", "SU", "US", "UU"],
        "pair_count": len(pair_rows),
        "pair_pattern_counts": dict(sorted(pair_counts.items())),
        "pair_rows_sha256": hashlib.sha256(compact).hexdigest(),
        "endpoints": endpoints,
        "flip_trail_from_zero": [
            {"flipped_prefix": q, "histogram": replay(clauses, "1" * q + "0" * (max(abs(l) for c in clauses for l in c) - q))["true_literal_histogram"]}
            for q in (0, 1, 2, 4, 8, 16, 32, 64, 128, max(abs(l) for c in clauses for l in c))
        ],
        "note": "Full indexed rows are deterministically regenerated by this script; hashes prevent silent omission or double counting.",
    }


def main() -> int:
    started = time.perf_counter()
    u = load_source(SOURCE)
    v = [list(c) for c in u]
    assert v[2][-1] == 197 and v[44][-1] == 196
    v[2][-1], v[44][-1] = 196, 197
    fixtures = {}
    for name, clauses in (("U", u), ("V", v)):
        fixtures[name] = {
            "syntax": valid_target(clauses),
            "clause_sha256": hashlib.sha256(json.dumps(clauses, separators=(",", ":")).encode()).hexdigest(),
            "extreme_control": clause_extreme_control(clauses),
            "baseline_cap_5000": dpll(clauses, {}, cap=5000),
        }
    fixtures["U"]["independent_unsat_certificate"] = module_certificate(u)
    fixtures["V"]["witness_replay"] = replay(v, SAT_WITNESS)
    result = {
        "run_id": "TARGET-SCOPE-FLMV-REFEREE247",
        "status": "COMPUTATIONAL",
        "source": "Doecker arXiv:1912.08032v1 Appendix C transcription",
        "fixtures": fixtures,
        "transport_counterexample": {
            "claim": "qualitative NP-completeness alone preserves a fixed time exponent",
            "status": "FALSIFIED/RETIRED",
            "witness": "postcompose any valid polynomial reduction with B-th degree inert padding; a target M^K simulation then costs N^(B K)",
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "out": str(OUT),
        "elapsed_seconds": result["elapsed_seconds"],
        "U_certificate": fixtures["U"]["independent_unsat_certificate"],
        "V_witness": fixtures["V"]["witness_replay"],
        "baseline": {k: fixtures[k]["baseline_cap_5000"] for k in ("U", "V")},
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
