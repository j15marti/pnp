#!/usr/bin/env python3
"""Independent arithmetic/readback checks for firewall 229 raw output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", type=Path)
    args = ap.parse_args()
    data = json.loads(args.raw.read_text(encoding="utf-8"))
    checks = 0

    assert data["id"] == "ARC-SOURCE-RETENTION-QUANTIFIER-FIREWALL229"; checks += 1
    expected_functions = 0
    expected_queries = 0
    expected_recognizer_words = 0
    for row in data["exhaustive_accessor_audit"]:
        b = row["b"]
        functions = 1 << (1 << b)
        queries = functions * (1 << b)
        clause_literal_words = 3 * (b - 2) * (1 << b)
        assert row["functions"] == functions; checks += 1
        assert row["point_queries"] == queries; checks += 1
        assert row["source_word_probes"] == queries; checks += 1
        assert row["probes_per_query"] == 1; checks += 1
        assert row["recognizer_literal_comparisons"] == functions * clause_literal_words; checks += 1
        expected_functions += functions
        expected_queries += queries
        expected_recognizer_words += functions * clause_literal_words

    counts = data["counts"]
    assert counts["functions_exhausted"] == expected_functions; checks += 1
    assert counts["point_queries"] == expected_queries; checks += 1
    assert counts["source_word_probes"] == expected_queries; checks += 1
    assert counts["recognizer_literal_comparisons"] == expected_recognizer_words; checks += 1

    paired = data["same_source_opposite_label_point_control"]
    assert paired["SAT_source_answer"] == 1 and paired["UNSAT_source_answer"] == 0; checks += 1
    assert abs(paired["SAT_probe"]["literal_read"]) > 4; checks += 1
    assert abs(paired["UNSAT_probe"]["literal_read"]) <= 4; checks += 1
    assert paired["SAT_probe"]["source_word_probes"] == 1; checks += 1
    assert paired["UNSAT_probe"]["source_word_probes"] == 1; checks += 1

    for row in data["batch_query_ledgers"]:
        assert row["cached_source_word_probes"] == row["distinct_queries"]; checks += 1
        assert row["cached_answer_bits"] == row["distinct_queries"]; checks += 1
        assert row["no_cache_source_word_probes"] == row["queries"]; checks += 1
        assert row["cached_source_word_probes"] <= row["no_cache_source_word_probes"]; checks += 1
        assert row["counterfactual_detached_summary_floor_bits"] == 1 << row["b"]; checks += 1

    controls = data["same_source_clause_extreme_and_dpll_controls"]
    assert len(controls) == 2; checks += 1
    assert controls[0]["SAT"] is True and controls[1]["SAT"] is False; checks += 1
    assert controls[0]["b"] == controls[1]["b"] == 4; checks += 1
    for control in controls:
        assert len(control["local_targets"]) == control["clauses"]; checks += 1
        assert len(control["pair_compatibility"]) == control["clauses"] * (control["clauses"] - 1) // 2; checks += 1

    result = {"status": "PASS", "independent_checks": checks,
              "functions": expected_functions, "point_queries": expected_queries}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
