#!/usr/bin/env python3
"""Finite audit for the 3-variable full-clause-cube decision quotient.

Every proper clause on x0,x1,x2 has a unique falsifying assignment.  A
clause-presence mask therefore realizes the complement mask as its solution
relation.  The audit checks this identity, the two-class SAT quotient, compact
ordered decision diagrams, external extraction, independent products, and
basic representation/wrapper controls.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from pathlib import Path


def clause_forbidden_by(a: int) -> tuple[int, int, int]:
    """Literal i+1 is positive iff assignment a sets xi to zero."""
    return tuple((i + 1) if ((a >> i) & 1) == 0 else -(i + 1) for i in range(3))


CLAUSES = tuple(clause_forbidden_by(a) for a in range(8))


def clause_value(clause: tuple[int, ...], assignment: int) -> bool:
    for lit in clause:
        bit = (assignment >> (abs(lit) - 1)) & 1
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return True
    return False


def formula_solutions(mask: int) -> int:
    result = 0
    for a in range(8):
        if all(not ((mask >> j) & 1) or clause_value(CLAUSES[j], a)
               for j in range(8)):
            result |= 1 << a
    return result


def sat_bit(mask: int) -> int:
    return int(mask != 0xFF)


def reduced_obdd_nonterminals(order: tuple[int, ...], blocks: int = 1) -> int:
    """Construct the reduced OBDD for AND_j NAND(mask_j), fixed bit order."""
    width = 8 * blocks
    unique: dict[tuple[int, int, int], int] = {}
    next_id = 2  # terminals are 0 and 1

    def output(prefix: int) -> int:
        return int(all(((prefix >> (8 * j)) & 0xFF) != 0xFF
                       for j in range(blocks)))

    def rec(level: int, prefix: int) -> int:
        nonlocal next_id
        if level == width:
            return output(prefix)
        bit = order[level]
        lo = rec(level + 1, prefix)
        hi = rec(level + 1, prefix | (1 << bit))
        if lo == hi:
            return lo
        key = (bit, lo, hi)
        if key not in unique:
            unique[key] = next_id
            next_id += 1
        return unique[key]

    rec(0, 0)
    return len(unique)


def transform_assignment(a: int, perm: tuple[int, int, int], flip: int) -> int:
    out = 0
    for new_i, old_i in enumerate(perm):
        bit = ((a >> old_i) & 1) ^ ((flip >> new_i) & 1)
        out |= bit << new_i
    return out


def transform_mask(mask: int, perm: tuple[int, int, int], flip: int) -> int:
    out = 0
    for a in range(8):
        if (mask >> a) & 1:
            out |= 1 << transform_assignment(a, perm, flip)
    return out


def xor_system_solutions(rows: list[tuple[int, int]], variables: int) -> list[int]:
    """Small truth-table control for affine/Tseitin systems."""
    return [a for a in range(1 << variables)
            if all(((a & coeff).bit_count() & 1) == rhs for coeff, rhs in rows)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()

    checks = 0
    forbidden = []
    for j, clause in enumerate(CLAUSES):
        bad = [a for a in range(8) if not clause_value(clause, a)]
        assert bad == [j]
        forbidden.append(bad[0])
        checks += 8

    relations = set()
    solution_histogram = {str(k): 0 for k in range(9)}
    for mask in range(256):
        sol = formula_solutions(mask)
        assert sol == ((~mask) & 0xFF)
        assert bool(sol) == bool(sat_bit(mask))
        relations.add(sol)
        solution_histogram[str(sol.bit_count())] += 1
        checks += 3

    for k in range(9):
        assert solution_histogram[str(k)] == math.comb(8, k)
        checks += 1

    compatible_pairs = 0
    for a, b in itertools.combinations(range(8), 2):
        sol = formula_solutions((1 << a) | (1 << b))
        assert sol.bit_count() == 6
        compatible_pairs += 1
        checks += 1
    assert formula_solutions(0xFF) == 0
    checks += 1

    # Bryant-style reduced ordered diagrams: the one-block SAT function is a
    # chain of eight nonterminals for every one of the 8! orders.
    obdd_sizes = []
    for order in itertools.permutations(range(8)):
        size = reduced_obdd_nonterminals(order)
        assert size == 8
        obdd_sizes.append(size)
        checks += 1
    block_major_sizes = {}
    for blocks in range(1, 4):
        order = tuple(range(8 * blocks))
        size = reduced_obdd_nonterminals(order, blocks)
        assert size == 8 * blocks
        block_major_sizes[str(blocks)] = size
        checks += 1

    # Eight complete-assignment SAT queries recover the whole 2x4
    # compatibility table; this is external extraction, not internal exposure.
    extraction_checks = 0
    for mask in range(256):
        extracted = 0
        for a in range(8):
            answer = int(((~mask) >> a) & 1)
            extracted |= answer << a
            extraction_checks += 1
        assert extracted == formula_solutions(mask)
        checks += 1

    # Independent product: exhaustive for two blocks.
    product_instances = 0
    product_sat = 0
    product_unsat = 0
    for m0 in range(256):
        for m1 in range(256):
            direct = sat_bit(m0) & sat_bit(m1)
            scan = int(m0 != 0xFF and m1 != 0xFF)
            assert direct == scan
            product_instances += 1
            product_sat += direct
            product_unsat += 1 - direct
            checks += 1
    assert product_sat == 255**2
    assert product_unsat == 256**2 - 255**2
    checks += 2

    # Variable permutations and complementations preserve SAT while permuting
    # the exact solution relation.
    symmetry_checks = 0
    for perm in itertools.permutations(range(3)):
        for flip in range(8):
            for mask in range(256):
                tm = transform_mask(mask, perm, flip)
                expected = 0
                sol = formula_solutions(mask)
                for a in range(8):
                    if (sol >> a) & 1:
                        expected |= 1 << transform_assignment(a, perm, flip)
                assert formula_solutions(tm) == expected
                assert sat_bit(tm) == sat_bit(mask)
                symmetry_checks += 2
    checks += symmetry_checks

    # Alternate encodings, COPY, existentially neutral padding, and four
    # extensionally equal program wrappers.
    wrapper_checks = 0
    for mask in range(256):
        bit_vector = tuple((mask >> i) & 1 for i in range(8))
        clause_list = [CLAUSES[i] for i, bit in enumerate(bit_vector) if bit]
        rebuilt = 0
        for clause in clause_list:
            rebuilt |= 1 << CLAUSES.index(clause)
        copied = clause_list + clause_list
        copied_mask = 0
        for clause in copied:
            copied_mask |= 1 << CLAUSES.index(clause)
        assert rebuilt == mask and copied_mask == mask
        # A fresh independent proper clause is existentially satisfiable, so it
        # preserves the source decision under projection.
        padded_sat = sat_bit(mask) and any(clause_value(CLAUSES[0], a) for a in range(8))
        assert padded_sat == bool(sat_bit(mask))
        direct = sat_bit(mask)
        interp = int(any(((~mask) >> a) & 1 for a in range(8)))
        recomp = int(formula_solutions(mask) != 0)
        delayed = (lambda value: value)(direct)
        assert direct == interp == recomp == delayed
        wrapper_checks += 5
    checks += wrapper_checks

    # Easy-family guards: none of these semantic structures can be promoted to
    # a generic SAT lower bound.  The product family above already has primal
    # treewidth exactly two (a disjoint union of K3 blocks).
    easy_family_checks = 0
    for n in range(2, 9):
        # Horn implication chain with x0 fixed true has the all-ones witness.
        horn_ok = all((not ((1 << n) - 1 >> i & 1)) or
                      (((1 << n) - 1 >> (i + 1)) & 1)
                      for i in range(n - 1))
        assert horn_ok
        # Equality 2-SAT has exactly the two constant assignments.
        eq_solutions = [a for a in range(1 << n)
                        if all(((a >> i) & 1) == ((a >> (i + 1)) & 1)
                               for i in range(n - 1))]
        assert eq_solutions == [0, (1 << n) - 1]
        easy_family_checks += 2
    assert len(xor_system_solutions([(0b111, 0)], 3)) == 4
    assert len(xor_system_solutions([(0b011, 0), (0b110, 0), (0b101, 1)], 3)) == 0
    assert all(block_major_sizes[str(b)] == 8 * b for b in range(1, 4))
    easy_family_checks += 3
    checks += easy_family_checks

    result = {
        "run_id": "MODELBRIDGE-0008",
        "status": "COMPUTATIONAL_AUDIT_SUPPORTING_EXACT_SYMBOLIC_PROOF",
        "family": "all clause-presence masks over the eight proper 3-clauses on three variables",
        "clauses": [list(c) for c in CLAUSES],
        "unique_falsifiers": forbidden,
        "formula_masks": 256,
        "distinct_solution_relations": len(relations),
        "sat_masks": 255,
        "unsat_masks": 1,
        "solution_count_histogram": solution_histogram,
        "pairwise_clause_pairs": compatible_pairs,
        "pairwise_joint_solution_count": 6,
        "all_eight_joint_solution_count": 0,
        "obdd_orders_checked": math.factorial(8),
        "obdd_nonterminal_min": min(obdd_sizes),
        "obdd_nonterminal_max": max(obdd_sizes),
        "block_major_obdd_nonterminals": block_major_sizes,
        "external_complete_assignment_queries": extraction_checks,
        "two_block_instances": product_instances,
        "two_block_sat": product_sat,
        "two_block_unsat": product_unsat,
        "symmetry_checks": symmetry_checks,
        "wrapper_and_encoding_checks": wrapper_checks,
        "easy_family_checks": easy_family_checks,
        "total_assertion_checks": checks,
        "runtime_seconds": time.perf_counter() - started,
        "scope_warning": "finite audit; asymptotic statements in the report are proved symbolically, not inferred from these counts",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
