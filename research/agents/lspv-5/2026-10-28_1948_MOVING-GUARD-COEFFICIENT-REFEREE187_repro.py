#!/usr/bin/env python3
"""Finite controls for MOVING-GUARD-COEFFICIENT-REFEREE187.

This validates the standard existential 3-CNF chain compiler for a boundary
truth table and records its exact clause/auxiliary growth.  It does not claim
that the direct table compiler is representation-optimal.
"""
from __future__ import annotations

import itertools as it
import json
import math
import random


def clause_value(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def compile_long_clause(literals, next_var):
    """Existentially equivalent proper exact-3-CNF; returns clauses,next_var."""
    k = len(literals)
    assert k >= 3 and len({abs(x) for x in literals}) == k
    if k == 3:
        return [tuple(literals)], next_var
    auxiliaries = list(range(next_var, next_var + k - 3))
    out = [(literals[0], literals[1], auxiliaries[0])]
    for j in range(1, k - 3):
        out.append((-auxiliaries[j - 1], literals[j + 1], auxiliaries[j]))
    out.append((-auxiliaries[-1], literals[-2], literals[-1]))
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in out)
    return out, next_var + k - 3


def existential_cnf_value(clauses, base_assignment, aux_vars):
    for bits in it.product((False, True), repeat=len(aux_vars)):
        assignment = dict(base_assignment)
        assignment.update(dict(zip(aux_vars, bits)))
        if all(clause_value(c, assignment) for c in clauses):
            return True
    return False


def validate_clause_compiler(max_width=9):
    assertions = 0
    rows = []
    for w in range(3, max_width + 1):
        literals = tuple(range(1, w + 1))
        clauses, nv = compile_long_clause(literals, w + 1)
        aux = list(range(w + 1, nv))
        for bits in it.product((False, True), repeat=w):
            base = {i + 1: bits[i] for i in range(w)}
            expected = any(bits)
            actual = existential_cnf_value(clauses, base, aux)
            assert expected == actual
            assertions += 1
        rows.append({"width": w, "three_clauses": len(clauses),
                     "auxiliaries": len(aux), "assignments": 1 << w})
    return rows, assertions


def relation_clauses(w, truth_bits):
    """One width-w clause for each forbidden boundary assignment."""
    assert len(truth_bits) == 1 << w
    out = []
    for mask, allowed in enumerate(truth_bits):
        if allowed:
            continue
        # The clause is false exactly at mask.
        out.append(tuple(-(i + 1) if (mask >> i) & 1 else (i + 1)
                         for i in range(w)))
    return out


def validate_random_relations(seed=18720261028):
    rng = random.Random(seed)
    assertions = 0
    records = []
    for w in range(3, 9):
        for rep in range(12):
            truth = [bool(rng.getrandbits(1)) for _ in range(1 << w)]
            clauses = relation_clauses(w, truth)
            for mask in range(1 << w):
                assignment = {i + 1: bool((mask >> i) & 1) for i in range(w)}
                actual = all(clause_value(c, assignment) for c in clauses)
                assert actual == truth[mask]
                assertions += 1
            # Independently validate the exact-3-CNF existential replacement
            # for every long clause, one clause at a time.
            for long_clause in clauses:
                compiled, nv = compile_long_clause(long_clause, w + 1)
                aux = list(range(w + 1, nv))
                forbidden = tuple(lit < 0 for lit in long_clause)
                base = {i + 1: forbidden[i] for i in range(w)}
                assert not existential_cnf_value(compiled, base, aux)
                assertions += 1
                if w <= 7:
                    # Flip each input once; the long clause and its compiler
                    # must become satisfiable.
                    for i in range(w):
                        changed = dict(base)
                        changed[i + 1] = not changed[i + 1]
                        assert existential_cnf_value(compiled, changed, aux)
                        assertions += 1
            records.append({"width": w, "rep": rep,
                            "allowed": sum(truth), "forbidden": len(clauses)})
    return records, assertions


def direct_guard_counts(w, forbidden):
    assert w >= 3
    return {
        "width": w,
        "forbidden_rows": forbidden,
        "three_clauses": forbidden * (w - 2),
        "auxiliaries": forbidden * (w - 3),
        "literal_occurrences": 3 * forbidden * (w - 2),
    }


def coefficient_ledger():
    rows = []
    for m in (20, 40, 80, 160):
        N = 1 << m
        for alpha in (0.25, 0.5, 0.75, 1.0):
            w = max(3, math.ceil(alpha * m))
            forbidden = 1 << (w - 1)  # half of the table forbidden
            c = direct_guard_counts(w, forbidden)
            # Count literal records; canonical bit encoding adds only
            # logarithmic factors, represented as an o(1) exponent here.
            effective = math.log2(max(1, c["literal_occurrences"])) / m
            rows.append({"log2_N": m, "alpha": alpha, "width": w,
                         "log2_direct_literal_records_over_log2_N": effective})
    return rows


def physical_dimacs_sizes():
    rows = []
    for w in range(3, 15):
        forbidden = 1 << (w - 1)
        next_var = w + 1
        clauses = []
        # Deterministic half-table: forbid masks with parity zero.
        for mask in range(1 << w):
            if mask.bit_count() & 1:
                continue
            long_clause = tuple(-(i + 1) if (mask >> i) & 1 else i + 1
                                for i in range(w))
            part, next_var = compile_long_clause(long_clause, next_var)
            clauses.extend(part)
        assert len(clauses) == forbidden * (w - 2)
        lines = [f"p cnf {next_var - 1} {len(clauses)}"]
        lines += [" ".join(map(str, c)) + " 0" for c in clauses]
        payload = "\n".join(lines) + "\n"
        rows.append({"width": w, "forbidden": forbidden,
                     "variables": next_var - 1, "clauses": len(clauses),
                     "physical_bits": 8 * len(payload)})
    return rows


def main():
    clause_rows, a1 = validate_clause_compiler()
    relation_rows, a2 = validate_random_relations()
    result = {
        "run_id": "MOVING-GUARD-COEFFICIENT-REFEREE187",
        "status": "PASS",
        "seed": 18720261028,
        "clause_compiler": clause_rows,
        "random_relations": relation_rows,
        "coefficient_ledger": coefficient_ledger(),
        "physical_dimacs": physical_dimacs_sizes(),
        "assertions": a1 + a2,
        "symbolic_guard_bound": "O(w*2^w*log(N+2^w)) bits plus retained source",
        "limitations": [
            "The direct truth-table compiler is an upper construction, not a representation lower bound.",
            "Finite truth-table tests do not prove asymptotic optimality.",
            "Python/RAM execution is not a native tape-machine measurement.",
            "A logarithmic boundary without its coefficient and retained-source size does not certify power shrinkage.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
