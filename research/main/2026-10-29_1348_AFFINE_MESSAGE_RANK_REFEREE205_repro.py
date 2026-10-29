#!/usr/bin/env python3
"""AFFINE-MESSAGE-RANK-REFEREE205 finite controls.

The symbolic theorem is in the paired LaTeX report.  This program independently
checks the relation recognizers, primitive-positive closure controls, GF(2)
rank accumulation, essential-row parity stars, and random mixed local cases.
It is dependency-free and deterministic; no finite check is promoted to an
unrestricted SAT theorem.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path

SEED = 202610291348


def gf2_basis(rows):
    pivots = {}
    for value in rows:
        v = int(value)
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return tuple(pivots[p] for p in sorted(pivots, reverse=True))


def gf2_rank(rows):
    return len(gf2_basis(rows))


def consistent(equations, n):
    coeff = [m for m, _ in equations]
    aug = [m | (b << n) for m, b in equations]
    return gf2_rank(coeff) == gf2_rank(aug)


def span(rows):
    basis = gf2_basis(rows)
    out = {0}
    for v in basis:
        out |= {x ^ v for x in tuple(out)}
    return out


def parity(mask, value):
    return (mask & value).bit_count() & 1


def affine_info(arity, relation):
    """Return exact affine equations or None; empty is an inconsistent system."""
    rel = set(map(int, relation))
    if any(x < 0 or x >= (1 << arity) for x in rel):
        raise ValueError("relation row outside arity")
    if not rel:
        return {"empty": True, "dimension": -1, "equations": [(0, 1)]}
    anchor = min(rel)
    basis = gf2_basis(x ^ anchor for x in rel)
    points = {anchor ^ v for v in span(basis)}
    if points != rel:
        return None
    orthogonal = []
    for mask in range(1, 1 << arity):
        if all(parity(mask, v) == 0 for v in basis):
            orthogonal.append(mask)
    equation_masks = gf2_basis(orthogonal)
    equations = [(m, parity(m, anchor)) for m in equation_masks]
    assert all(all(parity(m, x) == b for m, b in equations) for x in rel)
    reconstructed = {
        x for x in range(1 << arity)
        if all(parity(m, x) == b for m, b in equations)
    }
    assert reconstructed == rel
    return {
        "empty": False,
        "dimension": len(basis),
        "codimension": len(equations),
        "equations": equations,
    }


def majority(a, b, c):
    return (a & b) | (a & c) | (b & c)


def is_bijunctive(relation):
    rel = set(relation)
    return all(majority(a, b, c) in rel for a in rel for b in rel for c in rel)


def clause_holds(clause, assignment):
    return any(((assignment >> var) & 1) == sign for var, sign in clause)


def random_2cnf(rng, n, count):
    clauses = []
    for _ in range(count):
        width = rng.randrange(1, min(2, n) + 1)
        vars_ = rng.sample(range(n), width)
        clauses.append(tuple((v, rng.randrange(2)) for v in vars_))
    return clauses


def project_2cnf(n, clauses, kept):
    relation = set()
    for assignment in range(1 << n):
        if all(clause_holds(c, assignment) for c in clauses):
            row = sum(((assignment >> v) & 1) << i for i, v in enumerate(kept))
            relation.add(row)
    return relation


def exhaustive_relation_counts():
    rows = []
    total = 0
    for arity in range(4):
        universe = list(range(1 << arity))
        affine = bijunctive = both = 0
        for selector in range(1 << len(universe)):
            rel = {x for x in universe if selector >> x & 1}
            a = affine_info(arity, rel) is not None
            b = is_bijunctive(rel)
            affine += a
            bijunctive += b
            both += a and b
            total += 1
        rows.append({"arity": arity, "relations": 1 << len(universe),
                     "affine": affine, "bijunctive": bijunctive, "both": both})
    assert rows[-1]["bijunctive"] == 166
    assert rows[2]["bijunctive"] == 16
    return rows, total


def pp_bijunctive_controls(rng, trials=500):
    checked = 0
    for _ in range(trials):
        n = rng.randrange(1, 7)
        clauses = random_2cnf(rng, n, rng.randrange(0, 2 * n + 3))
        kept = tuple(sorted(rng.sample(range(n), rng.randrange(n + 1))))
        rel = project_2cnf(n, clauses, kept)
        assert is_bijunctive(rel)
        checked += 1
    return checked


def affine_recognizer_controls(rng, trials=800):
    affine_ok = nonaffine_rejected = 0
    for _ in range(trials):
        arity = rng.randrange(0, 9)
        anchor = rng.randrange(1 << arity) if arity else 0
        generators = [rng.randrange(1 << arity) for _ in range(rng.randrange(arity + 2))]
        rel = {anchor ^ v for v in span(generators)}
        info = affine_info(arity, rel)
        assert info is not None
        affine_ok += 1
        candidates = set(range(1 << arity)) - rel
        if candidates and rel:
            mutated = set(rel)
            mutated.add(rng.choice(tuple(candidates)))
            if affine_info(arity, mutated) is None:
                nonaffine_rejected += 1
    return affine_ok, nonaffine_rejected


def parity_star(h, beta):
    """h disjoint odd-parity edge messages plus their centre sum row."""
    children = []
    for j in range(h):
        mask = 0b111 << (3 * j)
        children.append((mask, 1))
    center_mask = 0
    for mask, _ in children:
        center_mask ^= mask
    equations = children + [(center_mask, beta)]
    n = 3 * h
    coeff_rank = gf2_rank(m for m, _ in equations)
    aug_rank = gf2_rank(m | (b << n) for m, b in equations)
    sat = coeff_rank == aug_rank
    expected = beta == (h & 1)
    assert sat == expected
    essential = None
    if not sat:
        essential = all(consistent(equations[:j] + equations[j + 1 :], n)
                        for j in range(h))
        assert essential
    brute = None
    if h <= 4:
        brute = any(all(parity(m, x) == b for m, b in equations)
                    for x in range(1 << n))
        assert brute == sat
    return {
        "h": h,
        "variables": n,
        "edge_width": 3,
        "per_edge_affine_codimension": 1,
        "aggregate_coefficient_rank": coeff_rank,
        "augmented_rank": aug_rank,
        "beta": beta,
        "sat": sat,
        "expected_sat": expected,
        "every_child_essential_when_unsat": essential,
        "bruteforce_checked": brute is not None,
    }


def star_controls():
    out = []
    for h in (1, 2, 3, 4, 8, 16, 32, 64):
        for beta in (0, 1):
            out.append(parity_star(h, beta))
    # Same tiny edge language, but independent messages accumulate linear rank.
    assert all(x["aggregate_coefficient_rank"] == x["h"] for x in out)
    return out


def overlapping_controls():
    # Arbitrarily many identical odd-parity messages share one separator.
    rows = []
    for copies in (1, 2, 4, 8, 16, 64):
        equations = [(0b111, 1)] * copies
        rows.append({"copies": copies, "union_width": 3,
                     "sum_edge_widths": 3 * copies,
                     "aggregate_rank": gf2_rank(m for m, _ in equations)})
    assert all(r["aggregate_rank"] == 1 for r in rows)
    return rows


def mixed_rank_controls(rng, trials=600):
    """Check that the charged exponent uses combined independent row rank."""
    rows = []
    for _ in range(trials):
        n = rng.randrange(1, 11)
        original = [(rng.randrange(1 << n), rng.randrange(2))
                    for _ in range(rng.randrange(0, 5))]
        child_groups = []
        for _ in range(rng.randrange(0, 7)):
            child_groups.append([(rng.randrange(1 << n), rng.randrange(2))
                                 for _ in range(rng.randrange(0, 4))])
        child = [row for group in child_groups for row in group]
        e = gf2_rank(m for m, _ in original)
        combined = gf2_rank(m for m, _ in original + child)
        rho = combined - e
        assert 0 <= rho <= sum(gf2_rank(m for m, _ in g) for g in child_groups)
        rows.append((e, rho, combined))
    return {
        "trials": trials,
        "max_original_rank": max(e for e, _, _ in rows),
        "max_incremental_child_rank": max(r for _, r, _ in rows),
        "max_combined_rank": max(c for _, _, c in rows),
        "identity_checks": sum(c == e + r for e, r, c in rows),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rng = random.Random(SEED)
    relation_rows, relation_total = exhaustive_relation_counts()
    affine_ok, rejected = affine_recognizer_controls(rng)
    result = {
        "run_id": "AFFINE-MESSAGE-RANK-REFEREE205",
        "status": {
            "symbolic": "PROVED/EXACT restricted theorem in paired report",
            "finite": "COMPUTATIONAL exhaustive/random controls",
            "unrestricted_sat": "OPEN",
        },
        "seed": SEED,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "relation_exhaustion": {"total_relations": relation_total, "by_arity": relation_rows},
        "affine_recognizer": {"affine_cosets_accepted": affine_ok,
                              "one_point_mutations_rejected": rejected},
        "bijunctive_pp_projection_trials": pp_bijunctive_controls(rng),
        "parity_stars": star_controls(),
        "overlapping_affine_messages": overlapping_controls(),
        "mixed_rank_accounting": mixed_rank_controls(rng),
        "limitations": [
            "Finite controls do not establish all-input decomposition coverage.",
            "The parity star is pure affine and Gaussian-elimination easy.",
            "Rank growth falsifies only a constant-aggregate-rank extension, not all SAT algorithms.",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "all_assertions_passed": True,
        "relations": relation_total,
        "pp_trials": result["bijunctive_pp_projection_trials"],
        "star_cases": len(result["parity_stars"]),
        "max_star_rank": max(x["aggregate_coefficient_rank"] for x in result["parity_stars"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
