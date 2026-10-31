#!/usr/bin/env python3
"""Independent checker for ARC-REALIZED-QUERY-TARIFF-FIREWALL230 raw JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = json.loads(args.raw.read_text(encoding="utf-8"))
    assert data["id"] == "ARC-REALIZED-QUERY-TARIFF-FIREWALL230"
    controls = data["paired_same_family_controls"]
    assert controls["SAT"]["answer"] == 1
    assert controls["UNSAT"]["answer"] == 0
    checks = 2
    sat_rows = controls["SAT"]["rows"]
    no_rows = controls["UNSAT"]["rows"]
    assert len(sat_rows) == len(no_rows) == 7
    for s, u in zip(sat_rows, no_rows):
        assert s["policy"] == u["policy"]
        for row in (s, u):
            recomputed = (row["address_generation_steps"] + row["delay_steps"]
                          + row["source_reads_including_repeats"]
                          + row["output_writes"] + row["guest_steps"]
                          + row["failed_strategy_steps"])
            assert row["selected_total_work"] == recomputed
            assert row["distinct_source_addresses"] <= row["source_reads_including_repeats"]
            assert row["selected_peak_live_bits"] == max(
                row["retained_bits_peak"], row["child_buffer_bits_peak"])
            checks += 3
        for key in s:
            if key != "answer":
                assert s[key] == u[key]
                checks += 1

    by_name = {r["policy"]: r for r in sat_rows}
    assert by_name["direct_one_probe"]["distinct_source_addresses"] == 1
    assert by_name["delay_2^12_then_one_probe"]["distinct_source_addresses"] == 1
    assert by_name["delay_2^12_then_one_probe"]["selected_total_work"] > by_name["direct_one_probe"]["selected_total_work"]
    assert by_name["repeat_same_probe_no_cache"]["distinct_source_addresses"] == 1
    assert by_name["repeat_same_probe_no_cache"]["source_reads_including_repeats"] == 128
    assert by_name["compiler_zero_probe_parent_fallback"]["distinct_source_addresses"] == 0
    assert by_name["compiler_zero_probe_parent_fallback"]["guest_steps"] > 0
    assert by_name["one_probe_materialize_32_children"]["output_writes"] == 8192
    assert by_name["one_probe_retain_32_ancestor_records"]["retained_bits_peak"] == 8192
    checks += 10

    clauses = data["same_source_clause_extreme_and_dpll_controls"]
    assert clauses["SAT"]["SAT"] and clauses["SAT"]["dpll_answer"]
    assert not clauses["UNSAT"]["SAT"] and not clauses["UNSAT"]["dpll_answer"]
    for side in ("SAT", "UNSAT"):
        assert clauses[side]["occurrence_extreme_checks"] > 0
        assert clauses[side]["pair_mode_checks"] > 0
        assert clauses[side]["complement_checks"] > 0
        checks += 3

    cases = data["symbolic_exponent_controls"]
    assert cases[0]["omission_changes_time_bound"] is False
    assert cases[1]["omission_changes_time_bound"] is True
    assert cases[2]["omission_changes_time_bound"] is True
    checks += 3
    out = {"id": data["id"], "status": "PASS", "independent_checks": checks}
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
