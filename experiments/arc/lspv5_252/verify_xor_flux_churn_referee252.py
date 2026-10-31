#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE252."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1648_LSPV5_XOR_FLUX_CHURN_REFEREE252_raw.json"
SOURCE = ROOT / "tmp/doecker61_source.txt"
WITNESS = (
    "001110010011110001010001110100111110011011000101000101001010100001011010"
    "101011000100000111001010110101001110001001101000110001100010100101101110"
    "010101011001001100000110111001001101001101101001010101"
)


def load_u():
    text = "\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#"))
    return ast.literal_eval(text)


def sat(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def valid(formula):
    if not formula:
        return False
    if any(len(c) != 3 or len({abs(x) for x in c}) != 3 for c in formula):
        return False
    if any(not (all(x > 0 for x in c) or all(x < 0 for x in c)) for c in formula):
        return False
    canon = [tuple(sorted(c)) for c in formula]
    if len(set(canon)) != len(canon):
        return False
    p, n = Counter(), Counter()
    for c in formula:
        for x in c:
            (p if x > 0 else n)[abs(x)] += 1
    names = set(p) | set(n)
    return names == set(range(1, max(names) + 1)) and all(p[v] == n[v] == 2 for v in names)


def simplify(clauses, seed):
    out = []
    for clause in clauses:
        row = []
        good = False
        for lit in clause:
            v = abs(lit)
            if v in seed:
                if seed[v] == (lit > 0):
                    good = True
                    break
            else:
                row.append(lit)
        if not good:
            if not row:
                return None
            out.append(tuple(row))
    return tuple(out)


def dpll(clauses, seed):
    cs = simplify(clauses, dict(seed))
    if cs is None:
        return False
    assignment = dict(seed)
    def go(rows):
        nonlocal assignment
        while True:
            units = [c[0] for c in rows if len(c) == 1]
            if not units:
                break
            lit = units[0]
            v, value = abs(lit), lit > 0
            if v in assignment and assignment[v] != value:
                return False
            assignment[v] = value
            rows = simplify(rows, {v: value})
            if rows is None:
                return False
            if not rows:
                return True
        if not rows:
            return True
        v = abs(rows[0][0])
        snapshot = dict(assignment)
        for value in (False, True):
            assignment = dict(snapshot)
            assignment[v] = value
            nxt = simplify(rows, {v: value})
            if nxt is not None and go(nxt):
                return True
        assignment = snapshot
        return False
    return go(cs)


def verify_u(u):
    boundary = range(193, 199)
    allowed = []
    for i in range(6):
        module = u[2 + 42 * i:2 + 42 * (i + 1)]
        rows = []
        for mask in range(64):
            seed = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if dpll(module, seed):
                rows.append(mask)
        allowed.append(set(rows))
    global_rows = set()
    for mask in range(64):
        bits = [False] * 199
        for v in boundary:
            bits[v] = bool((mask >> (v - 193)) & 1)
        if all(any(bits[abs(x)] == (x > 0) for x in c) for c in u[:2]):
            global_rows.add(mask)
    return sorted(global_rows.intersection(*allowed))


def main():
    r = json.loads(RAW.read_text())
    assert r["run_id"] == "XOR-FLUX-CHURN-REFEREE252"
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    assert valid(U) and valid(V)
    assert verify_u(U) == []
    assert sat(V, WITNESS)
    assert hashlib.sha256(WITNESS.encode()).hexdigest() == r["same_target_labels"]["V198"]["witness_sha256"]
    assert r["same_target_labels"]["U198"]["joint_rows"] == []
    assert r["same_target_labels"]["V198"]["status"] == "SAT"
    assert r["exhaustive_Y6_short_paths"]["paths_length_0_through_3"] == 16576
    assert r["exhaustive_Y6_short_paths"]["two_flip_restored_loops"] == 384
    checks = 0
    for name, row in r["sequence_flux_ledgers"].items():
        T = row["steps"]
        c0, c1 = row["paired_churn_C0"], row["paired_churn_C1"]
        dn0, dm = row["delta_N0"], row["delta_N0_plus_N1"]
        assert row["sum_adjacent_d_logic"]["gray"] == 5 * T + abs(dn0) + 2 * c0
        assert row["sum_adjacent_d_logic"]["binary"] == 5 * T + abs(dn0) + abs(dm) + 2 * (c0 + c1)
        assert row["sum_adjacent_d_logic"] == row["identity_rhs"]
        assert sum(row["changed_record_frequency"].values()) == 4 * T
        f = row["directional_crossings"]
        assert f.get("0to1", 0) + f.get("1to0", 0) == row["zero_boundary_total_B"]
        assert f.get("1to2", 0) + f.get("2to1", 0) == row["middle_boundary_total_H"]
        checks += 8
        if "restored_loop" in name:
            assert row["endpoint_d_logic"] == {"gray": 0, "binary": 0}
            assert row["sum_adjacent_d_logic"]["gray"] > 0
    assert len(r["malformed_rejections"]) == 5
    assert all(not x["valid"] for x in r["malformed_rejections"].values())
    assert r["actual_search_baseline"]["Y6"]["status"] == "SAT"
    assert r["actual_search_baseline"]["U198"]["status"] == "UNKNOWN"
    assert r["actual_search_baseline"]["V198"]["status"] == "UNKNOWN"
    assert r["proof_status"]["endpoint_plus_churn_identity"] == "PROVED/EXACT"
    assert r["proof_status"]["P_vs_NP"] == "OPEN"
    print(json.dumps({"status": "PASS", "ledger_checks": checks, "independent_U_certificate": "UNSAT", "independent_V_witness": "SAT"}))
    print("VERIFIED::READBACK::XOR-FLUX-CHURN-REFEREE252")
    return 0


if __name__ == "__main__":
    sys.exit(main())
