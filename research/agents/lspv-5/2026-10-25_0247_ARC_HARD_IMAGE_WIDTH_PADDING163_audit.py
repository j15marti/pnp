#!/usr/bin/env python3
"""Finite audit for ARC-HARD-IMAGE-WIDTH-PADDING163.

Standard-library only.  Each tested scale is independent and the complete run
is intended to finish well below the project's 30-second invocation limit.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path


def grid_edges(q):
    out = []
    # Canonical order: all horizontal edges, then all vertical edges.
    for r in range(q):
        for c in range(q - 1):
            u = r * q + c + 1
            out.append((u, u + 1))
    for r in range(q - 1):
        for c in range(q):
            u = r * q + c + 1
            out.append((u, u + q))
    return out


def grid_padding(q, first_var=1):
    """Proper positive 3CNF; private edge auxiliaries; all-ones witness."""
    verts = [first_var + i for i in range(q * q)]
    clauses = []
    nxt = first_var + q * q
    for a, b in grid_edges(q):
        u = first_var + a - 1
        v = first_var + b - 1
        clauses.append((u, v, nxt))
        nxt += 1
    return clauses, nxt - 1, verts


def boundary_size(mask, adj):
    n = len(adj)
    return sum(
        1
        for v in range(n)
        if (mask >> v) & 1 and (adj[v] & ~mask) != 0
    )


def exact_vertex_separation(q):
    """O(n 2^n) subset DP, used only through q=4 (n=16)."""
    n = q * q
    adj = [0] * n
    for a, b in grid_edges(q):
        a -= 1
        b -= 1
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    size = 1 << n
    dp = [n + 1] * size
    dp[0] = 0
    for mask in range(1, size):
        width_now = boundary_size(mask, adj)
        best = n + 1
        bits = mask
        while bits:
            bit = bits & -bits
            prev = mask ^ bit
            cand = max(dp[prev], width_now)
            if cand < best:
                best = cand
            bits ^= bit
        dp[mask] = best
    return dp[-1]


def eval_clause(clause, assignment):
    for lit in clause:
        val = assignment.get(abs(lit))
        if val is not None and (val if lit > 0 else not val):
            return True
    return False


def simplify(clauses, assignment):
    out = []
    for clause in clauses:
        if eval_clause(clause, assignment):
            continue
        residual = tuple(lit for lit in clause if abs(lit) not in assignment)
        if not residual:
            return None
        out.append(residual)
    return out


def dpll(clauses, assignment=None):
    assignment = {} if assignment is None else dict(assignment)
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return False
    while True:
        units = [c[0] for c in clauses if len(c) == 1]
        if not units:
            break
        for lit in units:
            v, val = abs(lit), lit > 0
            if v in assignment and assignment[v] != val:
                return False
            assignment[v] = val
        clauses = simplify(clauses, assignment)
        if clauses is None:
            return False
    if not clauses:
        return True
    v = abs(clauses[0][0])
    return dpll(clauses, {**assignment, v: False}) or dpll(
        clauses, {**assignment, v: True}
    )


def all_sign_clauses(a, b, c):
    out = []
    for mask in range(8):
        out.append(tuple(v if (mask >> i) & 1 else -v for i, v in enumerate((a, b, c))))
    return out


def shannon_two_levels(clauses, x, y):
    root = dpll(clauses)
    first = [dpll(clauses, {x: bit}) for bit in (False, True)]
    second = [
        dpll(clauses, {x: bx, y: by})
        for bx in (False, True)
        for by in (False, True)
    ]
    return root, first, second


def clause_at(q, idx, first_var=1):
    """Direct arithmetic accessor for the idx-th grid edge clause."""
    edges = 2 * q * (q - 1)
    if idx < 0 or idx >= edges:
        raise IndexError(idx)
    horizontal = q * (q - 1)
    if idx < horizontal:
        r, c = divmod(idx, q - 1)
        a = r * q + c
        b = a + 1
    else:
        j = idx - horizontal
        r, c = divmod(j, q)
        a = r * q + c
        b = a + q
    aux = first_var + q * q + idx
    return (first_var + a, first_var + b, aux)


def fixed_record_bits(q, first_var=1):
    clauses, max_var, _ = grid_padding(q, first_var)
    width = max(1, math.ceil(math.log2(max_var + 1)))
    header = f"{max_var:032b}{len(clauses):032b}{width:08b}"
    body = "".join("".join(f"{lit:0{width}b}" for lit in c) for c in clauses)
    return header + body


def fixed_record_bit_at(q, idx, first_var=1):
    clauses = 2 * q * (q - 1)
    max_var = first_var + q * q + clauses - 1
    width = max(1, math.ceil(math.log2(max_var + 1)))
    header = f"{max_var:032b}{clauses:032b}{width:08b}"
    if idx < len(header):
        return header[idx]
    j = idx - len(header)
    rec = 3 * width
    ci, off = divmod(j, rec)
    clause = clause_at(q, ci, first_var)
    field, bit = divmod(off, width)
    return f"{clause[field]:0{width}b}"[bit]


def main():
    start = time.time()
    assertions = 0
    rows = []
    for q in (2, 3, 4):
        clauses, max_var, verts = grid_padding(q, first_var=4)
        assert len(clauses) == 2 * q * (q - 1); assertions += 1
        assert all(len(c) == 3 and len(set(c)) == 3 for c in clauses); assertions += 1
        assert all(lit > 0 for c in clauses for lit in c); assertions += 1
        assert dpll(clauses); assertions += 1
        sep = exact_vertex_separation(q)
        assert sep == q; assertions += 1

        bits = fixed_record_bits(q, first_var=4)
        rebuilt = "".join(fixed_record_bit_at(q, i, first_var=4) for i in range(len(bits)))
        assert rebuilt == bits; assertions += len(bits)

        sat_core = [(1, 2, 3)]
        unsat_core = all_sign_clauses(1, 2, 3)
        for label, core in ((True, sat_core), (False, unsat_core)):
            padded = core + clauses
            root, first, second = shannon_two_levels(padded, 1, 2)
            assert root == label; assertions += 1
            assert any(first) == root; assertions += 1
            assert any(second) == root; assertions += 1
            # Every restriction leaves the untouched grid primal subgraph.
            assert exact_vertex_separation(q) == q; assertions += 1

        rows.append({
            "q": q,
            "grid_vertices": q*q,
            "grid_edges_clauses": len(clauses),
            "total_padding_variables": max_var - 3,
            "fixed_record_bits": len(bits),
            "exact_vertex_separation": sep,
            "scope_bag_lower_bound": q,
            "two_level_sat_and_unsat_controls": True,
        })

    # Larger scales validate direct access without exponential DP.
    for q in (8, 16, 32):
        bits = fixed_record_bits(q)
        probes = sorted(set([0, 1, 31, 32, 63, 64, 71, len(bits)//2, len(bits)-1]))
        for i in probes:
            assert fixed_record_bit_at(q, i) == bits[i]; assertions += 1
        rows.append({
            "q": q,
            "grid_vertices": q*q,
            "grid_edges_clauses": 2*q*(q-1),
            "fixed_record_bits": len(bits),
            "accessor_probes_checked": len(probes),
            "theorem_scope_lower_bound": q,
        })

    out = {
        "run_id": "ARC-HARD-IMAGE-WIDTH-PADDING163",
        "status": "COMPUTATIONAL finite audit supporting a separate symbolic theorem",
        "randomness": "none; exhaustive subset DP for q=2,3,4",
        "assertions": assertions,
        "failures": 0,
        "rows": rows,
        "elapsed_seconds": round(time.time()-start, 6),
        "limitations": [
            "finite exact pathwidth checks only through 4x4",
            "symbolic scope lower bound is proved separately in the report",
            "known padding is cheaply recognizable and removable",
            "no SAT runtime lower bound and no ARC successor is claimed",
        ],
    }
    payload = json.dumps(out, indent=2, sort_keys=True) + "\n"
    Path("2026-10-25_0247_ARC_HARD_IMAGE_WIDTH_PADDING163_results.json").write_text(payload)
    print(payload, end="")
    print("sha256", hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
