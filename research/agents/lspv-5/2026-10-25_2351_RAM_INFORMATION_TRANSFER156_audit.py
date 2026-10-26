#!/usr/bin/env python3
"""Finite checks for RAM_INFORMATION_TRANSFER156.

Every run is tiny: exhaustive truth tables on five variables and finite transcript
enumeration.  The symbolic checkpoint lemma is proved in the accompanying report.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


def unit_gadget(lit: int, a: int, b: int) -> list[tuple[int, int, int]]:
    return [
        (lit, a, b),
        (lit, a, -b),
        (lit, -a, b),
        (lit, -a, -b),
    ]


def sat_clause(clause: tuple[int, ...], assignment: dict[int, int]) -> bool:
    return any(assignment[abs(l)] == (1 if l > 0 else 0) for l in clause)


def models(clauses: list[tuple[int, ...]], variables: list[int]) -> list[str]:
    out: list[str] = []
    for bits in itertools.product((0, 1), repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        if all(sat_clause(c, assignment) for c in clauses):
            out.append("".join(map(str, bits)))
    return out


def transcript_capacity(s_bits: int, probes: int, word_bits: int) -> int:
    return 1 << (s_bits + probes * word_bits)


def main() -> None:
    # Two late blocks.  The first forces x=1.  The second either agrees or forces x=0.
    # The formulas differ in the four sign bits of x in the second block.
    sat_formula = unit_gadget(1, 2, 3) + unit_gadget(1, 4, 5)
    unsat_formula = unit_gadget(1, 2, 3) + unit_gadget(-1, 4, 5)
    sat_models = models(sat_formula, [1, 2, 3, 4, 5])
    unsat_models = models(unsat_formula, [1, 2, 3, 4, 5])

    # Verify properness and the exact four-bit late difference.
    proper = all(len(set(map(abs, c))) == 3 for c in sat_formula + unsat_formula)
    late_sign_differences = sum(
        int(c1[0] != c0[0]) for c1, c0 in zip(sat_formula[4:], unsat_formula[4:])
    )

    # Exhaustively instantiate the generic transcript bound on small parameters.
    transcript_cases = []
    for s_bits in range(5):
        for probes in range(5):
            for word_bits in range(1, 4):
                cap = transcript_capacity(s_bits, probes, word_bits)
                transcript_cases.append(
                    {
                        "S": s_bits,
                        "q": probes,
                        "w": word_bits,
                        "capacity": cap,
                        "identity_ok": cap == 2**s_bits * (2**word_bits) ** probes,
                    }
                )

    result = {
        "marker": "RAM_INFORMATION_TRANSFER156",
        "proper_3cnf": proper,
        "sat_formula_clause_count": len(sat_formula),
        "unsat_formula_clause_count": len(unsat_formula),
        "sat_formula_model_count": len(sat_models),
        "unsat_formula_model_count": len(unsat_models),
        "sat_formula_first_models": sat_models[:8],
        "late_x_sign_bit_differences": late_sign_differences,
        "zero_persistent_bits_four_binary_probes_capacity": transcript_capacity(0, 4, 1),
        "decision_outputs_required": 2,
        "all_transcript_identities_ok": all(x["identity_ok"] for x in transcript_cases),
        "transcript_cases_checked": len(transcript_cases),
        "interpretation": (
            "The formulas are decided after reading four late sign bits even if the "
            "checkpoint state retained no source information. This falsifies a "
            "state-only cut lower bound, not a bound that charges rereads."
        ),
    }
    assert proper
    assert len(sat_models) == 16
    assert len(unsat_models) == 0
    assert late_sign_differences == 4
    assert result["all_transcript_identities_ok"]
    out = Path(__file__).with_name("2026-10-25_2351_RAM_INFORMATION_TRANSFER156_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
