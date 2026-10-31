#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE251 raw output."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1548_LSPV5_XOR_ACTIVITY_IDENTITY_REFEREE251_raw.json"


def ints(d):
    return {int(k): int(v) for k, v in d.items()}


def main() -> int:
    r = json.loads(RAW.read_text())
    assert r["run_id"] == "XOR-ACTIVITY-IDENTITY-REFEREE251"
    assert r["same_target_labels"]["Y6"]["models"] == 20
    assert r["same_target_labels"]["U198"]["status"] == "UNSAT"
    assert r["same_target_labels"]["U198"]["joint_rows"] == []
    assert r["same_target_labels"]["V198"]["status"] == "SAT"
    assert len(r["malformed_rejections"]) == 5
    assert all(not row["valid"] for row in r["malformed_rejections"].values())
    y = r["exhaustive_Y6"]
    assert y["assignments"] == 64 and y["single_flips"] == 384
    assert sum(ints(y["distribution"]["gray"]).values()) == 384
    assert sum(ints(y["distribution"]["binary"]).values()) == 384
    for name in ("sampled_U198", "sampled_V198"):
        row = r[name]
        assert sum(ints(row["distribution"]["gray"]).values()) == row["single_flips"]
        assert sum(ints(row["distribution"]["binary"]).values()) == row["single_flips"]
        assert all(5 <= k <= 9 for k in ints(row["distribution"]["gray"]))
        assert all(5 <= k <= 9 for k in ints(row["distribution"]["binary"]))
        for ex in row["changed_record_examples"]:
            assert ex["degree"] == 4
            assert len(ex["changed_clause_ids_zero_based"]) == 4
            assert ex["observed_d_logic"] == ex["expected_d_logic"]
    for row in r["sequence_ledgers"].values():
        T, B, H = row["steps"], row["zero_boundary_crossings_B"], row["one_two_crossings_H"]
        assert row["sum_adjacent_d_logic"]["gray"] == 5 * T + B
        assert row["sum_adjacent_d_logic"]["binary"] == 5 * T + B + H
        assert row["sum_adjacent_d_logic"] == row["identity_rhs"]
        assert all(v == T * 4 for v in [sum(row["changed_record_frequency"].values())])
    assert r["actual_search_baseline"]["Y6"]["status"] == "SAT"
    assert r["actual_search_baseline"]["U198"]["status"] == "UNKNOWN"
    assert r["actual_search_baseline"]["V198"]["status"] == "UNKNOWN"
    assert r["proof_status"]["local_activity_identity"] == "PROVED/EXACT"
    assert r["proof_status"]["P_vs_NP"] == "OPEN"
    print("VERIFIED::READBACK::XOR-ACTIVITY-IDENTITY-REFEREE251")
    return 0


if __name__ == "__main__":
    sys.exit(main())
