#!/usr/bin/env python3
"""Exact finite audit for independent one/two-unknown Boolean CNF levels.

Standard library only. Enumerates every subset of the normalized non-tautological
clause types (8 one-variable inputs, 512 two-variable inputs). Direct assignment
evaluation is the oracle. Presence-DNF terms and shortest source cores are checked
independently. This is not a native parser, time lower-bound, or proof-kernel test.

Run: python boolean_static_audit.py > boolean_static_results.json
"""

from collections import Counter
from itertools import combinations, product
import hashlib
import json
from pathlib import Path


def clause_true(clause, assignment):
    return any(assignment[abs(literal) - 1] == int(literal > 0)
               for literal in clause)


def satisfiable(indices, clauses, variable_count):
    return any(all(clause_true(clauses[i][1], assignment) for i in indices)
               for assignment in product((0, 1), repeat=variable_count))


def check_level(variable_count, clauses, expected_terms):
    expected_terms = {frozenset(term) for term in expected_terms}
    observed_terms = set()
    histogram = Counter()
    unsat_count = 0
    for subset in range(1 << len(clauses)):
        indices = tuple(i for i in range(len(clauses)) if subset & (1 << i))
        names = {clauses[i][0] for i in indices}
        unsat = not satisfiable(indices, clauses, variable_count)
        dnf = any(term <= names for term in expected_terms)
        assert dnf == unsat, (variable_count, subset, names)
        if not unsat:
            continue
        unsat_count += 1
        minimum = next(size for size in range(1, len(indices) + 1)
                       if any(not satisfiable(core, clauses, variable_count)
                              for core in combinations(indices, size)))
        assert minimum == min(map(len, (term for term in expected_terms
                                        if term <= names)))
        histogram[minimum] += 1
        if all(satisfiable(tuple(j for j in indices if j != i), clauses,
                           variable_count) for i in indices):
            observed_terms.add(frozenset(names))
    assert observed_terms == expected_terms
    minimal_cores = sorted((sorted(term) for term in observed_terms),
                           key=lambda term: (len(term), term))
    return {
        "unknown_variables": variable_count,
        "clause_types": [{"name": name, "literals": list(clause)}
                         for name, clause in clauses],
        "all_clause_type_subsets": 1 << len(clauses),
        "unsat_subsets": unsat_count,
        "sat_subsets": (1 << len(clauses)) - unsat_count,
        "minimal_core_counts": dict(sorted(Counter(map(len, minimal_cores)).items())),
        "minimum_core_size_distribution": dict(sorted(histogram.items())),
        "minimal_cores": minimal_cores,
    }


def main():
    one = [("E", ()), ("Px", (1,)), ("Nx", (-1,))]
    one_terms = [("E",), ("Px", "Nx")]
    two = [("E", ()), ("Px", (1,)), ("Nx", (-1,)),
           ("Py", (2,)), ("Ny", (-2,)), ("B00", (1, 2)),
           ("B01", (1, -2)), ("B10", (-1, 2)), ("B11", (-1, -2))]
    two_terms = [
        ("E",), ("Px", "Nx"), ("Py", "Ny"),
        ("Px", "Py", "B11"), ("Px", "Ny", "B10"),
        ("Nx", "Py", "B01"), ("Nx", "Ny", "B00"),
        ("Px", "B10", "B11"), ("Nx", "B00", "B01"),
        ("Py", "B01", "B11"), ("Ny", "B00", "B10"),
        ("B00", "B01", "B10", "B11"),
    ]
    result = {
        "status": "PASS",
        "scope": "Exact normalized Boolean clause-type subsets for r=1,2; direct truth evaluation versus presence DNF and minimum source-clause core.",
        "not_tested": ["Native formula/assignment normalization", "Raw encoded input access", "Machine resource exponents", "Unrestricted lower bounds", "Formal proof kernel", "Strict T_q templates"],
        "seed": None,
        "deterministic_exhaustive": True,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "levels": [check_level(1, one, one_terms), check_level(2, two, two_terms)],
    }
    assert result["levels"][0]["unsat_subsets"] == 5
    assert result["levels"][1]["unsat_subsets"] == 417
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
