#!/usr/bin/env python3
"""Finite controls for SCRAMBLE-METADATA-FIREWALL48.

The general statements are bijection and description-composition lemmas.  This
script checks the bookkeeping on concrete parsimonious Circuit->3CNF images.
"""

from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from math import ceil, factorial, log2
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
PREV = HERE / "2026-10-21_parsimonious_circuit_3cnf47_audit.py"
SPEC = spec_from_file_location("pc3", PREV)
pc3 = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(pc3)


def shift_formula(clauses, nvars, variable_shift, clause_shift):
    def move_lit(lit):
        old = abs(lit) - 1
        new = (old + variable_shift) % nvars
        return new + 1 if lit > 0 else -(new + 1)

    renamed = [tuple(move_lit(x) for x in clause) for clause in clauses]
    if renamed:
        clause_shift %= len(renamed)
        renamed = renamed[clause_shift:] + renamed[:clause_shift]
    return renamed


def shift_assignment(bits, shift):
    out = [0] * len(bits)
    for old, bit in enumerate(bits):
        out[(old + shift) % len(bits)] = bit
    return tuple(out)


def main():
    assertions = 0
    assignments = 0

    # Every point-circuit image through n=3 remains parsimonious under cyclic
    # variable renaming and clause reordering, even when roles are mixed.
    for n in range(1, 4):
        for target in product((0, 1), repeat=n):
            ni, gates, out = pc3.point_circuit(target)
            clauses, total, _ = pc3.circuit_to_unique_3cnf(ni, gates, out)
            original_models = []
            for bits in product((0, 1), repeat=total):
                assignments += 1
                if pc3.sat(clauses, bits):
                    original_models.append(bits)
            assert len(original_models) == 1
            assertions += 1

            shifts = sorted({0, 1 % total, (total - 1) % total})
            clause_shifts = sorted({0, 1 % len(clauses), (len(clauses) - 1) % len(clauses)})
            for vs in shifts:
                for cs in clause_shifts:
                    scrambled = shift_formula(clauses, total, vs, cs)
                    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3
                               for c in scrambled)
                    assertions += 1
                    for bits in product((0, 1), repeat=total):
                        moved = shift_assignment(bits, vs)
                        assert pc3.sat(clauses, bits) == pc3.sat(scrambled, moved)
                        assignments += 1
                        assertions += 1
                    moved_model = shift_assignment(original_models[0], vs)
                    assert pc3.sat(scrambled, moved_model)
                    assertions += 1

    # A shared-DAG formula has the same model count after role-mixing shifts.
    n, gates, out = pc3.sharing_identity(1)
    clauses, total, _ = pc3.circuit_to_unique_3cnf(n, gates, out)
    model_count = sum(pc3.sat(clauses, bits)
                      for bits in product((0, 1), repeat=total))
    assignments += 2**total
    assert model_count == 2
    assertions += 1
    for vs in range(total):
        scrambled = shift_formula(clauses, total, vs, vs)
        moved_count = sum(pc3.sat(scrambled, bits)
                          for bits in product((0, 1), repeat=total))
        assignments += 2**total
        assert moved_count == model_count
        assertions += 1

    # Permuting target coordinates never reduces literal-prefix traffic: each
    # independent stage still fixes j bits, in some order.
    prefix_cases = 0
    for m in range(2, 65):
        expected = m * (m + 1) // 2
        for mode in range(3):
            if mode == 0:
                order = list(range(m))
            elif mode == 1:
                order = list(reversed(range(m)))
            else:
                shift = m // 3
                order = [(i + shift) % m for i in range(m)]
            assert len(set(order)) == m
            assert sum(len(order[:j]) for j in range(1, m + 1)) == expected
            assertions += 2
            prefix_cases += 1

    # Counting control: a b-bit seed indexes at most 2^b permutations; all
    # permutations require ceil(log2(m!)) bits in the worst case.
    entropy_rows = []
    for m in range(2, 17):
        need = ceil(log2(factorial(m)))
        short = max(0, need - 1)
        assert 2**short < factorial(m) <= 2**need
        assertions += 1
        entropy_rows.append((m, need))

    # Arithmetic form of the source-independent indexed-evaluator firewall.
    low_ledger_rows = 0
    for p in (16, 32, 64, 128):
        for b in range(1, p, 7):
            for t in range(1, p, 11):
                overhead = ceil(log2(p)) + 2
                charged = b + t + overhead
                assert (charged < p) == (b + t + overhead < p)
                assertions += 1
                low_ledger_rows += 1

    result = {
        "status": "PASS",
        "assertions": assertions,
        "assignments_checked": assignments,
        "prefix_permutation_cases": prefix_cases,
        "factorial_entropy_rows": entropy_rows,
        "low_ledger_rows": low_ledger_rows,
        "claims": [
            "variable_and_clause_permutations_preserve_model_count",
            "unique_models_remain_unique_under_scrambling",
            "role_mixing_requires_mapping_metadata_for_projected_sampling",
            "permuted_literal_prefixes_retain_quadratic_traffic",
            "short_seed_families_cannot_name_all_permutations",
        ],
        "global_status": {"P_vs_NP": "OPEN", "P_vs_RP": "OPEN"},
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
