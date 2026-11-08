#!/usr/bin/env python3
"""Rebuild balanced native SOURCE/AND3/XOR proofs and replay the /341 checker.

This is a restricted-calc audit.  It does not define or extend R_mix341 and it
does not establish an all-rule lower bound or a P-versus-NP result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKET = ROOT / "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
DEFAULT_CHECKER = ROOT / "replay/413/lspv2_341_independent_verify.js"


def source_table(literals: list[int], support: list[int]) -> int:
    table = 0
    for assignment in range(1 << len(support)):
        bits = {edge: (assignment >> i) & 1 for i, edge in enumerate(support)}
        sat = any((lit > 0 and bits[abs(lit) - 1]) or
                  (lit < 0 and not bits[abs(lit) - 1]) for lit in literals)
        table |= int(bool(sat)) << assignment
    return table


def depth(proof: list[dict], source_ids: set[str]) -> int:
    d = {sid: 0 for sid in source_ids}
    for node in proof:
        assert len(node["parents"]) == 2
        assert all(parent in d for parent in node["parents"])
        d[node["id"]] = 1 + max(d[parent] for parent in node["parents"])
    return d[proof[-1]["id"]]


def balance_fixture(fixture: dict) -> tuple[dict, dict]:
    h = fixture["graph"]["n"]
    by_vertex: dict[int, list[dict]] = {v: [] for v in range(h)}
    for clause in fixture["clauses"]:
        by_vertex[clause["vertex"]].append(clause)

    # Authenticate the cubic strict-3-CNF source shape before rebuilding.
    assert len(fixture["clauses"]) == 4 * h
    assert all(len(group) == 4 for group in by_vertex.values())
    assert len(fixture["graph"]["edges"]) * 2 == 3 * h

    original_rows = {}
    for node in fixture["proof"]:
        if node["rule"] == "AND3" and "row" in node:
            support = tuple(sorted(node["support"]))
            original_rows[support] = node["row"]

    proof: list[dict] = []
    affine_frontier: list[str] = []
    rows: dict[str, tuple[int, int]] = {}
    next_id = 0

    def fresh(prefix: str) -> str:
        nonlocal next_id
        value = f"{prefix}{next_id}"
        next_id += 1
        return value

    for vertex in range(h):
        group = sorted(by_vertex[vertex], key=lambda c: c["id"])
        support = sorted(abs(lit) - 1 for lit in group[0]["literals"])
        assert all(sorted(abs(lit) - 1 for lit in c["literals"]) == support for c in group)
        tables = {c["id"]: source_table(c["literals"], support) for c in group}

        pair_ids = []
        for left, right in ((group[0], group[1]), (group[2], group[3])):
            node_id = fresh("ba")
            table = tables[left["id"]] & tables[right["id"]]
            proof.append({"id": node_id, "kind": "factor", "rule": "AND3",
                          "parents": [left["id"], right["id"]],
                          "support": support, "table": table})
            tables[node_id] = table
            pair_ids.append(node_id)

        final_id = fresh("ba")
        final_table = tables[pair_ids[0]] & tables[pair_ids[1]]
        row = original_rows[tuple(support)]
        proof.append({"id": final_id, "kind": "factor", "rule": "AND3",
                      "parents": pair_ids, "support": support,
                      "table": final_table, "row": row})
        rows[final_id] = (int(row["mask"], 16), int(row["rhs"]))
        affine_frontier.append(final_id)

    while len(affine_frontier) > 1:
        nxt = []
        for i in range(0, len(affine_frontier), 2):
            if i + 1 == len(affine_frontier):
                nxt.append(affine_frontier[i])
                continue
            left, right = affine_frontier[i:i + 2]
            mask = rows[left][0] ^ rows[right][0]
            rhs = rows[left][1] ^ rows[right][1]
            node_id = fresh("bx")
            row = {"mask": hex(mask), "rhs": rhs}
            proof.append({"id": node_id, "kind": "affine", "rule": "XOR",
                          "parents": [left, right], "row": row})
            rows[node_id] = (mask, rhs)
            nxt.append(node_id)
        affine_frontier = nxt

    assert rows[affine_frontier[0]] == (0, 1)
    assert len(proof) == 4 * h - 1
    source_ids = {c["id"] for c in fixture["clauses"]}
    new_depth = depth(proof, source_ids)
    lower_depth = math.ceil(math.log2(4 * h))
    assert new_depth == lower_depth

    rebuilt = dict(fixture)
    rebuilt["proof"] = proof
    metrics = {
        "name": fixture["graph"]["name"],
        "vertices": h,
        "source_clauses": 4 * h,
        "paid_nodes": len(proof),
        "old_depth": depth(fixture["proof"], source_ids),
        "balanced_depth": new_depth,
        "binary_fanin_depth_lower_bound": lower_depth,
        "all_source_clauses_essential": fixture["properties"]["essential"] == 4 * h,
        "certified_minimum": fixture["properties"]["predictedMinimum"],
    }
    return rebuilt, metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--checker", type=Path, default=DEFAULT_CHECKER)
    parser.add_argument("--write-balanced", type=Path)
    args = parser.parse_args()

    source_bytes = args.packet.read_bytes()
    packet = json.loads(source_bytes)
    rebuilt_fixtures, metrics = zip(*(balance_fixture(f) for f in packet["fixtures"]))
    balanced = dict(packet)
    balanced["fixtures"] = list(rebuilt_fixtures)
    balanced_bytes = (json.dumps(balanced, indent=2, sort_keys=True) + "\n").encode()

    target = args.write_balanced
    cleanup = False
    if target is None:
        handle = tempfile.NamedTemporaryFile(prefix="lspv5_427_", suffix=".json", delete=False)
        target = Path(handle.name)
        handle.close()
        cleanup = True
    target.write_bytes(balanced_bytes)
    run = subprocess.run(["node", str(args.checker), str(target)], check=True,
                         text=True, capture_output=True)
    checker_result = json.loads(run.stdout)
    if cleanup:
        target.unlink()

    result = {
        "status": "PASS",
        "scope": "recovered SOURCE/AND3/XOR subgrammar only",
        "source_packet_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "balanced_packet_sha256": hashlib.sha256(balanced_bytes).hexdigest(),
        "checker_sha256": hashlib.sha256(args.checker.read_bytes()).hexdigest(),
        "checker_checks": checker_result["checks"],
        "checker_malformed_controls": checker_result["malformed"],
        "checker_corruption_controls": checker_result["corruptions"],
        "fixtures": list(metrics),
        "theorem_boundary": {
            "completion_robust_upper_bound": "W_R(B_h) <= 4h-1 for every completion retaining these legal core derivations",
            "exact_minimum_condition": "W_R(B_h) = 4h-1 only under the separately proved essential-source/binary-parent hypotheses",
            "not_proved": ["full historical R_mix341 grammar", "superpolynomial all-rule lower bound", "noncircular B3", "P versus NP"],
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
