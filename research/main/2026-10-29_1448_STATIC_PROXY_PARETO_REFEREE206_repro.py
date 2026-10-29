#!/usr/bin/env python3
"""Finite controls for STATIC-PROXY-PARETO-REFEREE206.

Checks the exact integer permitted proxy geometry, Pareto records, a q=0
endpoint realization under the residual-clause-hitting interpretation, and
the distinction between a stored boundary table and a streaming enumerator.
No finite check is promoted to a general SAT lower bound.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def q_permitted(n: int, b: int) -> int:
    # Small epsilon avoids floating artifacts at exact integer thresholds.
    return max(0, math.ceil(n / (12 * b) - 0.25 - 1e-12))


def proxy_points(n: int):
    return [
        {"b": b, "q": q_permitted(n, b),
         "log2_T_proxy": b + q_permitted(n, b), "log2_S_table_proxy": b}
        for b in range(1, n + 1)
    ]


def pareto_records(points):
    # Space exponent b is strictly increasing, so nondominated points are
    # exactly strict record lows of the time exponent.
    best = 10**100
    out = []
    for p in points:
        if p["log2_T_proxy"] < best:
            out.append(p)
            best = p["log2_T_proxy"]
    return out


def circulant_endpoint(b: int):
    """Connected proper strict exact22 formula with n=3b and every clause hit by Y.

    Private graph is C_(2b)(+-1,+-2). Its 4b edges are grouped four per
    boundary variable. Signs are assigned independently so each variable has
    exactly two positive and two negative occurrences.
    """
    if b < 3:
        raise ValueError("b >= 3 required")
    p = 2 * b
    edge_set = set()
    for i in range(p):
        for delta in (1, 2):
            u, v = sorted((i, (i + delta) % p))
            edge_set.add((u, v))
    edges = sorted(edge_set)
    assert len(edges) == 4 * b
    incidence = [[] for _ in range(p)]
    for eid, (u, v) in enumerate(edges):
        incidence[u].append(eid)
        incidence[v].append(eid)
    assert all(len(x) == 4 for x in incidence)

    private_sign = {}
    for v in range(p):
        for rank, eid in enumerate(sorted(incidence[v])):
            private_sign[(v, eid)] = 1 if rank < 2 else 0

    clauses = []
    for eid, (u, v) in enumerate(edges):
        y = eid // 4
        sy = 1 if eid % 4 < 2 else 0
        clauses.append((("y", y, sy), ("p", u, private_sign[(u, eid)]),
                        ("p", v, private_sign[(v, eid)])))
    return clauses


def validate_endpoint(b: int):
    clauses = circulant_endpoint(b)
    n = 3 * b
    assert len(clauses) == 4 * b == 4 * n // 3
    seen = set()
    counts = {}
    adjacency = {("y", i): set() for i in range(b)}
    adjacency.update({("p", i): set() for i in range(2 * b)})
    for clause in clauses:
        names = tuple((kind, idx) for kind, idx, _ in clause)
        assert len(set(names)) == 3
        assert names not in seen
        seen.add(names)
        assert sum(kind == "y" for kind, _, _ in clause) == 1
        for kind, idx, sign in clause:
            counts[(kind, idx, sign)] = counts.get((kind, idx, sign), 0) + 1
        for a, c in itertools.combinations(names, 2):
            adjacency[a].add(c)
            adjacency[c].add(a)
    for kind, size in (("y", b), ("p", 2 * b)):
        for idx in range(size):
            assert counts[(kind, idx, 0)] == 2
            assert counts[(kind, idx, 1)] == 2
    todo = [("y", 0)]
    reached = set(todo)
    while todo:
        x = todo.pop()
        for z in adjacency[x]:
            if z not in reached:
                reached.add(z)
                todo.append(z)
    assert len(reached) == n

    sat = None
    models = None
    if n <= 15:
        models = 0
        for mask in range(1 << n):
            ok = True
            for clause in clauses:
                cv = False
                for kind, idx, sign in clause:
                    pos = idx if kind == "y" else b + idx
                    cv |= ((mask >> pos) & 1) == sign
                if not cv:
                    ok = False
                    break
            models += ok
        sat = models > 0
    return {
        "b": b, "n": n, "clauses": len(clauses),
        "connected": True, "proper": True, "strict_exact22": True,
        "all_clauses_hit_by_Y": True,
        "private_modules_after_Y": 1,
        "residual_private_only_clauses": 0,
        "q_residual_hitting": 0,
        "bruteforce_models": models, "sat": sat,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    ns = [12, 48, 120, 1200, 12000]
    geometry = []
    for n in ns:
        pts = proxy_points(n)
        records = pareto_records(pts)
        min_t = min(p["log2_T_proxy"] for p in pts)
        minimizers = [p for p in pts if p["log2_T_proxy"] == min_t]
        equality = next(p for p in pts if p["q"] == 0)
        assert equality["b"] == math.ceil(n / 3)
        assert all(p["b"] <= minimizers[0]["b"] for p in records)
        geometry.append({
            "n": n,
            "continuous_b_star": math.sqrt(n / 12),
            "continuous_min_exponent": math.sqrt(n / 3) - 0.25,
            "integer_min_exponent": min_t,
            "integer_minimizers": minimizers,
            "first_log_proxy_equality": equality,
            "pareto_records": records,
            "equality_point_is_pareto": equality in records,
        })

    g1200 = next(g for g in geometry if g["n"] == 1200)
    assert [p["b"] for p in g1200["integer_minimizers"]] == [9, 10, 11]
    assert g1200["pareto_records"][-1]["b"] == 9
    assert g1200["first_log_proxy_equality"] == {
        "b": 400, "q": 0, "log2_T_proxy": 400,
        "log2_S_table_proxy": 400,
    }
    assert not g1200["equality_point_is_pareto"]

    endpoints = [validate_endpoint(b) for b in range(3, 13)]
    # For b=3..5 the formulas are exhaustively solved; exact labels are not
    # needed for the structural theorem but witnesses guard implementation.
    assert all(x["sat"] for x in endpoints if x["sat"] is not None)

    streaming_vs_table = []
    for p in [g1200["pareto_records"][-1], g1200["first_log_proxy_equality"]]:
        h = p["b"] + p["q"]
        streaming_vs_table.append({
            "b": p["b"], "q": p["q"],
            "same_enumeration_time_exponent": h,
            "stored_table_bits_exponent": p["b"],
            "streaming_assignment_bits": h,
            "note": "Streaming scans can use O(N+h) peak bits rather than storing 2^b table entries."
        })

    result = {
        "run_id": "STATIC-PROXY-PARETO-REFEREE206",
        "status": {
            "symbolic": "PROVED/EXACT restricted proxy geometry in paired report",
            "finite": "COMPUTATIONAL controls",
            "general_sat_time_space": "OPEN",
        },
        "integer_proxy_geometry": geometry,
        "q0_endpoint_realizations": endpoints,
        "streaming_vs_stored_table": streaming_vs_table,
        "limitations": [
            "Permitted points need not be realizable by a given source family.",
            "The q=0 construction uses residual private-only clause hitting; a stronger definition requiring B_i to hit boundary-touching clauses would exclude q=0.",
            "T_proxy and S_table_proxy are architecture costs, not all-algorithm lower bounds.",
            "Finite controls do not establish native RAM or Turing-machine exponents.",
        ],
    }
    source = Path(__file__).read_bytes()
    result["code_sha256"] = hashlib.sha256(source).hexdigest()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    print(json.dumps({
        "status": "PASS",
        "n1200_pareto_last": g1200["pareto_records"][-1],
        "n1200_first_equality": g1200["first_log_proxy_equality"],
        "endpoint_controls": len(endpoints),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
