#!/usr/bin/env python3
"""Source-retention quantifier firewall 229.

Reuses the canonical proper-3CNF family from firewall 228.  It checks the
opposite side of that theorem: once a point continuation is known, an indexed
read-only source accessor can recover the relevant boundary bit from one
literal word of the retained source.  The experiment is exhaustive for b=3,4
and includes same-source SAT/UNSAT, clause-extreme, complement, and DPLL
controls inherited from the audited producer for firewall 228.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
PREVIOUS = HERE / "2026-10-30_1648_reusable_boundary_summary_audit.py"


def load_previous():
    spec = importlib.util.spec_from_file_location("firewall228", PREVIOUS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {PREVIOUS}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load_previous()


def indexed_decode(clauses, boundary_assignment: int, b: int):
    """Decode f(a) from the first literal word of canonical block a."""
    clauses_per_block = b - 2
    clause_address = boundary_assignment * clauses_per_block
    literal = clauses[clause_address][0]
    # Exclusion blocks begin with boundary literal +/-x_1.  Dummy blocks use
    # their preallocated private range, whose identifiers are all above b.
    answer = int(abs(literal) > b)
    return answer, {
        "source_word_probes": 1,
        "clause_address": clause_address,
        "literal_position": 0,
        "literal_read": literal,
    }


def exact_canonical_recognizer(clauses, mask: int, b: int):
    """A charged full scan that verifies the promised canonical A_f syntax."""
    expected, _, _ = P.build_padded_formula(mask, b)
    literal_comparisons = 0
    if len(clauses) != len(expected):
        return False, literal_comparisons
    for got_clause, want_clause in zip(clauses, expected):
        if len(got_clause) != len(want_clause):
            return False, literal_comparisons
        for got, want in zip(got_clause, want_clause):
            literal_comparisons += 1
            if got != want:
                return False, literal_comparisons
    return True, literal_comparisons


def exhaustive_accessor_audit(b: int):
    boundary_size = 1 << b
    function_count = 1 << boundary_size
    queries = 0
    source_word_probes = 0
    recognizer_literal_comparisons = 0
    recognizer_checks = 0
    for mask in range(function_count):
        clauses, _, _ = P.build_padded_formula(mask, b)
        ok, comparisons = exact_canonical_recognizer(clauses, mask, b)
        assert ok
        recognizer_checks += 1
        recognizer_literal_comparisons += comparisons
        for a in range(boundary_size):
            answer, ledger = indexed_decode(clauses, a, b)
            assert answer == P.bit(mask, a)
            assert ledger["source_word_probes"] == 1
            queries += 1
            source_word_probes += ledger["source_word_probes"]
    return {
        "b": b,
        "functions": function_count,
        "point_queries": queries,
        "source_word_probes": source_word_probes,
        "probes_per_query": source_word_probes / queries,
        "full_source_recognizer_checks": recognizer_checks,
        "recognizer_literal_comparisons": recognizer_literal_comparisons,
    }


def batch_ledger(b: int, query_sequence: list[int]):
    distinct = len(set(query_sequence))
    # After one canonical-source verification, a no-cache controller pays one
    # targeted source probe per query; an answer cache pays one per distinct
    # query and retains one answer bit plus an address per cached item.
    address_bits = b
    return {
        "b": b,
        "queries": len(query_sequence),
        "distinct_queries": distinct,
        "no_cache_source_word_probes": len(query_sequence),
        "cached_source_word_probes": distinct,
        "cached_answer_bits": distinct,
        "cached_address_bits_upper_bound": distinct * address_bits,
        "counterfactual_detached_summary_floor_bits": 1 << b,
    }


def encoding_and_model_table():
    rows = []
    for b in range(3, 21):
        clauses = (b - 2) * (1 << b)
        variables = b + 3 * clauses
        index_bits = math.ceil(math.log2(variables + 1))
        source_bits = 3 * clauses * (1 + index_bits) + 2 * index_bits
        last_clause_address = ((1 << b) - 1) * (b - 2)
        rows.append({
            "b": b,
            "clauses": clauses,
            "source_bits_fixed_width_upper_encoding": source_bits,
            "detached_summary_lower_bound_bits": 1 << b,
            "indexed_post_continuation_source_word_probes": 1,
            "address_bits_upper_bound": math.ceil(math.log2(max(2, 3 * clauses))),
            "sequential_direct_scan_literal_words_to_last_block": 3 * last_clause_address + 1,
            "sequential_scan_status": "algorithm-specific upper cost, not a lower bound",
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    exhaustive = [exhaustive_accessor_audit(3), exhaustive_accessor_audit(4)]
    controls = [
        P.source_control("unique_boundary_model_SAT", 1 << 15, 4),
        P.source_control("zero_boundary_function_UNSAT", 0, 4),
    ]
    assert controls[0]["SAT"] and not controls[1]["SAT"]
    # Same canonical source layout, two opposite labels under the point a=15.
    sat_clauses, _, _ = P.build_padded_formula(1 << 15, 4)
    no_clauses, _, _ = P.build_padded_formula(0, 4)
    sat_answer, sat_probe = indexed_decode(sat_clauses, 15, 4)
    no_answer, no_probe = indexed_decode(no_clauses, 15, 4)
    assert (sat_answer, no_answer) == (1, 0)

    batches = [
        batch_ledger(16, [7] * 128),
        batch_ledger(16, list(range(128))),
        batch_ledger(16, [i % 8 for i in range(128)]),
    ]
    result = {
        "id": "ARC-SOURCE-RETENTION-QUANTIFIER-FIREWALL229",
        "date": "2026-10-30 America/Los_Angeles",
        "claim": (
            "On the canonical A_f family, after B_a reveals a, a fixed indexed "
            "source-retaining controller obtains SAT(A_f AND B_a)=f(a) with one "
            "source-word probe and O(b) address/work bits; this coexists with the "
            "2^b-bit detached reusable-summary lower bound."
        ),
        "status": {
            "canonical_family_indexed_accessor": "PROVED/EXACT restricted promise family",
            "detached_summary_floor_to_general_runtime": "FALSIFIED/RETIRED",
            "finite_audit": "COMPUTATIONAL",
            "arbitrary_input_recognition_or_fallback": "OPEN beyond the declared easy family",
            "ARC": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "quantifiers": {
            "detached_summary": "exists one summary state for A_f, then forall future a",
            "retained_source": "forall presented a, compute its address and probe retained A_f",
        },
        "machine_models": {
            "indexed_read_only_source": "one source-word probe after address calculation; O(b) address/work bits",
            "sequential_read_only_source": "the direct implementation may scan to the addressed block; no all-algorithm lower bound",
            "unpromised_arbitrary_input": "full syntax recognition costs a charged source scan; nonmatching inputs require an exact fallback",
        },
        "counts": {
            "functions_exhausted": sum(x["functions"] for x in exhaustive),
            "point_queries": sum(x["point_queries"] for x in exhaustive),
            "source_word_probes": sum(x["source_word_probes"] for x in exhaustive),
            "recognizer_literal_comparisons": sum(x["recognizer_literal_comparisons"] for x in exhaustive),
        },
        "exhaustive_accessor_audit": exhaustive,
        "same_source_opposite_label_point_control": {
            "boundary_assignment": 15,
            "SAT_source_answer": sat_answer,
            "UNSAT_source_answer": no_answer,
            "SAT_probe": sat_probe,
            "UNSAT_probe": no_probe,
        },
        "batch_query_ledgers": batches,
        "encoding_and_model_table": encoding_and_model_table(),
        "same_source_clause_extreme_and_dpll_controls": controls,
        "limitations": [
            "The one-probe theorem assumes the canonical A_f layout or a separately charged verification of that promise.",
            "It is an easy-family accessor, not an all-input SAT algorithm or ARC successor.",
            "One indexed source-word probe is not one bit-tape step on every machine model.",
            "The detached summary lower bound and retained-source accessor have different interfaces and cannot be combined into a runtime lower bound.",
            "All finite selected-operation counts are computational controls, not native FLMV measurements.",
        ],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
