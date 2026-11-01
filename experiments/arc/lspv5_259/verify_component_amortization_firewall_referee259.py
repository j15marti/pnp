#!/usr/bin/env python3
"""Independent verifier for REFEREE259; imports no producer code."""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
SUMMARY = ROOT / "results/raw/arc/2026-10-31_2348_LSPV5_COMPONENT_AMORTIZATION_FIREWALL_REFEREE259_raw.json"
ARCHIVE = ROOT / "results/raw/arc/2026-10-31_2348_LSPV5_COMPONENT_AMORTIZATION_FIREWALL_REFEREE259_raw.json.gz.b64"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def y6():
    p = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    n = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in p] + [[-x for x in c] for c in n]


def valid(formula):
    if not formula:
        return False
    keys, occ = [], Counter()
    for c in formula:
        if len(c) != 3 or len({abs(x) for x in c}) != 3 or not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False
        keys.append(tuple(sorted(c)))
        for x in c:
            occ[abs(x), x > 0] += 1
    vs = {abs(x) for c in formula for x in c}
    return vs == set(range(1, max(vs) + 1)) and len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in vs for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def simplify(clauses, assignment):
    out = []
    for c in clauses:
        row, done = [], False
        for x in c:
            if abs(x) in assignment:
                if assignment[abs(x)] == (x > 0):
                    done = True
                    break
            else:
                row.append(x)
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
        u = next((c[0] for c in clauses if len(c) == 1), None)
        if u is None:
            break
        assignment = {**assignment, abs(u): u > 0}
        clauses = simplify(clauses, {abs(u): u > 0})
        if clauses is None:
            return False
        if not clauses:
            return True
    if not clauses:
        return True
    p = abs(min(clauses, key=len)[0])
    return sat(clauses, {**assignment, p: False}) or sat(clauses, {**assignment, p: True})


def unsat_boundary(U, pin=None):
    B = list(range(193, 199))
    sets = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        ok = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in B}
            if pin:
                a[pin[0]] = pin[1]
            if sat(module, a):
                ok.add(mask)
        sets.append(ok)
    globals_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in B}
        if pin:
            a[pin[0]] = pin[1]
        if all(any(a.get(abs(x), None) == (x > 0) for x in c if abs(x) in a) for c in U[:2]):
            globals_ok.add(mask)
    return sorted(globals_ok.intersection(*sets))


def shift(formula, offset):
    return [[(1 if x > 0 else -1) * (abs(x) + offset) for x in c] for c in formula]


def pad(core, Y, p):
    out = [c[:] for c in core]
    for i in range(p):
        out.extend(shift(Y, 198 + 6 * i))
    return out


def gamma_len(x):
    return 2 * x.bit_length() - 1


def enc(n, m):
    return gamma_len(n) + gamma_len(m) + m * (1 + 3 * n.bit_length())


def components(formula):
    by_v = {}
    for j, c in enumerate(formula):
        for x in c:
            by_v.setdefault(abs(x), []).append(j)
    seen_v, seen_c, out = set(), set(), []
    for start in sorted(by_v):
        if start in seen_v:
            continue
        q, vs, cs = deque([("v", start)]), set(), set()
        while q:
            kind, i = q.popleft()
            if kind == "v":
                if i in seen_v:
                    continue
                seen_v.add(i); vs.add(i)
                q.extend(("c", j) for j in by_v[i])
            else:
                if i in seen_c:
                    continue
                seen_c.add(i); cs.add(i)
                q.extend(("v", abs(x)) for x in formula[i])
        out.append((len(vs), len(cs)))
    return out


def independent_child(formula, pivot, value, D):
    top = max(abs(x) for c in formula for x in c)
    rename = {v: v if v < pivot else v - 1 for v in range(1, top + 1) if v != pivot}
    kept, removed, binaries = [], [], []
    true_lit = pivot if value else -pivot
    for j, c in enumerate(formula):
        if true_lit in c:
            removed.append(c)
            continue
        row = [x for x in c if abs(x) != pivot]
        mapped = [(1 if x > 0 else -1) * rename[abs(x)] for x in row]
        if len(mapped) == 2:
            binaries.append((len(kept), j))
        kept.append(mapped)
    selected, opposite, offset = (1 if value else -1), (-1 if value else 1), top - 1
    dname = {v: offset + v for v in range(1, 199)}
    gadget = [[opposite * (1 if x > 0 else -1) * dname[abs(x)] for x in c] for c in D]
    ports = [opposite * dname[v] for v in (194, 196, 197)]
    for (position, _), port in zip(binaries, ports[:2]):
        kept[position].append(port)
    slots = [selected * rename[abs(x)] for c in removed for x in c if abs(x) != pivot]
    ps = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    pairing = next(p for p in ps if all(abs(slots[a]) != abs(slots[b]) for a, b in p))
    pairs = [[slots[a], slots[b]] for a, b in pairing]
    fresh = [offset + 199 + i for i in range(4)]
    z, nz = [selected * x for x in fresh], [opposite * x for x in fresh]
    closure = [
        pairs[0] + [z[0]], pairs[1] + [z[2]],
        [z[0], z[1], z[3]], [z[1], z[2], z[3]],
        [nz[0], nz[1], ports[2]], [nz[0], nz[2], nz[3]], [nz[1], nz[2], nz[3]],
    ]
    return kept + gadget + closure, closure


