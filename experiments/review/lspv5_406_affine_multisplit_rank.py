#!/usr/bin/env python3
"""Context-typed k-split GF(2) retraction and rank-compression audit.

This is an independent restricted model, not the historical R_mix341 checker.
It validates the q+k theorem on explicit full-cube branch unions and rejects
scope, identity, row, AND-obligation, and rank-certificate corruptions.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Row:
    mask: int
    const: int

    def xor(self, other: "Row") -> "Row":
        return Row(self.mask ^ other.mask, self.const ^ other.const)

    def packed(self, k: int) -> int:
        return self.mask | (self.const << k)


@dataclass(frozen=True)
class Node:
    node_id: str
    row: Row
    rule: str
    parents: tuple[str, ...]
    scope: str
    assumption_index: int | None = None


class Reject(ValueError):
    pass


def branch_name(bits: int, k: int) -> str:
    return "b" + format(bits, f"0{k}b")


def validate(nodes: list[Node], terminals: dict[str, str], k: int) -> dict:
    by_id: dict[str, Node] = {}
    tags: dict[str, int] = {}
    order: dict[str, int] = {}
    for pos, n in enumerate(nodes):
        if n.node_id in by_id:
            raise Reject(f"duplicate node id: {n.node_id}")
        by_id[n.node_id] = n
        order[n.node_id] = pos
        if n.rule == "source":
            if n.scope != "common" or n.parents or n.assumption_index is not None:
                raise Reject("bad common source")
            tags[n.node_id] = 0
        elif n.rule == "assume":
            if n.scope == "common" or n.parents:
                raise Reject("bad branch assumption")
            if n.assumption_index is None or not 0 <= n.assumption_index < k:
                raise Reject("bad assumption index")
            bits = int(n.scope[1:], 2)
            expected = Row(1 << n.assumption_index, (bits >> n.assumption_index) & 1)
            if n.row != expected:
                raise Reject("assumption row does not match branch label")
            tags[n.node_id] = 1 << n.assumption_index
        elif n.rule == "xor":
            if len(n.parents) != 2:
                raise Reject("xor arity")
            if any(p not in by_id for p in n.parents):
                raise Reject("missing or forward parent")
            if any(order[p] >= pos for p in n.parents):
                raise Reject("cycle or forward edge")
            a, b = (by_id[p] for p in n.parents)
            allowed = {"common"} if n.scope == "common" else {"common", n.scope}
            if a.scope not in allowed or b.scope not in allowed:
                raise Reject("cross-branch reuse")
            if n.row != a.row.xor(b.row):
                raise Reject("forged xor row")
            tags[n.node_id] = tags[a.node_id] ^ tags[b.node_id]
            if n.scope == "common" and tags[n.node_id] != 0:
                raise Reject("common inference has assumption ancestry")
        else:
            raise Reject(f"unknown rule: {n.rule}")

    expected_scopes = {branch_name(bits, k) for bits in range(1 << k)}
    if set(terminals) != expected_scopes:
        raise Reject("omitted or extra AND branch")
    for scope, terminal in terminals.items():
        if terminal not in by_id:
            raise Reject("missing terminal")
        n = by_id[terminal]
        if n.scope != scope or n.row != Row(0, 1):
            raise Reject("bad branch terminal")

    live: set[str] = set(terminals.values())
    todo = list(live)
    while todo:
        for p in by_id[todo.pop()].parents:
            if p not in live:
                live.add(p)
                todo.append(p)
    dead_paid = [n.node_id for n in nodes if n.rule == "xor" and n.node_id not in live]
    if dead_paid:
        raise Reject(f"unreachable paid inference: {dead_paid[0]}")

    discharged: dict[str, Row] = {}
    for scope, terminal in terminals.items():
        bits = int(scope[1:], 2)
        r = by_id[terminal].row
        tag = tags[terminal]
        for i in range(k):
            if tag >> i & 1:
                r = r.xor(Row(1 << i, bits >> i & 1))
        discharged[scope] = r
        # The discharged row must be false at its own branch assignment.
        if ((r.mask & bits).bit_count() ^ r.const) != 1:
            raise Reject("discharged terminal does not exclude its branch")

    q = sum(n.rule == "xor" for n in nodes)
    return {
        "q_distinct_context_typed_inferences": q,
        "tags": tags,
        "discharged": {s: {"mask": r.mask, "const": r.const} for s, r in discharged.items()},
        "live_nodes": len(live),
    }


def minimal_constant_one_subset(rows: list[Row], k: int) -> tuple[int, ...]:
    unique: list[Row] = []
    seen: set[tuple[int, int]] = set()
    for r in rows:
        key = (r.mask, r.const)
        if key not in seen:
            seen.add(key)
            unique.append(r)
    target = 1 << k
    for size in range(1, min(k + 1, len(unique)) + 1):
        for idxs in itertools.combinations(range(len(unique)), size):
            total = 0
            for i in idxs:
                total ^= unique[i].packed(k)
            if total == target:
                return idxs
    raise Reject("discharged affine rows do not span contradiction")


def span_contains_one(rows: list[Row], k: int) -> bool:
    """Gaussian XOR basis test in the (k+1)-dimensional augmented space."""
    basis = [0] * (k + 1)
    for row in rows:
        x = row.packed(k)
        while x:
            p = x.bit_length() - 1
            if basis[p]:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    x = 1 << k
    while x:
        p = x.bit_length() - 1
        if basis[p]:
            x ^= basis[p]
        else:
            return False
    return True


def exhaustive_affine_cover_audit(k: int) -> dict:
    """Enumerate every subset of affine rows for k<=3.

    Any subset that excludes every cube assignment must span 0=1.  This is a
    finite adversarial check of the coverage-to-inconsistency step, not the
    proof of the general theorem.
    """
    rows = [Row(mask, const) for mask in range(1 << k) for const in (0, 1)]
    full = (1 << (1 << k)) - 1
    cover_masks = []
    for r in rows:
        cover = 0
        for bits in range(1 << k):
            if ((r.mask & bits).bit_count() ^ r.const) & 1:
                cover |= 1 << bits
        cover_masks.append(cover)
    covering = 0
    failures = 0
    for subset in range(1 << len(rows)):
        cover = 0
        chosen: list[Row] = []
        for i, r in enumerate(rows):
            if subset >> i & 1:
                cover |= cover_masks[i]
                chosen.append(r)
        if cover == full:
            covering += 1
            if not span_contains_one(chosen, k):
                failures += 1
    assert failures == 0
    return {
        "k": k,
        "affine_rows": len(rows),
        "subsets_checked": 1 << len(rows),
        "cube_covering_subsets": covering,
        "coverage_without_constant_one_span": failures,
    }


def construct(k: int) -> tuple[list[Node], dict[str, str], dict]:
    nodes: list[Node] = []
    by_id: dict[str, Node] = {}

    def add(n: Node) -> str:
        nodes.append(n)
        by_id[n.node_id] = n
        return n.node_id

    # Common inconsistent affine source: x_i=0 for all i, and sum_i x_i=1.
    source_ids = [add(Node(f"S{i}", Row(1 << i, 0), "source", (), "common")) for i in range(k)]
    sum_source = add(Node("Ssum1", Row((1 << k) - 1, 1), "source", (), "common"))
    p = add(Node("Sp", Row(1 << k, 0), "source", (), "common"))
    qsrc = add(Node("Sq", Row(1 << (k + 1), 0), "source", (), "common"))
    wrow = by_id[p].row.xor(by_id[qsrc].row)
    w = add(Node("W_shared", wrow, "xor", (p, qsrc), "common"))

    terminals: dict[str, str] = {}
    for bits in range(1 << k):
        scope = branch_name(bits, k)
        assumptions = [
            add(Node(f"A_{bits}_{i}", Row(1 << i, bits >> i & 1), "assume", (), scope, i))
            for i in range(k)
        ]
        if bits:
            chosen = (bits & -bits).bit_length() - 1
            u = source_ids[chosen]
        else:
            chosen = None
            u = sum_source
        trow = by_id[u].row.xor(wrow)
        t = add(Node(f"T_{bits}", trow, "xor", (u, w), scope))
        v = add(Node(f"V_{bits}", by_id[u].row, "xor", (t, w), scope))
        cur = v
        if chosen is not None:
            nr = by_id[cur].row.xor(by_id[assumptions[chosen]].row)
            cur = add(Node(f"F_{bits}", nr, "xor", (cur, assumptions[chosen]), scope))
        else:
            for i, aid in enumerate(assumptions):
                nr = by_id[cur].row.xor(by_id[aid].row)
                cur = add(Node(f"Z_{bits}_{i}", nr, "xor", (cur, aid), scope))
        terminals[scope] = cur

    checked = validate(nodes, terminals, k)
    discharged_rows = [Row(**r) for r in checked["discharged"].values()]
    basis_idxs = minimal_constant_one_subset(discharged_rows, k)
    basis_rows: list[Row] = []
    unique: list[Row] = []
    seen: set[tuple[int, int]] = set()
    for r in discharged_rows:
        if (r.mask, r.const) not in seen:
            seen.add((r.mask, r.const))
            unique.append(r)
    basis_rows = [unique[i] for i in basis_idxs]
    total = Row(0, 0)
    for r in basis_rows:
        total = total.xor(r)
    assert total == Row(0, 1)
    expected_q = 3 * (1 << k) + k
    assert checked["q_distinct_context_typed_inferences"] == expected_q
    assert len(basis_rows) <= k + 1
    return nodes, terminals, {
        "k": k,
        "branches": 1 << k,
        "union_nodes": len(nodes),
        "q": expected_q,
        "unique_discharged_rows": len(unique),
        "basis_rows": [{"mask": r.mask, "const": r.const} for r in basis_rows],
        "extra_binary_joins": len(basis_rows) - 1,
        "q_plus_k_bound": expected_q + k,
        "shared_non_source_tag": checked["tags"]["W_shared"],
        "all_branches_excluded": True,
    }


def rejected(name: str, nodes: list[Node], terminals: dict[str, str], k: int) -> dict:
    try:
        validate(nodes, terminals, k)
    except Reject as exc:
        return {"name": name, "rejected": True, "reason": str(exc)}
    raise AssertionError(f"negative control accepted: {name}")


def main() -> int:
    started = time.perf_counter_ns()
    cases: list[dict] = []
    fixtures: dict[int, tuple[list[Node], dict[str, str]]] = {}
    for k in range(1, 7):
        nodes, terminals, summary = construct(k)
        fixtures[k] = (nodes, terminals)
        cases.append(summary)
    exhaustive = [exhaustive_affine_cover_audit(k) for k in (1, 2, 3)]

    nodes, terminals = fixtures[3]
    controls: list[dict] = []
    missing = dict(terminals)
    missing.pop(branch_name(7, 3))
    controls.append(rejected("omitted_AND_branch", nodes, missing, 3))
    dup = list(nodes) + [nodes[-1]]
    controls.append(rejected("duplicate_node_id", dup, terminals, 3))
    badrow = list(nodes)
    idx = next(i for i, n in enumerate(badrow) if n.node_id == "T_1")
    n = badrow[idx]
    badrow[idx] = Node(n.node_id, Row(0, 0), n.rule, n.parents, n.scope, n.assumption_index)
    controls.append(rejected("forged_row", badrow, terminals, 3))
    cross = list(nodes)
    idx = next(i for i, n in enumerate(cross) if n.node_id == "T_2")
    n = cross[idx]
    cross[idx] = Node(n.node_id, n.row, n.rule, ("V_1", n.parents[1]), n.scope, n.assumption_index)
    controls.append(rejected("cross_branch_reuse", cross, terminals, 3))
    badassume = list(nodes)
    idx = next(i for i, n in enumerate(badassume) if n.node_id == "A_5_0")
    n = badassume[idx]
    badassume[idx] = Node(n.node_id, Row(1, 0), n.rule, n.parents, n.scope, n.assumption_index)
    controls.append(rejected("branch_label_assumption_mismatch", badassume, terminals, 3))
    forward = list(nodes)
    idx = next(i for i, n in enumerate(forward) if n.node_id == "W_shared")
    n = forward[idx]
    forward[idx] = Node(n.node_id, n.row, n.rule, (n.parents[0], "F_7"), n.scope, n.assumption_index)
    controls.append(rejected("forward_or_cyclic_dependency", forward, terminals, 3))

    elapsed = time.perf_counter_ns() - started
    payload = {
        "schema": "lspv5-affine-multisplit-rank-v1",
        "classification": "PROVED-RESTRICTED theorem fixture; COMPUTATIONAL controls",
        "theorem": "context-typed k-split GF(2) union retracts with at most q+k paid XOR inferences",
        "cases": cases,
        "exhaustive_affine_cover_audit": exhaustive,
        "negative_controls": controls,
        "resources": {
            "elapsed_ns": elapsed,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "largest_k": cases[-1]["k"],
            "largest_branches": cases[-1]["branches"],
            "largest_union_nodes": cases[-1]["union_nodes"],
            "search_optimizer_calls": 0,
        },
        "limitations": [
            "independent GF(2) model, not authoritative historical R_mix341 execution",
            "assumes all 2^k branch obligations and immutable context-typed parent tuples",
            "does not cover RES, AND3, LOCAL-CONVERT or Boolean definitions",
            "does not prove full-mixed hardness, B3 or P versus NP",
        ],
    }
    prehash = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256_before_self_hash"] = hashlib.sha256(prehash).hexdigest()
    out = Path("results/raw/review/2026-11-07_0148_LSPV5_AFFINE_MULTISPLIT_RANK406.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "cases": len(cases), "max_k": 6, "negative_controls": len(controls), "output": str(out)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
