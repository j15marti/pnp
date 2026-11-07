#!/usr/bin/env python3
"""Adversarial replay of the recovered /341 affine-row namespace check.

The script mutates only K4's first two row-bearing AND3 nodes, which are the
two parents of the first XOR node.  It invokes the recovered historical
verifier as an external process for every trial.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(obj: object) -> bytes:
    return (json.dumps(obj, indent=2) + "\n").encode()


def run_checker(checker: Path, obj: object) -> dict:
    payload = encode(obj)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        fh.write(payload)
        path = Path(fh.name)
    started = time.perf_counter_ns()
    try:
        cp = subprocess.run(
            ["node", str(checker), str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    finally:
        path.unlink(missing_ok=True)
    return {
        "accepted": cp.returncode == 0,
        "returncode": cp.returncode,
        "elapsed_ns": time.perf_counter_ns() - started,
        "certificate_bytes": len(payload),
        "certificate_sha256": digest(payload),
        "stdout_sha256": digest(cp.stdout),
        "stdout_bytes": len(cp.stdout),
        "stderr_excerpt": cp.stderr.decode(errors="replace")[-500:],
    }


def graph_width(fixture: dict) -> int:
    return len(fixture["graph"]["edges"])


def row_nodes(fixture: dict) -> list[dict]:
    return [p for p in fixture["proof"] if p.get("rule") == "AND3" and "row" in p]


def xor_mask(node: dict, bit: int) -> None:
    node["row"]["mask"] = hex(int(node["row"]["mask"], 16) ^ (1 << bit))


def project_rows(packet: dict) -> dict:
    out = copy.deepcopy(packet)
    for fixture in out["fixtures"]:
        width = graph_width(fixture)
        keep = (1 << width) - 1
        for node in fixture["proof"]:
            if "row" in node:
                node["row"]["mask"] = hex(int(node["row"]["mask"], 16) & keep)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", required=True, type=Path)
    ap.add_argument("--certificate", required=True, type=Path)
    args = ap.parse_args()

    raw = args.certificate.read_bytes()
    base = json.loads(raw)
    k4 = base["fixtures"][0]
    assert k4["graph"]["name"] == "K4"
    width = graph_width(k4)
    rows = row_nodes(k4)
    assert [p["id"] for p in rows[:2]] == ["d2", "d5"]
    assert k4["proof"][12]["id"] == "d12"
    assert k4["proof"][12]["parents"] == ["d2", "d5"]

    baseline = run_checker(args.checker, base)
    assert baseline["accepted"]
    baseline_stdout = baseline["stdout_sha256"]

    trials = []
    largest = None
    for bit in [width, 64, 1024, 8192]:
        mutant = copy.deepcopy(base)
        mrows = row_nodes(mutant["fixtures"][0])
        xor_mask(mrows[0], bit)
        xor_mask(mrows[1], bit)
        result = run_checker(args.checker, mutant)
        result.update({
            "name": f"paired_ghost_bit_{bit}",
            "ghost_bit": bit,
            "mutated_nodes": [mrows[0]["id"], mrows[1]["id"]],
            "proof_nodes": len(mutant["fixtures"][0]["proof"]),
            "same_checker_summary": result["stdout_sha256"] == baseline_stdout,
            "byte_delta_from_serialized_baseline": result["certificate_bytes"] - baseline["certificate_bytes"],
        })
        assert result["accepted"]
        assert result["same_checker_summary"]
        projected = project_rows(mutant)
        projection_result = run_checker(args.checker, projected)
        result["projection"] = {
            "equals_original_object": projected == base,
            "accepted": projection_result["accepted"],
            "node_count_preserved": len(projected["fixtures"][0]["proof"]) == len(k4["proof"]),
            "certificate_sha256": projection_result["certificate_sha256"],
        }
        assert all(result["projection"].values())
        trials.append(result)
        largest = mutant

    single = copy.deepcopy(base)
    xor_mask(row_nodes(single["fixtures"][0])[0], 64)
    single_result = run_checker(args.checker, single)
    assert not single_result["accepted"]

    illegal_low = copy.deepcopy(base)
    first = row_nodes(illegal_low["fixtures"][0])[0]
    illegal_bit = next(e for e in range(width) if e not in first["support"])
    xor_mask(first, illegal_bit)
    illegal_low_result = run_checker(args.checker, illegal_low)
    assert not illegal_low_result["accepted"]

    malformed = copy.deepcopy(base)
    row_nodes(malformed["fixtures"][0])[0]["row"]["mask"] = "0xnothex"
    malformed_result = run_checker(args.checker, malformed)
    assert not malformed_result["accepted"]

    assert largest is not None
    mutation_delta = {
        "base_blob_sha256": digest(raw),
        "fixture": "K4",
        "declared_edge_width": width,
        "operations": [
            {
                "node_id": p["id"],
                "before_mask": row_nodes(k4)[i]["row"]["mask"],
                "after_mask": p["row"]["mask"],
                "operation": "mask XOR (1 << 8192)",
            }
            for i, p in enumerate(row_nodes(largest["fixtures"][0])[:2])
        ],
        "mutated_full_packet_sha256": digest(encode(largest)),
    }

    output = {
        "run": "LSPV-5/414",
        "status": "PROVED/RESTRICTED + COMPUTATIONAL EXACT REPLAY",
        "checker": {
            "path": str(args.checker),
            "sha256": digest(args.checker.read_bytes()),
        },
        "certificate": {
            "path": str(args.certificate),
            "sha256": digest(raw),
            "bytes": len(raw),
        },
        "baseline": baseline,
        "paired_ghost_trials": trials,
        "hostile_controls": {
            "single_ghost_rejected": not single_result["accepted"],
            "single_ghost_stderr": single_result["stderr_excerpt"],
            "illegal_in_range_bit_rejected": not illegal_low_result["accepted"],
            "illegal_in_range_bit": illegal_bit,
            "illegal_in_range_stderr": illegal_low_result["stderr_excerpt"],
            "malformed_mask_rejected": not malformed_result["accepted"],
            "malformed_mask_stderr": malformed_result["stderr_excerpt"],
        },
        "exact_mutation_delta": mutation_delta,
        "symbolic_repair": {
            "map": "P_E(mask) = mask AND ((1 << E) - 1)",
            "xor_homomorphism": "P_E(a XOR b) = P_E(a) XOR P_E(b)",
            "and3_truth_tables_unchanged": True,
            "sink_preserved": True,
            "node_count_preserved": True,
            "scope": "nonnegative integer masks in the recovered source/AND3/XOR checker only",
        },
        "logical_conclusion": "Out-of-range mask coordinates are not namespace-checked by AND3. Equal paired ghosts cancel at the first XOR and are accepted at unchanged paid-node work. Projection deletes them cost-preservingly, so this is an evidence-bit/checker-canonicalization defect, not a proof-size shortcut or lower bound.",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
