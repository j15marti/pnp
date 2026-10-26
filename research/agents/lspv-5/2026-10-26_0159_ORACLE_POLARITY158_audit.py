#!/usr/bin/env python3
"""Finite audit for ORACLE-POLARITY158.

Checks the exact equivalence between positive-witness-only transcript
soundness and monotonicity for fixed nonadaptive SAT-query vectors.  It also
constructs a proper-3CNF one-query counterexample for an UNSAT decider.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


Literal = int
Clause = tuple[Literal, ...]
CNF = tuple[Clause, ...]


def unit3(lit: int, a: int, b: int) -> CNF:
    """Four proper ternary clauses equivalent to the literal lit."""
    return tuple(
        (lit, sa * a, sb * b)
        for sa, sb in itertools.product((1, -1), repeat=2)
    )


def sat_models(cnf: CNF) -> list[tuple[int, ...]]:
    n = max(abs(lit) for clause in cnf for lit in clause)
    models = []
    for bits in itertools.product((0, 1), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in cnf):
            models.append(bits)
    return models


def proper(cnf: CNF) -> bool:
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in cnf)


def monotone_truth_table(table: int, k: int) -> bool:
    """Whether f(a)<=f(x) whenever a is coordinatewise <= x."""
    for a in range(1 << k):
        if not ((table >> a) & 1):
            continue
        for x in range(1 << k):
            if a & ~x == 0 and not ((table >> x) & 1):
                return False
    return True


def positive_only_sound(table: int, k: int) -> bool:
    """Soundness when claimed 1 bits are checked and claimed 0 bits are free."""
    for actual in range(1 << k):
        actual_accept = (table >> actual) & 1
        if actual_accept:
            continue
        for claimed in range(1 << k):
            yes_claims_true = claimed & ~actual == 0
            claimed_accept = (table >> claimed) & 1
            if yes_claims_true and claimed_accept:
                return False
    return True


def main() -> None:
    assertions = 0
    rows = []
    expected_dedekind = {1: 3, 2: 6, 3: 20, 4: 168}
    for k in range(1, 5):
        safe = 0
        total = 1 << (1 << k)
        for table in range(total):
            a = monotone_truth_table(table, k)
            b = positive_only_sound(table, k)
            assert a == b
            assertions += 1
            safe += int(a)
        assert safe == expected_dedekind[k]
        assertions += 1
        rows.append(
            {
                "queries": k,
                "all_acceptance_functions": total,
                "positive_only_sound_functions": safe,
                "unsafe_functions": total - safe,
            }
        )

    # Ordinary proper-3CNF depth-one polarity counterexample.
    f_sat = unit3(1, 2, 3)
    f_unsat = unit3(1, 2, 3) + unit3(-1, 4, 5)
    assert proper(f_sat) and proper(f_unsat)
    assertions += 2
    sat_count = len(sat_models(f_sat))
    unsat_count = len(sat_models(f_unsat))
    assert sat_count == 4
    assert unsat_count == 0
    assertions += 2

    # The correct oracle machine accepts UNSAT iff SAT(F)=0.
    actual_sat_answer = 1
    actual_unsat_answer = 0
    assert 1 - actual_sat_answer == 0
    assert 1 - actual_unsat_answer == 1
    assertions += 2

    # A forged claimed-NO transcript has no YES witness to check.
    claimed_answer = 0
    positive_checks_pass = True
    forged_accepts_unsat = 1 - claimed_answer == 1
    assert positive_checks_pass and forged_accepts_unsat
    assertions += 1
    # Full answer checking rejects it on the SAT source and accepts on UNSAT.
    assert claimed_answer != actual_sat_answer
    assert claimed_answer == actual_unsat_answer
    assertions += 2

    result = {
        "marker": "ORACLE_POLARITY158",
        "assertions": assertions,
        "failures": 0,
        "monotonicity_rows": rows,
        "proper_3cnf_counterexample": {
            "sat_formula_clauses": len(f_sat),
            "sat_formula_models": sat_count,
            "unsat_formula_clauses": len(f_unsat),
            "unsat_formula_models": unsat_count,
            "oracle_machine": "query SAT(F); accept UNSAT iff answer is NO",
            "forged_transcript": "claim NO on the SAT formula",
            "positive_witness_checks": 0,
            "positive_only_verifier_accepts_forgery": True,
            "full_answer_verifier_rejects_forgery": True,
        },
        "interpretation": (
            "Checking witnesses only for claimed SAT answers is sound exactly for "
            "upward-monotone acceptance predicates in the fixed nonadaptive model. "
            "The canonical one-query UNSAT predicate is antimonotone, so an unproved "
            "claimed-NO answer makes the transcript verifier unsound."
        ),
    }
    out = Path(__file__).with_name(
        "2026-10-26_0159_ORACLE_POLARITY158_results.json"
    )
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
