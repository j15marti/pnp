#!/usr/bin/env python3
"""Finite hostile-control audit for named extractor-call non-invariance.

Every variant decides the same explicit CNF by exhaustive search.  The point is
not speed: it is that a named helper call can be erased by inlining or by a
single-dispatcher simulation without changing the decision function.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

Literal = int
Clause = tuple[Literal, ...]


@dataclass
class Metrics:
    answer: bool = False
    assignments: int = 0
    clause_tests: int = 0
    literal_tests: int = 0
    host_api_calls: int = 0
    guest_logical_calls: int = 0
    materialized_bits: int = 0


def lit_value(lit: int, assignment: int) -> bool:
    bit = bool((assignment >> (abs(lit) - 1)) & 1)
    return bit if lit > 0 else not bit


def extract_clause_vector(clauses: tuple[Clause, ...], a: int, m: Metrics) -> list[bool]:
    """The deliberately named internal API used only by EXPLICIT."""
    m.host_api_calls += 1
    m.guest_logical_calls += 1
    out: list[bool] = []
    for clause in clauses:
        m.clause_tests += 1
        value = False
        for lit in clause:
            m.literal_tests += 1
            value = value or lit_value(lit, a)
        out.append(value)
    m.materialized_bits += len(out)
    return out


def decide_explicit(n: int, clauses: tuple[Clause, ...]) -> Metrics:
    m = Metrics()
    for a in range(1 << n):
        m.assignments += 1
        if all(extract_clause_vector(clauses, a, m)):
            m.answer = True
            break
    return m


def decide_inline(n: int, clauses: tuple[Clause, ...]) -> Metrics:
    m = Metrics()
    for a in range(1 << n):
        m.assignments += 1
        vector: list[bool] = []
        m.guest_logical_calls += 1
        for clause in clauses:
            m.clause_tests += 1
            value = False
            for lit in clause:
                m.literal_tests += 1
                value = value or lit_value(lit, a)
            vector.append(value)
        m.materialized_bits += len(vector)
        if all(vector):
            m.answer = True
            break
    return m


def decide_fused(n: int, clauses: tuple[Clause, ...]) -> Metrics:
    m = Metrics()
    for a in range(1 << n):
        m.assignments += 1
        good = True
        for clause in clauses:
            m.clause_tests += 1
            value = False
            for lit in clause:
                m.literal_tests += 1
                if lit_value(lit, a):
                    value = True
                    break
            if not value:
                good = False
                break
        if good:
            m.answer = True
            break
    return m


def decide_dispatch(n: int, clauses: tuple[Clause, ...]) -> Metrics:
    """One host loop simulating main/helper PCs; there is no host API call."""
    m = Metrics()
    for a in range(1 << n):
        m.assignments += 1
        pc, ci, li, clause_value = 0, 0, 0, False
        vector: list[bool] = []
        stack: list[int] = []
        while True:
            if pc == 0:  # simulated call
                m.guest_logical_calls += 1
                stack.append(4)
                pc = 1
            elif pc == 1:  # clause entry
                if ci == len(clauses):
                    pc = stack.pop()
                else:
                    m.clause_tests += 1
                    li, clause_value, pc = 0, False, 2
            elif pc == 2:  # literal loop
                if li == len(clauses[ci]):
                    vector.append(clause_value)
                    ci += 1
                    pc = 1
                else:
                    m.literal_tests += 1
                    clause_value = clause_value or lit_value(clauses[ci][li], a)
                    li += 1
            elif pc == 4:  # return site
                m.materialized_bits += len(vector)
                if all(vector):
                    m.answer = True
                break
            else:
                raise AssertionError(pc)
        if m.answer:
            break
    return m


def decide_table(n: int, clauses: tuple[Clause, ...]) -> Metrics:
    """Table-driven evaluator: same one-bit answer, no named logical call."""
    bytecode = tuple((lit, i == len(c) - 1) for c in clauses for i, lit in enumerate(c))
    m = Metrics()
    for a in range(1 << n):
        m.assignments += 1
        formula_value, clause_value = True, False
        for lit, end_clause in bytecode:
            m.literal_tests += 1
            clause_value = clause_value or lit_value(lit, a)
            if end_clause:
                m.clause_tests += 1
                formula_value = formula_value and clause_value
                clause_value = False
        if formula_value:
            m.answer = True
            break
    return m


def xor_cnf(x: int, y: int, z: int) -> list[Clause]:
    return [(x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z)]


def graph_3color(edges: Iterable[tuple[int, int]], vertices: int) -> tuple[int, list[Clause]]:
    var = lambda v, c: 3 * v + c + 1
    out: list[Clause] = []
    for v in range(vertices):
        out.append((var(v, 0), var(v, 1), var(v, 2)))
        for c in range(3):
            for d in range(c + 1, 3):
                out.append((-var(v, c), -var(v, d)))
    for u, v in edges:
        for c in range(3):
            out.append((-var(u, c), -var(v, c)))
    return 3 * vertices, out


def cases() -> dict[str, tuple[int, list[Clause]]]:
    affine = xor_cnf(1, 2, 3) + [(3,), (-3,)]
    path = [(1, 2), (-2, 3), (-3, 4), (-4, 5), (-5, 6), (6,)]
    k4_edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    n_k4, cnf_k4 = graph_3color(k4_edges, 4)
    n_k33, cnf_k33 = graph_3color(k33, 6)
    product = [(1, 2), (-1, 2), (3, 4), (-3, 4), (5, 6), (-5, 6)]
    redundant = [(1, 2, 3)] * 12 + [(-1, 2, 3)] * 12 + [(2,)]
    return {
        "2sat_implication": (5, [(1, 2), (-1, 3), (-3, 4), (-4, 5), (5,)]),
        "horn_chain": (6, [(1,), (-1, 2), (-2, 3), (-3, 4), (-4, 5), (-5, 6)]),
        "affine_tseitin_unsat": (3, affine),
        "bounded_treewidth_path": (6, path),
        "k4_3color_unsat": (n_k4, cnf_k4),
        "k33_3color_sat": (n_k33, cnf_k33),
        "independent_product": (6, product),
        "redundant_clauses": (3, redundant),
        "alternate_literal_order": (5, [(3, -1, 2), (5, -3), (4, -5), (1,)]),
        "padded_tautologies": (8, [(1, 2, 3)] + [(i, -i, 1) for i in range(4, 9)]),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    variants = {
        "EXPLICIT": decide_explicit,
        "INLINE": decide_inline,
        "FUSED": decide_fused,
        "DISPATCH": decide_dispatch,
        "TABLE": decide_table,
    }
    rows = []
    for name, (n, raw_clauses) in cases().items():
        clauses = tuple(tuple(c) for c in raw_clauses)
        case_rows = {}
        for variant, fn in variants.items():
            case_rows[variant] = asdict(fn(n, clauses))
        answers = {v["answer"] for v in case_rows.values()}
        assert len(answers) == 1, (name, answers)
        assert case_rows["EXPLICIT"]["host_api_calls"] > 0
        for variant in ("INLINE", "FUSED", "DISPATCH", "TABLE"):
            assert case_rows[variant]["host_api_calls"] == 0
        assert case_rows["EXPLICIT"]["literal_tests"] == case_rows["INLINE"]["literal_tests"]
        assert case_rows["DISPATCH"]["guest_logical_calls"] > 0
        rows.append({
            "case": name,
            "variables": n,
            "clauses": len(clauses),
            "answer": answers.pop(),
            "variants": case_rows,
        })
    payload = {
        "experiment": "API-CALL-FLATTENING-AUDIT1",
        "status": "COMPUTATIONAL",
        "claim": "named host extractor-call count is not invariant under semantics-preserving program transformations",
        "cases": rows,
        "checks": {
            "answer_agreement": len(rows) * len(variants),
            "zero_host_call_variants": len(rows) * 4,
            "positive_explicit_calls": len(rows),
            "dispatch_preserves_guest_events": len(rows),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_digest"] = hashlib.sha256(canonical).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(rows), "variants": len(variants), "sha256": payload["sha256_without_digest"]}))


if __name__ == "__main__":
    main()
