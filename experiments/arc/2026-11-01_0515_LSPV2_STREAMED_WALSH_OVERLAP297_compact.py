#!/usr/bin/env python3
"""Compact independently runnable finite certificate for LSPV-2 297.

These literal integer syndrome fixtures are extracted from the source-authenticated
producer and must NOT substitute for its acquisition/provenance proof.
Full source parser, producer, independently implemented verifier, exhaustive
Y6/F15 controls and U198/V198 source checks are in the ZIP archive.
The character identity itself is classical GF(2) orthogonality.
"""
from itertools import product
from math import prod

def signed_character_count(template_signatures, rhs, dimension):
    """Exact one-frequency-at-a-time Walsh sum, no exponential table."""
    assert 0 <= rhs < (1 << dimension)
    assert all(all(0 <= s < 1 << dimension for s in cycle)
               for cycle in template_signatures)
    numerator = 0
    factor_evaluations = 0
    max_absolute_term = 0
    for lam in range(1 << dimension):
        term = -1 if ((lam & rhs).bit_count() & 1) else 1
        for cycle in template_signatures:
            factor = 0
            for signature in cycle:
                factor += -1 if ((lam & signature).bit_count() & 1) else 1
                factor_evaluations += 1
            term *= factor
        max_absolute_term = max(max_absolute_term, abs(term))
        numerator += term
    denominator = 1 << dimension
    assert numerator % denominator == 0
    return {"count": numerator // denominator, "numerator": numerator,
            "denominator": denominator, "template_evaluations": factor_evaluations,
            "max_absolute_character_term": max_absolute_term}

def direct_template_count(cycles, rhs):
    return sum((sum(v) ^ rhs) == 0 for v in product(*cycles))

F9_POSITIVE = [(1,5,6),(2,3,8),(1,3,5),
               (4,6,9),(2,4,7),(7,8,9)]
F9_NEGATIVE = [(4,6,8),(1,6,7),(2,3,4),
               (3,5,8),(1,2,9),(5,7,9)]
F9_PIN = {8:0,3:0,7:0,6:0,1:1,5:1}

def f9_satisfied(assignment):
    return all(any(assignment[x] for x in clause) for clause in F9_POSITIVE) and \
           all(any(not assignment[x] for x in clause) for clause in F9_NEGATIVE)

def f9_models():
    all_models = 0
    pinned_models = 0
    for bits in product((0,1), repeat=9):
        assignment = dict(enumerate(bits, 1))
        if f9_satisfied(assignment):
            all_models += 1
            if all(assignment[v] == b for v,b in F9_PIN.items()):
                pinned_models += 1
    return all_models, pinned_models

def main():
    # Full projected coordinates from source-authenticated original-cycle rows.
    fixtures = [
      ("F9 UNSAT cube", [[3,6,2]], 7, 3, 0),
      ("F15 SAT cube", [[19,7,20],[3,2,2]], 5, 5, 2),
      ("K5 overlap SAT cube", [[7,18,2],[17,11,1]], 3, 5, 2),
    ]
    for name, cycles, rhs, dimension, expected in fixtures:
        result = signed_character_count(cycles, rhs, dimension)
        naive = direct_template_count(cycles, rhs)
        assert result["count"] == naive == expected, (name,result,naive)
        print(name, result)
    k5, rhs, _ = fixtures[2][1:4]
    missing_equality = [[s & 15 for s in cycle] for cycle in k5]
    assert signed_character_count(missing_equality, rhs, 4)["count"] == 4
    print("K5 OMIT OVERLAP EQUALITY: FALSE MODEL COUNT 4 vs CORRECT 2")
    assert f9_models() == (70,0)
    print("F9 ORIGINAL SOURCE: global models 70, six-pin cube 0")
    print("ALL COMPACT INDEPENDENT ASSERTIONS PASS; P vs NP OPEN")

if __name__ == "__main__":
    main()
