#!/usr/bin/env python3
"""No-import verifier for REFEREE250 raw records."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1448_LSPV5_XOR_ORDER_SCOPE_REFEREE250_raw.json"


def main() -> int:
    d = json.loads(RAW.read_text())
    assert d["run_id"] == "XOR-ORDER-SCOPE-REFEREE250"
    assert d["same_target_labels"]["Y6"]["models"] == 20
    assert d["same_target_labels"]["U198"]["joint_rows"] == []
    assert d["same_target_labels"]["V198"]["status"] == "SAT"
    assert len(d["malformed_rejections"]) == 5
    assert all(not row["valid"] for row in d["malformed_rejections"].values())
    assert d["exhaustive_comparable_Y6"]["endpoint_pairs_with_orientation"] == 1458
    assert d["exhaustive_comparable_Y6"]["ordered_paths"] > 5000
    for name, row in d["full_sweeps"].items():
        n, m = d["same_target_labels"][name]["n"], d["same_target_labels"][name]["m"]
        for policy in row.values():
            assert policy["binary"]["sum_adjacent"] == n + 5 * m
            assert policy["gray"]["sum_adjacent"] == n + 4 * m
            assert policy["binary"]["endpoint"] == n + 3 * m
            assert policy["gray"]["endpoint"] == n + 2 * m
    dist = d["Y6_all_full_sweep_orders"]
    assert dist["permutations"] == 720
    assert dist["binary_single_tape_native_cost_range"][0] < dist["binary_single_tape_native_cost_range"][1]
    assert set(d["minimal_incomparable_counterexamples"]) == {"binary", "gray"}
    for enc, row in d["minimal_incomparable_counterexamples"].items():
        assert len({v for _, v in row["orders_and_sums"]}) > 1, enc
    assert d["backtrack_control"]["restore"]["binary"]["sum_adjacent"] > d["backtrack_control"]["direct"]["binary"]["sum_adjacent"]
    assert d["index_reset_amortization"]["assertions"] == 32
    assert all(x["endpoint_d_phys"] == 0 for x in d["zero_delta_work_controls"])
    assert d["standard_solver"]["V198"]["success"]
    assert d["standard_solver"]["U198"]["status"] in (1, 2)
    assert d["proof_status"]["P_vs_NP"] == "OPEN"
    print("VERIFIED::READBACK::XOR-ORDER-SCOPE-REFEREE250")
    return 0


if __name__ == "__main__":
    sys.exit(main())
