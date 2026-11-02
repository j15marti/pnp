#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE296 raw output."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["oracle_model"].startswith("one abstract SAT-membership query")
    assert data["decisions"]["sat"]["label"] == "SAT"
    assert data["decisions"]["sat"]["witness"] in (0, 1, 2, 3)
    assert data["decisions"]["unit_unsat"]["label"] == "UNSAT"
    assert data["decisions"]["xor_unsat"]["label"] == "UNSAT"
    assert all(row["queries"] == 1 for row in data["decisions"].values())
    assert all(data["transcript_checks"].values())
    assert data["malformed_count"] == 6 and data["malformed_all_rejected"]
    sweep = data["resolution_blocking_sweep"]
    assert len(sweep) == 6
    for row in sweep:
        assert row["cost"] == 2 ** (row["nvars"] + 1) - 1
        assert row["verified"] and row["corruption_rejected"]
    assert data["status"] == {
        "B3": "OPEN",
        "P_vs_NP": "OPEN",
        "finite_controls": "COMPUTATIONAL",
        "global_B2": "OPEN",
        "symbolic_barrier": "PROVED/EXACT in report",
    }
    checks = 1 + 3 + 2 + 3 + 4 + 2 + 6 * 3 + 1
    print(json.dumps({"verified": True, "independent_assertion_groups": checks, "scope": "finite controls only; asymptotic barrier checked from report proof"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_black_box_relativization_referee296.py RAW_JSON")
    main(sys.argv[1])
