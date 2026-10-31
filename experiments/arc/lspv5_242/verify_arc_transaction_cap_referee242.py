#!/usr/bin/env python3
"""Independent raw-record verifier for ARC-TRANSACTION-CAP-REFEREE242."""
from __future__ import annotations

import json
import math
import sys


def main(path: str) -> None:
    data = json.load(open(path, encoding="utf-8"))
    assert data["run"] == "ARC-TRANSACTION-CAP-REFEREE242"
    assert data["status"] == "PASS" and data["seed"] is None
    src = data["sources"]
    assert len(src) == data["totals"]["sources"] == 16
    assert {r["label"] for r in src} == {"SAT", "UNSAT"}
    assert data["totals"]["sat_sources"] == 8
    assert data["totals"]["unsat_sources"] == 8
    checks = 0
    for r in src:
        assert (r["model_count"] > 0) == (r["label"] == "SAT")
        assert r["complete_assignments_checked"] == 2 ** r["variables"]
        assert r["dpll"]["nodes"] >= 1 and r["dpll"]["literal_probes"] >= 0
        for c in r["su"]["clauses"]:
            s = {int(k): v for k, v in c["S"].items()}
            u = {int(k): v for k, v in c["U"].items()}
            assert set(s) == set(u)
            assert all(u[v] == 1 - s[v] for v in s)
            assert {int(k): v for k, v in c["invert_S_is_U"].items()} == u
            assert {int(k): v for k, v in c["invert_U_is_S"].items()} == s
            checks += 4 * len(s)
        checks += r["su"]["pair_mode_checks"]
        if r["meta"]["kind"] == "h":
            assert r["certificate"]["verified"] and r["certificate"]["corrupt_certificate_rejected"]
            u = r["controller"]["uncapped"]
            c = r["controller"]["capped"]
            assert u["peak_trial_space"] >= u["easy_steps"]
            assert c["peak_trial_space"] <= c["cap"] + 1
            assert u["reset_steps"] > 0 and c["reset_steps"] > 0
            assert u["total_policy_and_reset_and_verify_steps"] >= u["easy_steps"]
            assert c["total_policy_and_reset_and_verify_steps"] >= c["easy_steps"]
            checks += len(u["trail"]) + len(c["trail"]) + 10
    ce = data["cap_completeness_counterexample"]
    assert not ce["capped_policy_completes"]
    assert ce["uncapped_fallback_peak"] > ce["cap"]
    aff = data["affine_scope_audit"]
    assert "u_N+1" in aff["accepted_bound"]
    assert aff["sat_runtime_consequence"] == "none"
    checks += 12
    print(json.dumps({"status": "PASS", "independent_checks": checks, "sources": len(src)}, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_arc_transaction_cap_referee242.py RAW.json")
    main(sys.argv[1])
