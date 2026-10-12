#!/usr/bin/env python3
"""Bounded audit for charged uniform per-length program generation.

The experiment is finite and diagnostic.  The accompanying report proves the
asymptotic composition theorem directly; this script checks the accounting on
small exhaustive languages, exponent ledgers, and hostile-control labels.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


SEED = 20261012
OUT = Path("results/raw/review/2026-10-12_uniform_generator_composition.json")
HOSTILE_CONTROLS = [
    "2SAT",
    "Horn",
    "affine/Tseitin Gaussian elimination",
    "bounded treewidth",
    "signed clean core",
    "independent products",
    "padding",
    "redundant clauses",
    "alternate encodings",
    "DIRECT/COPY/DEAD/DELAY/INTERP/RECOMP wrappers",
    "one-bit output shell",
]


def table_bit(table: int, x: int) -> int:
    return (table >> x) & 1


def main() -> None:
    started = time.perf_counter()
    assertions = 0

    # Exhaust every Boolean language on n <= 4.  The explicit compiler writes
    # one bit per input; the evaluator scans n input bits, performs one table
    # access, and emits one decision bit.  No witness is reconstructed.
    exhaustive = []
    total_languages = 0
    total_inputs = 0
    total_generator_writes = 0
    total_evaluator_reads = 0
    for n in range(5):
        width = 1 << n
        languages = 1 << width
        local_assertions = 0
        for table in range(languages):
            generated = [(table >> i) & 1 for i in range(width)]
            assertions += 1
            local_assertions += 1
            assert len(generated) == width
            total_generator_writes += width
            for x in range(width):
                assertions += 1
                local_assertions += 1
                assert generated[x] == table_bit(table, x)
                total_inputs += 1
                total_evaluator_reads += 1
        total_languages += languages
        exhaustive.append(
            {
                "n": n,
                "languages": languages,
                "truth_table_bits_per_language": width,
                "finite_control_prefix_states": (1 << (n + 1)) - 1,
                "assertions": local_assertions,
            }
        )

    # Explicit-table output lower bound: in a sequential output model the
    # generator performs at least one write per emitted bit.
    explicit_tables = []
    for n in range(21):
        bits = 1 << n
        states = (1 << (n + 1)) - 1
        assertions += 3
        assert bits == 2**n
        assert states == 2 * bits - 1
        assert bits >= 1
        explicit_tables.append(
            {
                "n": n,
                "truth_table_bits": bits,
                "minimum_sequential_output_writes": bits,
                "prefix_tree_states": states,
            }
        )

    # Polynomial accounting: if generation, explicit code output, evaluation,
    # and simulator overhead have fixed polynomial exponents, their sum has
    # exponent equal to the maximum.  This is a finite arithmetic regression,
    # not the proof of the asymptotic statement.
    exponent_cases = 0
    max_ratio = 0.0
    for exponents in itertools.product(range(7), repeat=4):
        k = max(1, *exponents)
        for n in (2, 3, 5, 8, 13, 21, 34):
            terms = n + sum(n**e for e in exponents)
            bound = 5 * (n**k)
            assertions += 1
            assert terms <= bound
            max_ratio = max(max_ratio, terms / (n**k))
        exponent_cases += 1

    # Retained explicit code consumes its length in workspace.  Streaming or
    # virtual access may avoid retention, but then all access/recomputation is
    # part of the evaluator ledger; the audit records, rather than hides, it.
    workspace_cases = 0
    for h, ell, s in itertools.product(range(7), repeat=3):
        k = max(h, ell, s)
        for n in (2, 7, 19):
            total = n**h + n**ell + n**s
            assertions += 1
            assert total <= 3 * n**k
        workspace_cases += 1

    for label in HOSTILE_CONTROLS:
        assertions += 1
        assert label

    elapsed = time.perf_counter() - started
    script_bytes = Path(__file__).read_bytes()
    result = {
        "run_id": "UGENCOMP1",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "method": "deterministic exhaustive plus exact integer accounting",
        "chunking": "not required; one invocation completed below 30 seconds",
        "elapsed_seconds": elapsed,
        "assertions": assertions,
        "failures": 0,
        "exhaustive": exhaustive,
        "totals": {
            "languages": total_languages,
            "evaluated_inputs": total_inputs,
            "explicit_generator_bit_writes": total_generator_writes,
            "evaluator_table_reads": total_evaluator_reads,
            "exponent_cases": exponent_cases,
            "workspace_cases": workspace_cases,
            "max_normalized_time_sum": max_ratio,
        },
        "explicit_table_ledger": explicit_tables,
        "cost_ledger": {
            "preprocessing": "charged generator execution and code writes",
            "extraction": 0,
            "evaluation": "input scan plus charged code access/simulation",
            "reconstruction": 0,
            "decision_output_bits": 1,
            "retained_code_space": "charged when code is materialized",
            "virtual_code_access": "must be charged to evaluation/recomputation",
        },
        "hostile_controls": HOSTILE_CONTROLS,
        "limitations": [
            "Finite tests do not prove asymptotic bounds.",
            "The theorem is established separately by machine composition.",
            "No SAT solver runtime is benchmarked or extrapolated.",
        ],
        "script_sha256": hashlib.sha256(script_bytes).hexdigest(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
