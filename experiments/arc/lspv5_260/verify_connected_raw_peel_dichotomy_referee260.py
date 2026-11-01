#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE260."""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tmp/doecker61_source.txt"
SUMMARY = ROOT / "results/raw/arc/2026-11-01_0048_LSPV5_CONNECTED_RAW_PEEL_DICHOTOMY_REFEREE260_raw.json"
FULL = ROOT / "results/raw/arc/2026-11-01_0048_LSPV5_CONNECTED_RAW_PEEL_DICHOTOMY_REFEREE260_raw.full.json"
ARCHIVE = ROOT / "results/raw/arc/2026-11-01_0048_LSPV5_CONNECTED_RAW_PEEL_DICHOTOMY_REFEREE260_raw.json.gz.b64"
V_WITNESS = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"


def load_u():
    return ast.literal_eval("\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#")))


def y6():
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def satisfies(formula, bits):
    return all(any((bits[abs(x) - 1] == "1") == (x > 0) for x in c) for c in formula)


def simplify(clauses, assignment):
    out = []
    for c in clauses:
        row, sat = [], False
        for x in c:
            if abs(x) not in assignment:
                row.append(x)
            elif assignment[abs(x)] == (x > 0):
                sat = True
                break
        if not sat:
            if not row:
                return None
            out.append(row)
    return out


def module_sat(clauses, assignment):
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return False
    if not clauses:
        return True
    unit = next((c[0] for c in clauses if len(c) == 1), None)
    if unit is not None:
        return module_sat(clauses, {abs(unit): unit > 0})
    v = abs(min(clauses, key=len)[0])
    return module_sat(clauses, {v: False}) or module_sat(clauses, {v: True})


def u_boundary_empty(U):
    boundary = list(range(193, 199))
    module_rows = []
    for module in [U[2 + 42 * i:2 + 42 * (i + 1)] for i in range(6)]:
        rows = set()
        for mask in range(64):
            a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
            if module_sat(module, a):
                rows.add(mask)
        module_rows.append(rows)
    globals_ok = set()
    for mask in range(64):
        a = {v: bool((mask >> (v - 193)) & 1) for v in boundary}
        if all(any(a[abs(x)] == (x > 0) for x in c) for c in U[:2]):
            globals_ok.add(mask)
    return globals_ok.intersection(*module_rows), [len(x) for x in module_rows], len(globals_ok)


def valid(formula):
    if not formula:
        return False
    occ, keys = Counter(), []
    for c in formula:
        if len(c) != 3 or len(set(map(abs, c))) != 3 or not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False
        keys.append(tuple(sorted(c)))
        for x in c:
            occ[abs(x), x > 0] += 1
    vs = set(v for v, _ in occ)
    return len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in vs for s in (False, True))


def cofactor(formula, assignment):
    out = []
    for c in formula:
        row, sat = [], False
        for x in c:
            v = abs(x)
            if v not in assignment:
                row.append(x)
            elif assignment[v] == (x > 0):
                sat = True
                break
        if not sat:
            if not row:
                return None
            out.append(row)
    return out


def comps(formula, verts):
    adj = {v: set() for v in verts}
    for c in formula:
        for u, v in itertools.combinations(map(abs, c), 2):
            adj[u].add(v); adj[v].add(u)
    out = []
    while adj:
        r = next(iter(adj)); q = deque([r]); seen = {r}
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); q.append(v)
        out.append(sorted(seen))
        for v in seen:
            del adj[v]
    return sorted(out)


def pair_mask(c1, c2):
    universe = sorted(set(map(abs, c1)) | set(map(abs, c2)))
    mask = 0
    for mode, (w1, w2) in enumerate(((1, 1), (1, 0), (0, 1), (0, 0))):
        for bits in itertools.product((0, 1), repeat=len(universe)):
            a = dict(zip(universe, bits))
            if all(int(a[abs(x)] == int(x > 0)) == w1 for x in c1) and all(int(a[abs(x)] == int(x > 0)) == w2 for x in c2):
                mask |= 1 << mode
                break
    return mask


