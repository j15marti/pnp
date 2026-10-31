#!/usr/bin/env python3
"""Independent structural verifier for REFEREE235 raw JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def lit_value(lit, assignment):
    return assignment[str(abs(lit))] == int(lit > 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw")
    args = parser.parse_args()
    data = json.loads(Path(args.raw).read_text(encoding="utf-8"))
    checks = 0
    labels = set()
    for source in data["sources"]:
        labels.add(source["expected_label"])
        formula = source["formula"]
        for row in source["local_extremes"]:
            clause = formula[row["clause_index"]]
            for occ, lit in zip(row["occurrences"], clause):
                assert occ["variable"] == abs(lit)
                assert occ["S_value"] == int(lit > 0)
                assert occ["U_value"] == 1 - int(lit > 0)
                assert occ["invert_S_to_U"] == occ["U_value"]
                assert occ["invert_U_to_S"] == occ["S_value"]
                checks += 5
        zero, one = source["zero_to_one_flip_trail"][0], source["zero_to_one_flip_trail"][-1]
        assert all(a + b == 3 for a, b in zip(zero["true_literal_counts"],
                                               one["true_literal_counts"]))
        checks += len(formula)
        for run in source["runs"]:
            sched = run["schedule"]
            t = run["direct_trace_steps"]
            phases = sched["phases"]
            assert phases[-1]["completed"]
            assert all(not p["completed"] for p in phases[:-1])
            assert sched["first_success_horizon"] < 2 * t
            assert sched["total_budget"] < 4 * t
            assert sched["total_guest_steps"] < 4 * t
            assert run["computed_label"] == source["expected_label"]
            assert sched["total_work"] >= run["direct_work"]
            assert sum(p["simulation_work"] + p["scrub_work"] for p in phases) == sched["total_work"]
            checks += 8 + len(phases)
    assert labels == {"SAT", "UNSAT"}
    checks += 1
    for row in data["hostile_far_index_controls"]:
        assert row["sequential_prefix_scrub"] > row["wrapped_time_proxy"]
        assert row["label_effect"].startswith("none")
        checks += 2
    assert data["status"]["universal_scrub_claim"] == "FALSIFIED/RETIRED"
    checks += 1
    print(json.dumps({"verified": True, "checks": checks, "labels": sorted(labels)}))


if __name__ == "__main__":
    main()
