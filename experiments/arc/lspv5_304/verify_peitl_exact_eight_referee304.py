#!/usr/bin/env python3
"""No-import auditor for PEITL-EXACT-EIGHT-REFEREE304 artifacts."""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


RAW = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_raw.json")
DIMACS = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EIGHT_NODE_ENCODING_REFEREE304.cnf")
SOURCE = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
OUT = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_verify.json")


def parse_source(text):
    clauses = []
    n = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            _, kind, ns, ms = line.split()
            assert kind == "cnf"
            n = int(ns)
            expected = int(ms)
            continue
        vals = [int(x) for x in line.split()]
        assert vals and vals[-1] == 0 and all(x != 0 for x in vals[:-1])
        clauses.append(tuple(vals[:-1]))
    assert n is not None and len(clauses) == expected
    return n, clauses


def models(clauses, n):
    return sum(
        all(any(((a >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause) for clause in clauses)
        for a in range(1 << n)
    )


def resolve(left, right, pivot):
    assert pivot in left and -pivot in right
    raw = (set(left) - {pivot}) | (set(right) - {-pivot})
    assert not any(-lit in raw for lit in raw)
    return tuple(sorted(raw))


def parse_dimacs_shape(path):
    header = None
    clause_count = 0
    max_var = 0
    for raw in path.read_text().splitlines():
        if not raw or raw[0] == "c":
            continue
        if raw[0] == "p":
            _, kind, vs, cs = raw.split()
            assert kind == "cnf"
            header = (int(vs), int(cs))
            continue
        vals = [int(x) for x in raw.split()]
        assert vals[-1] == 0
        clause_count += 1
        if len(vals) > 1:
            max_var = max(max_var, max(abs(x) for x in vals[:-1]))
    assert header is not None
    return header, clause_count, max_var


def main():
    started = time.perf_counter()
    raw = json.loads(RAW.read_text())
    source_bytes = SOURCE.read_bytes()
    n, clauses = parse_source(source_bytes.decode())

    deletion_counts = [models(clauses[:i] + clauses[i + 1 :], n) for i in range(len(clauses))]
    flip_counts = []
    for ci, clause in enumerate(clauses):
        for li in range(len(clause)):
            changed = list(clauses)
            c = list(clause)
            c[li] *= -1
            changed[ci] = tuple(c)
            flip_counts.append(models(changed, n))

    lines = list(clauses)
    for step in raw["resolution_upper_certificate"]:
        made = resolve(lines[step["left_line"] - 1], lines[step["right_line"] - 1], step["pivot"])
        assert set(made) == set(step["clause"])
        lines.append(made)

    cases = raw["solver_records"][0]["degree_cases"]
    expected = [("triple", (i,)) for i in range(14)]
    expected += [("double_pair", p) for p in itertools.combinations(range(14), 2)]
    observed = [(x["kind"], tuple(x["exceptional_lines"])) for x in cases]
    header, actual_clauses, max_var = parse_dimacs_shape(DIMACS)

    checks = {
        "source_hash": hashlib.sha256(source_bytes).hexdigest() == raw["input"]["sha256"],
        "source_unsat": models(clauses, n) == 0,
        "deletions_match_and_sat": deletion_counts == raw["input"]["deletion_model_counts"] and all(x > 0 for x in deletion_counts),
        "sign_flips_match_and_sat": flip_counts == raw["input"]["sign_flip_model_counts"] and all(x > 0 for x in flip_counts),
        "resolution_upper_replays_to_empty": len(lines) == 16 and lines[-1] == (),
        "degree_identity": 2 * 8 - 14 == 2,
        "all_105_patterns_exactly_once": observed == expected and len(set(observed)) == 105,
        "all_105_patterns_unsat": len(cases) == 105 and all(not x["sat"] for x in cases),
        "dimacs_hash": hashlib.sha256(DIMACS.read_bytes()).hexdigest() == raw["encoding"]["dimacs_sha256"],
        "dimacs_shape": header == (raw["encoding"]["variables"], raw["encoding"]["clauses"]) and actual_clauses == header[1] and max_var == header[0],
        "primary_solver_unsat": raw["solver_records"][0]["solver"] == "glucose4" and raw["solver_records"][0]["sat"] is False,
        "malformed_controls": all(raw["malformed_controls"].values()),
        "parity_both_labels": raw["parity_controls"] == {"odd_models": 0, "even_models": 8},
        "transfer_open": raw["status"]["B1_B2_B3"] == "OPEN",
    }
    assert all(checks.values()), checks
    result = {
        "claim_id": "PEITL-EXACT-EIGHT-REFEREE304-VERIFY",
        "status": "PASS",
        "checks": checks,
        "check_count": len(checks),
        "source_model_count": models(clauses, n),
        "degree_pattern_count": len(cases),
        "dimacs": {"sha256": hashlib.sha256(DIMACS.read_bytes()).hexdigest(), "variables": header[0], "clauses": header[1]},
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "Independent artifact/control/topology audit; it does not independently prove each UNSAT solver answer or B1/B2/B3.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
