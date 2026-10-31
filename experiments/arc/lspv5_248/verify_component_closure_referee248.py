#!/usr/bin/env python3
"""Independent readback verifier for COMPONENT-CLOSURE-REFEREE248."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1248_LSPV5_COMPONENT_CLOSURE_REFEREE248_raw.json"


def main() -> int:
    d = json.loads(RAW.read_text())
    assert d["run_id"] == "COMPONENT-CLOSURE-REFEREE248"
    for audit in d["subset_audits"].values():
        assert audit["mismatches"] == 0
        assert audit["valid_subsets"] == audit["component_unions"]
    assert d["subset_audits"]["Y6_connected"]["valid_subsets"] == 1
    assert d["subset_audits"]["Y6_disjoint_union_Y6"]["valid_subsets"] == 3
    assert d["controls"]["U198"]["exact_status"] == "UNSAT"
    assert d["controls"]["U198"]["certificate"]["joint_rows"] == []
    assert d["controls"]["V198"]["exact_status"] == "SAT"
    assert d["controls"]["V198"]["witness_replay"]["satisfied"]
    assert d["controls"]["Y6"]["model_count"] > 0
    assert d["controls"]["Y6_union_Y6"]["model_count"] == d["controls"]["Y6"]["model_count"] ** 2
    assert all(not x["valid_children"] for x in d["one_clause_deletion_audit"].values())
    assert all(x["ratio"] == 1.0 for x in d["contraction_obstruction"].values())
    print("VERIFIED::READBACK::COMPONENT-CLOSURE-REFEREE248")
    return 0


if __name__ == "__main__":
    sys.exit(main())
