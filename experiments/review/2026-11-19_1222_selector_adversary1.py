#!/usr/bin/env python3
"""Exact finite audits for row/block selector counterexamples.

The constructions are ordinary CNFs.  Shared variables are 1..h and every
block has fresh private variables.  No SAT/UNSAT answer bit is supplied.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path


def bits(x: int, h: int) -> tuple[int, ...]:
    return tuple((x >> j) & 1 for j in range(h))


def eval_clause(clause: tuple[int, ...], assignment: dict[int, bool]):
    unknown = []
    for lit in clause:
        v = abs(lit)
        if v not in assignment:
            unknown.append(lit)
        elif assignment[v] == (lit > 0):
            return True, ()
    return False, tuple(unknown)


def solve_cnf(clauses: list[tuple[int, ...]], fixed: dict[int, bool]):
    """Small exact DPLL used only as an independent finite checker."""
    stats = {"nodes": 0, "unit_assignments": 0}

    def rec(assignment: dict[int, bool]):
        stats["nodes"] += 1
        assignment = dict(assignment)
        while True:
            unit = None
            all_true = True
            for clause in clauses:
                sat, rem = eval_clause(clause, assignment)
                if sat:
                    continue
                all_true = False
                if not rem:
                    return None
                if len(rem) == 1:
                    unit = rem[0]
                    break
            if all_true:
                return assignment
            if unit is None:
                break
            v, value = abs(unit), unit > 0
            if v in assignment and assignment[v] != value:
                return None
            assignment[v] = value
            stats["unit_assignments"] += 1

        candidate = min(
            abs(lit)
            for clause in clauses
            for lit in clause
            if abs(lit) not in assignment
        )
        for value in (False, True):
            child = dict(assignment)
            child[candidate] = value
            answer = rec(child)
            if answer is not None:
                return answer
        return None

    answer = rec(fixed)
    if answer is not None:
        assert all(eval_clause(c, answer)[0] for c in clauses)
    return answer, stats


def xor_gate(a: int, b: int, out: int) -> list[tuple[int, ...]]:
    """CNF for out = a XOR b."""
    return [
        (a, b, -out),
        (a, -b, out),
        (-a, b, out),
        (-a, -b, -out),
    ]


def affine_value(row: tuple[int, ...]) -> tuple[int, ...]:
    """(J+I)z over GF(2): output j is XOR of every input except j."""
    return tuple(sum(row[k] for k in range(len(row)) if k != j) & 1
                 for j in range(len(row)))


def affine_block(h: int, target: tuple[int, ...], next_var: int):
    clauses: list[tuple[int, ...]] = []
    outputs: list[int] = []
    for j in range(h):
        inputs = [k + 1 for k in range(h) if k != j]
        assert inputs
        if len(inputs) == 1:
            outputs.append(inputs[0])
            continue
        acc = inputs[0]
        for x in inputs[1:]:
            out = next_var
            next_var += 1
            clauses.extend(xor_gate(acc, x, out))
            acc = out
        outputs.append(acc)
    # At least one output bit must differ from the target.
    clauses.append(tuple(out if t == 0 else -out
                         for out, t in zip(outputs, target)))
    return clauses, next_var


def row_guard_block(h: int, bad_row: tuple[int, ...], private: int):
    """Two clauses, UNSAT exactly when z == bad_row."""
    mismatch = tuple((j + 1) if bit == 0 else -(j + 1)
                     for j, bit in enumerate(bad_row))
    return [mismatch + (private,), mismatch + (-private,)]


def audit_affine(h: int):
    assert h % 2 == 0
    rows = [bits(x, h) for x in range(1 << h)]
    images = [affine_value(row) for row in rows]
    assert len(set(images)) == len(rows), "J+I must be invertible for even h"

    blocks = []
    next_var = h + 1
    for target in map(bits, range(1 << h), itertools.repeat(h)):
        cnf, next_var = affine_block(h, target, next_var)
        blocks.append(cnf)

    total_solves = total_nodes = total_units = 0
    unique = []
    for row, image in zip(rows, images):
        fixed = {j + 1: bool(v) for j, v in enumerate(row)}
        bad = []
        for target_id, cnf in enumerate(blocks):
            answer, stats = solve_cnf(cnf, fixed)
            total_solves += 1
            total_nodes += stats["nodes"]
            total_units += stats["unit_assignments"]
            if answer is None:
                bad.append(target_id)
        expected = sum(v << j for j, v in enumerate(image))
        assert bad == [expected]
        unique.append(expected)

    # Every shared variable is semantically relevant to every block: the
    # unique bad row for a block becomes SAT after flipping any one bit.
    semantic_support_checks = 0
    inverse = {sum(v << j for j, v in enumerate(im)): row
               for row, im in zip(rows, images)}
    for target_id, bad_row in inverse.items():
        for j in range(h):
            flipped = list(bad_row)
            flipped[j] ^= 1
            assert affine_value(tuple(flipped)) != bits(target_id, h)
            semantic_support_checks += 1

    # Remove one block: exactly its inverse row becomes a SAT row.
    hole = (1 << h) // 3
    remaining = [cnf for i, cnf in enumerate(blocks) if i != hole]
    sat_rows = []
    for row in rows:
        fixed = {j + 1: bool(v) for j, v in enumerate(row)}
        if all(solve_cnf(cnf, fixed)[0] is not None for cnf in remaining):
            sat_rows.append(row)
    assert sat_rows == [inverse[hole]]

    return {
        "h": h,
        "rows": len(rows),
        "blocks": len(blocks),
        "cnf_solves": total_solves,
        "dpll_nodes": total_nodes,
        "unit_assignments": total_units,
        "selector_is_permutation": len(set(unique)) == len(rows),
        "no_fixed_bad_block": len(set(unique)) > 1,
        "semantic_support_checks": semantic_support_checks,
        "one_hole_target": hole,
        "one_hole_sat_row": list(sat_rows[0]),
    }


def audit_arbitrary_permutation(h: int):
    r = 1 << h
    # Fixed nonlinear-looking permutation; it is data, not advice to solver.
    permutation = [(5 * x + 3 * (x.bit_count() & 1) + 1) % r for x in range(r)]
    if len(set(permutation)) != r:
        # Deterministic fallback: bit reversal, still an arbitrary table order.
        permutation = [int(f"{x:0{h}b}"[::-1], 2) for x in range(r)]
    assert len(set(permutation)) == r
    inverse = [0] * r
    for row_id, block_id in enumerate(permutation):
        inverse[block_id] = row_id

    blocks = [row_guard_block(h, bits(inverse[i], h), h + 1 + i)
              for i in range(r)]
    observed = []
    for row_id in range(r):
        fixed = {j + 1: bool(v) for j, v in enumerate(bits(row_id, h))}
        bad = [i for i, cnf in enumerate(blocks)
               if solve_cnf(cnf, fixed)[0] is None]
        assert bad == [permutation[row_id]]
        observed.append(bad[0])
    return {
        "h": h,
        "rows": r,
        "selector_table": permutation,
        "observed_table": observed,
        "clauses_per_block": 2,
        "literals_per_block": 2 * (h + 1),
        "private_variables_disjoint": True,
    }


def selector_table_scaling():
    cases = []
    for q in (64, 128, 256, 512, 1024):
        # N=2^q, R<=N^.195, B<=N^.65.
        h = math.floor(0.195 * q)
        log_b = math.ceil(0.65 * q)
        table_log2_upper = h + math.log2(max(1, log_b))
        sqrt_log2 = 0.5 * q
        assert table_log2_upper < sqrt_log2
        cases.append({
            "log2_N": q,
            "log2_R": h,
            "ceil_log2_B": log_b,
            "log2_selector_table_bits_upper": table_log2_upper,
            "log2_sqrt_N": sqrt_log2,
            "margin_bits_in_log2": sqrt_log2 - table_log2_upper,
        })
    return cases


def audit_t5(source: Path, result_path: Path):
    raw = source.read_bytes()
    arcs = []
    n = None
    for line in raw.decode("ascii").splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "p":
            n = int(f[2])
        elif f[0] == "a":
            arcs.append((int(f[1]), int(f[2])))
    data = json.loads(result_path.read_text())
    assert n == data["vertices"] and len(arcs) == data["arcs"]
    checks = 0
    for omitted_text, entry in data["per_edge"].items():
        omitted = int(omitted_text)
        colors = entry["colors"]
        assert len(colors) == n
        for rotation in range(5):
            rotated = [(c + rotation) % 5 for c in colors]
            false_edges = []
            for eid, (u, v) in enumerate(arcs):
                checks += 1
                if (rotated[v] - rotated[u]) % 5 not in (1, 3):
                    false_edges.append(eid)
            assert false_edges == [omitted]
    return {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "vertices": n,
        "arcs": len(arcs),
        "deletion_witnesses": len(data["per_edge"]),
        "rotations_per_witness": 5,
        "arc_checks": checks,
        "interpretation": "supplied witness verification only; acquisition not tested",
    }


def main():
    affine = [audit_affine(h) for h in (2, 4)]
    arbitrary = audit_arbitrary_permutation(3)
    scaling = selector_table_scaling()
    result = {
        "status": "PASS",
        "P_vs_NP": "OPEN",
        "affine_unique_bad_block": affine,
        "arbitrary_permutation_selector": arbitrary,
        "selector_table_scaling": scaling,
    }
    source = Path("source079.t5")
    t5_results = Path("t5_cycle_mitm_results.json")
    if source.exists() and t5_results.exists():
        result["t5_control"] = audit_t5(source, t5_results)
    Path("adversarial_selector_audit_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
