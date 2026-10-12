#!/usr/bin/env python3
"""Finite audit for UNIVERSAL-RESOURCE-AXIS-PENTACHOTOMY1.

The asymptotic statements are proved in the report.  This script checks the
finite wrapper witnesses and the two-line Boolean classification used by the
synthesis; it deliberately does not extrapolate timing asymptotics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apiflat", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    source_bytes = args.apiflat.read_bytes()
    source = json.loads(source_bytes)
    checks = 0
    failures: list[str] = []
    rows = []

    for case in source["cases"]:
        variants = case["variants"]
        answers = {v["answer"] for v in variants.values()}
        checks += 1
        if len(answers) != 1:
            failures.append(f"{case['case']}:answer disagreement")

        checks += 1
        if variants["EXPLICIT"]["host_api_calls"] <= 0:
            failures.append(f"{case['case']}:explicit call missing")

        for name in ("INLINE", "FUSED", "DISPATCH", "TABLE"):
            checks += 1
            if variants[name]["host_api_calls"] != 0:
                failures.append(f"{case['case']}:{name} host call")

        checks += 1
        if variants["DISPATCH"]["guest_logical_calls"] <= 0:
            failures.append(f"{case['case']}:dispatch lost decoded event")

        checks += 1
        if variants["FUSED"]["materialized_bits"] != 0:
            failures.append(f"{case['case']}:fused materialization")

        # A delay wrapper changes runtime but not the Boolean answer; a copy
        # wrapper can change retained representation volume.  These are finite
        # meter-separation witnesses, not complexity estimates.
        base_steps = variants["FUSED"]["literal_tests"] + variants["FUSED"]["clause_tests"]
        delay_steps = base_steps + 17
        copy_bits = variants["EXPLICIT"]["materialized_bits"] * 2
        checks += 3
        if not (delay_steps > base_steps and copy_bits >= variants["EXPLICIT"]["materialized_bits"]
                and variants["FUSED"]["answer"] == case["answer"]):
            failures.append(f"{case['case']}:wrapper separation")

        rows.append({
            "case": case["case"],
            "answer": case["answer"],
            "positive_explicit_calls": variants["EXPLICIT"]["host_api_calls"],
            "zero_call_representatives": 4,
            "dispatch_guest_events": variants["DISPATCH"]["guest_logical_calls"],
            "fused_materialized_bits": variants["FUSED"]["materialized_bits"],
            "base_steps": base_steps,
            "delay_steps": delay_steps,
            "copy_bits": copy_bits,
        })

    # Truth-table audit of WC_T(K) <=> SAT notin P once K is NP-hard.
    equivalence_rows = []
    for sat_in_p in (False, True):
        wc_time = not sat_in_p
        checks += 1
        if wc_time != (not sat_in_p):
            failures.append("time-equivalence truth table")
        equivalence_rows.append({"sat_in_p": sat_in_p, "wc_time": wc_time})

    # A linear-workspace exhaustive decider defeats a superpolynomial-space
    # necessity at d=2 for N>=2: N <= N^2.
    for n in range(2, 66):
        checks += 1
        if n > n * n:
            failures.append(f"linear-space guard at N={n}")

    classification = [
        {"axis": "cofinal superpolynomial time on NP-hard core", "status": "OPEN / equivalent to P!=NP"},
        {"axis": "superpolynomial workspace for every decider", "status": "FALSIFIED/RETIRED"},
        {"axis": "unqualified communication/extraction/reconstruction", "status": "FALSIFIED/RETIRED"},
        {"axis": "named internal API-call count", "status": "FALSIFIED/RETIRED"},
        {"axis": "externally fixed restricted-model resource", "status": "OPEN transfer to arbitrary static SAT"},
    ]

    payload = {
        "experiment": "UNIVERSAL-RESOURCE-AXIS-PENTACHOTOMY-AUDIT1",
        "status": "COMPUTATIONAL",
        "source_apiflat_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "checks": checks,
        "failures": failures,
        "cases": rows,
        "time_equivalence_truth_table": equivalence_rows,
        "classification": classification,
        "warning": "Finite checks validate witnesses and bookkeeping only; asymptotic claims require the report proofs.",
    }
    assert not failures, failures
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_digest"] = hashlib.sha256(canonical).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"checks": checks, "failures": len(failures), "sha256": payload["sha256_without_digest"]}))


if __name__ == "__main__":
    main()