def logical_state(formula, a, gray):
    out = list(a)
    for c in formula:
        t = sum(a[abs(x) - 1] == int(x > 0) for x in c)
        code = t ^ (t >> 1) if gray else t
        out.extend((code & 1, (code >> 1) & 1, int(t > 0)))
    return out


def verify_trace(formula, trace):
    n, checks = max(abs(x) for c in formula for x in c), 0
    for name, rec in trace.items():
        a = [0] * n
        first = prev = logical_state(formula, a, name == "gray")
        total = 0
        for row in rec["rows"]:
            before = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
            a[row["pivot_zero_based"]] ^= 1
            after = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
            cur = logical_state(formula, a, name == "gray")
            changed = [i for i, (x, y) in enumerate(zip(prev, cur)) if x != y]
            assert changed == row["changed_cell_ids"] and len(changed) == row["d_logic"]
            assert [i for i, (x, y) in enumerate(zip(before, after)) if x != y] == row["changed_clause_ids"]
            total += len(changed); prev = cur; checks += 3
        assert total == rec["sum_adjacent_d_logic"]
        assert sum(x != y for x, y in zip(first, prev)) == rec["endpoint_d_logic"]
        checks += 2
    return checks


def main():
    summary = json.loads(SUMMARY.read_text())
    archive_bytes = ARCHIVE.read_bytes()
    full_bytes = gzip.decompress(base64.b64decode(archive_bytes))
    assert hashlib.sha256(archive_bytes).hexdigest() == summary["full_raw"]["archive_sha256"]
    assert hashlib.sha256(full_bytes).hexdigest() == summary["full_raw"]["full_sha256"]
    data = json.loads(full_bytes)
    checks = 2

    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = y6()
    assert valid(U) and valid(V) and valid(Y)
    assert unsat_boundary(U) == [] and unsat_boundary(U, (3, True)) == []
    assert satisfies(V, V_WITNESS)
    yw = next(f"{mask:06b}"[::-1] for mask in range(64) if satisfies(Y, f"{mask:06b}"[::-1]))
    checks += 7

    formulas = {}
    for p in (33, 34):
        for name, core in (("U", U), ("V", V)):
            F = pad(core, Y, p)
            formulas[p, name] = F
            assert valid(F)
            assert components(F) == [(198, 264)] + [(6, 8)] * p
            rec = data["actual_controls"][f"{name}_p{p}"]
            assert (rec["variables"], rec["clauses"], rec["encoding_bits"]) == (198 + 6 * p, 264 + 8 * p, enc(198 + 6 * p, 264 + 8 * p))
            if name == "V":
                witness = V_WITNESS + yw * p
                assert satisfies(F, witness)
                assert hashlib.sha256(witness.encode()).hexdigest() == rec["witness_sha256"]
            checks += 6

    D = U[:1] + U[2:]
    Uc, closure = independent_child(U, 3, True, D)
    Vc, closure2 = independent_child(V, 3, True, D)
    assert valid(Uc) and valid(Vc) and len(Uc) == len(Vc) == 532 and closure == closure2 == data["child"]["closure"]
    assert satisfies(Vc, data["child"]["V_witness"])
    assert satisfies(D, data["child"]["D_witness"])
    assert all(data["child"]["D_witness"][abs(x) - 1] == "0" for x in U[1])
    checks += 9

    for p, row in enumerate(data["threshold_table"]):
        assert row["padding_copies"] == p
        n, m = 198 + 6 * p, 264 + 8 * p
        assert row["source_bits"] == enc(n, m)
        assert row["strict_structural_shrink"] == (6 * p > 201)
        assert row["strict_bit_shrink"] == (enc(399, 532) < enc(n, m))
        checks += 4
    assert not data["threshold_table"][33]["strict_structural_shrink"]
    assert data["threshold_table"][34]["strict_structural_shrink"]
    checks += 2

    for name, formula in (("U_p34", formulas[34, "U"]), ("V_p34", formulas[34, "V"]), ("Y6", Y)):
        ctrl = data["controls"][name]
        assert len(ctrl["clause_extremes"]) == len(formula)
        for j, row in enumerate(ctrl["clause_extremes"]):
            assert row["clause_index"] == j and row["clause"] == formula[j]
            checks += 1
        sig = Counter()
        rows = ctrl["pair_matrix"]["rows"]
        assert len(rows) == len(formula) * (len(formula) - 1) // 2
        for row, (i, j) in zip(rows, itertools.combinations(range(len(formula)), 2)):
            same = any(x in formula[j] for x in formula[i])
            opposite = any(-x in formula[j] for x in formula[i])
            expected = (not opposite, not same, not same, not opposite)
            assert (row["i"], row["j"]) == (i, j)
            assert tuple(row[x] for x in ("SS", "SU", "US", "UU")) == expected
            sig["".join("1" if x else "0" for x in expected)] += 1
            checks += 2
        assert dict(sig) == ctrl["pair_matrix"]["signature_counts"]
        checks += verify_trace(formula, ctrl["xor"])
        checks += 1

    assert data["xor_guard"]["actual_d_phys"] == "NOT MEASURED"
    assert data["xor_guard"]["delay"]["data_bit_changes"] == 0
    assert data["xor_guard"]["reread"]["writes"] == 0
    checks += 3
    print(json.dumps({"verified": True, "run_id": data["run_id"], "checks": checks, "p33_bits": enc(396, 528), "p34_bits": enc(402, 536), "child_bits": enc(399, 532)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
