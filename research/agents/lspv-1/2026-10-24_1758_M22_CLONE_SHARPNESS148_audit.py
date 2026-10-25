#!/usr/bin/env python3
"""Finite independent controls for M22-CLONE-SHARPNESS148.
The symbolic proof is in the adjacent LaTeX report. Pure Python stdlib.
No SAT machine-resource, FLMV bit-step or target recursive claim.
"""
import json
from itertools import combinations, product


def cycle_clauses(r):
    assert r >= 3
    return [
        clause
        for i in range(r)
        for clause in (
            ((i, False), ((i + 1) % r, True), ((i + 2) % r, True)),
            ((i, False), ((i + 1) % r, True), ((i + 2) % r, False)),
        )
    ]


def is_true(clause, word):
    return any(word[v] == sign for v, sign in clause)


def inspect(r):
    clauses = cycle_clauses(r)
    assert len(clauses) == 2 * r
    assert len(set(tuple(sorted(c)) for c in clauses)) == 2 * r
    assert all(len({v for v, _ in c}) == 3 for c in clauses)
    assert all((
        sum((j, True) in c for c in clauses),
        sum((j, False) in c for c in clauses)
    ) == (3, 3) for j in range(r))
    models = []
    for word in product((False, True), repeat=r):
        if all(is_true(c, word) for c in clauses):
            models.append("".join("1" if bit else "0" for bit in word))
    assert models == ["0" * r, "1" * r]

    near_constants = []
    for j in range(r):
        one_hot = [False] * r
        one_hot[j] = True
        one_cold = [True] * r
        one_cold[j] = False
        near_constants.extend((one_hot, one_cold))
    eligible_mixed = 0
    pure_tested = 0
    for triple in combinations(range(r), 3):
        for bits in product((False, True), repeat=3):
            c = tuple(zip(triple, bits))
            if all(bits) or not any(bits):
                pure_tested += 1
                if all(bits):
                    assert not is_true(c, [False] * r)
                else:
                    assert not is_true(c, [True] * r)
                continue
            eligible_mixed += 1
            assert is_true(c, [False] * r) and is_true(c, [True] * r)
            assert sum(not is_true(c, w) for w in near_constants) == 1
    return {
        "r": r, "clauses": 2 * r, "assignments_checked": 2 ** r,
        "models": models, "signed_degree_per_variable": [3, 3],
        "eligible_mixed_clauses_checked": eligible_mixed,
        "pure_monotone_clauses_checked": pure_tested,
    }


def main():
    records = [inspect(r) for r in range(3, 13)]
    large = []
    for r in (20, 50, 100):
        cs = cycle_clauses(r)
        assert len(cs) == 2 * r and len(set(tuple(sorted(c)) for c in cs)) == 2 * r
        assert all(is_true(c, [False] * r) and is_true(c, [True] * r) for c in cs)
        large.append({"r": r, "structural_checks_only": True})
    out = {
        "run": "M22-CLONE-SHARPNESS148", "seed": None,
        "scope": "proper ternary mixed-sign clone-only relation, NOT C_star",
        "assignments_total": sum(x["assignments_checked"] for x in records),
        "eligible_mixed_clauses_total": sum(x["eligible_mixed_clauses_checked"] for x in records),
        "pure_monotone_clauses_total": sum(x["pure_monotone_clauses_checked"] for x in records),
        "exhaustive_records": records, "large_structural_only": large,
        "failures": 0,
        "limitation": "finite relation checks only; no physical machine bit work, no SAT reduction"
    }
    assert out["assignments_total"] == 8184
    assert out["eligible_mixed_clauses_total"] == 4290
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
