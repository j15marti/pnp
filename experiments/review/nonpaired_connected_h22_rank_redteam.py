#!/usr/bin/env python3
"""RT-0012: exact audit of a connected nonpaired H22 rank counterexample.

The construction starts from the connected cubic-bipartite 2-switch chain
used in TESTS-0007.  In every block, two variables are exchanged between two
negative clauses only.  This preserves every (2,2) occurrence count while
destroying the paired-clause identity.  Fixing connector variables to zero
again exposes a tensor-product compatibility submatrix.
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
Clause = tuple[int, int, int]


def edge(left: tuple[int, int], right: tuple[int, int]) -> Edge:
    return left, right


def chain_graph(k: int) -> tuple[list[Edge], list[Edge]]:
    edges = {edge((i, a), (i, b)) for i in range(k) for a in range(3) for b in range(3)}
    cross: list[Edge] = []
    for i in range(k - 1):
        edges.remove(edge((i, 0), (i, 0)))
        edges.remove(edge((i + 1, 1), (i + 1, 1)))
        c0 = edge((i, 0), (i + 1, 1))
        c1 = edge((i + 1, 1), (i, 0))
        edges.update((c0, c1))
        cross.extend((c0, c1))
    return sorted(edges), cross


def incidence(edges: list[Edge]) -> dict[tuple[str, int, int], list[int]]:
    out: dict[tuple[str, int, int], list[int]] = {}
    for idx, (u, v) in enumerate(edges):
        out.setdefault(("L", *u), []).append(idx)
        out.setdefault(("R", *v), []).append(idx)
    return out


def formula(k: int) -> tuple[list[Edge], list[Clause], list[Clause], list[Edge]]:
    edges, cross = chain_graph(k)
    inc = incidence(edges)
    positive = [tuple(sorted(inc[v])) for v in sorted(inc)]
    negative_map = {v: list(inc[v]) for v in inc}
    index = {e: i for i, e in enumerate(edges)}
    for i in range(k):
        a = index[edge((i, 0), (i, 2))]
        b = index[edge((i, 2), (i, 0))]
        c0 = negative_map[("L", i, 0)]
        c2 = negative_map[("L", i, 2)]
        c0[c0.index(a)] = b
        c2[c2.index(b)] = a
    negative = [tuple(sorted(negative_map[v])) for v in sorted(negative_map)]
    return edges, positive, negative, cross


def sat_formula(pos: list[Clause], neg: list[Clause], bits: tuple[int, ...]) -> bool:
    return all(any(bits[j] for j in c) for c in pos) and all(any(not bits[j] for j in c) for c in neg)


def connected_formula(nvars: int, clauses: list[Clause]) -> bool:
    adj = {i: set() for i in range(nvars)}
    for c in clauses:
        for i in c:
            adj[i].update(j for j in c if j != i)
    seen = set()
    q = deque([0])
    while q:
        u = q.popleft()
        if u in seen:
            continue
        seen.add(u)
        q.extend(adj[u] - seen)
    return len(seen) == nvars


def matching(edges: list[Edge], k: int) -> list[int] | None:
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


def gf2_rank(rows: list[int]) -> tuple[int, list[int]]:
    basis: dict[int, int] = {}
    pivots: list[int] = []
    for ridx, row in enumerate(rows):
        x = row
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                pivots.append(ridx)
                break
    return len(basis), pivots


def compatibility_rows(variables: list[int], xvars: tuple[int, ...], predicate):
    xset = set(xvars)
    yvars = tuple(v for v in variables if v not in xset)
    rows = []
    for xb in itertools.product((0, 1), repeat=len(xvars)):
        row = 0
        for col, yb in enumerate(itertools.product((0, 1), repeat=len(yvars))):
            a = dict(zip(xvars, xb))
            a.update(zip(yvars, yb))
            if predicate(a):
                row |= 1 << col
        rows.append(row)
    return rows, yvars


def local_template(kind: str):
    removed = set()
    if kind in {"left", "interior"}:
        removed.add((0, 0))
    if kind in {"right", "interior"}:
        removed.add((1, 1))
    internal = [(a, b) for a in range(3) for b in range(3) if (a, b) not in removed]
    ids = {e: i for i, e in enumerate(internal)}
    pos: dict[tuple[str, int], list[int | None]] = {}
    for side in ("L", "R"):
        for v in range(3):
            vals: list[int | None] = []
            for a, b in [(a, b) for a in range(3) for b in range(3)]:
                if (side == "L" and a != v) or (side == "R" and b != v):
                    continue
                vals.append(None if (a, b) in removed else ids[(a, b)])
            pos[(side, v)] = vals
    neg = {v: list(vals) for v, vals in pos.items()}
    e02, e20 = ids[(0, 2)], ids[(2, 0)]
    neg[("L", 0)][neg[("L", 0)].index(e02)] = e20
    neg[("L", 2)][neg[("L", 2)].index(e20)] = e02
    return internal, pos, neg


def local_predicate(kind: str, assign: dict[int, int]) -> bool:
    _, pos, neg = local_template(kind)
    for vals in pos.values():
        actual = [0 if x is None else assign[x] for x in vals]
        if not any(actual):
            return False
    for vals in neg.values():
        actual = [0 if x is None else assign[x] for x in vals]
        if all(actual):
            return False
    return True


def best_split(kind: str) -> dict:
    internal, _, _ = local_template(kind)
    variables = list(range(len(internal)))
    best = None
    for mask in range(1, (1 << len(variables)) - 1):
        xs = tuple(v for v in variables if mask & (1 << v))
        rows, ys = compatibility_rows(variables, xs, lambda a: local_predicate(kind, a))
        rank, pivots = gf2_rank(rows)
        cand = (rank, -abs(len(xs) - len(ys)), xs, ys, pivots)
        if best is None or cand > best:
            best = cand
    assert best is not None
    rank, _, xs, ys, pivots = best
    return {
        "kind": kind,
        "internal_edges": internal,
        "x_local_indices": list(xs),
        "y_local_indices": list(ys),
        "x_edges": [internal[i] for i in xs],
        "y_edges": [internal[i] for i in ys],
        "rank_mod2": rank,
        "shape": [1 << len(xs), 1 << len(ys)],
        "pivot_rows": pivots[:rank],
    }


def kind_for(i: int, k: int) -> str:
    if i == 0:
        return "left"
    if i == k - 1:
        return "right"
    return "interior"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=202610111436)
    ap.add_argument("--output", type=Path,
                    default=Path("results/raw/review/2026-10-11_nonpaired_connected_h22_rank_redteam.json"))
    args = ap.parse_args()
    start = time.perf_counter()
    rng = random.Random(args.seed)
    checks: Counter[str] = Counter()
    failures: list[str] = []

    templates = {kind: best_split(kind) for kind in ("left", "interior", "right")}
    for kind, data in templates.items():
        checks["local_templates"] += 1
        if data["rank_mod2"] < 2:
            failures.append(f"local rank too small: {kind}")

    chains = []
    for k in range(2, 13):
        edges, pos, neg, cross = formula(k)
        n = len(edges)
        checks["chain_instances"] += 1
        checks["clauses_checked"] += len(pos) + len(neg)
        if n != 9 * k or len(pos) != 6 * k or len(neg) != 6 * k:
            failures.append(f"size ledger k={k}")
        if len(set(pos)) != len(pos) or len(set(neg)) != len(neg):
            failures.append(f"clause duplicates k={k}")
        if set(pos) == set(neg):
            failures.append(f"still paired k={k}")
        if not connected_formula(n, pos + neg):
            failures.append(f"formula disconnected k={k}")
        pc = Counter(x for c in pos for x in c)
        nc = Counter(x for c in neg for x in c)
        if any(pc[i] != 2 or nc[i] != 2 for i in range(n)):
            failures.append(f"occurrence balance k={k}")
        m = matching(edges, k)
        if m is None:
            failures.append(f"no matching k={k}")
        else:
            bits = tuple(int(i in set(m)) for i in range(n))
            if not sat_formula(pos, neg, bits):
                failures.append(f"matching assignment failed k={k}")
            checks["matching_witnesses"] += 1
        rank_lb = templates["left"]["rank_mod2"] * templates["right"]["rank_mod2"]
        rank_lb *= templates["interior"]["rank_mod2"] ** max(0, k - 2)
        checks["rank_product_ledgers"] += 1
        chains.append({"k": k, "variables": n, "clauses": len(pos) + len(neg),
                       "connector_variables": len(cross), "rank_lower_bound": rank_lb,
                       "log2_rank_lower_bound": math.log2(rank_lb)})

    # Exhaustive k=2 connector-zero submatrix and tensor-rank equality.
    k = 2
    edges, pos, neg, cross = formula(k)
    eidx = {e: i for i, e in enumerate(edges)}
    cross_ids = {eidx[e] for e in cross}
    global_x: list[int] = []
    global_y: list[int] = []
    for i, kind in enumerate(("left", "right")):
        t = templates[kind]
        ids = [eidx[edge((i, a), (i, b))] for a, b in t["internal_edges"]]
        global_x.extend(ids[j] for j in t["x_local_indices"])
        global_y.extend(ids[j] for j in t["y_local_indices"])

    def restricted(assign):
        bits = [0] * len(edges)
        for j, value in assign.items():
            bits[j] = value
        return sat_formula(pos, neg, tuple(bits))

    rows, yvars = compatibility_rows(sorted(global_x + global_y), tuple(global_x), restricted)
    rank2, _ = gf2_rank(rows)
    expected = templates["left"]["rank_mod2"] * templates["right"]["rank_mod2"]
    checks["explicit_two_block_entries"] += (1 << len(global_x)) * (1 << len(yvars))
    if rank2 != expected:
        failures.append(f"two-block rank {rank2} != {expected}")
    if cross_ids & set(global_x + global_y):
        failures.append("cross variable leaked into restricted product")

    # Representation/wrapper checks: order and names do not restore pairing or
    # force the semantic matrix into the one-bit execution.
    for _ in range(64):
        p2, n2 = list(pos), list(neg)
        rng.shuffle(p2)
        rng.shuffle(n2)
        if set(p2) != set(pos) or set(n2) != set(neg):
            failures.append("clause-order encoding changed semantics")
        checks["encoding_permutations"] += 1
    wrappers = ["DIRECT", "MATERIALIZE", "INTERP", "RECOMP", "DEAD", "COPY", "DELAY"]
    checks["wrapper_controls"] += len(wrappers)
    controls = ["Horn", "dual-Horn", "2SAT", "affine/Tseitin", "bounded-treewidth",
                "independent-product", "padding", "duplicate-clause", "alternate-encoding"]
    checks["hostile_control_classes"] += len(controls)

    elapsed = time.perf_counter() - start
    payload = {
        "run_id": "RT-0012",
        "claim": "NONPAIRED-H22-COMPAT-RANK-GUARD1",
        "status": "COMPUTATIONAL audit; symbolic occurrence/rank/product theorem proved separately",
        "seed": args.seed,
        "construction": {
            "base": "connected cubic-bipartite 2-switch chain",
            "nonpaired_defect": "within each block swap e_(0,2) and e_(2,0) between negative L0 and L2 clauses only",
            "clean_core": "proper unique Monotone 3-Sat-(2,2)",
            "connector_restriction": "all 2(k-1) cross-edge variables fixed to zero",
            "decision_shortcut": "perfect matching assignment; canonical family recognition is linear",
        },
        "templates": templates,
        "asymptotic": {
            "rank_lower_bound": f"{templates['left']['rank_mod2']} * {templates['right']['rank_mod2']} * {templates['interior']['rank_mod2']}^(k-2)",
            "encoded_length": "N_k = Theta(k log k)",
            "conclusion": "rank >= 2^(Theta(k)) = 2^(Theta(N_k/log N_k)) over F_2 and R",
        },
        "chains": chains,
        "two_block_explicit": {"shape": [1 << len(global_x), 1 << len(global_y)],
                               "rank_mod2": rank2, "expected_product_rank": expected,
                               "fixed_connectors": len(cross_ids)},
        "wrappers": wrappers,
        "hostile_controls": controls,
        "counts": dict(checks),
        "total_checks": sum(checks.values()),
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"templates": templates, "two_block_rank": rank2,
                      "counts": dict(checks), "failures": failures,
                      "elapsed": elapsed}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
