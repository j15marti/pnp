#!/usr/bin/env python3
"""Independent verifier for REFEREE257; imports no producer code."""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
RAW = ROOT / "results/raw/arc/2026-10-31_2148_LSPV5_ALL_K_CRITICAL_PORT_FIREWALL_REFEREE257_raw.json"
PREV = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.json"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def valid(formula):
    keys, occ = [], Counter()
    for c in formula:
        if len(c) != 3 or len({abs(x) for x in c}) != 3 or not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False
        keys.append(tuple(sorted(c)))
        for x in c:
            occ[abs(x), x > 0] += 1
    variables = {abs(x) for c in formula for x in c}
    return bool(formula) and len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in variables for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def simplify(clauses, assignment):
    out = []
    for c in clauses:
        row, done = [], False
        for lit in c:
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


def sat(clauses, assignment):
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return False
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        v, val = abs(unit), unit > 0
        assignment = dict(assignment)
        assignment[v] = val
        clauses = simplify(clauses, {v: val})
        if clauses is None:
            return False
        if not clauses:
            return True
    if not clauses:
        return True
    pivot = abs(min(clauses, key=len)[0])
    return sat(clauses, {**assignment, pivot: False}) or sat(clauses, {**assignment, pivot: True})


def unsat_boundary(U):
    boundary = list(range(193, 199))
    sets = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        ok = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if sat(module, a):
                ok.add(mask)
        sets.append(ok)
    global_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in U[:2]):
            global_ok.add(mask)
    return sorted(global_ok.intersection(*sets))


def logical_state(formula, assignment, gray):
    out = list(assignment)
    for clause in formula:
        count = sum(assignment[abs(x) - 1] == int(x > 0) for x in clause)
        code = count ^ (count >> 1) if gray else count
        out.extend((code & 1, (code >> 1) & 1, int(count > 0)))
    return out


def check_trace(formula, records):
    n = max(abs(x) for c in formula for x in c)
    checks = 0
    for name, record in records.items():
        assignment = [0] * n
        first = previous = logical_state(formula, assignment, name == "gray")
        total = 0
        for row in record["rows"]:
            assignment[row["pivot_zero_based"]] ^= 1
            current = logical_state(formula, assignment, name == "gray")
            changed = [i for i, (x, y) in enumerate(zip(previous, current)) if x != y]
            assert changed == row["changed_cell_ids"]
            assert len(changed) == row["d_logic"]
            total += len(changed)
            previous = current
            checks += 2
        assert total == record["sum_adjacent_d_logic"]
        assert sum(x != y for x, y in zip(first, previous)) == record["endpoint_d_logic"]
        checks += 2
    return checks


def main():
    data = json.loads(RAW.read_text())
    prev = json.loads(PREV.read_text())
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = [[1, 2, 3], [1, 4, 5], [2, 4, 6], [3, 5, 6], [-1, -2, -4], [-1, -3, -6], [-2, -3, -5], [-4, -5, -6]]
    checks = 0
    assert valid(U) and valid(V) and valid(Y)
    assert unsat_boundary(U) == []
    assert satisfies(V, V_WITNESS)
    assert satisfies(Y, data["same_target_controls"]["Y6"]["witness"])
    checks += 6
    D = U[:1] + U[2:]
    w = data["critical_source"]["D_witness"]
    assert satisfies(D, w)
    assert all(w[abs(x) - 1] == "0" for x in U[1])
    assert hashlib.sha256(w.encode()).hexdigest() == data["critical_source"]["D_witness_sha256"]
    checks += 3
    assert hashlib.sha256(PREV.read_bytes()).hexdigest() == data["prior_exact_audits"]["sha256"]
    for k in ("1", "2"):
        assert prev["closure_summary"][k]["equal_relations"] == 0
        assert data["prior_exact_audits"]["k" + k] == prev["closure_summary"][k]
        checks += 2
    rows = data["theorem"]["symbolic_table_k_1_to_256"]
    assert len(rows) == 768
    for row in rows:
        k, a = row["k"], row["negative_z_pads_a"]
        assert 3 * row["minimum_c"] - 4 * row["minimum_q"] == 2 + 3 * k
        assert row["minimum_q"] == 1 and row["minimum_c"] == k + 2
        assert row["remaining_negative_z_occurrences"] == 2 - a
        assert row["forced_port_only_clause_lower_bound"] == max(0, k - (2 - a))
        assert row["minimum_closure_unsat"] == (row["forced_port_only_clause_lower_bound"] > 0)
        if k >= 3:
            assert row["minimum_closure_unsat"]
        checks += 5
    checks += check_trace(U, data["xor_adjunct"]["U198"])
    checks += check_trace(V, data["xor_adjunct"]["V198"])
    checks += check_trace(Y, data["xor_adjunct"]["Y6"])
    assert data["xor_adjunct"]["delay"]["data_bit_changes"] == 0
    assert data["xor_adjunct"]["source_reread"]["writes"] == 0
    checks += 2
    print(json.dumps({"verified": True, "run_id": data["run_id"], "checks": checks}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
