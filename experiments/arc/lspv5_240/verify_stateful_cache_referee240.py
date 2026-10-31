#!/usr/bin/env python3
"""Independent arithmetic/logic checker for ARC-STATEFUL-CACHE-REFEREE240."""
import json
import sys


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    assert data["status"] == "PASS"
    checks = 1
    for row in data["onehot_actual_serialization"]:
        m = row["m"]
        assert m % 2 == 0 and row["actual_ascii_bit_query_depth"] == m // 2
        assert row["sat_sources"] == row["unsat_sources"] == m // 2
        assert len(row["model_count_pairs"]) == m
        for hidden, (source_models, child_models) in enumerate(row["model_count_pairs"], 1):
            assert (source_models > 0) == (child_models > 0) == (hidden % 2 == 0)
            checks += 1
    for row in data["stateful_cache_ledger"]:
        assert row["cold_stateless_source_probes"] == row["guest_character_queries"] * row["m"] // 2
        assert row["stateful_cached_source_probes"] == row["m"] // 2
        assert row["persistent_label_bits"] == 1
        checks += 3
    seen = set()
    for row in data["star_core_projections"]:
        tau = row["p"] ^ row["q"] ^ row["r"]
        assert tau == row["tau"]
        feasible = [count > 0 for count in row["extensions_by_x"]]
        assert feasible == [tau == 0, tau == 1]
        seen.add((row["p"], row["q"], row["r"]))
        checks += 2
    assert len(seen) == 8
    for row in data["star_size_checks"]:
        k = row["k"]
        assert row["variables"] == 1 + k * (5 + 2 * k)
        assert row["source_clauses"] == k * (12 + 4 * k)
        assert row["child_clauses"] == 10 + 2 * k
        checks += 3
    print(json.dumps({"status": "PASS", "independent_checks": checks, "both_labels": True}))


if __name__ == "__main__":
    main(sys.argv[1])
