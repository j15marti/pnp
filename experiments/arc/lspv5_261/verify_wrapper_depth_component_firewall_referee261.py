#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE261."""
from __future__ import annotations

import base64
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VERIFY260 = ROOT / "experiments/arc/lspv5_260/verify_connected_raw_peel_dichotomy_referee260.py"
SUMMARY = ROOT / "results/raw/arc/2026-11-01_0148_LSPV5_WRAPPER_DEPTH_COMPONENT_FIREWALL_REFEREE261_raw.json"
FULL = ROOT / "results/raw/arc/2026-11-01_0148_LSPV5_WRAPPER_DEPTH_COMPONENT_FIREWALL_REFEREE261_raw.full.json"
ARCHIVE = ROOT / "results/raw/arc/2026-11-01_0148_LSPV5_WRAPPER_DEPTH_COMPONENT_FIREWALL_REFEREE261_raw.json.gz.b64"


def load_verify260():
    spec = importlib.util.spec_from_file_location("verify260_independent", VERIFY260)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def audit(v, formula, assignment):
    n = max(abs(x) for c in formula for x in c)
    b = len(assignment)
    k1 = sum(assignment.values())
    k0 = b - k1
    residual = v.cofactor(formula, assignment)
    if residual is None:
        return {"status": "UNSAT_TERMINAL", "b": b, "k0": k0, "k1": k1}
    if not residual:
        return {"status": "SAT_TERMINAL", "b": b, "k0": k0, "k1": k1}
    free = set(range(1, n + 1)) - set(assignment)
    retained = {abs(x) for c in residual for x in c}
    erased = free - retained
    components = v.comps(residual, retained)
    c = len(components)
    largest = max(map(len, components))
    erased_bound = 2 * min(k0, k1)
    retained_bound = n - 2 * b
    component_bound = 1 + 5 * b
    largest_bound = max(0, math.ceil(retained_bound / component_bound))
    assert len(erased) <= erased_bound
    assert len(retained) >= retained_bound
    assert c <= component_bound
    assert largest >= largest_bound
    return {
        "status": "NONTERMINAL", "b": b, "k0": k0, "k1": k1,
        "erased": len(erased), "erased_ids": sorted(erased), "erased_bound": erased_bound,
        "retained": len(retained), "retained_bound": retained_bound,
        "components": c, "component_bound": component_bound,
        "component_sizes": sorted(map(len, components), reverse=True),
        "largest": largest, "largest_bound": largest_bound,
    }


def inverse_threshold(n, M):
    return 0 if n <= M else math.ceil((n - M) / (2 + 5 * M))


def main():
    v = load_verify260()
    summary = json.loads(SUMMARY.read_text())
    full_text = FULL.read_text()
    full = json.loads(full_text)
    archive = ARCHIVE.read_text()
    assert hashlib.sha256(full_text.encode()).hexdigest() == summary["full_raw"]["full_sha256"]
    assert hashlib.sha256(archive.encode()).hexdigest() == summary["full_raw"]["archive_sha256"]
    assert gzip.decompress(base64.b64decode(archive)).decode() == full_text
    checks = 3

    U = v.load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = v.y6()
    assert v.valid(U) and v.valid(V) and v.valid(Y)
    assert not v.u_boundary_empty(U)[0]
    assert v.satisfies(V, v.V_WITNESS)
    checks += 6

    expected_y = []
    for state in itertools.product((-1, 0, 1), repeat=6):
        assignment = {i + 1: bool(s) for i, s in enumerate(state) if s >= 0}
        row = audit(v, Y, assignment)
        row["state"] = "".join("*" if s < 0 else str(s) for s in state)
        expected_y.append(row)
    assert expected_y == full["y6_exhaustive"]
    checks += len(expected_y)

    rng = random.Random(202611010148)
    expected_paired = []
    for b in range(1, 13):
        for trial in range(40):
            chosen = sorted(rng.sample(range(1, 199), b))
            assignment = {x: v.V_WITNESS[x - 1] == "1" for x in chosen}
            ur, vr = audit(v, U, assignment), audit(v, V, assignment)
            assert vr["status"] != "UNSAT_TERMINAL"
            expected_paired.append({
                "b": b, "trial": trial, "assigned_ids": chosen,
                "assignment_bits": "".join("1" if assignment[x] else "0" for x in chosen),
                "U198_label": "UNSAT", "V198_label": "SAT", "U198": ur, "V198": vr,
            })
    assert expected_paired == full["paired_uv_samples"]
    checks += len(expected_paired)

    for row in full["exact_thresholds"]:
        assert row["minimum_pins"] == inverse_threshold(row["n"], row["M"])
        checks += 1
    for row in full["power_thresholds"]:
        assert row["minimum_pins"] == inverse_threshold(row["n"], row["M_floor"])
        checks += 1

    for name, formula in (("U198", U), ("V198", V), ("Y6", Y)):
        checks += v.check_controls(formula, full["controls"][name])
    assert full["malformed_rejected"] == 5
    assert full["claim_status"]["P_vs_NP"] == "OPEN"
    assert full["claim_status"]["semantic_reencoder"] == "OPEN"
    assert full["xor_guard"]["actual_d_phys"] == "NOT MEASURED"
    checks += 4
    print(json.dumps({
        "run_id": full["run_id"],
        "independent_checks": checks,
        "y6_assignments": len(expected_y),
        "paired_same-source_rows": len(expected_paired),
        "controls": "all recomputed",
        "P_vs_NP": "OPEN",
    }, indent=2))


if __name__ == "__main__":
    main()
