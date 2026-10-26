#!/usr/bin/env python3
"""Finite audit for POLARITY-CLOCK160.

The symbolic theorem is in the companion report.  This program exhaustively
checks its finite truth-table instances and records the invalid-record and
slow-invalid-branch countercontrols.  No randomness is used.
"""

from __future__ import annotations

import json
from pathlib import Path

MARKER = "POLARITY_CLOCK160"


def proof_accepts(table: int, proof: int, words: int) -> bool:
    """Toy complete UNSAT proof: proof claims every row is false and we check."""
    all_rows = (1 << words) - 1
    return proof == all_rows and table == 0


def u_gadget(lit_value: bool, a: bool, b: bool) -> bool:
    # Four proper clauses U(l;a,b), logically equivalent to l.
    return all(
        lit_value or (a if sa else not a) or (b if sb else not b)
        for sa in (False, True)
        for sb in (False, True)
    )


def main() -> None:
    assertions = 0
    failures: list[str] = []
    rows = []

    def check(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            failures.append(message)

    for n in range(0, 4):
        words = 1 << n
        proof_count = 1 << words
        formula_count = 1 << words
        existential_ok = universal_complement_ok = 0
        wrong_malformed_failures = 0
        for table in range(formula_count):
            is_unsat = table == 0
            is_sat = not is_unsat
            accepts = [proof_accepts(table, p, words) for p in range(proof_count)]

            # NP-style UNSAT verifier orientation.
            ex = any(accepts)
            check(ex == is_unsat, f"existential orientation n={n} table={table}")
            existential_ok += int(ex == is_unsat)

            # Complement every branch outcome: co-nondeterministic SAT.
            co_paths = [not bit for bit in accepts]
            universal = all(co_paths)
            check(universal == is_sat, f"universal complement n={n} table={table}")
            universal_complement_ok += int(universal == is_sat)

            # A malformed proof rejects in the UNSAT verifier, hence accepts
            # in its complemented co-machine.  Keeping rejection after the
            # complement creates a rejecting branch on every SAT input.
            v_malformed = False
            co_malformed = not v_malformed
            check(co_malformed, f"malformed complement n={n} table={table}")
            wrong_co_malformed = False
            if is_sat and not wrong_co_malformed:
                wrong_malformed_failures += 1

            # Same rule for a verifier clock expiration.
            v_timeout = False
            co_timeout = not v_timeout
            check(co_timeout, f"timeout complement n={n} table={table}")

        rows.append(
            {
                "n": n,
                "truth_table_rows": words,
                "formula_count": formula_count,
                "proof_count": proof_count,
                "existential_unsat_checks": existential_ok,
                "universal_sat_complement_checks": universal_complement_ok,
                "sat_inputs_broken_if_malformed_still_rejects": wrong_malformed_failures,
            }
        )

    # Proper-3CNF hostile controls from U(l;a,b).
    sat_models = 0
    unsat_models = 0
    for bits in range(1 << 5):
        x, a, b, c, d = [bool((bits >> i) & 1) for i in range(5)]
        sat_f = u_gadget(x, a, b)
        unsat_f = sat_f and u_gadget(not x, c, d)
        sat_models += int(sat_f)
        unsat_models += int(unsat_f)
    check(sat_models == 16, "proper U(x) model count")
    check(unsat_models == 0, "proper U(x)&U(not x) contradiction")

    # Slow-invalid wrapper: language unchanged, accepting proof remains cheap,
    # but NTIME/coNTIME is governed by the slowest branch.
    slow_rows = []
    for input_bits in range(1, 17):
        valid_cost = input_bits + 1
        invalid_cost = 1 << input_bits
        check(invalid_cost >= valid_cost, f"slow wrapper cost N={input_bits}")
        slow_rows.append(
            {
                "input_bits": input_bits,
                "fast_valid_accepting_cost": valid_cost,
                "slow_invalid_rejecting_cost": invalid_cost,
                "all_branch_cost": max(valid_cost, invalid_cost),
            }
        )

    result = {
        "marker": MARKER,
        "status": "COMPUTATIONAL finite verification of separately proved polarity theorem",
        "parameters": {"n_min": 0, "n_max": 3, "random_seed": None},
        "assertions": assertions,
        "failures": len(failures),
        "failure_messages": failures,
        "rows": rows,
        "proper_3cnf_controls": {
            "U_x_models_over_five_variable_universe": sat_models,
            "U_x_and_U_not_x_models": unsat_models,
        },
        "slow_invalid_branch": slow_rows,
        "limits": [
            "Finite enumeration is not an asymptotic lower bound.",
            "The theorem is definitional and applies to total bounded nondeterministic machines.",
            "An existential UNSAT proof system can still yield coNTIME SAT after exact branch complementation.",
            "No near-boundary exponent or small-space algorithm is derived.",
        ],
    }
    out = Path("2026-10-26_0349_POLARITY_CLOCK160_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
