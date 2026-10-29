#!/usr/bin/env python3
"""Independent finite check of ARC225's high-h, codim-one source family.
No SAT solver and no complexity lower bound. Full polynomial selector is in
ARC225_one_parity_interface_audit.py in the complete reproducibility bundle.
"""
from itertools import combinations, product
import json


def xor_quartet(scope, rhs=0):
    return [tuple((i + 1) if bit == 0 else -(i + 1)
                  for i, bit in zip(scope, bits))
            for bits in product((0, 1), repeat=3)
            if sum(bits) % 2 != rhs]


def clauses_true(clauses, assignment):
    return all(any(((assignment >> (abs(lit)-1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses)


def source(k, pin=None):
    assert k >= 3
    aux = list(range(k, 2*k-3))
    if k == 3:
        triples = [(0, 1, 2)]
    else:
        triples = [(0, 1, aux[0])]
        triples += [(aux[j-2], j, aux[j-1]) for j in range(2, k-2)]
        triples.append((aux[-1], k-2, k-1))
    assert len(triples) == k-2
    parity_blocks = [xor_quartet(triple) for triple in triples]
    binary = [(-(i+1), -(j+1)) for i, j in combinations(range(k), 2)]
    all_clauses = [c for group in parity_blocks for c in group] + binary
    if pin is not None:
        all_clauses += [(-i,) for i in range(1, k)]
        all_clauses.append((k if pin else -k,))
    return 2*k-3, triples, parity_blocks, binary, all_clauses


def audit():
    pointwise = 0
    projected = 0
    for k in range(3, 9):
        n, triples, blocks, binary, source_clauses = source(k)
        assert n == 2*k-3
        for triple, block in zip(triples, blocks):
            assert len(block) == 4 and len(set(block)) == 4
            for a in range(1 << n):
                expected = sum((a >> v) & 1 for v in triple) % 2 == 0
                assert clauses_true(block, a) == expected
                pointwise += 1
        projected_forms = {
            a & ((1 << k)-1) for a in range(1 << n)
            if clauses_true([clause for group in blocks for clause in group], a)
        }
        assert projected_forms == {
            a for a in range(1 << k) if a.bit_count() % 2 == 0
        }
        assert len(projected_forms) == (1 << (k-1))
        # A single nontrivial parity dependency, hence delta=1; no coloop.
        assert all(any((a >> i) & 1 for a in projected_forms)
                   for i in range(k))
        assert clauses_true(source_clauses, 0)
        for pin, satisfiable in [(0, True), (1, False)]:
            n2, _, _, _, fixed_clauses = source(k, pin)
            assert any(clauses_true(fixed_clauses, a)
                       for a in range(1 << n2)) == satisfiable
            # Each subsystem is satisfiable regardless of combined answer.
            quartets = [clause for group in blocks for clause in group]
            assert any(clauses_true(quartets, a)
                       for a in range(1 << n2))
            assert any(clauses_true(binary + fixed_clauses[len(quartets)+len(binary):], a)
                       for a in range(1 << n2))
        projected += 1
    # Two individually feasible linear constraints may be jointly infeasible.
    B = [(1, 2)]
    assert any(clauses_true(B, a) and (a & 1) == 0 for a in range(4))
    assert any(clauses_true(B, a) and (a & 2) == 0 for a in range(4))
    assert not any(clauses_true(B, a) and a == 0 for a in range(4))
    out = {'status':'PASS','projected_chain_sizes':projected,
           'source_quartet_pointwise_checks':pointwise,
           'two_parity_counterexample':'PASS',
           'scope':'finite k=3..8; full proof and solver in separate files'}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == '__main__':
    audit()
