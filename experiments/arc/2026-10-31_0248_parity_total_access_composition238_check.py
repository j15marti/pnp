#!/usr/bin/env python3
"""Integrity and claim-scope checker for PARITY-TOTAL-ACCESS-COMPOSITION238."""

import hashlib
import json
from pathlib import Path

RAW = Path("2026-10-31_0248_PARITY_TOTAL_ACCESS_COMPOSITION238_raw.json")
PRODUCER = Path("2026-10-31_0248_parity_total_access_composition238.py")

data = json.loads(RAW.read_text(encoding="utf-8"))
assert data["run_id"] == "PARITY-TOTAL-ACCESS-COMPOSITION238"
assert data["status"]["universal_arc"] == "OPEN"
assert data["status"]["p_vs_np"] == "OPEN"
assert len(data["cases"]) == 2

sat, unsat = data["cases"]
assert sat["name"] == "all_even_SAT" and sat["source_models"] > 0 and sat["child_models"] > 0
assert unsat["name"] == "mixed_UNSAT" and unsat["source_models"] == 0 and unsat["child_models"] == 0
for case in data["cases"]:
    assert case["baseline_dpll"]["sat"] == case["child_dpll"]["sat"]
    assert case["corrupt_source_rejected"] is True
    assert case["extreme_controls"]["pair_mode_checks"] == 1104
    assert case["validation"]["blocks"] == 2

expected_sizes = [
    (3, 1500, 3095632, 1016, "SAT"),
    (3, 7001, 16122008, 1984, "UNSAT"),
    (7, 5000, 22492120, 2560, "SAT"),
    (7, 10000, 46027040, 5120, "UNSAT"),
]
for row, expected in zip(data["size_controls"], expected_sizes):
    got = (row["b"], row["q"], row["source_bits"], row["child_bits"], row["label"])
    assert got == expected
    assert row["child_lt_sqrt_source"] is True
    assert row["accessor"]["queries"] > 0

out = {
    "run_id": data["run_id"],
    "passed": True,
    "checked_cases": 2,
    "checked_large_sizes": 4,
    "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
    "producer_sha256": hashlib.sha256(PRODUCER.read_bytes()).hexdigest(),
}
Path("2026-10-31_0248_PARITY_TOTAL_ACCESS_COMPOSITION238_check.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(out))
