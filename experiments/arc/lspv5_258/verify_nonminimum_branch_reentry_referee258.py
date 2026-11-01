#!/usr/bin/env python3
"""Independent verifier for REFEREE258; imports no producer code."""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
SUMMARY = ROOT / "results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json"
ARCHIVE = ROOT / "results/raw/arc/2026-10-31_2248_LSPV5_NONMINIMUM_BRANCH_REENTRY_REFEREE258_raw.json.gz.b64"
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
    return bool(formula) and variables == set(range(1, max(variables) + 1)) and len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in variables for s in (False, True))


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def independent_child(formula, pivot, value, base_D):
    """Second implementation of the q=4 repair (no producer import)."""
    top = max(abs(x) for c in formula for x in c)
    rename = {v: v if v < pivot else v - 1 for v in range(1, top + 1) if v != pivot}
    kept, removed, binaries = [], [], []
    true_lit = pivot if value else -pivot
    for source_i, clause in enumerate(formula):
        if true_lit in clause:
            removed.append(clause)
            continue
        row = [x for x in clause if abs(x) != pivot]
        mapped = [(1 if x > 0 else -1) * rename[abs(x)] for x in row]
        if len(mapped) == 2:
            binaries.append((len(kept), source_i))
        kept.append(mapped)
    assert len(removed) == len(binaries) == 2
    selected = 1 if value else -1
    opposite = -selected
    offset = top - 1
    dname = {v: offset + v for v in range(1, 199)}
    gadget = [[opposite * (1 if x > 0 else -1) * dname[abs(x)] for x in c] for c in base_D]
    ports = [opposite * dname[v] for v in (194, 196, 197)]
    for (position, _), port in zip(binaries, ports[:2]):
        kept[position].append(port)
    slots = [selected * rename[abs(x)] for c in removed for x in c if abs(x) != pivot]
    pairings = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    pairing = next(p for p in pairings if all(abs(slots[a]) != abs(slots[b]) for a, b in p))
    pairs = [[slots[a], slots[b]] for a, b in pairing]
    fresh = [offset + 199 + i for i in range(4)]
    z = [selected * x for x in fresh]
    nz = [opposite * x for x in fresh]
    closure = [
        pairs[0] + [z[0]], pairs[1] + [z[2]],
        [z[0], z[1], z[3]], [z[1], z[2], z[3]],
        [nz[0], nz[1], ports[2]], [nz[0], nz[2], nz[3]],
        [nz[1], nz[2], nz[3]],
    ]
    return kept + gadget + closure, closure, slots, [x[1] for x in binaries]


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
    g = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in B}
        if pin:
            a[pin[0]] = pin[1]
        if all(any(a.get(abs(x), None) == (x > 0) for x in c if abs(x) in a) for c in U[:2]):
            g.add(mask)
    return sorted(g.intersection(*sets))


def partitions(tokens):
    tokens = tuple(tokens)
    if not tokens:
        yield ()
        return
    for inds in itertools.combinations(range(1, len(tokens)), 2):
        idx = (0,) + inds
        b = tuple(tokens[i] for i in idx)
        if len({x[1] for x in b}) != 3:
            continue
        rem = tuple(x for i, x in enumerate(tokens) if i not in idx)
        for tail in partitions(rem):
            yield (tuple(sorted(b)),) + tail


def relation_census():
    toks = [(f"o{i}", f"o{i}") for i in range(4)] + [(f"z{i}{j}", f"z{i}") for i in range(4) for j in range(2)]
    P = sorted({tuple(sorted(tuple(sorted(x[1] for x in b)) for b in p)) for p in partitions(toks) if len({tuple(sorted(x[1] for x in b)) for b in p}) == 4})
    subs = [tuple(i for i in range(4) if mask >> i & 1) for mask in range(1, 16) if mask.bit_count() <= 3]
    N = [f for f in itertools.combinations_with_replacement(subs, 3) if not any(f.count(s) > 1 and len(s) == 3 for s in f) and sum(map(len, f)) == 8 and all(sum(z in s for s in f) == 2 for z in range(4))]

    def full(p, n):
        return all(any(all(any(((om >> int(v[1])) & 1) if v[0] == "o" else ((zm >> int(v[1])) & 1) for v in c) for c in p) and all(any(not ((zm >> z) & 1) for z in c) for c in n) for zm in range(16)) for om in range(16))

    exact = [(p, n) for n in N for p in P if full(p, n)]
    return len(P), len(N), exact, hashlib.sha256(json.dumps(exact, separators=(",", ":"), sort_keys=True).encode()).hexdigest()


