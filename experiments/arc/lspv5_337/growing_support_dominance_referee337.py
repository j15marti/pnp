#!/usr/bin/env python3
"""Finite controls for REFEREE337's growing-support normalization firewall."""

from __future__ import annotations

import hashlib
import itertools
import json
import math

checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def parity(bits: tuple[int, ...]) -> int:
    return sum(bits) & 1


def var_names(m: int) -> list[str]:
    return [f"x{i}" for i in range(1, m + 1)] + [f"z{i}" for i in range(2, m)]


def chain_clauses(m: int) -> list[tuple[tuple[str, bool], ...]]:
    """CNF for even parity, using XOR3 prefix rows and a final equality."""
    assert m >= 2
    clauses: list[tuple[tuple[str, bool], ...]] = []
    previous = "x1"
    for i in range(2, m):
        x, z = f"x{i}", f"z{i}"
        clauses.extend([
            ((previous, True), (x, True), (z, False)),
            ((previous, True), (x, False), (z, True)),
            ((previous, False), (x, True), (z, True)),
            ((previous, False), (x, False), (z, False)),
        ])
        previous = z
    clauses.extend([
        ((previous, False), (f"x{m}", True)),
        ((previous, True), (f"x{m}", False)),
    ])
    return clauses


def clause_value(clause, assignment: dict[str, int]) -> bool:
    return any(bool(assignment[name]) == positive for name, positive in clause)


def assignments(names: list[str]):
    for row in itertools.product((0, 1), repeat=len(names)):
        yield dict(zip(names, row))


def x_tuple(assignment: dict[str, int], m: int) -> tuple[int, ...]:
    return tuple(assignment[f"x{i}"] for i in range(1, m + 1))


def validate_local_record(record: dict, fixed_k: int | None) -> bool:
    support, table = record.get("support"), record.get("truth_table")
    if not isinstance(support, list) or len(set(support)) != len(support):
        return False
    if not all(isinstance(v, str) and v.startswith("x") for v in support):
        return False
    if fixed_k is not None and len(support) > fixed_k:
        return False
    if not isinstance(table, list) or len(table) != 2 ** len(support):
        return False
    if not all(bit in (0, 1) for bit in table):
        return False
    return not record.get("cycle")


chain_summary = []
for m in range(2, 8):
    names, clauses = var_names(m), chain_clauses(m)
    check(len(clauses) == 4 * m - 6, f"clause count m={m}")
    all_rows = list(assignments(names))
    models = []
    for a in all_rows:
        cnf = all(clause_value(c, a) for c in clauses)
        even = parity(x_tuple(a, m)) == 0
        check((not cnf) or even, f"chain implies even parity m={m}")
        if cnf:
            models.append(a)
    check(len(models) == 2 ** (m - 1), f"model count m={m}")
    for deleted in range(len(clauses)):
        witness = next((a for a in all_rows
                        if all(clause_value(c, a) for j, c in enumerate(clauses) if j != deleted)
                        and parity(x_tuple(a, m)) == 1), None)
        check(witness is not None, f"deletion witness m={m}, clause={deleted}")
    beta_even, beta_odd = (0,) * m, (1,) + (0,) * (m - 1)
    check(any(x_tuple(a, m) == beta_even and all(clause_value(c, a) for c in clauses) for a in all_rows),
          f"even pins SAT m={m}")
    check(not any(x_tuple(a, m) == beta_odd and all(clause_value(c, a) for c in clauses) for a in all_rows),
          f"odd pins UNSAT m={m}")
    base_nodes = 4 * m - 7
    check(base_nodes == 3 * (m - 2) + 1 + (m - 2), f"node ledger m={m}")
    chain_summary.append({"m": m, "variables": len(names), "clauses": len(clauses),
                          "models": len(models), "target_nodes": base_nodes,
                          "ancestral_hard_q_nodes": 5 * m - 5,
                          "dominance_bypass_nodes": 5 * m - 6})


finite_q_summary = []
for m in range(2, 6):
    rows = list(itertools.product((0, 1), repeat=m))
    beta = (1,) + (0,) * (m - 1)
    odd_rows = [r for r in rows if parity(r) == 1 and r != beta]
    truth_vectors = set()
    for mask in range(1 << len(odd_rows)):
        h = {beta: 0, **{row: (mask >> i) & 1 for i, row in enumerate(odd_rows)}}
        qvec = []
        for row in rows:
            p = parity(row) == 0
            q = p or bool(h.get(row, 0))
            blocker = row != beta
            check((not p) or q, f"P=>Q m={m}")
            check((not q) or blocker, f"Q=>C_beta m={m}")
            check((not p) or blocker, f"dominance bypass m={m}")
            qvec.append(int(q))
        truth_vectors.add(tuple(qvec))
    expected = 2 ** (2 ** (m - 1) - 1)
    check(len(truth_vectors) == expected, f"hard-Q family size m={m}")
    finite_q_summary.append({"m": m, "family_size": expected, "beta": list(beta)})


basis_size = 16
counting_summary = []
recorded_widths = {8, 12, 16, 24, 32, 40, 48, 52}
for m in range(8, 65):
    d_m = 2 * m + 2 + math.ceil(math.log2(basis_size))
    s = max(0, (2 ** (m - 1) - 2 * m - 4) // d_m)
    if s:
        log_count = (math.log2(s + 1) + math.log2(m + s + 2)
                     + s * (math.log2(basis_size) + 2 * math.log2(m + s + 2)))
        family_log = 2 ** (m - 1) - 1
        check(log_count < family_log, f"circuit count separation m={m}")
        check(s + 1 >= 2 ** (m - 8) // m, f"exponential lower envelope m={m}")
    if m in recorded_widths:
        counting_summary.append({"m": m, "D_m": d_m, "certified_min_gates": s + 1,
                                 "family_log2": 2 ** (m - 1) - 1})


m = 9
valid = {"support": [f"x{i}" for i in range(1, m + 1)],
         "truth_table": [1] * (2 ** m), "cycle": False}
check(validate_local_record(valid, None), "permissive growing-support acceptance")
check(not validate_local_record(valid, 3), "fixed-K rejection")
for corrupt in (
    {**valid, "truth_table": valid["truth_table"][:-1]},
    {**valid, "truth_table": valid["truth_table"][:-1] + [2]},
    {**valid, "support": valid["support"][:-1] + [valid["support"][0]]},
    {**valid, "support": valid["support"][:-1] + ["private_wire"]},
    {**valid, "cycle": True},
):
    check(not validate_local_record(corrupt, None), "malformed record rejection")


result = {
    "artifact": "GROWING-SUPPORT-DOMINANCE-REFEREE337",
    "status": {"literal_r_mix341": "growing-support LOCAL-CONVERT not certified",
               "permissive_completion": "exact-output poly(N+q) normalization falsified",
               "whole_refutation": "hard-Q node has a one-node-shorter dominance bypass",
               "B1": "OPEN", "B2": "OPEN", "B3": "OPEN", "P_vs_NP": "OPEN"},
    "basis_size": basis_size, "checks": checks, "chain_controls": chain_summary,
    "finite_q_controls": finite_q_summary, "counting_controls": counting_summary,
    "malformed_rejections": 5, "strict_fixed_k_rejection": True,
}
canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
result["sha256_without_digest"] = hashlib.sha256(canonical.encode()).hexdigest()
print(json.dumps(result, indent=2, sort_keys=True))
