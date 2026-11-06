#!/usr/bin/env python3
"""Build and verify the complete 37-node LSPV-1/445 bridge-cut trace.

The output is a source-labelled, typed rule-level certificate.  It is not an
execution format for an authoritative historical R_mix341 byte checker.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

VARS = 15
ASSIGNMENTS = 1 << VARS
MASK_BYTES = ASSIGNMENTS // 8


def build_source():
    edges = []
    for off in (0, 5):
        for u in range(4):
            for v in range(u + 1, 4):
                if (u, v) == (0, 1):
                    edges.extend(((off, off + 4), (off + 4, off + 1)))
                else:
                    edges.append((off + u, off + v))
    edges.append((4, 9))
    assert len(edges) == 15 and edges[-1] == (4, 9)
    incident = [[] for _ in range(10)]
    for edge_id, (u, v) in enumerate(edges, 1):
        incident[u].append(edge_id); incident[v].append(edge_id)
    assert all(len(row) == 3 for row in incident)
    charges = [1] + [0] * 9
    clauses, by_vertex = [], []
    for v in range(10):
        ids = []
        for t in range(8):
            bits = ((t >> 2) & 1, (t >> 1) & 1, t & 1)
            if bits[0] ^ bits[1] ^ bits[2] == charges[v]:
                continue
            ids.append(len(clauses))
            clauses.append([(-e if bits[j] else e) for j, e in enumerate(incident[v])])
        assert len(ids) == 4
        by_vertex.append(ids)
    dimacs = "p cnf 15 40\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
    assert hashlib.sha256(dimacs.encode()).hexdigest() == "4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18"
    return edges, incident, charges, clauses, by_vertex, dimacs


def lit_true(lit, assignment):
    return ((assignment >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0)


def clause_true(clause, assignment):
    return any(lit_true(lit, assignment) for lit in clause)


def clause_mask(clause):
    out = 0
    for a in range(ASSIGNMENTS):
        if clause_true(clause, a):
            out |= 1 << a
    return out


def affine_mask(support, rhs):
    out = 0
    for a in range(ASSIGNMENTS):
        value = 0
        for v in support:
            value ^= (a >> (v - 1)) & 1
        if value == rhs:
            out |= 1 << a
    return out


def mask_hash(mask):
    return hashlib.sha256(mask.to_bytes(MASK_BYTES, "little")).hexdigest()


def build_trace(incident, charges, clauses, by_vertex):
    nodes, state = [], {}

    def source_state(source_id):
        clause = clauses[source_id]
        return {"mask": clause_mask(clause), "support": sorted(map(abs, clause)),
                "clause": clause, "affine": None}

    def get(ref):
        return source_state(ref[1]) if ref[0] == "s" else state[ref[1]]

    def emit(rule, parents, output, **extra):
        node_id = len(nodes)
        rec = {"id": node_id, "rule": rule,
               "parents": [[kind, value] for kind, value in parents],
               "support": output["support"], "mask_sha256": mask_hash(output["mask"])}
        if output.get("clause") is not None:
            rec["clause"] = output["clause"]
        if output.get("affine") is not None:
            rec["affine"] = output["affine"]
        rec.update(extra)
        nodes.append(rec); state[node_id] = output
        return ("n", node_id)

    def and3(left, right, annotation=None):
        a, b = get(left), get(right)
        support = sorted(set(a["support"]) | set(b["support"]))
        assert len(support) <= 3
        mask = a["mask"] & b["mask"]
        affine = None
        if annotation is not None:
            affine = {"vars": sorted(annotation[0]), "rhs": annotation[1]}
            assert mask == affine_mask(affine["vars"], affine["rhs"])
        return emit("AND3", [left, right], {"mask": mask, "support": support,
                    "clause": None, "affine": affine})

    def xor(left, right):
        a, b = get(left), get(right)
        assert a["affine"] is not None and b["affine"] is not None
        support = sorted(set(a["affine"]["vars"]) ^ set(b["affine"]["vars"]))
        rhs = a["affine"]["rhs"] ^ b["affine"]["rhs"]
        mask = affine_mask(support, rhs)
        return emit("XOR", [left, right], {"mask": mask, "support": support,
                    "clause": None, "affine": {"vars": support, "rhs": rhs}})

    def local(parent, clause):
        a = get(parent); cmask = clause_mask(clause)
        assert a["mask"] & ~cmask == 0
        return emit("LOCAL", [parent], {"mask": cmask,
                    "support": sorted(map(abs, clause)), "clause": clause, "affine": None})

    def resolution(left, right, pivot):
        a, b = get(left), get(right)
        assert a["clause"] is not None and b["clause"] is not None
        assert pivot in a["clause"] and -pivot in b["clause"]
        clause = []
        for lit in a["clause"] + b["clause"]:
            if lit not in (pivot, -pivot) and lit not in clause:
                clause.append(lit)
        assert not any(-lit in clause for lit in clause)
        return emit("RES", [left, right], {"mask": clause_mask(clause),
                    "support": sorted(map(abs, clause)), "clause": clause, "affine": None},
                    pivot=pivot)

    def vertex_row(v):
        refs = [("s", sid) for sid in by_vertex[v]]
        left = and3(refs[0], refs[1]); right = and3(refs[2], refs[3])
        return and3(left, right, (incident[v], charges[v]))

    side_units = []
    for side, endpoint in (((0, 1, 2, 3, 4), 4), ((5, 6, 7, 8, 9), 9)):
        internal = [v for v in side if v != endpoint]
        rows = [vertex_row(v) for v in internal]
        pair0 = xor(rows[0], rows[1]); pair1 = xor(rows[2], rows[3])
        boundary = xor(pair0, pair1)
        boundary_state = get(boundary)
        bridge = 15
        nonbridge = [e for e in incident[endpoint] if e != bridge]
        side_charge = 0
        for v in side: side_charge ^= charges[v]
        selected = []
        for sid in by_vertex[endpoint]:
            wrong = {abs(lit): int(lit < 0) for lit in clauses[sid]}
            if wrong[bridge] == (1 ^ side_charge) and (wrong[nonbridge[0]] ^ wrong[nonbridge[1]]) == boundary_state["affine"]["rhs"]:
                selected.append(sid)
        assert len(selected) == 2
        endpoint_pair = and3(("s", selected[0]), ("s", selected[1]))
        joined = and3(endpoint_pair, boundary)
        side_units.append(local(joined, [bridge if side_charge else -bridge]))
    root = resolution(side_units[0], side_units[1], 15)
    assert get(root)["clause"] == [] and get(root)["mask"] == 0
    return nodes, root


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); args = ap.parse_args()
    start = time.perf_counter()
    edges, incident, charges, clauses, by_vertex, dimacs = build_source()
    full_models, only_bad = [], {}
    for assignment in range(ASSIGNMENTS):
        bad = [i for i, clause in enumerate(clauses) if not clause_true(clause, assignment)]
        if not bad: full_models.append(assignment)
        if len(bad) == 1 and bad[0] not in only_bad: only_bad[bad[0]] = assignment
    assert not full_models and len(only_bad) == 36
    core = sorted(only_bad)
    assert not any(all(clause_true(clauses[i], a) for i in core) for a in range(ASSIGNMENTS))
    for sid, witness in only_bad.items():
        assert not clause_true(clauses[sid], witness)
        assert all(i == sid or clause_true(clause, witness) for i, clause in enumerate(clauses))
    nonessential = sorted(set(range(40)) - set(core))
    for sid in nonessential:
        assert not any(all(i == sid or clause_true(c, a) for i, c in enumerate(clauses))
                       for a in range(ASSIGNMENTS))

    nodes, root = build_trace(incident, charges, clauses, by_vertex)
    assert len(nodes) == 37
    counts = {rule: sum(n["rule"] == rule for n in nodes) for rule in ("AND3", "XOR", "LOCAL", "RES")}
    assert counts == {"AND3": 28, "XOR": 6, "LOCAL": 2, "RES": 1}
    source_ancestors, node_ancestors = set(), set()
    def walk(ref):
        kind, value = ref
        if kind == "s": source_ancestors.add(value); return
        if value in node_ancestors: return
        node_ancestors.add(value)
        for p in nodes[value]["parents"]: walk(p)
    walk(root)
    assert source_ancestors == set(core) and len(node_ancestors) == 37
    edge_count = sum(len(n["parents"]) for n in nodes)
    beta = edge_count - (len(source_ancestors) + len(nodes) - 1)
    unary = sum(len(n["parents"]) == 1 for n in nodes)
    nullary = sum(len(n["parents"]) == 0 for n in nodes)
    assert (edge_count, beta, unary, nullary) == (72, 0, 2, 0)
    depths = {}
    for node in nodes:
        depths[node["id"]] = 1 + max((0 if p[0] == "s" else depths[p[1]]) for p in node["parents"])
    assert depths[root[1]] == 7

    result = {
        "run": "LSPV-5/REFEREE386", "timestamp_pst": "2026-11-06 05:48 PST",
        "status": "PROVED_RESTRICTED topology application; COMPUTATIONAL complete finite trace",
        "source": {"variables": VARS, "clauses": clauses, "edges": edges, "incident": incident,
                   "charges": charges, "dimacs_sha256": hashlib.sha256(dimacs.encode()).hexdigest()},
        "core": core, "deletion_witnesses": {str(k): v for k, v in sorted(only_bad.items())},
        "nonessential": nonessential, "trace": nodes, "root": list(root),
        "work": len(nodes), "span": depths[root[1]], "rule_counts": counts,
        "ancestry": {"used_sources": len(source_ancestors), "paid_nodes": len(nodes),
                     "dependency_edges": edge_count, "cycle_rank": beta,
                     "unary_paid": unary, "nullary_paid": nullary},
        "near_floor_classes": {
            "q35": ["r=36,beta=0,u=0,d0=0: full binary source-once tree"],
            "q36": ["r=37,beta=0,u=0,d0=0", "r=36,beta=1,u=0,d0=0", "r=36,beta=0,u=1,d0=0"],
            "q37_exhibited": "r=36,beta=0,u=2,d0=0"
        },
        "scope": "No historical accepted-byte checker; global minimum remains 35 <= W <= 37",
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    }
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass": True, "out": str(out), "work": 37, "span": 7,
                      "core": len(core), "topology": result["ancestry"]}, sort_keys=True))


if __name__ == "__main__": main()
