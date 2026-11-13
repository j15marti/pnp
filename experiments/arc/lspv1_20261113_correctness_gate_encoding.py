#!/usr/bin/env python3
"""Finite sanity checks for the strict 3-CNF encoding G_q.
Not a formal verification of Godel incompleteness.
"""
import json
from itertools import product

def encode(bits):
    if not bits or any(c not in "01" for c in bits):
        raise ValueError("Expected nonempty binary proof-code string")
    clauses = []
    for i, bit in enumerate(bits):
        a, b = 2 * i + 2, 2 * i + 3
        clauses.append((1, a, b if bit == "0" else -b))
    return tuple(clauses)

def decode(clauses):
    if not clauses:
        return None
    bits = []
    for i, clause in enumerate(clauses):
        a, b = 2 * i + 2, 2 * i + 3
        if len(clause) != 3 or clause[0] != 1 or clause[1] != a:
            return None
        if clause[2] == b:
            bits.append("0")
        elif clause[2] == -b:
            bits.append("1")
        else:
            return None
    return "".join(bits)

def is_strict_3cnf(clauses):
    return all(len(c) == 3 and len(set(map(abs, c))) == 3
               and all(x != 0 for x in c) for c in clauses)

def eval_cnf(clauses, assignment):
    return all(any((assignment.get(abs(x), False) if x > 0
                    else not assignment.get(abs(x), False)) for x in c)
               for c in clauses)

def main():
    checked = 0
    for m in range(1, 9):
        for tup in product("01", repeat=m):
            q = "".join(tup)
            F = encode(q)
            assert is_strict_3cnf(F)
            assert decode(F) == q
            assert eval_cnf(F, {1: True})
            checked += 1
    negatives = (
        (), ((1, 2, 2),), ((1, 2, 99),),
        ((-1, 2, 3),), ((1, 2, -3), (1, 4, 99))
    )
    assert all(decode(F) is None for F in negatives)
    print(json.dumps({
        "result_type": "finite_encoding_regression_only",
        "bit_lengths": list(range(1, 9)),
        "strict_3cnf_roundtrip_and_explicit_sat_witness_checks": checked,
        "malformed_range_controls_rejected": len(negatives),
        "symbolic_claim": "G_q is satisfiable by z=true and carries q in b_i sign",
        "limitations": "Finite tests do not establish unprovability or consistency"
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
