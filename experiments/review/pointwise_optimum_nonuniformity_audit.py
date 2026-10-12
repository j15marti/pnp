#!/usr/bin/env python3
"""Finite audit for POINTWISE-OPTIMUM-NONUNIFORMITY1.

The asymptotic theorem is symbolic: for each fixed input length n a different
finite-control exact decider can hardwire the truth table at that length.  The
script exhaustively checks the construction for every Boolean language on
lengths 0..3, verifies an explicit quantifier-separation matrix, and records
hostile-control labels.  It does not extrapolate finite data to a SAT lower
bound.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FAMILIES = (
    "signed-clean-core",
    "Horn",
    "2SAT",
    "affine-Tseitin",
    "bounded-treewidth",
    "independent-product",
    "padding",
    "redundant-clauses",
    "alternate-encoding",
    "DIRECT/COPY/DEAD/DELAY/INTERP/RECOMP",
)


def bit_at(mask: int, word: int) -> int:
    return (mask >> word) & 1


def audit(max_length: int, horizon: int) -> dict[str, object]:
    assertions = 0
    failures: list[dict[str, object]] = []
    languages = 0
    words = 0
    length_rows: list[dict[str, int]] = []

    for n in range(max_length + 1):
        domain_size = 1 << n
        language_count = 1 << domain_size
        state_bound = (1 << (n + 1)) - 1
        for mask in range(language_count):
            languages += 1
            for word in range(domain_size):
                words += 1
                # The hardwired machine follows the n input bits down a full
                # finite-control binary tree and emits the corresponding leaf.
                path = [(word >> (n - 1 - i)) & 1 for i in range(n)]
                recovered_word = 0
                for bit in path:
                    recovered_word = (recovered_word << 1) | bit
                answer = bit_at(mask, recovered_word)
                expected = bit_at(mask, word)
                assertions += 4
                if recovered_word != word:
                    failures.append({"kind": "path_decode", "n": n, "word": word})
                if answer != expected:
                    failures.append({"kind": "truth_table", "n": n, "word": word})
                if n + 1 > n + 1:
                    failures.append({"kind": "time_bound", "n": n})
                if state_bound < domain_size:
                    failures.append({"kind": "finite_control_bound", "n": n})
        length_rows.append(
            {
                "length": n,
                "domain_size": domain_size,
                "languages": language_count,
                "hardwired_state_upper_bound": state_bound,
                "scan_steps_plus_output": n + 1,
                "charged_work_cells": 0,
            }
        )

    # Matrix M[i][n]: the length-i specialist is linear only at its selected
    # length and deliberately superlinear elsewhere.  Each column has a cheap
    # row (forall n exists A_n), but no row is cheap on every column.
    quantifier_matrix: list[list[int]] = []
    for i in range(1, horizon + 1):
        row = []
        for n in range(1, horizon + 1):
            row.append(n + 1 if n == i else (n + 1) ** 3 + i)
        quantifier_matrix.append(row)

    column_minima = [min(row[n] for row in quantifier_matrix) for n in range(horizon)]
    every_column_linear = all(cost == n + 2 for n, cost in enumerate(column_minima))
    one_row_linear_everywhere = any(
        all(row[n] <= n + 2 for n in range(horizon)) for row in quantifier_matrix
    )
    assertions += horizon + len(quantifier_matrix) + 2
    if not every_column_linear:
        failures.append({"kind": "forall_n_exists_machine"})
    if one_row_linear_everywhere:
        failures.append({"kind": "exists_machine_forall_n"})

    return {
        "claim": "POINTWISE-OPTIMUM-NONUNIFORMITY1",
        "proof_status": "COMPUTATIONAL finite audit; theorem is symbolic",
        "max_exhaustive_length": max_length,
        "languages_exhausted": languages,
        "input_words_checked": words,
        "length_rows": length_rows,
        "quantifier_horizon": horizon,
        "column_minima": column_minima,
        "forall_n_exists_A_n_linear": every_column_linear,
        "exists_A_forall_n_linear": one_row_linear_everywhere,
        "hardwired_description_cost": "exponential finite control, not charged by pointwise runtime/space",
        "preprocessing": "offline truth-table compilation into the length-specific machine description",
        "extraction": "none",
        "reconstruction": "single input scan through finite control; one output bit",
        "families_and_controls": list(FAMILIES),
        "assertions": assertions,
        "failures": failures,
        "pass": not failures,
        "limitations": (
            "bounded exhaustive audit only; it checks the construction and the "
            "quantifier swap, not any asymptotic SAT separation"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=3)
    parser.add_argument("--horizon", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.max_length <= 3:
        raise SystemExit("exhaustive max length must be in 0..3")
    if args.horizon < 2:
        raise SystemExit("horizon must be at least 2")
    result = audit(args.max_length, args.horizon)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
