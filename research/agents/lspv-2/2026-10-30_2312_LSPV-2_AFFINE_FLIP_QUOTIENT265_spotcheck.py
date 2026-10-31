#!/usr/bin/env python3
"""Independent compact source-level checks for LSPV-2 AFFINE-FLIP-QUOTIENT265.
Python standard library; no import from the producer. These checks are a subset
of the full independent 31,335-assertion verifier in the dated archive.
"""
from itertools import product

XOR_SOURCE = [
    (1, 3, -4), (1, -3, 4), (-1, 3, 4), (-1, -3, -4),
    (2, 3, -4), (2, -3, 4), (-2, 3, 4), (-2, -3, -4),
]
C8, C9 = (1, 5, 6), (-2, 7, 8)
UNITS = [(-5,), (-6,), (-7,), (-8,)]
# Source IDs 0..13, and a complete original-source 26-node resolution DAG.
SOURCE_UNSAT = XOR_SOURCE + [C8, C9] + UNITS
STEPS = [
    (14, 0, 7, 3, (1, -2, -4)),
    (15, 2, 5, 3, (-1, 2, 4)),
    (16, 4, 3, 3, (-1, 2, -4)),
    (17, 6, 1, 3, (1, -2, 4)),
    (18, 15, 16, 4, (-1, 2)),
    (19, 17, 14, 4, (1, -2)),
    (20, 8, 10, 5, (1, 6)),
    (21, 20, 11, 6, (1,)),
    (22, 9, 12, 7, (-2, 8)),
    (23, 22, 13, 8, (-2,)),
    (24, 18, 21, 1, (2,)),
    (25, 24, 23, 2, ()),
]

def value(lit, assignment):
    return assignment[abs(lit)] if lit > 0 else not assignment[abs(lit)]

def true_count(clause, assignment):
    return sum(value(lit, assignment) for lit in clause)

def holds(formula, assignment):
    return all(true_count(c, assignment) > 0 for c in formula)

def assignments(n=8):
    for bits in product((False, True), repeat=n):
        yield {i + 1: bits[i] for i in range(n)}

def local_target(clause, mode):
    # This refers to ONE source variable per signed occurrence.
    return {abs(lit): (lit > 0) == (mode == "S") for lit in clause}

def check_resolution():
    seen = {i: frozenset(c) for i, c in enumerate(SOURCE_UNSAT)}
    for ident, left, right, pivot, expected in STEPS:
        a, b = seen[left], seen[right]
        assert (pivot in a and -pivot in b) or (-pivot in a and pivot in b)
        resolvent = (a | b) - {pivot, -pivot}
        assert frozenset(expected) == resolvent
        assert not any(-x in resolvent for x in resolvent)
        seen[ident] = resolvent
    assert seen[18] == frozenset((-1, 2))
    assert seen[19] == frozenset((1, -2))
    assert seen[25] == frozenset()
    return len(seen), len(STEPS)

def main():
    checks = 0
    for a in assignments(8):
        assert holds(XOR_SOURCE[:4], a) == (a[1] ^ a[3] ^ a[4] == False)
        assert holds(XOR_SOURCE[4:], a) == (a[2] ^ a[3] ^ a[4] == False)
        checks += 2
    modes = ["S", "U"]
    actual = {}
    for m in modes:
        for n in modes:
            t8, t9 = local_target(C8, m), local_target(C9, n)
            # They have disjoint syntactic variable supports, so all modes cohere.
            assert not (set(t8) & set(t9))
            actual[m + n] = any(
                holds(XOR_SOURCE, a) and
                all(a[k] == v for k, v in (t8 | t9).items())
                for a in assignments(8)
            )
    assert actual == {"SS": False, "SU": True, "US": True, "UU": False}
    unpinned = XOR_SOURCE + [C8, C9]
    yes = XOR_SOURCE + [C8, (2, 7, 8)] + UNITS
    no = SOURCE_UNSAT
    model_unpinned = next((a for a in assignments(8) if holds(unpinned, a)), None)
    model_yes = next((a for a in assignments(8) if holds(yes, a)), None)
    model_no = next((a for a in assignments(8) if holds(no, a)), None)
    assert model_unpinned and model_yes and model_no is None
    # Endpoint and complement category identity for ORIGINAL proper ternary clauses.
    for a in assignments(8):
        comp = {i: not v for i, v in a.items()}
        for c in unpinned:
            assert true_count(c, a) + true_count(c, comp) == 3
            checks += 1
    proof_nodes, steps = check_resolution()
    print({"status": "PASS", "coherent_assignments_checked": 256,
           "literal_count_complement_checks": checks,
           "conditioned_SS_SU_US_UU": actual,
           "SAT_original_witness": model_yes,
           "UNSAT_original_resolution_nodes": proof_nodes,
           "resolution_steps": steps})
if __name__ == "__main__":
    main()