def check_controls(formula, control):
    checks = 0
    assert len(control["clause_extremes"]) == len(formula); checks += len(formula)
    expected_pairs = len(formula) * (len(formula) - 1) // 2
    assert len(control["pair_matrix"]) == expected_pairs
    for i, j, mask in control["pair_matrix"]:
        assert pair_mask(formula[i], formula[j]) == mask
        checks += 1
    n = max(abs(x) for c in formula for x in c)
    for name, bits in (("zero", [0] * n), ("one", [1] * n)):
        hist = Counter(sum(bits[abs(x) - 1] == int(x > 0) for x in c) for c in formula)
        assert control["endpoints"][name] == {str(k): hist[k] for k in range(4)}
        checks += len(formula)
    a = [0] * n
    for row in control["flip_trail"]:
        p = row["pivot_zero_based"]
        before = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
        a[p] ^= 1
        after = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
        assert row["changed_clause_ids"] == [j for j, (x, y) in enumerate(zip(before, after)) if x != y]
        assert row["counts"] == after
        checks += len(formula)
    for name, gray in (("binary", False), ("gray", True)):
        trace = control["xor"][name]
        a = [0] * n
        def state(bits):
            ans = list(bits)
            for c in formula:
                t = sum(bits[abs(x) - 1] == int(x > 0) for x in c)
                code = t ^ (t >> 1) if gray else t
                ans.extend((code & 1, (code >> 1) & 1, int(t > 0)))
            return ans
        first = prev = state(a)
        total = 0
        for row in trace["rows"]:
            p = row["pivot_zero_based"]
            before = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
            a[p] ^= 1
            after = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
            cur = state(a)
            changed = [j for j, (x, y) in enumerate(zip(prev, cur)) if x != y]
            assert row["changed_clause_ids"] == [j for j, (x, y) in enumerate(zip(before, after)) if x != y]
            assert row["changed_cell_ids"] == changed and row["d_logic"] == len(changed)
            total += len(changed); prev = cur; checks += len(cur)
        assert trace["state_bits"] == len(first)
        assert trace["sum_adjacent_d_logic"] == total
        assert trace["endpoint_d_logic"] == sum(x != y for x, y in zip(first, prev))
        assert trace["actual_d_phys"] == "NOT MEASURED"
        checks += 4
    return checks


def main():
    summary = json.loads(SUMMARY.read_text())
    full_text = FULL.read_text()
    full = json.loads(full_text)
    archive = ARCHIVE.read_text()
    assert hashlib.sha256(full_text.encode()).hexdigest() == summary["full_raw"]["full_sha256"]
    assert hashlib.sha256(archive.encode()).hexdigest() == summary["full_raw"]["archive_sha256"]
    assert gzip.decompress(base64.b64decode(archive)).decode() == full_text
    U = load_u(); V = [c[:] for c in U]; V[2][-1], V[44][-1] = V[44][-1], V[2][-1]; Y = y6()
    assert valid(U) and valid(V) and valid(Y)
    assert satisfies(V, V_WITNESS)
    surviving, module_sizes, global_size = u_boundary_empty(U)
    assert not surviving and len(module_sizes) == 6 and global_size >= 0
    checks = 4 + 64 * 7
    for name, formula in (("U198", U), ("V198", V), ("Y6", Y)):
        n = max(abs(x) for c in formula for x in c)
        assert len(comps(formula, range(1, n + 1))) == 1
        rows = full["pivot_rows"][name]
        assert len(rows) == 2 * n
        for row in rows:
            p, bit = row["pivot"], row["bit"]
            residual = cofactor(formula, {p: bool(bit)})
            assert residual is not None and residual
            cs = comps(residual, [v for v in range(1, n + 1) if v != p])
            neigh = sorted({abs(x) for c in formula if p in set(map(abs, c)) for x in c if abs(x) != p})
            assert row["neighbors"] == neigh
            assert row["component_sizes"] == sorted(map(len, cs), reverse=True)
            assert len(cs) <= len(neigh) <= 8
            assert all(set(c) & set(neigh) for c in cs)
            assert max(map(len, cs)) >= math.ceil((n - 1) / 8)
            assert not valid(residual)
            checks += 8
        checks += check_controls(formula, full["controls"][name])
    counts = Counter()
    for state in itertools.product((-1, 0, 1), repeat=6):
        a = {i + 1: bool(s) for i, s in enumerate(state) if s >= 0}
        r = cofactor(Y, a)
        status = "CONTRADICTION" if r is None else "EMPTY_SAT_TERMINAL" if not r else "CANONICAL" if valid(r) else "NONCANONICAL"
        counts[status] += 1
        checks += 1
    ysum = full["y6_exhaustive"]
    assert ysum["canonical_nonempty"] == counts["CANONICAL"] == 1
    assert ysum["empty_sat"] == counts["EMPTY_SAT_TERMINAL"]
    assert ysum["contradictions"] == counts["CONTRADICTION"]
    assert full["malformed_rejected"] == 5
    checks += 5
    print(json.dumps({"verified": True, "run_id": full["run_id"], "checks": checks, "U_boundary_intersection": sorted(surviving), "U_module_boundary_sizes": module_sizes, "U_global_boundary_size": global_size, "pivot_summary": summary["pivot_summary"], "y6_counts": dict(counts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
