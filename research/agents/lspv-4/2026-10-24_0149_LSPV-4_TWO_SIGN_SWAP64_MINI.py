#!/usr/bin/env python3
"""TWO-SIGN-SWAP64. Stdlib-only exact replay of the signed source and fixed witness.

Run from repository root:
  python research/agents/lspv-4/2026-10-24_0149_LSPV-4_TWO_SIGN_SWAP64_MINI.py

The UNSAT label of the 198/264 original is imported from independently
verified DOECKER-CORE-CERT61. This script does not reprove that certificate.
"""
import ast
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ORIGINAL = Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
WITNESS_HEX = "39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598"
N = 198
M = 264


def load_source():
    body = "\n".join(
        line for line in ORIGINAL.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )
    return [tuple(map(int, c)) for c in ast.literal_eval(body)]


def validated_formula(clauses):
    assert len(clauses) == M
    assert all(len(c) == 3 and len(set(abs(l) for l in c)) == 3 for c in clauses)
    assert max(abs(l) for c in clauses for l in c) == N
    assert len(set(clauses)) == M
    counts = Counter(l for c in clauses for l in c)
    assert all(counts[x] == 2 and counts[-x] == 2 for x in range(1, N + 1))
    return True


def repair(clauses):
    result = [list(c) for c in clauses]
    assert tuple(result[3]) == (-2, -3, -194)
    assert tuple(result[13]) == (3, 9, 10)
    result[3][1] = 3
    result[13][0] = -3
    return [tuple(c) for c in result]


def clause_satisfied(clause, assignment):
    return any(assignment[abs(l)] == (l > 0) for l in clause)


def swap_graph_diameter():
    vertices = tuple(combinations(range(4), 2))
    def distance(a, b):
        return 2 - len(set(a) & set(b))
    return max(distance(a, b) for a in vertices for b in vertices)


def main():
    source = load_source()
    target = repair(source)
    assert validated_formula(source)
    assert validated_formula(target)
    assert all(
        tuple(abs(l) for l in source[i]) ==
        tuple(abs(l) for l in target[i])
        for i in range(M)
    )
    differences = [
        (i, j, source[i][j], target[i][j])
        for i in range(M) for j in range(3)
        if source[i][j] != target[i][j]
    ]
    assert differences == [(3, 1, -3, 3), (13, 0, 3, -3)]
    bitstring = format(int(WITNESS_HEX, 16), "0198b")
    assert len(bitstring) == 198
    assignment = {i + 1: bit == "1" for i, bit in enumerate(bitstring)}
    assert assignment[3] and assignment[9]
    rejected_old = [i for i, c in enumerate(source)
                    if not clause_satisfied(c, assignment)]
    rejected_new = [i for i, c in enumerate(target)
                    if not clause_satisfied(c, assignment)]
    assert rejected_old == [3] and rejected_new == []
    assert swap_graph_diameter() == 2
    assert 4 * N == 3 * M
    w = (64 * (N + M + 1) - 1).bit_length()
    assert w == 15
    assert (4 * M + 2) * w == 15870
    products = []
    for p in (1, 2, 4, 8, 16, 32):
        n, m = N * p, M * p
        width = (64 * (n + m + 1) - 1).bit_length()
        products.append({
            "p": p,
            "source_variables": n,
            "ternary_clauses": m,
            "input_bits": (4 * m + 2) * width,
            "minimum_addressed_word_probes_on_all_sat": p,
        })
    result = {
        "status": "COMPUTATIONAL source/witness replay, with imported UNSAT certificate",
        "source_path": str(ORIGINAL),
        "n": N,
        "m": M,
        "word_width": w,
        "input_bits": 15870,
        "witness_hex": WITNESS_HEX,
        "witness_bits": len(bitstring),
        "source_unsatisfied_by_witness": rejected_old,
        "repaired_unsatisfied_by_witness": rejected_new,
        "difference_signed_literal_words": differences,
        "same_unsigned_clause_supports": True,
        "each_variable_occurs_2_positive_and_2_negative": True,
        "J_4_2_diameter": swap_graph_diameter(),
        "product_ledger": products,
        "unsat_provenance": "LSPV-2 DOECKER-CORE-CERT61 checked certificate (external dependency)",
        "checks_failed": 0
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
