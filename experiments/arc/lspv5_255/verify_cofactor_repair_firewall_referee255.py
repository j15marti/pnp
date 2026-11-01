#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE255."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1948_LSPV5_COFACTOR_REPAIR_FIREWALL_REFEREE255_raw.json"
SOURCE = ROOT / "tmp/doecker61_source.txt"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def valid(formula):
    if not formula or any(len(c) != 3 or len({abs(x) for x in c}) != 3 for c in formula): return False
    if any(not (all(x > 0 for x in c) or all(x < 0 for x in c)) for c in formula): return False
    keys = [tuple(sorted(c)) for c in formula]
    if len(keys) != len(set(keys)): return False
    occ = Counter((abs(x), x > 0) for c in formula for x in c)
    return all(occ[v, s] == 2 for v in {abs(x) for c in formula for x in c} for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def cofactor(formula, pivot, value):
    out = []
    for c in formula:
        hit = next((x for x in c if abs(x) == pivot), None)
        if hit is None: out.append(c[:])
        elif (hit > 0) != bool(value): out.append([x for x in c if abs(x) != pivot])
    return out


def independently_check_unsat_certificate(U):
    # Reimplement the six-module boundary decomposition without importing any project solver.
    def simplify(clauses, assignment):
        out = []
        for c in clauses:
            row = []; done = False
            for lit in c:
                if abs(lit) in assignment:
                    if assignment[abs(lit)] == (lit > 0): done = True; break
                else: row.append(lit)
            if done: continue
            if not row: return None
            out.append(row)
        return out
    def sat(clauses, assignment):
        clauses = simplify(clauses, assignment)
        if clauses is None: return False
        while True:
            unit = next((c[0] for c in clauses if len(c) == 1), None)
            if unit is None: break
            v, val = abs(unit), unit > 0
            if v in assignment and assignment[v] != val: return False
            assignment = dict(assignment); assignment[v] = val
            clauses = simplify(clauses, {v: val})
            if clauses is None: return False
            if not clauses: return True
        if not clauses: return True
        v = abs(clauses[0][0])
        return sat(clauses, {**assignment, v: False}) or sat(clauses, {**assignment, v: True})
    boundary = list(range(193, 199))
    allowed = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        rows = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if sat(module, a): rows.add(mask)
        allowed.append(rows)
    globals_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a.get(abs(x), False) == (x > 0) for x in c) for c in U[:2]): globals_ok.add(mask)
    return sorted(globals_ok.intersection(*allowed))


def main():
    raw = json.loads(RAW.read_text())
    U = load_u(); checks = 0
    assert valid(U); checks += 1
    assert independently_check_unsat_certificate(U) == []; checks += 1
    sols = raw["diophantine"]["solutions_through_20"]
    assert sols[:5] == [
        {"added_clauses_c": 2, "new_or_reintroduced_variables_z": 1},
        {"added_clauses_c": 6, "new_or_reintroduced_variables_z": 4},
        {"added_clauses_c": 10, "new_or_reintroduced_variables_z": 7},
        {"added_clauses_c": 14, "new_or_reintroduced_variables_z": 10},
        {"added_clauses_c": 18, "new_or_reintroduced_variables_z": 13},
    ]; checks += 5
    assert len(raw["same_raw_residual_opposite_label_completions"]) == 4; checks += 1
    for row in raw["same_raw_residual_opposite_label_completions"]:
        repaired = row["repair_formula"]
        assert valid(repaired); checks += 1
        assert satisfies(repaired, row["repair_witness"]); checks += 1
        assert len(cofactor(U, row["pivot"], row["value"])) == 262; checks += 1
        assert row["raw_residual_status"].startswith("UNSAT"); checks += 1
        digest = hashlib.sha256(json.dumps(repaired, separators=(",", ":")).encode()).hexdigest()
        assert digest == row["repair_sha256"]; checks += 1
        assert row["source_xor"]["binary_endpoint_delta"] > 0; checks += 1
    for name, audit in raw["completion_audits"].items():
        expected = 6 * 2 * 3 if name == "Y6" else 198 * 2 * 3
        assert len(audit["completion_rows"]) == expected; checks += 1
        for row in audit["completion_rows"]:
            if row["pairing_index"] == 0:
                assert row["valid_target"] and row["restores_parent"]
            checks += 1
    for name in ("Y6", "U198", "V198"):
        for enc in ("binary", "gray"):
            t = raw["xor_adjunct"]["traces"][name][enc]
            assert t["sum_adjacent_d_logic"] == t["eager_fixed_cell_d_phys"]
            assert t["lazy_assignment_only_d_phys"] == t["steps"]
            assert sum(len(r["changed_record_ids"]) for r in t["rows"]) == t["sum_adjacent_d_logic"]
            checks += 3
    for name, controls in raw["original_clause_controls"].items():
        m = 8 if name == "Y6" else 264
        assert len(controls["occurrence_rows"]) == 3 * m; checks += 1
        assert len(controls["pair_rows"]) == m * (m - 1) // 2; checks += 1
        for j, k, ss, su, us, uu in controls["pair_rows"]:
            assert j < k and ss == uu and su == us
            checks += 1
    assert raw["actual_search_baseline"]["U198"]["status"] == "UNKNOWN"
    assert raw["actual_search_baseline"]["V198"]["status"] == "UNKNOWN"
    assert raw["actual_search_baseline"]["SAT_repair_x2_pair1"]["status"] == "UNKNOWN"
    checks += 3
    print(json.dumps({"verified": True, "checks": checks, "run_id": raw["run_id"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
