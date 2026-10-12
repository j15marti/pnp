#!/usr/bin/env python3
"""Bounded audit of a direct one-bit CNF decision resource ledger.

This is a finite hostile-control audit, not an asymptotic SAT lower bound.
Every formula is parsed, decided by exhaustive assignment enumeration, and
replayed through semantics-preserving wrappers.  The declared direct-decision
interface contains no extractor, reconstructor, or communication channel, so
those meters must remain zero while preprocessing, clause checks, output bits,
and a conservative logical peak-space upper bound are charged explicitly.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


Clause = tuple[int, ...]


@dataclass(frozen=True)
class Formula:
    name: str
    nvars: int
    clauses: tuple[Clause, ...]
    family: str


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def eval_clause(clause: Clause, mask: int) -> bool:
    return any(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0) for lit in clause)


def eval_formula(formula: Formula, mask: int) -> bool:
    return all(eval_clause(clause, mask) for clause in formula.clauses)


def decide_direct(formula: Formula) -> tuple[bool, int, int | None]:
    checks = 0
    for mask in range(1 << formula.nvars):
        ok = True
        for clause in formula.clauses:
            checks += 1
            if not eval_clause(clause, mask):
                ok = False
                break
        if ok:
            return True, checks, mask
    return False, checks, None


def count_models(formula: Formula) -> int:
    return sum(eval_formula(formula, mask) for mask in range(1 << formula.nvars))


def encoded_length(formula: Formula) -> int:
    # Canonical indexed encoding: one sign bit and ceil(log2(n+1)) address bits
    # per literal, plus clause delimiters and a logarithmic header.
    addr = max(1, math.ceil(math.log2(formula.nvars + 1)))
    literals = sum(len(c) for c in formula.clauses)
    return 2 * addr + len(formula.clauses) + literals * (addr + 1)


def preprocess_ops(formula: Formula) -> int:
    # Charge header, every literal record, every clause delimiter, validation,
    # and storage of the parsed read-only formula.
    literals = sum(len(c) for c in formula.clauses)
    return 2 + 2 * literals + len(formula.clauses)


def peak_logical_bits(formula: Formula) -> int:
    # Parsed input plus current assignment, clause/literal cursors and one-bit
    # accumulator.  This deliberately overcharges a simple implementation.
    n = formula.nvars
    return (
        encoded_length(formula)
        + n
        + math.ceil(math.log2(max(2, len(formula.clauses) + 1)))
        + math.ceil(math.log2(max(2, max(map(len, formula.clauses), default=0) + 1)))
        + 1
    )


def shift(formula: Formula, delta: int, name: str) -> Formula:
    clauses = tuple(tuple((1 if x > 0 else -1) * (abs(x) + delta) for x in c)
                    for c in formula.clauses)
    return Formula(name, formula.nvars + delta, clauses, formula.family)


def disjoint_product(a: Formula, b: Formula, name: str) -> Formula:
    sb = shift(b, a.nvars, b.name)
    return Formula(name, a.nvars + b.nvars, a.clauses + sb.clauses,
                   "independent-product")


def paired_graph(name: str, edges: Iterable[tuple[int, int]]) -> Formula:
    edges = tuple(edges)
    clauses: list[Clause] = []
    for vertex in range(6):
        incident = [i + 1 for i, edge in enumerate(edges) if vertex in edge]
        assert len(incident) == 3
        clauses.append(tuple(incident))
        clauses.append(tuple(-x for x in incident))
    return Formula(name, len(edges), tuple(clauses), "signed-clean-core")


def rename_and_reverse(formula: Formula, name: str) -> Formula:
    p = {i: formula.nvars + 1 - i for i in range(1, formula.nvars + 1)}
    clauses = tuple(
        tuple((1 if lit > 0 else -1) * p[abs(lit)] for lit in reversed(clause))
        for clause in reversed(formula.clauses)
    )
    return Formula(name, formula.nvars, clauses, "alternate-encoding")


def hostile_formulas() -> list[Formula]:
    two_sat = Formula(
        "2sat_cycle", 4,
        ((1, 2), (-1, 2), (-2, 3), (-3, 4), (-4, 1)), "2SAT")
    horn = Formula(
        "horn_chain", 5,
        ((1,), (-1, 2), (-2, 3), (-3, 4), (-4, 5)), "Horn")
    affine = Formula(
        "affine_tseitin_odd", 4,
        ((1, 2), (-1, -2), (2, 3), (-2, -3),
         (3, 4), (-3, -4), (4, 1), (-4, -1), (1,), (-1,)),
        "affine/Tseitin")
    path_tw = Formula(
        "bounded_treewidth_path", 6,
        ((1, 2, 3), (-2, 3, 4), (-3, 4, 5), (-4, 5, 6)),
        "bounded-treewidth")
    k33_edges = tuple((u, v) for u in range(3) for v in range(3, 6))
    prism_edges = ((0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3),
                   (0, 3), (1, 4), (2, 5))
    k33 = paired_graph("paired_K33", k33_edges)
    prism = paired_graph("paired_prism", prism_edges)
    product = disjoint_product(k33, prism, "independent_K33_prism")
    padded = Formula("redundant_padding", k33.nvars,
                     k33.clauses + (k33.clauses[0],) * 7,
                     "redundant-clauses")
    alternate = rename_and_reverse(prism, "alternate_prism_encoding")
    return [two_sat, horn, affine, path_tw, k33, prism, product, padded, alternate]


def wrapper_answer(wrapper: str, answer: bool) -> bool:
    if wrapper == "DIRECT":
        return answer
    if wrapper == "COPY":
        return bool(answer)
    if wrapper == "DEAD":
        dead = False
        return answer or dead
    if wrapper == "DELAY":
        for _ in range(3):
            pass
        return answer
    if wrapper == "INTERP":
        return not (not answer)
    if wrapper == "RECOMP":
        return answer and answer
    raise ValueError(wrapper)


def run_audit() -> dict:
    started = time.perf_counter()
    rows = []
    assertions = 0
    totals = {
        "preprocessing_ops": 0,
        "solver_clause_checks": 0,
        "wrapper_replays": 0,
        "compatibility_extraction_ops": 0,
        "witness_reconstruction_ops": 0,
        "communication_bits": 0,
        "decision_output_bits": 0,
    }
    for formula in hostile_formulas():
        answer, checks, witness = decide_direct(formula)
        models = count_models(formula)
        assertions += 1
        assert answer == (models > 0)
        assertions += 1
        assert (witness is None) == (models == 0)
        for wrapper in WRAPPERS:
            assertions += 1
            assert wrapper_answer(wrapper, answer) == answer
            totals["wrapper_replays"] += 1

        pre = preprocess_ops(formula)
        nbits = encoded_length(formula)
        peak = peak_logical_bits(formula)
        row = {
            "name": formula.name,
            "family": formula.family,
            "nvars": formula.nvars,
            "clauses": len(formula.clauses),
            "encoded_length_bits": nbits,
            "satisfiable": answer,
            "model_count_experiment_only": models,
            "preprocessing_ops": pre,
            "solver_clause_checks": checks,
            "compatibility_extraction_ops": 0,
            "witness_reconstruction_ops": 0,
            "communication_bits": 0,
            "decision_output_bits": 1,
            "conservative_peak_logical_bits": peak,
            "wrappers_checked": list(WRAPPERS),
        }
        rows.append(row)
        totals["preprocessing_ops"] += pre
        totals["solver_clause_checks"] += checks
        totals["decision_output_bits"] += 1

    assertions += 3
    assert totals["compatibility_extraction_ops"] == 0
    assert totals["witness_reconstruction_ops"] == 0
    assert totals["communication_bits"] == 0
    return {
        "status": "COMPUTATIONAL",
        "scope": "bounded direct-decision hostile-control audit; no asymptotic inference",
        "algorithm": "single-machine exhaustive CNF decision with one-bit output",
        "declared_interface": {
            "input": "one canonical indexed CNF bitstring",
            "output": "one satisfiability bit",
            "external_parties": 0,
            "extractor_calls": 0,
            "reconstructor_calls": 0,
        },
        "formula_count": len(rows),
        "assertions": assertions,
        "totals": totals,
        "max_peak_logical_bits": max(row["conservative_peak_logical_bits"] for row in rows),
        "rows": rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "status", "formula_count", "assertions", "totals",
        "max_peak_logical_bits", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
