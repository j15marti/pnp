#!/usr/bin/env python3
"""Exact audit for the Fano signed-NAE equality and linear-port compiler."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Lit:
    var: int
    neg: int = 0


Clause = tuple[Lit, Lit, Lit]


def nae(values: tuple[int, int, int]) -> bool:
    return not (values[0] == values[1] == values[2])


def clause_sat(clause: Clause, assignment: int) -> bool:
    vals = tuple(((assignment >> lit.var) & 1) ^ lit.neg for lit in clause)
    return nae(vals)


def fano_equal(a: int, b: int, first_aux: int) -> list[Clause]:
    u1, u2, u3, u4, u5 = range(first_aux, first_aux + 5)
    return [
        (Lit(a), Lit(b, 1), Lit(u1, 1)),
        (Lit(a), Lit(u2), Lit(u3)),
        (Lit(a), Lit(u4, 1), Lit(u5, 1)),
        (Lit(b), Lit(u2), Lit(u4, 1)),
        (Lit(b), Lit(u3), Lit(u5, 1)),
        (Lit(u1), Lit(u2, 1), Lit(u5)),
        (Lit(u1), Lit(u3, 1), Lit(u4)),
    ]


def fano_local_audit() -> dict:
    clauses = fano_equal(0, 1, 2)
    supports = [set(l.var for l in c) for c in clauses]
    intersections = [len(supports[i] & supports[j]) for i in range(7) for j in range(i)]
    occurrences = Counter(l.var for c in clauses for l in c)
    rows = []
    witnesses = {}
    for a, b in itertools.product((0, 1), repeat=2):
        row_witnesses = []
        for z in range(32):
            assignment = a | (b << 1) | (z << 2)
            if all(clause_sat(c, assignment) for c in clauses):
                row_witnesses.append([(z >> i) & 1 for i in range(5)])
        rows.append({"a": a, "b": b, "count": len(row_witnesses)})
        witnesses[f"{a}{b}"] = row_witnesses
    assert [r["count"] for r in rows] == [5, 0, 0, 5]
    assert set(intersections) == {1}
    assert set(occurrences.values()) == {3}
    return {
        "rows": rows,
        "witnesses": witnesses,
        "pairwise_support_intersections": intersections,
        "variable_occurrences": dict(sorted(occurrences.items())),
    }


def build_linear_compiler(source: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]):
    """Return clauses, variable count, and bookkeeping for a proper 3-CNF.

    Each source literal is (variable_id, negation_bit).  Isolated source
    variables are omitted by definition; n is the number appearing in source.
    """
    next_var = 0
    occurrence_vars: dict[int, list[int]] = defaultdict(list)
    per_clause_occurrences: list[list[Lit]] = []
    for source_clause in source:
        local = []
        for src_var, neg in source_clause:
            occ = next_var
            next_var += 1
            occurrence_vars[src_var].append(occ)
            local.append(Lit(occ, neg))
        per_clause_occurrences.append(local)

    gauge_vars = list(range(next_var, next_var + len(source)))
    next_var += len(source)
    clauses: list[Clause] = []
    frontend_u = []
    for i, (l1, l2, l3) in enumerate(per_clause_occurrences):
        u = next_var
        next_var += 1
        frontend_u.append(u)
        clauses.append((l1, l2, Lit(u)))
        clauses.append((Lit(u, 1), l3, Lit(gauge_vars[i])))

    equality_edges: list[tuple[str, int, int]] = []
    for src_var, copies in sorted(occurrence_vars.items()):
        for left, right in zip(copies, copies[1:]):
            equality_edges.append((f"x{src_var}", left, right))
    for left, right in zip(gauge_vars, gauge_vars[1:]):
        equality_edges.append(("g", left, right))

    for _, left, right in equality_edges:
        clauses.extend(fano_equal(left, right, next_var))
        next_var += 5

    return {
        "clauses": clauses,
        "nvars": next_var,
        "nsource": len(occurrence_vars),
        "m": len(source),
        "occurrence_vars": occurrence_vars,
        "gauge_vars": gauge_vars,
        "frontend_u": frontend_u,
        "equality_edges": equality_edges,
    }


def source_sat(source, source_assignment: int) -> bool:
    for clause in source:
        if not any(((source_assignment >> var) & 1) ^ neg for var, neg in clause):
            return False
    return True


def h_value(source, source_assignment: int) -> int:
    total = 0
    for clause in source:
        values = [((source_assignment >> var) & 1) ^ neg for var, neg in clause]
        total += int(values[0] != values[1] and values[2] == 1)
    return total


def compiler_audit(source, exhaustive_target: bool) -> dict:
    built = build_linear_compiler(source)
    clauses = built["clauses"]
    supports = [set(l.var for l in c) for c in clauses]
    max_intersection = max((len(supports[i] & supports[j]) for i in range(len(clauses)) for j in range(i)), default=0)
    occurrences = Counter(l.var for c in clauses for l in c)
    n, m = built["nsource"], built["m"]
    edges = len(built["equality_edges"])
    assert edges == 4 * m - n - 1
    assert built["nvars"] == 25 * m - 5 * n - 5
    assert len(clauses) == 30 * m - 7 * n - 7
    assert max_intersection <= 1
    assert max(occurrences.values(), default=0) <= 7

    expected = 0
    source_models = 0
    for assignment in range(1 << n):
        if source_sat(source, assignment):
            source_models += 1
            expected += 2 * (5 ** edges) * (2 ** h_value(source, assignment))

    observed = None
    if exhaustive_target:
        observed = 0
        for assignment in range(1 << built["nvars"]):
            if all(clause_sat(c, assignment) for c in clauses):
                observed += 1
        assert observed == expected
    return {
        "n": n,
        "m": m,
        "target_variables": built["nvars"],
        "target_clauses": len(clauses),
        "equality_gadgets": edges,
        "source_models": source_models,
        "expected_target_models": expected,
        "observed_target_models": observed,
        "max_support_intersection": max_intersection,
        "max_variable_occurrence": max(occurrences.values(), default=0),
    }


def main() -> None:
    local = fano_local_audit()
    formulas = [
        [((0, 0), (1, 0), (2, 0))],
        [((0, 0), (1, 0), (2, 0)), ((3, 1), (4, 0), (5, 1))],
        [((0, 0), (1, 1), (2, 0)), ((0, 1), (3, 0), (4, 1))],
    ]
    rows = [compiler_audit(f, exhaustive_target=True) for f in formulas]
    payload = {
        "run_id": "FANO-LINEAR-PORT27",
        "status": "PASS",
        "local_gadget": local,
        "compiler_rows": rows,
        "limitations": [
            "The audit proves signed-NAE semantics and Boolean-port incidence only.",
            "The actual FTNC matching/fold-state specification remains unavailable.",
            "Linearity and PC degree do not imply unrestricted SAT runtime lower bounds.",
        ],
    }
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload["script_sha256"] = script_hash
    out = Path("FANO_LINEAR_PORT27_results.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
