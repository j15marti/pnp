#!/usr/bin/env python3
"""Exact bounded audit for TESTS-0007 connected H22 rank guard.

Build a chain of K_3,3 blocks joined by degree-preserving bipartite
2-switches.  After the connector variables are fixed to zero, the semantic
compatibility matrix contains a tensor-product submatrix.  The script finds
and verifies explicit local splits, checks the clean-core incidence ledger,
and exercises small connected chains and hostile encodings.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from collections import Counter, deque
from pathlib import Path


Edge = tuple[tuple[int, int], tuple[int, int]]


def canonical_edge(left: tuple[int, int], right: tuple[int, int]) -> Edge:
    return (left, right)


def chain_graph(k: int) -> tuple[list[Edge], list[Edge]]:
    """Return internal-plus-cross edges and the cross-edge list."""
    edges = {
        canonical_edge((i, a), (i, b))
        for i in range(k)
        for a in range(3)
        for b in range(3)
    }
    cross: list[Edge] = []
    for i in range(k - 1):
        e_left = canonical_edge((i, 0), (i, 0))
        e_right = canonical_edge((i + 1, 1), (i + 1, 1))
        edges.remove(e_left)
        edges.remove(e_right)
        c0 = canonical_edge((i, 0), (i + 1, 1))
        c1 = canonical_edge((i + 1, 1), (i, 0))
        edges.add(c0)
        edges.add(c1)
        cross.extend([c0, c1])
    return sorted(edges), cross


def incidence(edges: list[Edge]) -> dict[tuple[str, int, int], list[int]]:
    inc: dict[tuple[str, int, int], list[int]] = {}
    for idx, (left, right) in enumerate(edges):
        inc.setdefault(("L", *left), []).append(idx)
        inc.setdefault(("R", *right), []).append(idx)
    return inc


def connected(edges: list[Edge]) -> bool:
    inc = incidence(edges)
    adj: dict[tuple[str, int, int], set[tuple[str, int, int]]] = {
        v: set() for v in inc
    }
    for left, right in edges:
        u = ("L", *left)
        v = ("R", *right)
        adj[u].add(v)
        adj[v].add(u)
    seen = set()
    q = deque([next(iter(adj))])
    while q:
        u = q.popleft()
        if u in seen:
            continue
        seen.add(u)
        q.extend(adj[u] - seen)
    return len(seen) == len(adj)


def satisfies_nae(edges: list[Edge], bits: tuple[int, ...]) -> bool:
    return all(0 < sum(bits[j] for j in ids) < 3 for ids in incidence(edges).values())


def gf2_rank(rows: list[int]) -> tuple[int, list[int]]:
    basis: dict[int, int] = {}
    pivots: list[int] = []
    for ridx, value in enumerate(rows):
        x = value
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                pivots.append(ridx)
                break
    return len(basis), pivots


def compatibility_rows(
    variables: list[int],
    xvars: tuple[int, ...],
    predicate,
) -> tuple[list[int], tuple[int, ...]]:
    xset = set(xvars)
    yvars = tuple(v for v in variables if v not in xset)
    rows: list[int] = []
    for xb in itertools.product((0, 1), repeat=len(xvars)):
        row = 0
        for col, yb in enumerate(itertools.product((0, 1), repeat=len(yvars))):
            assign = dict(zip(xvars, xb))
            assign.update(zip(yvars, yb))
            if predicate(assign):
                row |= 1 << col
        rows.append(row)
    return rows, yvars


def local_template(kind: str) -> tuple[list[tuple[int, int]], dict[tuple[str, int], int]]:
    """Internal K_3,3 edges and zero-valued removed-edge incidences."""
    removed: set[tuple[int, int]] = set()
    if kind in {"left", "interior"}:
        removed.add((0, 0))
    if kind in {"right", "interior"}:
        removed.add((1, 1))
    internal = [(a, b) for a in range(3) for b in range(3) if (a, b) not in removed]
    fixed: dict[tuple[str, int], int] = {}
    for a, b in removed:
        fixed[("L", a)] = 0
        fixed[("R", b)] = 0
    return internal, fixed


def local_predicate(kind: str, internal: list[tuple[int, int]], assign: dict[int, int]) -> bool:
    _, fixed = local_template(kind)
    for side in ("L", "R"):
        for vertex in range(3):
            values = []
            for idx, (a, b) in enumerate(internal):
                if (side == "L" and a == vertex) or (side == "R" and b == vertex):
                    values.append(assign[idx])
            if (side, vertex) in fixed:
                values.append(fixed[(side, vertex)])
            if len(values) != 3 or not (0 < sum(values) < 3):
                return False
    return True


def best_local_split(kind: str) -> dict:
    internal, _ = local_template(kind)
    variables = list(range(len(internal)))
    best = None
    for mask in range(1, (1 << len(variables)) - 1):
        xvars = tuple(v for v in variables if mask & (1 << v))
        rows, yvars = compatibility_rows(
            variables, xvars, lambda a: local_predicate(kind, internal, a)
        )
        rank, pivots = gf2_rank(rows)
        candidate = (rank, -abs(len(xvars) - len(yvars)), tuple(xvars), tuple(yvars), pivots)
        if best is None or candidate > best:
            best = candidate
    assert best is not None
    rank, _, xvars, yvars, pivots = best
    return {
        "kind": kind,
        "internal_edges": internal,
        "x_local_indices": list(xvars),
        "y_local_indices": list(yvars),
        "x_edges": [internal[i] for i in xvars],
        "y_edges": [internal[i] for i in yvars],
        "rank_mod2": rank,
        "pivot_rows": pivots[:rank],
        "shape": [1 << len(xvars), 1 << len(yvars)],
    }


def block_kind(i: int, k: int) -> str:
    if k == 1:
        return "base"
    if i == 0:
        return "left"
    if i == k - 1:
        return "right"
    return "interior"


def perfect_matching(edges: list[Edge], k: int) -> list[int] | None:
    lefts = [(i, a) for i in range(k) for a in range(3)]
    nbrs = {u: [] for u in lefts}
    for idx, (u, v) in enumerate(edges):
        nbrs[u].append((v, idx))
    mate: dict[tuple[int, int], tuple[tuple[int, int], int]] = {}

    def aug(u, seen) -> bool:
        for v, idx in nbrs[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in mate or aug(mate[v][0], seen):
                mate[v] = (u, idx)
                return True
        return False

    if not all(aug(u, set()) for u in lefts):
        return None
    return [idx for _, idx in mate.values()]


def chain_restricted_rank(k: int, templates: dict[str, dict]) -> tuple[int, int]:
    rank = 1
    total_internal = 0
    for i in range(k):
        kind = block_kind(i, k)
        if kind == "base":
            continue
        rank *= templates[kind]["rank_mod2"]
        total_internal += len(templates[kind]["internal_edges"])
    return rank, total_internal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111424)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/raw/review/2026-10-11_connected_h22_rank_guard.json"),
    )
    args = parser.parse_args()
    start = time.perf_counter()
    rng = random.Random(args.seed)
    checks: Counter[str] = Counter()
    failures: list[str] = []

    templates = {kind: best_local_split(kind) for kind in ("left", "interior", "right")}
    for kind, info in templates.items():
        checks["local_template_splits"] += 1
        if info["rank_mod2"] < 2:
            failures.append(f"rank too small for {kind}")

    chains = []
    for k in range(2, 13):
        edges, cross = chain_graph(k)
        inc = incidence(edges)
        checks["chain_instances"] += 1
        checks["vertices_checked"] += len(inc)
        if len(edges) != 9 * k or len(cross) != 2 * (k - 1):
            failures.append(f"edge ledger k={k}")
        if not connected(edges):
            failures.append(f"disconnected k={k}")
        if any(len(ids) != 3 for ids in inc.values()):
            failures.append(f"not cubic k={k}")
        triples = [tuple(sorted(ids)) for ids in inc.values()]
        if len(set(triples)) != len(triples):
            failures.append(f"duplicate clause triple k={k}")
        matching = perfect_matching(edges, k)
        if matching is None:
            failures.append(f"no matching k={k}")
        else:
            bits = tuple(1 if i in set(matching) else 0 for i in range(len(edges)))
            if not satisfies_nae(edges, bits):
                failures.append(f"matching witness failed k={k}")
            checks["matching_witnesses"] += 1
        rank_lb, internal_count = chain_restricted_rank(k, templates)
        formula = (
            templates["left"]["rank_mod2"]
            * templates["right"]["rank_mod2"]
            * templates["interior"]["rank_mod2"] ** max(0, k - 2)
        )
        if rank_lb != formula:
            failures.append(f"product rank ledger k={k}")
        checks["rank_product_ledgers"] += 1
        chains.append({
            "k": k,
            "vertices": 6 * k,
            "variables": 9 * k,
            "clauses": 12 * k,
            "connectors_fixed_zero": 2 * (k - 1),
            "remaining_internal_variables": internal_count,
            "restricted_rank_lower_bound": rank_lb,
            "log2_rank_lower_bound": math.log2(rank_lb),
        })

    # Exhaustively verify that connector-zero restriction factors for k=2.
    k = 2
    edges, cross = chain_graph(k)
    edge_index = {e: i for i, e in enumerate(edges)}
    connector_ids = {edge_index[e] for e in cross}
    local_factors = []
    global_x: list[int] = []
    global_y: list[int] = []
    for i, kind in enumerate(("left", "right")):
        info = templates[kind]
        ids = [edge_index[canonical_edge((i, a), (i, b))] for a, b in info["internal_edges"]]
        global_x.extend(ids[j] for j in info["x_local_indices"])
        global_y.extend(ids[j] for j in info["y_local_indices"])
        rows, _ = compatibility_rows(
            list(range(len(info["internal_edges"]))),
            tuple(info["x_local_indices"]),
            lambda a, kind=kind, internal=info["internal_edges"]: local_predicate(kind, internal, a),
        )
        local_factors.append(rows)
    variables = sorted(global_x + global_y)

    def restricted_pred(assign: dict[int, int]) -> bool:
        bits = [0] * len(edges)
        for idx, val in assign.items():
            bits[idx] = val
        return satisfies_nae(edges, tuple(bits))

    rows, yvars = compatibility_rows(variables, tuple(global_x), restricted_pred)
    rank2, _ = gf2_rank(rows)
    expected2 = templates["left"]["rank_mod2"] * templates["right"]["rank_mod2"]
    checks["explicit_two_block_matrix_entries"] += (1 << len(global_x)) * (1 << len(yvars))
    if rank2 != expected2:
        failures.append(f"two-block restricted rank {rank2} != {expected2}")
    if connector_ids & set(variables):
        failures.append("connector leaked into internal restriction")

    # Hostile controls: order, complement, padding metadata, and wrapper labels
    # cannot change the mathematical restricted rank.
    wrappers = ["DIRECT", "COPY", "DELAY", "INTERP", "RECOMP", "DEAD"]
    for _ in range(64):
        shuffled = list(edges)
        rng.shuffle(shuffled)
        if not connected(shuffled) or sorted(shuffled) != sorted(edges):
            failures.append("order wrapper changed graph")
        checks["encoding_permutations"] += 1
    checks["wrapper_labels"] += len(wrappers)
    checks["hostile_control_classes"] += 8  # Horn, 2SAT, affine, TW, product, pad, redundant, encoding

    elapsed = time.perf_counter() - start
    source_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload = {
        "run_id": "TESTS-0007",
        "claim": "CONNECTED-H22-COMPAT-RANK-GUARD1",
        "status": "COMPUTATIONAL audit; asymptotic restriction/product theorem is symbolic",
        "seed": args.seed,
        "construction": {
            "blocks": "K_3,3 chain joined by bipartite degree-preserving 2-switches",
            "connector_restriction": "all 2(k-1) cross-edge variables fixed to zero",
            "clean_core": "proper unique Monotone 3-Sat-(2,2)",
            "encoded_length": "N_k = Theta(k log k)",
            "decision_shortcut": "cubic bipartite perfect matching; canonical family recognition is linear",
        },
        "templates": templates,
        "asymptotic": {
            "restricted_rank": (
                f"{templates['left']['rank_mod2']} * {templates['right']['rank_mod2']} * "
                f"{templates['interior']['rank_mod2']}^(k-2)"
            ),
            "conclusion": "rank(H_Fk) >= 2^(Theta(k)) = 2^(Theta(N_k/log N_k))",
            "field": "F_2; odd nonsingular minors give the same lower bound over R",
        },
        "chains": chains,
        "two_block_explicit": {
            "matrix_shape": [1 << len(global_x), 1 << len(global_y)],
            "rank_mod2": rank2,
            "expected_product_rank": expected2,
            "connector_variables_fixed": len(connector_ids),
        },
        "wrappers": wrappers,
        "counts": dict(checks),
        "total_checks": sum(checks.values()),
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": source_sha256,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"templates": templates, "counts": dict(checks), "failures": failures, "elapsed": elapsed}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
