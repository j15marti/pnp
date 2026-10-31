#!/usr/bin/env python3
"""Independent raw-record verifier for XOR-STATE-DIFFERENCE-REFEREE249."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1348_LSPV5_XOR_STATE_DIFFERENCE_REFEREE249_raw.json"


def main() -> int:
    d = json.loads(RAW.read_text())
    assert d["run_id"] == "XOR-STATE-DIFFERENCE-REFEREE249"
    assert d["exact_theorem_controls"]["checks"] > 10000
    assert d["same_source_labels"]["U198"]["module_joint_rows"] == []
    assert d["same_source_labels"]["V198"]["status"] == "SAT"
    assert d["same_source_labels"]["Y6"]["model_count"] == 20
    for fixture in ("Y6", "U198", "V198"):
        b = d["binary_gray_assignment_cycles"][fixture]["binary_cycle"]
        g = d["binary_gray_assignment_cycles"][fixture]["gray_cycle"]
        assert b["endpoint_d_logic"] == g["endpoint_d_logic"] == 0
        assert b["sum_adjacent_d_phys_lazy"] >= g["sum_adjacent_d_phys_lazy"]
        assert b["sum_adjacent_d_logic"] >= b["sum_adjacent_d_phys_lazy"]
        assert g["sum_adjacent_d_logic"] >= g["sum_adjacent_d_phys_lazy"]
    pf = d["same_endpoint_flip_order_paths"]["V198_witness_forward"]
    pr = d["same_endpoint_flip_order_paths"]["V198_witness_reverse"]
    assert pf["endpoint_d_logic"] == pr["endpoint_d_logic"]
    assert pf["sum_adjacent_d_logic"] == pr["sum_adjacent_d_logic"]
    assert pf["transition_sha256"] != pr["transition_sha256"]
    assert all(row["start_end_d_phys"] == 0 for row in d["wrapper_controls"]["rows"])
    assert any(row["native_steps"] == 10000 for row in d["wrapper_controls"]["rows"])
    assert d["counter_encoding"]["width10"]["gray_cycle_delta"] == 1024
    assert d["counter_encoding"]["width10"]["binary_cycle_delta"] > 1024
    assert d["unaligned_encoding"]["status"].startswith("FAILED TRANSFER")
    assert d["standard_solver"]["U198"]["status"] in (1, 2)
    assert not d["standard_solver"]["U198"]["success"]
    assert d["standard_solver"]["V198"]["success"]
    assert d["proof_status"]["P_vs_NP"] == "OPEN"
    print("VERIFIED::READBACK::XOR-STATE-DIFFERENCE-REFEREE249")
    return 0


if __name__ == "__main__":
    sys.exit(main())
