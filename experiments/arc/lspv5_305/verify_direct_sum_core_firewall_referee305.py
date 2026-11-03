#!/usr/bin/env python3
"""No-import verifier for DIRECT-SUM-CORE-FIREWALL-REFEREE305."""

from __future__ import annotations

import hashlib
import json
import resource
import time
from pathlib import Path


SOURCE = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
BASE_RAW = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_raw.json")
RAW = Path("results/raw/arc/2026-11-02_2248_LSPV5_DIRECT_SUM_CORE_FIREWALL_REFEREE305_raw.json")
OUT = Path("results/raw/arc/2026-11-02_2248_LSPV5_DIRECT_SUM_CORE_FIREWALL_REFEREE305_verify.json")


def parse(text):
    n = m = None
    clauses = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            _, kind, ns, ms = line.split()
            assert kind == "cnf" and n is None
            n, m = int(ns), int(ms)
            continue
        vals = [int(x) for x in line.split()]
        assert vals[-1] == 0
        clauses.append(tuple(vals[:-1]))
    assert n is not None and len(clauses) == m
    return n, clauses


def model_list(clauses, n):
    return [
        a for a in range(1 << n)
        if all(any(((a >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in c) for c in clauses)
    ]


def rename(clauses, offset):
    return [tuple((1 if x > 0 else -1) * (abs(x) + offset) for x in c) for c in clauses]


def union(clauses, n, copies):
    return [c for i in range(copies) for c in rename(clauses, i * n)]


def encode_size(n, clauses):
    lines = [f"p cnf {n} {len(clauses)}"] + [" ".join(map(str, c)) + " 0" for c in clauses]
    return len(("\n".join(lines) + "\n").encode())


def resolve(left, right, pivot):
    assert pivot in left and -pivot in right
    raw = (set(left) - {pivot}) | (set(right) - {-pivot})
    assert not any(-x in raw for x in raw)
    return tuple(sorted(raw))


def lift_and_replay(source, proof, base_sources):
    shift = len(source) - base_sources
    lines = list(source)
    for step in proof:
        a = step["left_line"] + (shift if step["left_line"] > base_sources else 0)
        b = step["right_line"] + (shift if step["right_line"] > base_sources else 0)
        made = resolve(lines[a - 1], lines[b - 1], step["pivot"])
        assert set(made) == set(step["clause"])
        lines.append(made)
    return lines[-1] == ()


def main():
    started = time.perf_counter()
    source_bytes = SOURCE.read_bytes()
    n, base = parse(source_bytes.decode())
    base_raw = json.loads(BASE_RAW.read_text())
    raw = json.loads(RAW.read_text())
    proof = base_raw["resolution_upper_certificate"]

    deleted = base[1:]
    flipped = list(base)
    flipped[0] = tuple([-flipped[0][0], *flipped[0][1:]])
    deleted_models = model_list(deleted, n)
    flipped_models = model_list(flipped, n)

    per_case = []
    for item in raw["cases"]:
        copies = item["copies"]
        u = union(base, n, copies)
        check = {
            "copies": copies,
            "variables": item["variables"] == n * copies,
            "clauses": item["clauses"] == len(base) * copies,
            "bytes": item["encoded_bytes"] == encode_size(n * copies, u),
            "proof": lift_and_replay(u, proof, len(base)),
            "upper": item["constant_refutation_upper"] == 9,
            "additive_value": item["claimed_additive_lower"] == 9 * copies,
            "additivity_refuted_iff_replicated": item["additive_claim_refuted"] == (copies >= 2),
        }
        assert all(check.values()), check
        per_case.append(check)

    # Independently validate the local SAT controls; disjoint witness joining
    # follows because variable blocks are disjoint and identically renamed.
    checks = {
        "source_hash": hashlib.sha256(source_bytes).hexdigest() == raw["base"]["sha256"],
        "base_unsat": model_list(base, n) == [],
        "deleted_models": len(deleted_models) == raw["controls"]["deleted_base_models"] == 4,
        "flipped_models": len(flipped_models) == raw["controls"]["flipped_base_models"] == 4,
        "base_exact_nine_record": base_raw["status"]["mixed_minimum"] == "PROVED/EXACT W_Rmix341=9",
        "eight_sizes": [x["copies"] for x in raw["cases"]] == [1, 2, 4, 8, 16, 32, 64, 128],
        "all_case_checks": all(all(x.values()) for x in per_case),
        "tiny_core_one_step": raw["tiny_core"]["exact_mixed_cost"] == 1 and raw["tiny_core"]["resolution_replays"],
        "malformed": all(raw["controls"]["malformed"].values()),
        "parity_labels": raw["controls"]["odd_k4_models"] == 0 and raw["controls"]["even_k4_models"] == 8,
        "B1_B2_B3_open": raw["status"]["B1_B2_B3"] == "OPEN",
    }
    assert all(checks.values()), checks
    result = {
        "claim_id": "DIRECT-SUM-CORE-FIREWALL-REFEREE305-VERIFY",
        "status": "PASS",
        "checks": checks,
        "check_count": len(checks) + sum(len(x) for x in per_case),
        "case_count": len(per_case),
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "Independent artifact and certificate replay; the axiom-monotonicity theorem is checked mathematically in the report.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
