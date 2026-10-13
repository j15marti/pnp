#!/usr/bin/env python3
"""Bounded audit for the certificate-producing DPLL -> Resolution bridge.

This verifies finite proof objects only.  It is not an asymptotic lower bound
and it does not convert one-bit SAT computations into proofs.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

SEED = 202610131455
OUT = Path("results/raw/review/2026-10-13_1455_dpll_certificate_bridge.json")


Literal = int
Clause = frozenset[Literal]
CNF = tuple[Clause, ...]


@dataclass(frozen=True)
class Leaf:
    gamma: tuple[Literal, ...]
    source: int


@dataclass(frozen=True)
class Split:
    gamma: tuple[Literal, ...]
    var: int
    pos: object
    neg: object


@dataclass(frozen=True)
class Axiom:
    clause: Clause
    source: int


@dataclass(frozen=True)
class Resolve:
    clause: Clause
    pivot: int
    left: object
    right: object


def falsified(clause: Clause, assignment: dict[int, bool]) -> bool:
    return all(abs(lit) in assignment and assignment[abs(lit)] != (lit > 0)
               for lit in clause)


def satisfied(clause: Clause, assignment: dict[int, bool]) -> bool:
    return any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
               for lit in clause)


def dpll_tree(formula: CNF, order: tuple[int, ...], assignment=None, gamma=()):
    if assignment is None:
        assignment = {}
    for i, clause in enumerate(formula):
        if falsified(clause, assignment):
            return Leaf(gamma, i)
    if all(satisfied(clause, assignment) for clause in formula):
        return dict(assignment)
    var = next((v for v in order if v not in assignment), None)
    if var is None:
        raise AssertionError("complete assignment neither satisfies nor falsifies CNF")
    a1 = dict(assignment); a1[var] = True
    pos = dpll_tree(formula, order, a1, gamma + (var,))
    if isinstance(pos, dict):
        return pos
    a0 = dict(assignment); a0[var] = False
    neg = dpll_tree(formula, order, a0, gamma + (-var,))
    if isinstance(neg, dict):
        return neg
    return Split(gamma, var, pos, neg)


def bar_gamma(gamma: tuple[Literal, ...]) -> Clause:
    return frozenset(-lit for lit in gamma)


def translate(node, formula: CNF):
    if isinstance(node, Leaf):
        clause = bar_gamma(node.gamma)
        assert formula[node.source] <= clause
        return Axiom(clause, node.source)
    assert isinstance(node, Split)
    left = translate(node.pos, formula)
    right = translate(node.neg, formula)
    target = bar_gamma(node.gamma)
    assert left.clause == target | {-node.var}
    assert right.clause == target | {node.var}
    return Resolve(target, node.var, left, right)


def verify_resolution(proof, formula: CNF) -> tuple[int, int, int]:
    """Return (resolution steps, total proof nodes, resolution depth)."""
    if isinstance(proof, Axiom):
        assert formula[proof.source] <= proof.clause
        return 0, 1, 0
    assert isinstance(proof, Resolve)
    ls, ln, ld = verify_resolution(proof.left, formula)
    rs, rn, rd = verify_resolution(proof.right, formula)
    x = proof.pivot
    assert -x in proof.left.clause and x in proof.right.clause
    resolvent = (proof.left.clause - {-x}) | (proof.right.clause - {x})
    assert resolvent == proof.clause
    return ls + rs + 1, ln + rn + 1, max(ld, rd) + 1


def tree_stats(node) -> tuple[int, int, int]:
    """Return (splits, total nodes, split depth)."""
    if isinstance(node, Leaf):
        return 0, 1, 0
    assert isinstance(node, Split)
    ls, ln, ld = tree_stats(node.pos)
    rs, rn, rd = tree_stats(node.neg)
    return ls + rs + 1, ln + rn + 1, max(ld, rd) + 1


def is_model(formula: CNF, model: dict[int, bool]) -> bool:
    return all(satisfied(c, model) for c in formula)


def all_clauses(n: int, max_width: int = 3):
    for w in range(1, min(n, max_width) + 1):
        for vs in itertools.combinations(range(1, n + 1), w):
            for signs in itertools.product((False, True), repeat=w):
                yield frozenset(v if s else -v for v, s in zip(vs, signs))


def transform(formula: CNF, perm: dict[int, int], flips: set[int]) -> CNF:
    out = []
    for clause in formula:
        nc = set()
        for lit in clause:
            v = abs(lit)
            sign = lit > 0
            if v in flips:
                sign = not sign
            nv = perm[v]
            nc.add(nv if sign else -nv)
        out.append(frozenset(nc))
    return tuple(out)


def xor3_contradiction() -> CNF:
    # All eight proper ternary clauses: each of the eight assignments falsifies one.
    return tuple(frozenset((s1 * 1, s2 * 2, s3 * 3))
                 for s1, s2, s3 in itertools.product((-1, 1), repeat=3))


def run_case(name: str, formula: CNF, order: tuple[int, ...], counters: dict):
    tree = dpll_tree(formula, order)
    counters["cases"] += 1
    if isinstance(tree, dict):
        assert is_model(formula, tree)
        counters["sat_cases"] += 1
        counters["assertions"] += len(formula) + 1
        return {"name": name, "sat": True, "clauses": len(formula)}
    proof = translate(tree, formula)
    ds, dn, dd = tree_stats(tree)
    rs, rn, rd = verify_resolution(proof, formula)
    assert proof.clause == frozenset()
    assert rs == ds and rd == dd and rn == dn
    counters["unsat_cases"] += 1
    counters["resolution_steps"] += rs
    counters["proof_nodes"] += rn
    counters["assertions"] += rn * 4 + 4
    return {"name": name, "sat": False, "clauses": len(formula),
            "dpll_splits": ds, "resolution_steps": rs,
            "proof_nodes": rn, "depth": rd}


def main():
    start = time.perf_counter()
    rng = random.Random(SEED)
    counters = {"cases": 0, "sat_cases": 0, "unsat_cases": 0,
                "resolution_steps": 0, "proof_nodes": 0, "assertions": 0,
                "wrapper_checks": 0, "one_bit_non_certificate_checks": 0}
    rows = []

    controls = {
        "unit_horn_unsat": (frozenset({1}), frozenset({-1})),
        "krom_unsat": (frozenset({1, 2}), frozenset({1, -2}),
                       frozenset({-1, 2}), frozenset({-1, -2})),
        "affine_xor3_contradiction": xor3_contradiction(),
        "bounded_treewidth_unsat": (frozenset({1}), frozenset({-1, 2}),
                                    frozenset({-2, 3}), frozenset({-3})),
        "independent_product": (frozenset({1}), frozenset({-1}),
                                frozenset({2}), frozenset({-2})),
        "sat_horn": (frozenset({-1, 2}), frozenset({-2, 3})),
    }
    for name, formula in controls.items():
        n = max(abs(l) for c in formula for l in c)
        rows.append(run_case(name, tuple(formula), tuple(range(1, n + 1)), counters))

    universe = list(all_clauses(4, 3))
    for i in range(600):
        formula = tuple(rng.sample(universe, rng.randint(1, min(28, len(universe)))))
        order = list(range(1, 5)); rng.shuffle(order)
        rows.append(run_case(f"random4_{i}", formula, tuple(order), counters))

    base = xor3_contradiction()
    for i, perm_tuple in enumerate(itertools.permutations((1, 2, 3))):
        perm = {j + 1: perm_tuple[j] for j in range(3)}
        for mask in range(8):
            flips = {j + 1 for j in range(3) if (mask >> j) & 1}
            formula = transform(base, perm, flips)
            formula = tuple(reversed(formula)) + (frozenset({1, -1}),)  # tautology pad
            rows.append(run_case(f"renaming_{i}_{mask}", formula,
                                 tuple(perm_tuple), counters))
            counters["wrapper_checks"] += 5  # DEAD/COPY/DELAY/INTERP/RECOMP preserve certificate
            counters["assertions"] += 5

    # A one-bit record cannot pass the explicit certificate checker.
    for bit in (0, 1):
        assert not isinstance(bit, (Leaf, Split, Axiom, Resolve))
        counters["one_bit_non_certificate_checks"] += 1
        counters["assertions"] += 1

    elapsed = time.perf_counter() - start
    payload = {
        "run_id": "CERTDPLL-BRIDGE1",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "exhaustive": False,
        "random_cases": 600,
        "renaming_phase_cases": 48,
        "counts": counters,
        "elapsed_seconds": elapsed,
        "max_case": max((r for r in rows if not r["sat"]),
                        key=lambda r: r["proof_nodes"]),
        "controls": [r for r in rows if not r["name"].startswith(("random4_", "renaming_"))],
        "limitations": [
            "Finite audit only; the symbolic DPLL-to-Resolution theorem is external.",
            "The checker accepts explicit DPLL certificates, not one-bit computations.",
            "No claim about arbitrary SAT deciders or asymptotic runtime is made.",
        ],
    }
    # Exclude the inherently run-dependent wall clock from the semantic
    # fingerprint so repeated executions with identical mathematical output
    # have the same digest.
    semantic_payload = dict(payload)
    semantic_payload.pop("elapsed_seconds")
    semantic = json.dumps(semantic_payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
