#!/usr/bin/env python3
"""Independent checker for ARC-DP-QUADRATIC-OUTPUT-FIREWALL234."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location("producer234", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--producer", required=True)
    p.add_argument("--raw", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    mod = load(Path(a.producer))
    raw = json.loads(Path(a.raw).read_text(encoding="utf-8"))
    checks = []
    for sat in (True, False):
        for r in (2, 3):
            source, meta = mod.family(r, sat)
            child = mod.eliminate(source, meta["pivot"])["clauses"]
            boundary = [v for v in range(1, meta["nvars"] + 1) if v != meta["pivot"]]
            compared = 0
            for bits in itertools.product((False, True), repeat=len(boundary)):
                b = dict(zip(boundary, bits))
                source_exists = any(mod.satisfies(source, {**b, meta["pivot"]: x}) for x in (False, True))
                child_value = mod.satisfies(child, b)
                assert source_exists == child_value
                compared += 1
            checks.append({"r": r, "label": "SAT" if sat else "UNSAT",
                           "boundary_assignments_compared": compared,
                           "pointwise_projection_exact": True})
    for case in raw["cases"]:
        assert case["complete_dp_resolvents"] == case["r"] ** 2
        assert case["baseline_up_dpll"]["answer"] == (case["label"] == "SAT")
        assert case["transactional_dp_then_fallback"]["answer"] == (case["label"] == "SAT")
    result = {"run_id": raw["run_id"], "independent_checks": checks,
              "all_raw_rows_consistent": True,
              "verdict": "PASS"}
    Path(a.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
