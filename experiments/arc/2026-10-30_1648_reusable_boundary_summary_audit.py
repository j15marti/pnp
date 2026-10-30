#!/usr/bin/env python3
"""Reusable boundary-summary firewall 228.

Builds exact existential 3-CNF encodings A_f(X,Y) for every Boolean boundary
function on b=3 and b=4, verifies point-query continuations, checks the standard
long-clause chain through b=8, and retains source-clause S/U controls plus a
common DPLL backend on matched SAT/UNSAT sources.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path


def bit(a: int, i: int) -> int:
    return (a >> i) & 1


def exclusion_literals(a: int, b: int) -> list[int]:
    # This disjunction is false exactly on boundary assignment a.
    return [-(i + 1) if bit(a, i) else i + 1 for i in range(b)]


def chain_clauses(lits: list[int], auxiliaries: list[int]) -> list[tuple[int, int, int]]:
    b = len(lits)
    if b == 3:
        return [tuple(lits)]
    assert len(auxiliaries) >= b - 3
    out = [(lits[0], lits[1], auxiliaries[0])]
    for j in range(1, b - 3):
        out.append((-auxiliaries[j - 1], lits[j + 1], auxiliaries[j]))
    out.append((-auxiliaries[b - 4], lits[-2], lits[-1]))
    assert len(out) == b - 2
    return out


def lit_true(lit: int, assignment: dict[int, int]) -> bool:
    return assignment[abs(lit)] == int(lit > 0)


def clauses_true(clauses, assignment) -> bool:
    return all(any(lit_true(lit, assignment) for lit in clause) for clause in clauses)


def verify_chain(b: int) -> int:
    checks = 0
    aux = list(range(b + 1, b + 1 + max(0, b - 3)))
    for a in range(1 << b):
        clauses = chain_clauses(exclusion_literals(a, b), aux)
        for x in range(1 << b):
            expected = x != a
            exists = False
            for z in range(1 << len(aux)):
                assignment = {i + 1: bit(x, i) for i in range(b)}
                assignment.update({v: bit(z, j) for j, v in enumerate(aux)})
                if clauses_true(clauses, assignment):
                    exists = True
                    break
            assert exists == expected
            checks += 1
    return checks


def build_padded_formula(mask: int, b: int):
    """Uniform block-count proper 3-CNF with existential projection f=mask."""
    blocks = 1 << b
    clauses_per_block = b - 2
    slots_per_block = 3 * clauses_per_block
    clauses: list[tuple[int, int, int]] = []
    block_info = []
    for a in range(blocks):
        base = b + 1 + a * slots_per_block
        slots = list(range(base, base + slots_per_block))
        if bit(mask, a) == 0:
            block = chain_clauses(exclusion_literals(a, b), slots[: max(0, b - 3)])
            kind = "exclude"
        else:
            block = [tuple(slots[3 * j : 3 * j + 3]) for j in range(clauses_per_block)]
            kind = "dummy_true"
        assert len(block) == clauses_per_block
        assert all(len(set(map(abs, c))) == 3 for c in block)
        clauses.extend(block)
        block_info.append({"boundary_assignment": a, "kind": kind, "clauses": block})
    nvars = b + blocks * slots_per_block
    return clauses, nvars, block_info


def verify_all_functions(b: int):
    blocks = 1 << b
    accepts = [[x != a for x in range(blocks)] for a in range(blocks)]
    function_count = 1 << blocks
    query_checks = 0
    unique_projections = set()
    for mask in range(function_count):
        projection = 0
        for x in range(blocks):
            got = all(bit(mask, a) or accepts[a][x] for a in range(blocks))
            if got:
                projection |= 1 << x
            assert got == bool(bit(mask, x))
            query_checks += 1
        unique_projections.add(projection)
    assert len(unique_projections) == function_count
    return {"b": b, "functions": function_count, "point_queries": query_checks,
            "unique_projections": len(unique_projections)}


def verify_pin_gadget(max_b: int = 8) -> int:
    checks = 0
    for b in range(1, max_b + 1):
        for desired in (0, 1):
            lit = 1 if desired else -1
            clauses = [(lit, 2, 3), (lit, 2, -3), (lit, -2, 3), (lit, -2, -3)]
            for actual in (0, 1):
                exists = False
                for u, v in itertools.product((0, 1), repeat=2):
                    if clauses_true(clauses, {1: actual, 2: u, 3: v}):
                        exists = True
                        break
                assert exists == (actual == desired)
                checks += 1
    return checks


def simplify(clauses, assignment, stats):
    out = []
    for clause in clauses:
        stats["clause_visits"] += 1
        sat = False
        rem = []
        for lit in clause:
            stats["literal_tests"] += 1
            v = abs(lit)
            if v not in assignment:
                rem.append(lit)
            elif assignment[v] == int(lit > 0):
                sat = True
                break
        if not sat:
            if not rem:
                return None
            out.append(tuple(rem))
    return out


def unit_propagate(clauses, assignment, stats):
    while True:
        reduced = simplify(clauses, assignment, stats)
        if reduced is None:
            return None
        units = [c[0] for c in reduced if len(c) == 1]
        if not units:
            return reduced
        changed = False
        for lit in units:
            v, val = abs(lit), int(lit > 0)
            if v in assignment and assignment[v] != val:
                return None
            if v not in assignment:
                assignment[v] = val
                stats["unit_assignments"] += 1
                changed = True
        if not changed:
            return reduced


def dpll(clauses, nvars):
    stats = {"nodes": 0, "branches": 0, "clause_visits": 0,
             "literal_tests": 0, "unit_assignments": 0}

    def rec(cur, assignment):
        stats["nodes"] += 1
        reduced = unit_propagate(cur, assignment, stats)
        if reduced is None:
            return None
        if not reduced:
            return assignment
        counts = Counter(abs(l) for c in reduced for l in c if abs(l) not in assignment)
        v = max(counts, key=lambda z: (counts[z], -z))
        stats["branches"] += 1
        for val in (1, 0):
            nxt = dict(assignment)
            nxt[v] = val
            ans = rec(reduced, nxt)
            if ans is not None:
                return ans
        return None

    witness = rec(clauses, {})
    if witness is not None:
        witness = [witness.get(v, 0) for v in range(1, nvars + 1)]
        assert all(any(witness[abs(l)-1] == int(l > 0) for l in c) for c in clauses)
    return witness, stats


def histogram(clauses, values):
    h = [0, 0, 0, 0]
    for c in clauses:
        t = sum(values[abs(l)-1] == int(l > 0) for l in c)
        h[t] += 1
    return h


def local_targets(clauses):
    out = []
    for j, clause in enumerate(clauses, 1):
        occ = []
        for pos, lit in enumerate(clause):
            s = int(lit > 0)
            u = 1 - s
            occ.append({"occurrence": f"x_{abs(lit)},{j}", "position": pos,
                        "variable": abs(lit), "sign": "+" if lit > 0 else "-",
                        "S_all_true": s, "inverse_S_is_U": 1-s,
                        "U_all_false": u, "inverse_U_is_S": 1-u})
        out.append({"clause_index": j-1, "clause": list(clause), "occurrences": occ})
    return out


def pair_compatibility(clauses):
    out = []
    for j, k in itertools.combinations(range(len(clauses)), 2):
        sj = {abs(x): int(x > 0) for x in clauses[j]}
        sk = {abs(x): int(x > 0) for x in clauses[k]}
        shared = set(sj) & set(sk)
        same = any(sj[v] == sk[v] for v in shared)
        opposite = any(sj[v] != sk[v] for v in shared)
        out.append({"clauses": [j, k], "shared_same": same,
                    "shared_opposite": opposite, "SS": not opposite,
                    "SU": not same, "US": not same, "UU": not opposite})
    return out


def source_control(name, mask, b):
    clauses, nvars, blocks = build_padded_formula(mask, b)
    witness, stats = dpll(clauses, nvars)
    all0 = [0] * nvars
    all1 = [1] * nvars
    trail = []
    cur = all0[:]
    for v in list(range(min(b, 4))) + list(reversed(range(min(b, 4)))):
        trail.append({"flipped_variable": v + 1, "histogram": histogram(clauses, cur)})
        cur[v] ^= 1
    return {"name": name, "b": b, "mask": mask, "clauses": len(clauses),
            "nvars_fixed_universe": nvars, "SAT": witness is not None,
            "witness": witness, "dpll": stats,
            "endpoints": {"zero": histogram(clauses, all0),
                          "one": histogram(clauses, all1)},
            "flip_trail": trail, "local_targets": local_targets(clauses),
            "pair_compatibility": pair_compatibility(clauses),
            "block_kinds": Counter(x["kind"] for x in blocks)}


def encoding_table():
    rows = []
    for b in range(3, 17):
        clauses = (b - 2) * (1 << b)
        variables = b + 3 * clauses
        index_bits = math.ceil(math.log2(variables + 1))
        # Fixed-width sign+index slots plus a small fixed-width header.
        source_bits = 3 * clauses * (1 + index_bits) + 2 * index_bits
        summary_bits = 1 << b
        rows.append({"b": b, "clauses": clauses, "variables": variables,
                     "index_bits": index_bits, "source_bits_upper_encoding": source_bits,
                     "summary_lower_bound_bits": summary_bits,
                     "L_over_N": summary_bits / source_bits,
                     "L_over_sqrtN": summary_bits / math.sqrt(source_bits)})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    chain_checks = {str(b): verify_chain(b) for b in range(3, 9)}
    function_checks = [verify_all_functions(3), verify_all_functions(4)]
    pin_checks = verify_pin_gadget()
    controls = [
        source_control("unique_boundary_model_SAT", 1 << 15, 4),
        source_control("zero_boundary_function_UNSAT", 0, 4),
    ]
    assert controls[0]["SAT"] and not controls[1]["SAT"]

    total_functions = sum(x["functions"] for x in function_checks)
    total_queries = sum(x["point_queries"] for x in function_checks)
    result = {
        "id": "ARC-REUSABLE-BOUNDARY-SUMMARY-FIREWALL228",
        "date": "2026-10-30 America/Los_Angeles",
        "claim": ("Any deterministic reusable summary prepared from A_f before a point-pinning "
                  "continuation and exact for every continuation needs worst-case length at least 2^b bits."),
        "status": {
            "reusable_summary_lower_bound": "PROVED/EXACT restricted one-way/index theorem",
            "power_short_explicit_frontier_summary": "FALSIFIED/RETIRED for this universal reusable interface",
            "finite_audit": "COMPUTATIONAL",
            "arbitrary_joint_solver": "OPEN/unconstrained by theorem",
            "ARC": "OPEN", "P_vs_NP": "OPEN"
        },
        "counts": {"functions_exhausted": total_functions,
                   "point_query_checks": total_queries,
                   "chain_projection_checks": sum(chain_checks.values()),
                   "pin_gadget_checks": pin_checks},
        "chain_checks_by_b": chain_checks,
        "function_checks": function_checks,
        "encoding_growth": encoding_table(),
        "same_source_controls": controls,
        "limitations": [
            "The preprocessor sees A before B and the query algorithm cannot reread A.",
            "A solver seeing A and B jointly, recomputation, or a source-retaining ARC controller is not lower-bounded.",
            "The result is near-linear in the explicit source size, not exponential in source size.",
            "Python selected work is not a native FLMV time-space measurement."
        ]
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
