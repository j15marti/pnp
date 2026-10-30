#!/usr/bin/env python3
"""Independent compact checker for ARC-EXPONENT-DISCOVERY-FIREWALL224."""
import hashlib
import json
from pathlib import Path


def main() -> None:
    raw_path = Path("results/raw/arc/2026-10-30_1248_ARC_EXPONENT_DISCOVERY_FIREWALL224_raw.json")
    summary_path = Path("results/raw/arc/2026-10-30_1248_ARC_EXPONENT_DISCOVERY_FIREWALL224_summary.json")
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert raw["status"] == summary["status"] == "PASS"
    assert len(raw["sources"]) == 4
    labels = [r["label"] for r in raw["sources"]]
    assert labels.count("SAT") == 3 and labels.count("UNSAT") == 1
    assert all(r["identical_on_all_tested_lengths"] for r in raw["wrapper_rows"])
    assert all(r["triggered_asymptotic_degree"] == 6 for r in raw["wrapper_rows"])
    assert all(r["first_triggered_cost"]["triggered"] for r in raw["wrapper_rows"])
    for source in raw["sources"]:
        for target in source["targets"]:
            assert target["invert_S_equals_U"] and target["invert_U_equals_S"]
        assert all(x + y == 3 for x, y in zip(source["zero_counts"], source["one_counts"]))
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    assert digest == summary["raw_sha256"]
    check = {
        "run_id": raw["run_id"],
        "status": "PASS",
        "independent_assertion_groups": 9 + sum(len(s["targets"]) + len(s["pair_modes"]) for s in raw["sources"]),
        "raw_sha256": digest,
    }
    out = Path("results/raw/arc/2026-10-30_1248_ARC_EXPONENT_DISCOVERY_FIREWALL224_check.json")
    out.write_text(json.dumps(check, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(check, sort_keys=True))


if __name__ == "__main__":
    main()
