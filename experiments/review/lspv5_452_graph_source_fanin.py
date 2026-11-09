#!/usr/bin/env python3
"""Exact finite controls for the LSPV-5 graph/source/fan-in lemma.

This audits strict3 mod-3 source semantics and an abstract bounded-fan-in
dependency DAG.  It is not an implementation of the historical R_mix341
byte checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from collections import deque
from itertools import combinations, product


def solve3(rows, rhs, nvars):
    a = [[z % 3 for z in row] + [b % 3] for row, b in zip(rows, rhs)]
    r = 0
    for c in range(nvars):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        if a[r][c] == 2:
            a[r] = [(2 * z) % 3 for z in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [(x - z * y) % 3 for x, y in zip(a[i], a[r])]
        r += 1
    if any(all(z == 0 for z in row[:-1]) and row[-1] for row in a):
        return None
    x = [0] * nvars
    for row in a:
        p = next((i for i, z in enumerate(row[:-1]) if z), None)
        if p is not None:
            x[p] = row[-1]
    return x


def incidence(n, edges):
    inc = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(edges):
        inc[u].append((eid, 1))
        inc[v].append((eid, -1))
    for row in inc:
        row.sort()
    return inc


def components_without(n, edges, banned):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if banned not in (u, v):
            adj[u].append(v)
            adj[v].append(u)
    seen, out = {banned}, []
    for s in range(n):
        if s in seen:
            continue
        q, comp = deque([s]), []
        seen.add(s)
        while q:
            u = q.popleft()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        out.append(sorted(comp))
    return out


def flow(n, edges, inc, charges, equations, fixed=None, excluded=None):
    fixed, excluded = dict(fixed or {}), set(excluded or set())
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
    sol = solve3(rows, rhs, len(free))
    if sol is None:
        return None
    ans = dict(fixed)
    ans.update({e: sol[pos[e]] for e in free})
    return ans


def tight_dag(leaves, arity):
    active = [f"S{i}" for i in range(leaves)]
    nodes = []
    while len(active) > 1:
        take = min(arity, len(active))
        ants = active[:take]
        active = active[take:]
        nid = f"D{len(nodes)}"
        nodes.append({"id": nid, "antecedents": ants})
        active.append(nid)
    return {"arity": arity, "root": active[0], "nodes": nodes}


def graph_catalogue():
    k4 = list(combinations(range(4), 2))
    k33 = [(u, v) for u in range(3) for v in range(3, 6)]
    cube = []
    for u in range(8):
        for bit in (1, 2, 4):
            v = u ^ bit
            if u < v:
                cube.append((u, v))
    petersen = []
    for i in range(5):
        petersen += [(i, (i + 1) % 5), (i, 5 + i)]
        a, b = 5 + i, 5 + ((i + 2) % 5)
        petersen.append(tuple(sorted((a, b))))
    petersen = sorted(set(tuple(sorted(e)) for e in petersen))
    art = []
    for arm in range(3):
        p = 1 + 5 * arm
        a, b, c, d = [2 + 5 * arm + i for i in range(4)]
        art += [(0, p), (p, a), (p, b), (a, c), (a, d),
                (b, c), (b, d), (c, d)]
    return {
        "K4": (4, sorted(k4)),
        "K33": (6, sorted(k33)),
        "cube": (8, sorted(cube)),
        "Petersen": (10, sorted(petersen)),
        "three_arm_articulation": (16, sorted(set(tuple(sorted(e)) for e in art))),
    }


def audit_graph(name, n, edges):
    assert len(edges) == 3 * n // 2
    inc = incidence(n, edges)
    assert all(len(row) == 3 for row in inc)
    charges = [0] * n
    charges[0] = 1
    cvals = [len(components_without(n, edges, v)) for v in range(n)]
    essential_count = sum(3 ** (3 - c) for c in cvals)
    essential, alo, pairs = [], [], []

    for v in range(n):
        eids = [eid for eid, _ in inc[v]]
        signs = [s for _, s in inc[v]]
        count, e_class = 0, set()
        for vals in product(range(3), repeat=3):
            signed = sum(s * x for s, x in zip(signs, vals)) % 3
            if signed == charges[v] % 3:
                continue
            ans = flow(n, edges, inc, charges, [w for w in range(n) if w != v],
                       fixed=dict(zip(eids, vals)))
            if ans is None:
                continue
            assert signed == (charges[v] - 1) % 3
            essential.append({"vertex": v, "tuple": list(vals),
                              "flow": [ans[e] for e in range(len(edges))]})
            e_class.add(vals)
            count += 1
        assert count == 3 ** (3 - cvals[v])

        r_class = {vals for vals in product(range(3), repeat=3)
                   if sum(s * x for s, x in zip(signs, vals)) % 3 == (charges[v] + 1) % 3}
        assert len(r_class) == 9 and not (e_class & r_class)

    for eid, (u, v) in enumerate(edges):
        ans = flow(n, edges, inc, charges,
                   [w for w in range(n) if w not in (u, v)], excluded={eid})
        assert ans is not None
        alo.append({"edge": eid, "flow": [ans.get(e, 0) for e in range(len(edges))]})

    for u, v in combinations(range(n), 2):
        target = charges[:]
        target[u] = (target[u] + 1) % 3
        target[v] = (target[v] + 1) % 3
        ans = flow(n, edges, inc, target, range(n))
        assert ans is not None
        pairs.append({"vertices": [u, v], "flow": [ans[e] for e in range(len(edges))]})
    for u in range(n):
        target = charges[:]
        target[u] = (target[u] + 1) % 3
        assert flow(n, edges, inc, target, range(n)) is None

    leaves = len(edges) + essential_count + (n - 1)
    dags = []
    for a in (2, 3, 4):
        d = tight_dag(leaves, a)
        q = len(d["nodes"])
        assert q == (leaves - 1 + (a - 2)) // (a - 1)
        d["lower_bound"] = (leaves - 1 + (a - 2)) // (a - 1)
        dags.append(d)
    return {
        "name": name, "vertices": n, "edges": [list(e) for e in edges],
        "edge_count": len(edges), "components_after_deletion": cvals,
        "indispensable_forbidden": essential_count,
        "required_pair_defect_groups": n - 1,
        "required_distinct_sources": leaves,
        "binary_charged_node_lower_bound": leaves - 1,
        "essential_witnesses": essential, "alo_witnesses": alo,
        "pair_defect_witnesses": pairs, "tight_dependency_dags": dags,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    graphs = [audit_graph(name, n, edges) for name, (n, edges) in graph_catalogue().items()]
    art = next(g for g in graphs if g["name"] == "three_arm_articulation")
    assert art["indispensable_forbidden"] == 118
    assert art["required_distinct_sources"] == 157
    assert art["binary_charged_node_lower_bound"] == 156
    payload = {
        "artifact": "LSPV5-GRAPH-SOURCE-FANIN452",
        "status": "PASS",
        "scope": "strict3 mod-3 source semantics plus abstract dependency DAG; not historical byte grammar",
        "formula": "r(G)=|E|+sum_v 3^(3-c_v)+|V|-1; q>=ceil((r-1)/(a-1))",
        "graphs": graphs,
        "hostile_controls": [
            {"label": "sigma_zero_merges_E_and_R", "expected": "REJECT"},
            {"label": "omit_two_R_groups", "expected": "SAT_WITNESS"},
            {"label": "unbounded_arity_jump", "expected": "OUTSIDE_ASSUMPTIONS"},
            {"label": "cyclic_dependency", "expected": "REJECT"},
        ],
        "resources": {
            "producer_seconds": time.perf_counter() - t0,
            "producer_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "finite_witnesses": sum(len(g["essential_witnesses"]) + len(g["alo_witnesses"]) + len(g["pair_defect_witnesses"]) for g in graphs),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["canonical_sha256_without_self_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
