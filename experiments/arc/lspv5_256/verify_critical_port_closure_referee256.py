#!/usr/bin/env python3
"""Independent verifier for REFEREE256; imports no producer code."""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
RAW = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.json"
ARCHIVE = ROOT / "results/raw/arc/2026-10-31_2048_LSPV5_CRITICAL_PORT_CLOSURE_REFEREE256_raw.json.gz.b64"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def valid(formula):
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
        if v in assignment and assignment[v] != val:
            return False
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


def unsat_boundary_certificate(U):
    boundary = list(range(193, 199))
    allowed = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        rows = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if sat(module, a):
                rows.add(mask)
        allowed.append(rows)
    globals_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in U[:2]):
            globals_ok.add(mask)
    return sorted(globals_ok.intersection(*allowed))


def token_value(token, old, z, plus):
    var = token[1]
    if var == "z":
        return z if plus else 1 - z
    if var.startswith("o"):
        return old[int(var[1:])]
    return 0


def row_relation(row):
    relation = raw = 0
    plus_blocks = row["plus_blocks"]
    minus_blocks = row["minus_blocks"]
    pad_vars = row["pad_variables"]
    for mask in range(256):
        old = [(mask >> i) & 1 for i in range(4)]
        binary = [(mask >> (4 + i)) & 1 for i in range(4)]
        raw_ok = bool(binary[0] or binary[1]) and bool(binary[2] or binary[3])
        if raw_ok:
            raw |= 1 << mask
        ok = False
        for z in (0, 1):
            pad = [(1 - z) if v == "z" else 0 for v in pad_vars]
            binaries = bool(binary[0] or binary[1] or pad[0]) and bool(binary[2] or binary[3] or pad[1])
            pos = all(any(token_value(t, old, z, True) for t in block) for block in plus_blocks)
            neg = all(any(token_value(t, old, z, False) for t in block) for block in minus_blocks)
            if binaries and pos and neg:
                ok = True
                break
        if ok:
            relation |= 1 << mask
    return raw, relation


def verify_n6(expected):
    triples = list(itertools.combinations(range(1, 7), 3))
    families = []
    for family in itertools.combinations(triples, 4):
        degree = Counter(x for e in family for x in e)
        if all(degree[v] == 2 for v in range(1, 7)):
            families.append(family)
    formulas = one = two = 0
    min_models = 64
    for pos in families:
        for neg in families:
            formula = [list(c) for c in pos] + [[-x for x in c] for c in neg]
            models = [mask for mask in range(64) if satisfies(formula, f"{mask:06b}"[::-1])]
            formulas += 1
            min_models = min(min_models, len(models))
            one += int(all({(m >> (v - 1)) & 1 for m in models} == {0, 1} for v in range(1, 7)))
            two += int(all({(m >> (u - 1)) & 1 | (((m >> (v - 1)) & 1) << 1) for m in models} == {0, 1, 2, 3} for u, v in itertools.combinations(range(1, 7), 2)))
    assert expected == {"positive_families": len(families), "ordered_formulas": formulas, "full_one_pin_projection": one, "full_two_pin_projection": two, "minimum_models": min_models}
    return formulas


def truth_count(c, assignment):
    return sum(assignment[abs(x) - 1] == int(x > 0) for x in c)


def logical_state(formula, assignment, encoding):
    out = list(assignment)
    for c in formula:
        count = truth_count(c, assignment)
        code = count if encoding == "binary" else count ^ (count >> 1)
        out.extend((code & 1, (code >> 1) & 1, int(count > 0)))
    return out


def verify_trace(formula, trace):
    n = max(abs(x) for c in formula for x in c)
    checks = 0
    for encoding, record in trace.items():
        assignment = [0] * n
        first = previous = logical_state(formula, assignment, encoding)
        total = 0
        for row in record["rows"]:
            assignment[row["pivot_zero_based"]] ^= 1
            current = logical_state(formula, assignment, encoding)
            changed = [i for i, (a, b) in enumerate(zip(previous, current)) if a != b]
            assert changed == row["changed_cell_ids"] and len(changed) == row["d_logic"]
            total += len(changed)
            previous = current
            checks += 1
        assert total == record["sum_adjacent_d_logic"] == record["offline_eager_fixed_cell_delta"]
        assert sum(a != b for a, b in zip(first, previous)) == record["endpoint_d_logic"]
        checks += 2
    return checks


def main():
    summary = json.loads(RAW.read_text())
    archive_bytes = ARCHIVE.read_bytes()
    full_bytes = gzip.decompress(base64.b64decode(archive_bytes))
    assert hashlib.sha256(archive_bytes).hexdigest() == summary["full_raw"]["archive_text_sha256"]
    assert hashlib.sha256(full_bytes).hexdigest() == summary["full_raw"]["full_json_sha256"]
    data = json.loads(full_bytes)
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    checks = 0
    assert valid(U) and valid(V)
    checks += 2
    assert satisfies(V, V_WITNESS)
    checks += 1
    assert unsat_boundary_certificate(U) == []
    checks += 1
    D = U[:1] + U[2:]
    witness = data["critical_source"]["D_witness"]
    assert satisfies(D, witness)
    assert hashlib.sha256(witness.encode()).hexdigest() == data["critical_source"]["D_witness_sha256"]
    assert all(witness[abs(x) - 1] == "0" for x in U[1])
    checks += 3
    for k, audit in data["minimum_closure_audits"].items():
        assert 3 * audit["minimum_new_clauses_c"] - 4 * audit["minimum_new_variables_q"] == 2 + 3 * int(k)
        assert len(audit["rows"]) == audit["proper_labelled_slot_layouts"]
        hist = Counter()
        for row in audit["rows"]:
            raw, relation = row_relation(row)
            assert raw.bit_count() == row["raw_models"] == 144
            assert relation.bit_count() == row["closure_models"]
            assert (raw & ~relation).bit_count() == row["raw_only"]
            assert (relation & ~raw).bit_count() == row["closure_only"]
            assert (raw == relation) == row["equal"] is False
            assert hashlib.sha256(relation.to_bytes(32, "little")).hexdigest() == row["relation_sha256"]
            hist[row["closure_models"], row["raw_only"], row["closure_only"]] += 1
            checks += 7
        expected_hist = {(r["closure_models"], r["raw_only"], r["closure_only"]): r["layouts"] for r in audit["outcome_histogram"]}
        assert hist == Counter(expected_hist)
        assert audit["equal_relations"] == 0
        checks += 4
    checks += verify_n6(data["n6_closed_catalogue"])
    Y = [[1, 2, 3], [1, 4, 5], [2, 4, 6], [3, 5, 6], [-1, -2, -4], [-1, -3, -6], [-2, -3, -5], [-4, -5, -6]]
    checks += verify_trace(U, data["xor_adjunct"]["U198"])
    checks += verify_trace(V, data["xor_adjunct"]["V198"])
    checks += verify_trace(Y, data["xor_adjunct"]["Y6"])
    assert data["xor_adjunct"]["delay_control"]["data_bit_changes"] == 0
    assert data["xor_adjunct"]["source_reread_control"]["writes"] == 0
    checks += 2
    print(json.dumps({"verified": True, "checks": checks, "run_id": data["run_id"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
