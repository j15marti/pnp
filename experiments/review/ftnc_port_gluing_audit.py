#!/usr/bin/env python3
"""Incidence-level audit for the laminar gauge tree at the stated FTNC K4 ports.

This deliberately does not invent the missing physical FTNC face-gluing rules.
It audits everything forced by the only explicit interface in FTNCNAESLICE1:
one fresh selector port plus three Boolean literal ports per NAE predicate.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

SEED = 202610190704


def unrooted_binary_tree(m: int):
    if m < 2:
        raise ValueError("unrooted construction requires m >= 2")
    leaves = [f"L{i}" for i in range(m)]
    if m == 2:
        return leaves, [(leaves[0], leaves[1])]
    if m == 3:
        center = "I0"
        return leaves + [center], [(center, leaf) for leaf in leaves]
    internals = [f"I{i}" for i in range(m - 2)]
    edges = [(internals[i], internals[i + 1]) for i in range(m - 3)]
    edges += [(internals[0], leaves[0]), (internals[0], leaves[1])]
    # Middle internal vertices each receive one leaf.
    for j in range(1, len(internals) - 1):
        edges.append((internals[j], leaves[j + 1]))
    edges += [(internals[-1], leaves[-2]), (internals[-1], leaves[-1])]
    assert len(edges) == 2 * m - 3
    deg = Counter(v for e in edges for v in e)
    assert all(deg[x] == 1 for x in leaves)
    assert all(deg[x] == 3 for x in internals)
    return leaves + internals, edges


def components_without(nodes, edges, cut):
    adj = defaultdict(list)
    for a, b in edges:
        if {a, b} == set(cut):
            continue
        adj[a].append(b)
        adj[b].append(a)
    out = []
    unseen = set(nodes)
    while unseen:
        root = unseen.pop()
        comp = {root}
        q = deque([root])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    comp.add(v)
                    q.append(v)
        out.append(comp)
    assert len(out) == 2
    return out


def source_formula(m: int, n: int, rng: random.Random):
    # Proper triples; repetitions, permutations, and arbitrary signs are allowed.
    if n < 3:
        raise ValueError("need at least three source variables")
    out = []
    for _ in range(m):
        vs = rng.sample([f"x{j}" for j in range(n)], 3)
        out.append(tuple((v, rng.randrange(2)) for v in vs))
    return out


def compile_supports(source):
    m = len(source)
    nodes, edges = unrooted_binary_tree(m)
    clauses = []
    owner = []
    kind = []
    for i, c in enumerate(source):
        a, b, cc = [v for v, _ in c]
        clauses.append(frozenset((a, b, f"u{i}")))
        owner.append(f"L{i}")
        kind.append("front-A")
        clauses.append(frozenset((f"u{i}", cc, f"g_L{i}")))
        owner.append(f"L{i}")
        kind.append("front-B")
    for k, (v, w) in enumerate(edges):
        support = frozenset((f"g_{v}", f"g_{w}", f"e{k}"))
        clauses.extend((support, support))
        owner.extend(((v, w, k), (v, w, k)))
        kind.extend(("eq-0", "eq-1"))
    return nodes, edges, clauses, owner, kind


def port_complex(source):
    nodes, edges, supports, owner, kind = compile_supports(source)
    tetra = [frozenset((f"s{j}", *sorted(s))) for j, s in enumerate(supports)]
    bool_vertices = set().union(*supports)
    vertices = set().union(*tetra)
    occurrence = Counter(v for s in supports for v in s)
    multidegree = Counter()
    simple_edges = set()
    for t in tetra:
        for a, b in itertools.combinations(sorted(t), 2):
            multidegree[a] += 1
            multidegree[b] += 1
            simple_edges.add((a, b))
    simple_degree = Counter(v for e in simple_edges for v in e)
    face_pairs = []
    for i, j in itertools.combinations(range(len(tetra)), 2):
        common = tetra[i] & tetra[j]
        if len(common) == 3:
            face_pairs.append((i, j, tuple(sorted(common))))
    return {
        "nodes": nodes,
        "tree_edges": edges,
        "supports": supports,
        "owner": owner,
        "kind": kind,
        "tetra": tetra,
        "bool_vertices": bool_vertices,
        "vertices": vertices,
        "occurrence": occurrence,
        "multidegree": multidegree,
        "simple_degree": simple_degree,
        "simple_edges": simple_edges,
        "face_pairs": face_pairs,
    }


def boundary_for_cut(source, pc, edge_index):
    nodes, edges = pc["nodes"], pc["tree_edges"]
    cut = edges[edge_index]
    comps = components_without(nodes, edges, cut)
    side_of = {v: i for i, comp in enumerate(comps) for v in comp}
    # Put the two cut-edge tetrahedra on the side of cut[0].
    clause_sides = []
    for own in pc["owner"]:
        if isinstance(own, str):
            clause_sides.append(side_of[own])
        else:
            v, w, k = own
            clause_sides.append(side_of[v] if k == edge_index else side_of[v])
            assert k == edge_index or side_of[v] == side_of[w]
    by_port = defaultdict(set)
    for j, side in enumerate(clause_sides):
        for p in pc["tetra"][j]:
            by_port[p].add(side)
    target_boundary = {p for p, ss in by_port.items() if len(ss) == 2}
    leaves_by_side = [{int(v[1:]) for v in comp if v.startswith("L")} for comp in comps]
    source_sides = []
    for leafset in leaves_by_side:
        source_sides.append({v for i in leafset for v, _ in source[i]})
    source_boundary = source_sides[0] & source_sides[1]
    added = target_boundary - source_boundary
    return source_boundary, target_boundary, added


def hidden_state_counterexample():
    rows = []
    for p in (0, 1):
        separate = any(h0 == p and h1 == 1 - p for h0, h1 in itertools.product((0, 1), repeat=2))
        shared = any(h == p and h == 1 - p for h in (0, 1))
        rows.append({"port": p, "separate_hidden": separate, "shared_hidden": shared})
    assert all(r["separate_hidden"] for r in rows)
    assert not any(r["shared_hidden"] for r in rows)
    return rows


def main():
    start = time.perf_counter()
    rng = random.Random(SEED)
    scale_rows = []
    cut_checks = 0
    randomized_cases = 0
    for m in [2, 3, 4, 5, 8, 16, 32, 64]:
        n = max(3, min(17, 2 * m + 1))
        source = source_formula(m, n, rng)
        pc = port_complex(source)
        M = 6 * m - 6
        assert len(pc["supports"]) == M
        assert len(pc["bool_vertices"]) == len({v for c in source for v, _ in c}) + 5 * m - 5
        assert len(pc["vertices"]) == len(pc["bool_vertices"]) + M
        assert sum(len(t) * (len(t) - 1) // 2 for t in pc["tetra"]) == 36 * m - 36
        aux_occ = {v: c for v, c in pc["occurrence"].items() if not v.startswith("x")}
        assert max(aux_occ.values()) <= 6
        assert max(pc["multidegree"][v] for v in aux_occ) == 18 if m >= 3 else max(pc["multidegree"][v] for v in aux_occ) <= 18
        assert len(pc["face_pairs"]) == 2 * m - 3
        for edge_index in range(len(pc["tree_edges"])):
            sb, tb, added = boundary_for_cut(source, pc, edge_index)
            assert len(tb) == len(sb) + 1
            assert len(added) == 1 and next(iter(added)).startswith("g_")
            assert not any(x.startswith("s") for x in tb)
            cut_checks += 1
        scale_rows.append({
            "m": m,
            "source_distinct_variables": len({v for c in source for v, _ in c}),
            "nae_predicates_tetrahedra": M,
            "boolean_ports": len(pc["bool_vertices"]),
            "selector_ports": M,
            "physical_vertices_port_identification_only": len(pc["vertices"]),
            "k4_edge_incidences_with_multiplicity": 36 * m - 36,
            "distinct_simple_edges_observed": len(pc["simple_edges"]),
            "max_aux_nae_occurrence": max(aux_occ.values()),
            "max_aux_k4_multidegree": max(pc["multidegree"][v] for v in aux_occ),
            "max_aux_k4_simple_degree_observed": max(pc["simple_degree"][v] for v in aux_occ),
            "three_port_face_sharing_pairs": len(pc["face_pairs"]),
        })
    # Additional hostile inputs with repeated clauses, sign flips, and permutations.
    for m in range(2, 13):
        for _ in range(20):
            source = source_formula(m, 6, rng)
            if rng.randrange(2):
                source[rng.randrange(m)] = tuple(reversed(source[0]))
            pc = port_complex(source)
            assert len(pc["face_pairs"]) == 2 * m - 3
            for edge_index in range(len(pc["tree_edges"])):
                sb, tb, added = boundary_for_cut(source, pc, edge_index)
                assert len(tb) == len(sb) + 1
                assert len(added) == 1
                cut_checks += 1
            randomized_cases += 1
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "run_id": "FTNCPORTGLUE1",
        "seed": SEED,
        "status": {
            "incidence_ledger": "COMPUTATIONAL confirmation of symbolic counting lemma",
            "hidden_state_noncomposition": "PROVED/EXACT truth-table counterexample",
            "actual_ftnc_face_gluing": "OPEN: no immutable wiring/gluing semantics in accessible corpus",
            "p_vs_np": "OPEN",
        },
        "script_sha256": script_hash,
        "randomized_cases": randomized_cases,
        "aligned_cut_checks": cut_checks,
        "scale_rows": scale_rows,
        "hidden_state_counterexample": hidden_state_counterexample(),
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "limitations": [
            "Only the explicit K4 selector-plus-three-literal port interface is audited.",
            "No unprovided FTNC occurrence-consistency or face-gluing rule is assumed.",
            "K4 multidegree is a physical incidence ledger, not an algorithmic lower bound.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
