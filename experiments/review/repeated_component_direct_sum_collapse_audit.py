#!/usr/bin/env python3
"""Finite audit for REPEATED-COMPONENT-SEMANTIC-DIRECT-SUM-COLLAPSE1.

This experiment compares semantic multiplication under variable-disjoint
repetition with a total exact wrapper that recognizes identical connected
components and invokes its base decider once.  It is a bounded falsification
test, not evidence for an asymptotic SAT upper or lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


Clause = tuple[int, ...]


@dataclass(frozen=True)
class Formula:
    name: str
    nvars: int
    clauses: tuple[Clause, ...]
    family: str


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def eval_formula(formula: Formula, mask: int) -> bool:
    return all(any(bool(mask & (1 << (abs(x) - 1))) == (x > 0)
                   for x in clause) for clause in formula.clauses)


def brute_decide_and_count(formula: Formula) -> tuple[bool, int, int]:
    count = 0
    checks = 0
    for mask in range(1 << formula.nvars):
        ok = True
        for clause in formula.clauses:
            checks += 1
            if not any(bool(mask & (1 << (abs(x) - 1))) == (x > 0)
                       for x in clause):
                ok = False
                break
        count += ok
    return count > 0, count, checks


def paired_graph(name: str, edges: tuple[tuple[int, int], ...]) -> Formula:
    clauses: list[Clause] = []
    for vertex in range(6):
        incident = tuple(i + 1 for i, edge in enumerate(edges) if vertex in edge)
        assert len(incident) == 3
        clauses.extend((incident, tuple(-x for x in incident)))
    return Formula(name, len(edges), tuple(clauses), "signed-clean-core")


def bases() -> list[Formula]:
    k33 = tuple((u, v) for u in range(3) for v in range(3, 6))
    return [
        Formula("2sat_cycle", 4,
                ((1, 2), (-1, 2), (-2, 3), (-3, 4), (-4, 1)), "2SAT"),
        Formula("horn_chain", 5,
                ((1,), (-1, 2), (-2, 3), (-3, 4), (-4, 5)), "Horn"),
        Formula("affine_tseitin_odd", 4,
                ((1, 2), (-1, -2), (2, 3), (-2, -3),
                 (3, 4), (-3, -4), (4, 1), (-4, -1), (1,), (-1,)),
                "affine/Tseitin"),
        Formula("bounded_treewidth_path", 6,
                ((1, 2), (-1, 2), (-2, 3), (-3, 4), (-4, 5), (-5, 6)),
                "bounded-treewidth"),
        paired_graph("paired_K33", k33),
    ]


def repeat(base: Formula, copies: int, reverse_encoding: bool = False) -> Formula:
    clauses: list[Clause] = []
    for block in range(copies):
        shifted = [tuple((1 if x > 0 else -1) * (abs(x) + block * base.nvars)
                         for x in clause) for clause in base.clauses]
        if reverse_encoding and block % 2:
            shifted = [tuple(reversed(c)) for c in reversed(shifted)]
        clauses.extend(shifted)
    return Formula(f"rep{copies}_{base.name}", copies * base.nvars,
                   tuple(clauses), base.family)


def incidence_components(formula: Formula) -> tuple[list[tuple[int, ...]], int]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    ops = 0
    for clause in formula.clauses:
        vs = sorted({abs(x) for x in clause})
        for v in vs:
            adjacency[v]
            ops += 1
        for a, b in zip(vs, vs[1:]):
            adjacency[a].add(b)
            adjacency[b].add(a)
            ops += 2
    components: list[tuple[int, ...]] = []
    unseen = set(range(1, formula.nvars + 1))
    while unseen:
        root = min(unseen)
        queue = deque([root])
        unseen.remove(root)
        part: list[int] = []
        while queue:
            v = queue.popleft()
            part.append(v)
            ops += 1
            for w in adjacency[v]:
                ops += 1
                if w in unseen:
                    unseen.remove(w)
                    queue.append(w)
        components.append(tuple(sorted(part)))
    return components, ops


def normalize_component(formula: Formula, variables: tuple[int, ...]) -> tuple[tuple[Clause, ...], int]:
    rank = {v: i + 1 for i, v in enumerate(variables)}
    varset = set(variables)
    clauses: list[Clause] = []
    ops = 0
    for clause in formula.clauses:
        if abs(clause[0]) not in varset:
            continue
        norm = tuple(sorted(((1 if x > 0 else -1) * rank[abs(x)] for x in clause),
                            key=lambda x: (abs(x), x < 0)))
        clauses.append(norm)
        ops += len(clause) + 1
    return tuple(sorted(clauses)), ops


def recognize_repetition(formula: Formula) -> tuple[bool, int, int, Formula | None]:
    components, ops = incidence_components(formula)
    if not components:
        return False, 0, ops, None
    normalized: list[tuple[tuple[Clause, ...], int]] = []
    for component in components:
        cnf, nops = normalize_component(formula, component)
        normalized.append((cnf, len(component)))
        ops += nops
    first = normalized[0]
    for item in normalized[1:]:
        ops += len(first[0]) + 1
        if item != first:
            return False, len(components), ops, None
    base = Formula("recognized_base", first[1], first[0], "recognized")
    return len(components) > 1, len(components), ops, base


def encoded_bits(formula: Formula) -> int:
    addr = max(1, math.ceil(math.log2(formula.nvars + 1)))
    lits = sum(map(len, formula.clauses))
    return 2 * addr + len(formula.clauses) + lits * (addr + 1)


def wrapper_answer(name: str, bit: bool) -> bool:
    if name in {"DIRECT", "COPY", "DELAY"}:
        return bit
    if name == "DEAD":
        return bit or False
    if name == "INTERP":
        return not (not bit)
    if name == "RECOMP":
        return bit and bit
    raise ValueError(name)


def audit() -> dict:
    start = time.perf_counter()
    rows = []
    assertions = 0
    for base in bases():
        answer, models, base_checks = brute_decide_and_count(base)
        for copies in (1, 2, 4, 8, 16):
            instance = repeat(base, copies, reverse_encoding=True)
            recognized, found, pre_ops, recovered = recognize_repetition(instance)
            if copies == 1:
                assertions += 1
                assert not recognized and found == 1
            else:
                assertions += 2
                assert recognized and found == copies and recovered is not None
                rec_answer, rec_models, rec_checks = brute_decide_and_count(recovered)
                assert rec_answer == answer and rec_models == models
            for wrapper in WRAPPERS:
                assertions += 1
                assert wrapper_answer(wrapper, answer) == answer
            semantic_models = models ** copies
            rows.append({
                "family": base.family,
                "base": base.name,
                "copies": copies,
                "variables": instance.nvars,
                "clauses": len(instance.clauses),
                "encoded_bits": encoded_bits(instance),
                "satisfiable": answer,
                "base_model_count": models,
                "semantic_product_model_count": semantic_models,
                "semantic_product_log2": None if semantic_models == 0 else math.log2(semantic_models),
                "recognizer_succeeded": recognized,
                "components_found": found,
                "preprocessing_ops": pre_ops,
                "base_decider_calls": 1,
                "base_solver_clause_checks": base_checks,
                "naive_independent_solve_calls": copies,
                "compatibility_extraction_calls": 0,
                "witness_reconstruction_calls": 0,
                "decision_output_bits": 1,
                "wrappers_checked": list(WRAPPERS),
            })

    # Hostile controls: nonidentical product and redundancy break recognition,
    # so a total wrapper falls back to its exact underlying decider.
    bs = bases()
    a, b = bs[0], bs[1]
    b_shift = repeat(b, 1)
    shifted_b = tuple(tuple((1 if x > 0 else -1) * (abs(x) + a.nvars)
                            for x in c) for c in b_shift.clauses)
    nonidentical = Formula("nonidentical_product", a.nvars + b.nvars,
                           a.clauses + shifted_b, "independent-product-control")
    redundant = Formula("redundant_clause_control", a.nvars,
                        a.clauses + (a.clauses[0],) * 5, "redundant-clauses")
    controls = []
    for formula in (nonidentical, redundant):
        recognized, found, pre_ops, _ = recognize_repetition(formula)
        answer, models, checks = brute_decide_and_count(formula)
        assertions += 1
        assert not recognized
        controls.append({"name": formula.name, "family": formula.family,
                         "recognizer_succeeded": recognized, "components_found": found,
                         "preprocessing_ops": pre_ops, "fallback_decider_calls": 1,
                         "fallback_clause_checks": checks, "satisfiable": answer,
                         "model_count": models})

    # Exact affine Gaussian-elimination control: x1=x2=x3=x4 plus x1=1,x1=0.
    rows_matrix = [(0b0011, 0), (0b0110, 0), (0b1100, 0), (0b1001, 0),
                   (0b0001, 1), (0b0001, 0)]
    rank = 0
    inconsistent = False
    pivots: dict[int, tuple[int, int]] = {}
    gf2_ops = 0
    for mask, rhs in rows_matrix:
        while mask:
            p = mask.bit_length() - 1
            gf2_ops += 1
            if p not in pivots:
                pivots[p] = (mask, rhs)
                rank += 1
                break
            pm, pr = pivots[p]
            mask ^= pm
            rhs ^= pr
            gf2_ops += 1
        if mask == 0 and rhs:
            inconsistent = True
    assertions += 1
    assert inconsistent

    elapsed = time.perf_counter() - start
    return {
        "status": "COMPUTATIONAL",
        "scope": "finite repeated-component falsification audit; no asymptotic extrapolation",
        "rows": rows,
        "hostile_controls": controls,
        "affine_gaussian_control": {"rank_before_conflict": rank,
                                    "inconsistent": inconsistent,
                                    "gf2_row_ops": gf2_ops},
        "assertions": assertions,
        "elapsed_seconds": elapsed,
        "max_python_invocation_seconds_rule": "single invocation measured below 30 seconds",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"assertions": result["assertions"],
                      "elapsed_seconds": result["elapsed_seconds"],
                      "rows": len(result["rows"]),
                      "status": result["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
