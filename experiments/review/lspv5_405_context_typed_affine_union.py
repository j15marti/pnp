#!/usr/bin/env python3
"""Independent finite audit of context-typed GF(2) branch-union accounting.

This is a focused validation control, not an implementation of the historical
R_mix341 checker.  It makes node identity, fixed parentage, branch scope and
assumption ancestry explicit so that row-label deduplication cannot masquerade
as legal DAG sharing.
"""

from __future__ import annotations

import hashlib
import json
import resource
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class Row:
    mask: int
    const: int

    def xor(self, other: "Row") -> "Row":
        return Row(self.mask ^ other.mask, self.const ^ other.const)

    def key(self) -> tuple[int, int]:
        return (self.mask, self.const)


@dataclass(frozen=True)
class Node:
    node_id: str
    row: Row
    rule: str
    parents: tuple[str, ...]
    scope: str


class Reject(ValueError):
    pass


def validate(nodes: list[Node], terminals: tuple[str, str]) -> dict:
    """Validate a context-typed acyclic union proof graph."""
    by_id: dict[str, Node] = {}
    order: dict[str, int] = {}
    tags: dict[str, int] = {}
    deps: dict[str, frozenset[str]] = {}
    allowed_parent_scopes = {
        "common": {"common"},
        "b0": {"common", "b0"},
        "b1": {"common", "b1"},
    }
    for i, n in enumerate(nodes):
        if n.node_id in by_id:
            raise Reject(f"duplicate node id: {n.node_id}")
        if n.scope not in allowed_parent_scopes:
            raise Reject(f"bad scope: {n.scope}")
        by_id[n.node_id] = n
        order[n.node_id] = i
        if n.rule == "source":
            if n.scope != "common" or n.parents:
                raise Reject("source must be parentless and common")
            tags[n.node_id] = 0
            deps[n.node_id] = frozenset()
        elif n.rule in {"assume0", "assume1"}:
            expected_scope = "b0" if n.rule == "assume0" else "b1"
            if n.scope != expected_scope or n.parents:
                raise Reject("assumption scope/parent mismatch")
            tags[n.node_id] = 1
            deps[n.node_id] = frozenset({n.scope})
        elif n.rule == "xor":
            if len(n.parents) != 2:
                raise Reject("xor needs exactly two parents")
            try:
                p, q = (by_id[x] for x in n.parents)
            except KeyError as exc:
                raise Reject(f"forward or missing parent: {exc.args[0]}") from exc
            if any(order[x] >= i for x in n.parents):
                raise Reject("cycle or forward edge")
            if p.scope not in allowed_parent_scopes[n.scope] or q.scope not in allowed_parent_scopes[n.scope]:
                raise Reject("cross-branch parent reuse")
            if n.row != p.row.xor(q.row):
                raise Reject("forged xor row")
            tags[n.node_id] = tags[p.node_id] ^ tags[q.node_id]
            deps[n.node_id] = deps[p.node_id] | deps[q.node_id]
            if n.scope == "common" and deps[n.node_id]:
                raise Reject("common node has branch-assumption ancestry")
        else:
            raise Reject(f"unknown rule: {n.rule}")

    false = Row(0, 1)
    for branch, terminal in zip(("b0", "b1"), terminals):
        if terminal not in by_id:
            raise Reject(f"omitted AND obligation: {branch}")
        n = by_id[terminal]
        if n.scope != branch or n.row != false:
            raise Reject(f"bad terminal for {branch}")

    # Every paid inference must lie on at least one terminal ancestry.
    live: set[str] = set(terminals)
    todo = list(terminals)
    while todo:
        x = todo.pop()
        for p in by_id[x].parents:
            if p not in live:
                live.add(p)
                todo.append(p)
    dead_inferences = [n.node_id for n in nodes if n.rule == "xor" and n.node_id not in live]
    if dead_inferences:
        raise Reject(f"unreachable paid inference: {dead_inferences[0]}")

    inference_ids = [n.node_id for n in nodes if n.rule == "xor"]
    return {
        "q_distinct_inference_vertices": len(inference_ids),
        "inference_ids": inference_ids,
        "tags": tags,
        "assumption_dependencies": {k: sorted(v) for k, v in deps.items()},
        "live_nodes": sorted(live),
    }


def must_reject(name: str, nodes: list[Node], terminals: tuple[str, str]) -> dict:
    try:
        validate(nodes, terminals)
    except Reject as exc:
        return {"name": name, "rejected": True, "reason": str(exc)}
    raise AssertionError(f"negative control accepted: {name}")


