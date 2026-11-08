#!/usr/bin/env python3
"""LSPV-5/435: exact recovered /341 checker unknown-field malleability audit.

Runs the unmodified recovered checker against the exact balanced accepted packet.
Branch/context/discharge-looking JSON fields are deliberately adversarial metadata:
acceptance means only that the checker ignores them, not that it authenticates them.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import resource
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "experiments/arc/lspv2_341_independent_verify.js"
PACKET = ROOT / "results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json"
if not CHECKER.exists():  # scratch-only materialization used during this audit
    CHECKER = ROOT / "tmp_native/lspv2_341_independent_verify.js"
if not PACKET.exists():
    PACKET = ROOT / "tmp_native/balanced_packet.json"
EXPECTED_CHECKER_BLOB = "fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"
EXPECTED_PACKET_BLOB = "481423a2f5271ab600bbc2f9a526fe62523239a9"


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def run_bytes(packet_bytes: bytes) -> tuple[int, bytes, bytes]:
    with tempfile.NamedTemporaryFile(prefix="lspv5_435_", suffix=".json", delete=False) as f:
        f.write(packet_bytes)
        name = f.name
    try:
        p = subprocess.run(
            ["node", str(CHECKER), name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=15,
        )
        return p.returncode, p.stdout, p.stderr
    finally:
        os.unlink(name)


def encoded(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=False) + "\n").encode()


def main() -> None:
    started = time.perf_counter_ns()
    checker_bytes = CHECKER.read_bytes()
    packet_bytes = PACKET.read_bytes()
    assert git_blob_sha1(checker_bytes) == EXPECTED_CHECKER_BLOB
    assert git_blob_sha1(packet_bytes) == EXPECTED_PACKET_BLOB
    base = json.loads(packet_bytes)
    rc, baseline_out, baseline_err = run_bytes(packet_bytes)
    assert rc == 0 and not baseline_err
    baseline = json.loads(baseline_out)
    assert baseline["checks"] == 30714

    accepted: list[dict[str, object]] = []

    def accepts(name: str, mutate) -> None:
        v = copy.deepcopy(base)
        mutate(v)
        raw = encoded(v)
        code, out, err = run_bytes(raw)
        assert code == 0, (name, err.decode(errors="replace"))
        assert out == baseline_out, name
        accepted.append({
            "name": name,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "stdout_identical_to_baseline": True,
        })

    accepts("forged_version_and_definition", lambda v: (
        v.__setitem__("version", "FORGED-Rmix341-WITH-SPLIT-DISCHARGE/v999"),
        v.__setitem__("definition", "claims native SPLIT, ASSUME, WEAKEN and DISCHARGE"),
    ))
    accepts("cyclic_ignored_branch_dag", lambda v: v.__setitem__("branchDAG", {
        "nodes": ["left", "right"], "edges": [["left", "right"], ["right", "left"]],
        "and_cases_discharged": ["left"], "omitted_required_case": "right",
    }))
    accepts("one_sided_context_on_every_inference", lambda v: [
        p.__setitem__("context", ["x=1"]) for f in v["fixtures"] for p in f["proof"]
    ])
    accepts("inconsistent_context_at_sink", lambda v: [
        f["proof"][-1].update({"context": ["x=0", "x=1"], "branch_local": True})
        for f in v["fixtures"]
    ])
    accepts("fake_discharge_annotations", lambda v: [
        p.update({"assumptions": ["x=1"], "discharged": ["x=1"], "join": "AND"})
        for f in v["fixtures"] for p in f["proof"][-2:]
    ])
    accepts("branch_local_sources", lambda v: [
        c.update({"context": ["x=0"], "branch_local": True})
        for f in v["fixtures"] for c in f["clauses"][::2]
    ])
    accepts("cross_branch_reuse_claim", lambda v: [
        f["proof"][0].update({"declared_context": "left"}) or
        f["proof"][1].update({"declared_context": "right", "reuses": f["proof"][0]["id"]})
        for f in v["fixtures"]
    ])
    accepts("fake_rule_alias_field", lambda v: [
        p.update({"rule_alias": "DISCHARGE", "paid_weight_override": 0})
        for f in v["fixtures"] for p in f["proof"]
    ])

    rejected: list[dict[str, object]] = []

    def rejects(name: str, mutate) -> None:
        v = copy.deepcopy(base)
        mutate(v)
        raw = encoded(v)
        code, out, err = run_bytes(raw)
        assert code != 0, name
        rejected.append({
            "name": name,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "stderr_prefix": err.decode(errors="replace")[:180],
        })

    rejects("actual_rule_changed_to_SPLIT", lambda v: v["fixtures"][0]["proof"][0].__setitem__("rule", "SPLIT"))
    rejects("actual_parent_removed", lambda v: v["fixtures"][0]["proof"][0].__setitem__("parents", v["fixtures"][0]["proof"][0]["parents"][:1]))
    rejects("actual_sink_corrupted", lambda v: v["fixtures"][0]["proof"][-1]["row"].__setitem__("rhs", 0))
    rejects("actual_source_corrupted", lambda v: v["fixtures"][0]["clauses"][0]["literals"].__setitem__(0, 999))

    result = {
        "run": "LSPV-5/435",
        "status": "PROVED/RESTRICTED source-code theorem + COMPUTATIONAL exact-checker replay; P versus NP OPEN",
        "checker_git_blob": git_blob_sha1(checker_bytes),
        "packet_git_blob": git_blob_sha1(packet_bytes),
        "packet_bytes": len(packet_bytes),
        "baseline_stdout_sha256": hashlib.sha256(baseline_out).hexdigest(),
        "baseline_checks": baseline["checks"],
        "accepted_unknown_field_mutants": accepted,
        "rejected_semantic_field_mutants": rejected,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "theorem": (
            "For this recovered checker, validation depends only on the accessed graph/charge/clause/proof/deletion/witness fields. "
            "Arbitrary extra JSON metadata, including branch/context/discharge-looking fields and top-level version/definition strings, "
            "is observationally irrelevant. Acceptance authenticates only the unconditional SOURCE/AND3/XOR semantics actually read."
        ),
        "limitation": (
            "This is not an unsound accepted refutation: every accepted mutant has the same checked unconditional proof. "
            "It is a provenance/schema malleability counterexample to treating ignored annotations as authenticated native rules."
        ),
        "elapsed_ns": time.perf_counter_ns() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
