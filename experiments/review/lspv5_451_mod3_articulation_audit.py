#!/usr/bin/env python3
"""Independent exact audit of mod-3 strict-3 Tseitin source essentiality.

This is a source-semantics audit.  It does not implement or authenticate the
historical R_mix341 byte grammar.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from collections import deque


def inv3(x: int) -> int:
    x %= 3
    if x == 1:
        return 1
    if x == 2:
        return 2
    raise ValueError("zero has no inverse")


def solve_mod3(rows: list[list[int]], rhs: list[int], nvars: int):
    a = [[x % 3 for x in row] + [b % 3] for row, b in zip(rows, rhs)]
    pivots: list[int] = []
    r = 0
    for c in range(nvars):
        p = next((i for i in range(r, len(a)) if a[i][c] % 3), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        z = inv3(a[r][c])
        a[r] = [(z * q) % 3 for q in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c] % 3:
                z = a[i][c] % 3
                a[i] = [(x - z * y) % 3 for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    for row in a:
        if all(x % 3 == 0 for x in row[:-1]) and row[-1] % 3:
            return None
    x = [0] * nvars
    for i, c in enumerate(pivots):
        x[c] = a[i][-1] % 3
    return x


def build_graph():
    edges: list[tuple[int, int]] = []
    center = 0
    for arm in range(3):
        p = 1 + 5 * arm
        k0, k1, k2, k3 = (2 + 5 * arm + i for i in range(4))
        arm_edges = [
            (center, p),
            (p, k0),
            (p, k1),
            (k0, k2),
            (k0, k3),
            (k1, k2),
            (k1, k3),
            (k2, k3),
        ]
        edges.extend(tuple(sorted(e)) for e in arm_edges)
    edges = sorted(set(edges))
    assert len(edges) == 24
    deg = [0] * 16
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    assert deg == [3] * 16
    return edges


def incidence(edges):
    inc = [[] for _ in range(16)]
    for eid, (u, v) in enumerate(edges):
        inc[u].append((eid, 1))
        inc[v].append((eid, -1))
    for row in inc:
        row.sort()
        assert len(row) == 3
    return inc


def components_without(v: int, edges):
    adj = [[] for _ in range(16)]
    for a, b in edges:
        if a == v or b == v:
            continue
        adj[a].append(b)
        adj[b].append(a)
    seen = {v}
    comps = []
    for s in range(16):
        if s in seen:
            continue
        q = deque([s])
        seen.add(s)
        comp = []
        while q:
            x = q.popleft()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        comps.append(sorted(comp))
    return comps


def flow_solution(edges, inc, charges, equations, fixed=None, excluded=None):
    fixed = dict(fixed or {})
    excluded = set(excluded or set())
    free = [e for e in range(len(edges)) if e not in fixed and e not in excluded]
    pos = {e: i for i, e in enumerate(free)}
    rows, rhs = [], []
    for v in equations:
        row = [0] * len(free)
        b = charges[v] % 3
        for eid, sign in inc[v]:
            if eid in excluded:
                continue
            if eid in fixed:
                b = (b - sign * fixed[eid]) % 3
            else:
                row[pos[eid]] = sign % 3
        rows.append(row)
        rhs.append(b)
    sol = solve_mod3(rows, rhs, len(free))
    if sol is None:
        return None
    out = dict(fixed)
    out.update({eid: sol[pos[eid]] for eid in free})
    return out


def clauses(edges, inc, charges):
    out = []
    for eid in range(len(edges)):
        out.append({"id": f"A:{eid}", "kind": "ALO", "edge": eid})
    for v in range(16):
        items = inc[v]
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    vals = (a, b, c)
                    s = sum(sign * val for (_, sign), val in zip(items, vals)) % 3
                    if s != charges[v] % 3:
                        out.append({
                            "id": f"D:{v}:{a}{b}{c}",
                            "kind": "FORBID",
                            "vertex": v,
                            "edges": [eid for eid, _ in items],
                            "values": list(vals),
                            "signed_sum": s,
                        })
    assert len(out) == 24 + 18 * 16
    return out


def indicators(edge_values, missing=None):
    missing = set(missing or set())
    bits = {}
    for eid in range(24):
        for t in range(3):
            bits[f"{eid}:{t}"] = False if eid in missing else edge_values[eid] == t
    return bits


def false_clauses(source, bits):
    bad = []
    for cl in source:
        if cl["kind"] == "ALO":
            eid = cl["edge"]
            ok = any(bits[f"{eid}:{t}"] for t in range(3))
        else:
            ok = any(not bits[f"{eid}:{t}"] for eid, t in zip(cl["edges"], cl["values"]))
        if not ok:
            bad.append(cl["id"])
    return bad


def run():
    t0 = time.perf_counter()
    edges = build_graph()
    inc = incidence(edges)
    component_rows = []
    for v in range(16):
        comps = components_without(v, edges)
        component_rows.append({
            "vertex": v,
            "components": comps,
            "c_v": len(comps),
            "predicted_forbidden_essential": 3 ** (3 - len(comps)),
        })
    assert [x["c_v"] for x in component_rows].count(3) == 1
    assert [x["c_v"] for x in component_rows].count(2) == 3
    assert [x["c_v"] for x in component_rows].count(1) == 12

    runs = []
    checks = 0
    for sigma in (1, 2):
        charges = [0] * 16
        charges[0] = sigma
        source = clauses(edges, inc, charges)
        forbidden_witnesses = []
        forbidden_counts = []
        for v in range(16):
            good = 0
            for cl in [q for q in source if q.get("vertex") == v]:
                fixed = dict(zip(cl["edges"], cl["values"]))
                flow = flow_solution(edges, inc, charges, [w for w in range(16) if w != v], fixed=fixed)
                if flow is not None:
                    bits = indicators(flow)
                    bad = false_clauses(source, bits)
                    assert bad == [cl["id"]]
                    forbidden_witnesses.append({"deleted": cl["id"], "edge_values": [flow[e] for e in range(24)]})
                    good += 1
                    checks += len(source)
            predicted = 3 ** (3 - len(components_without(v, edges)))
            assert good == predicted
            forbidden_counts.append(good)

        alo_witnesses = []
        for eid, (u, v) in enumerate(edges):
            flow = flow_solution(edges, inc, charges, [w for w in range(16) if w not in (u, v)], excluded={eid})
            assert flow is not None
            bits = indicators(flow, missing={eid})
            bad = false_clauses(source, bits)
            assert bad == [f"A:{eid}"]
            alo_witnesses.append({"deleted": f"A:{eid}", "missing_edge": eid,
                                  "edge_values": [flow.get(e, 0) for e in range(24)]})
            checks += len(source)

        pair_witnesses = []
        for u in range(16):
            for v in range(u + 1, 16):
                target = charges[:]
                target[u] = (target[u] + sigma) % 3
                target[v] = (target[v] + sigma) % 3
                flow = flow_solution(edges, inc, target, list(range(16)))
                assert flow is not None
                bits = indicators(flow)
                bad = false_clauses(source, bits)
                assert len(bad) == 2
                assert {int(x.split(":")[1]) for x in bad} == {u, v}
                bad_cls = [next(q for q in source if q["id"] == x) for x in bad]
                assert all(q["signed_sum"] == (charges[q["vertex"]] + sigma) % 3 for q in bad_cls)
                pair_witnesses.append({"vertices": [u, v], "false_sources": bad,
                                       "edge_values": [flow[e] for e in range(24)]})
                checks += len(source)

        # One wrong-defect group cannot be enough: its target divergence has nonzero total.
        for u in range(16):
            target = charges[:]
            target[u] = (target[u] + sigma) % 3
            assert flow_solution(edges, inc, target, list(range(16))) is None
            checks += 1

        essential_forbidden = sum(forbidden_counts)
        assert essential_forbidden == 118
        assert essential_forbidden + len(edges) == 142
        runs.append({
            "sigma": sigma,
            "source_clause_count": len(source),
            "forbidden_essential_count": essential_forbidden,
            "total_individually_essential_sources": essential_forbidden + len(edges),
            "two_connected_formula_would_claim": 24 + 9 * 16,
            "forbidden_counts_by_vertex": forbidden_counts,
            "forbidden_witnesses": forbidden_witnesses,
            "alo_witnesses": alo_witnesses,
            "pair_defect_witnesses": pair_witnesses,
            "single_wrong_group_unsat_vertices": list(range(16)),
        })

    # Hostile controls are structural and must be rejected by the independent verifier.
    hostile = [
        {"label": "duplicate_source_id", "expected": "REJECT"},
        {"label": "corrupt_forbidden_owner", "expected": "REJECT"},
        {"label": "wrong_pair_vertex_scope", "expected": "REJECT"},
        {"label": "multi_hot_edge", "expected": "REJECT"},
        {"label": "drop_alo_without_missing_edge", "expected": "REJECT"},
    ]
    payload = {
        "artifact": "LSPV5-MOD3-ARTICULATION-AUDIT451",
        "status": "PASS",
        "scope": "original-source strict3 modulo-three semantics; no historical R_mix341 byte checker",
        "graph": {"vertices": 16, "edges": edges, "edge_count": len(edges), "cubic": True},
        "component_rows": component_rows,
        "theorem_prediction": "forbidden essential at v = 3^(3-c_v); total = |E| + sum_v 3^(3-c_v)",
        "runs": runs,
        "hostile_controls": hostile,
        "checks": checks,
        "resources": {
            "producer_seconds": time.perf_counter() - t0,
            "producer_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_witnesses": 2 * (118 + 24 + 120),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["canonical_sha256_without_self_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    data = run()
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({
        "status": data["status"],
        "vertices": data["graph"]["vertices"],
        "edges": data["graph"]["edge_count"],
        "essential_sources_each_sigma": [r["total_individually_essential_sources"] for r in data["runs"]],
        "pair_witnesses_each_sigma": [len(r["pair_defect_witnesses"]) for r in data["runs"]],
        "checks": data["checks"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