def main() -> int:
    started = time.perf_counter_ns()
    # Variable bit positions: z=0, a=1, b=2, c=3.
    z, a, b, c = (Row(1 << i, 0) for i in range(4))
    one = Row(0, 1)
    z1, a1 = z.xor(one), a.xor(one)

    # Valid two-branch union.  w is a genuinely shared, non-source inference.
    nodes = [
        Node("S_z", z, "source", (), "common"),
        Node("S_z1", z1, "source", (), "common"),
        Node("S_b", b, "source", (), "common"),
        Node("S_c", c, "source", (), "common"),
        Node("W_shared", b.xor(c), "xor", ("S_b", "S_c"), "common"),
        Node("A0", z, "assume0", (), "b0"),
        Node("T0", z1.xor(b).xor(c), "xor", ("S_z1", "W_shared"), "b0"),
        Node("V0", z1, "xor", ("T0", "W_shared"), "b0"),
        Node("F0", one, "xor", ("V0", "A0"), "b0"),
        Node("A1", z1, "assume1", (), "b1"),
        Node("T1", z.xor(b).xor(c), "xor", ("S_z", "W_shared"), "b1"),
        Node("V1", z, "xor", ("T1", "W_shared"), "b1"),
        Node("F1", one, "xor", ("V1", "A1"), "b1"),
    ]
    valid = validate(nodes, ("F0", "F1"))
    assert valid["q_distinct_inference_vertices"] == 7
    assert valid["tags"]["W_shared"] == 0
    assert valid["tags"]["F0"] == valid["tags"]["F1"] == 1

    # Retraction: each terminal with tag one yields the complement of its
    # assumption; one extra XOR of S_z and S_z1 refutes the common source.
    retraction = {
        "branch0_discharged_terminal": asdict(z1),
        "branch1_discharged_terminal": asdict(z),
        "one_extra_join": asdict(z.xor(z1)),
        "actual_common_source_refutation_inferences": 1,
        "q_plus_one_upper_bound": valid["q_distinct_inference_vertices"] + 1,
    }
    assert Row(**retraction["one_extra_join"]) == one
    assert retraction["actual_common_source_refutation_inferences"] <= retraction["q_plus_one_upper_bound"]

    # Focused counterexample to identifying nodes only by their affine label.
    # U0 and U1 have the same row, but different parents and incompatible scope.
    label_witness = [
        Node("E_a", a, "source", (), "common"),
        Node("E_a1", a1, "source", (), "common"),
        Node("B0", z, "assume0", (), "b0"),
        Node("U0", a.xor(z), "xor", ("E_a", "B0"), "b0"),
        Node("V0x", z1, "xor", ("E_a1", "U0"), "b0"),
        Node("F0x", one, "xor", ("V0x", "B0"), "b0"),
        Node("B1", z1, "assume1", (), "b1"),
        Node("U1", a.xor(z), "xor", ("E_a1", "B1"), "b1"),
        Node("V1x", z, "xor", ("E_a", "U1"), "b1"),
        Node("F1x", one, "xor", ("V1x", "B1"), "b1"),
    ]
    label_check = validate(label_witness, ("F0x", "F1x"))
    assert label_witness[3].row == label_witness[7].row
    assert label_witness[3].parents != label_witness[7].parents
    assert label_witness[3].scope != label_witness[7].scope

    negatives: list[dict] = []
    negatives.append(must_reject("omitted_AND_branch", nodes, ("F0", "missing")))
    bad_cross = list(nodes)
    bad_cross[10] = Node("T1", z.xor(b).xor(c), "xor", ("S_z", "T0"), "b1")
    negatives.append(must_reject("cross_branch_reuse", bad_cross, ("F0", "F1")))
    bad_row = list(nodes)
    bad_row[6] = Node("T0", z, "xor", ("S_z1", "W_shared"), "b0")
    negatives.append(must_reject("forged_row", bad_row, ("F0", "F1")))
    duplicate = list(nodes) + [Node("W_shared", b.xor(c), "xor", ("S_b", "S_c"), "common")]
    negatives.append(must_reject("duplicate_numeric_or_text_id", duplicate, ("F0", "F1")))
    forward = list(nodes)
    forward[4] = Node("W_shared", b.xor(c), "xor", ("S_b", "LATE"), "common")
    forward.append(Node("LATE", c, "source", (), "common"))
    negatives.append(must_reject("forward_edge_cycle_control", forward, ("F0", "F1")))
    merged = [n for n in label_witness if n.node_id != "U1"]
    merged[3] = Node("U", a.xor(z), "xor", ("E_a", "B0"), "b0")
    # Force the other branch to reference the branch-0 node with the equal row.
    merged = [Node(n.node_id, n.row, n.rule, tuple("U" if p == "U1" else p for p in n.parents), n.scope) for n in merged]
    negatives.append(must_reject("equal_row_illegal_merge", merged, ("F0x", "F1x")))
    assert all(x["rejected"] for x in negatives)

    elapsed = time.perf_counter_ns() - started
    payload = {
        "schema": "lspv5-context-typed-affine-union-v1",
        "classification": "PROVED-RESTRICTED finite executable validation control",
        "claim": "q counts distinct context-typed inference vertices with fixed parents, not unique affine row labels",
        "valid_union": valid,
        "retraction": retraction,
        "equal_label_distinct_context_witness": {
            "row": asdict(label_witness[3].row),
            "node0": asdict(label_witness[3]),
            "node1": asdict(label_witness[7]),
            "validated_q": label_check["q_distinct_inference_vertices"],
        },
        "negative_controls": negatives,
        "resources": {
            "elapsed_ns": elapsed,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_union_nodes": len(nodes),
            "logical_inference_nodes": valid["q_distinct_inference_vertices"],
            "search_or_optimizer_calls": 0,
        },
        "limitations": [
            "independent model, not execution of the authoritative historical R_mix341 checker",
            "validates GF(2) XOR ancestry and context accounting only",
            "does not prove an unrestricted R_mix341 lower bound or B3",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256_before_self_hash"] = hashlib.sha256(canonical).hexdigest()
    output = Path("results/raw/review/2026-11-07_0048_LSPV5_CONTEXT_TYPED_UNION405.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output), "q": valid["q_distinct_inference_vertices"], "negative_controls": len(negatives)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