def logical_state(formula, a, gray):
    out = list(a)
    for c in formula:
        t = sum(a[abs(x) - 1] == int(x > 0) for x in c)
        code = t ^ (t >> 1) if gray else t
        out.extend((code & 1, (code >> 1) & 1, int(t > 0)))
    return out


def verify_trace(formula, trace):
    n = max(abs(x) for c in formula for x in c)
    checks = 0
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
            total += len(changed)
            prev = cur
            checks += 3
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
    U = load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = [[1, 2, 3], [1, 4, 5], [2, 4, 6], [3, 5, 6], [-1, -2, -4], [-1, -3, -6], [-2, -3, -5], [-4, -5, -6]]
    checks = 2
    assert valid(U) and valid(V) and valid(Y)
    assert unsat_boundary(U) == [] and unsat_boundary(U, (3, True)) == []
    assert satisfies(V, V_WITNESS)
    checks += 5
    p, n, exact, digest = relation_census()
    q = data["q4_relation_census"]
    assert (p, n, len(exact), digest) == (q["positive_forms"], q["negative_forms"], q["exact_relations"], q["exact_forms_sha256"])
    assert (p, n, len(exact)) == (438, 6, 2304)
    checks += 5
    chosen_p = tuple(tuple(x for x in c) for c in q["chosen_positive"])
    chosen_n = tuple(tuple(x for x in c) for c in q["chosen_negative"])
    assert (chosen_p, chosen_n) in exact
    # Fixed z=(1,0,1,0) proves all 16 old-boundary projections.
    z = (1, 0, 1, 0)
    for om in range(16):
        assert all(any(((om >> int(v[1])) & 1) if v[0] == "o" else z[int(v[1])] for v in c) for c in chosen_p)
        assert all(any(not z[i] for i in c) for c in chosen_n)
        checks += 2
    assert q["raw_models"] == q["closure_models"] == 144 and q["raw_only"] == q["closure_only"] == 0
    checks += 4

    # Reconstruct both actual children with an independent implementation.
    uc = data["actual_controls"]["U_child"]
    vc = data["actual_controls"]["V_child"]
    assert uc["variables"] == vc["variables"] == 399 and uc["clauses"] == vc["clauses"] == 532
    D = U[:1] + U[2:]
    U_child, U_closure, U_slots, U_binary_sources = independent_child(U, 3, True, D)
    V_child, V_closure, V_slots, V_binary_sources = independent_child(V, 3, True, D)
    assert valid(U_child) and valid(V_child)
    assert len(U_child) == len(V_child) == 532
    assert U_closure == uc["closure"] == V_closure
    assert U_slots == uc["selected_slots"] == V_slots
    assert U_binary_sources == uc["binary_source_indices"] == V_binary_sources
    vw = data["actual_controls"]["V_child"]["witness"]
    assert hashlib.sha256(vw.encode()).hexdigest() == vc["witness_sha256"] and len(vw) == 399
    assert satisfies(V_child, vw)
    checks += 12
    dw = data["actual_controls"]["D"]["witness"]
    assert satisfies(D, dw) and all(dw[abs(x) - 1] == "0" for x in U[1])
    checks += 2
    # Verify original source controls and complete logical traces.
    for name, form in (("U198", U), ("V198", V), ("Y6", Y)):
        checks += verify_trace(form, data["same_target_controls"][name]["xor"])
        assert len(data["same_target_controls"][name]["clause_extremes"]) == len(form)
        assert len(data["same_target_controls"][name]["pair_matrix"]["rows"]) == len(form) * (len(form) - 1) // 2
        checks += 2
    assert data["xor_controls"]["delay"]["data_bit_changes"] == 0
    assert data["xor_controls"]["source_reread"]["writes"] == 0
    checks += 2
    print(json.dumps({"verified": True, "run_id": data["run_id"], "checks": checks, "q4_exact_relations": len(exact)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
