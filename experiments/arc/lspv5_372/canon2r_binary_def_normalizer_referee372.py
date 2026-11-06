#!/usr/bin/env python3
"""REFEREE372: instantiate REFEREE371 in the frozen CANON2R byte grammar.

This executes the actual proposed CANON2/CANON2R checker already published by
REFEREE361/362.  It does not turn that proposed serialization into historical
R_mix341 authority.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_raw.json"
CERTS = ROOT / "results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_certificates.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


C2 = load("canon2_ref361", ROOT / "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py")
C2R = load("canon2r_ref362", ROOT / "experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py")
R371 = load("semantic_ref371", ROOT / "experiments/arc/lspv5_371/boolean_def_to_signed_and_referee371.py")


RAW_SOURCE = b"c REFEREE372 exact raw source\np cnf 2 2\n1 0\n-1 0\n"
SOURCE = C2R.parse_strict_dimacs(RAW_SOURCE)


def key(c):
    return tuple(c)


def and_truth(left_neg: bool, right_neg: bool) -> list[int]:
    return [int((bool(a) ^ left_neg) and (bool(b) ^ right_neg))
            for b in (0, 1) for a in (0, 1)]


def add_def_network(template, nodes):
    reps = {R371.A: 1, R371.B: 2}
    next_var = SOURCE["nvars"] + 1
    seed = {}
    defs = []
    for p, np, r, nr, h in template:
        node_id = len(nodes)
        truth = and_truth(np, nr)
        node = {"id": node_id, "rule": "DEF", "var": next_var,
                "inputs": [reps[p], reps[r]], "truth": truth}
        nodes.append(node)
        facets = C2.def_facets(reps[p], reps[r], next_var, tuple(truth))
        for j, clause in enumerate(facets):
            seed.setdefault(key(clause), {"node": node_id, "view": "clause", "facet": j})
        defs.append({"node": node_id, "var": next_var, "inputs": node["inputs"], "truth": truth})
        reps[h] = next_var
        next_var += 1
    return reps[template[-1][-1]], seed, defs


def resolution_closure(seed, nodes):
    clauses = dict(seed)
    parents = {c: None for c in clauses}
    changed = True
    while changed:
        changed = False
        current = list(clauses)
        for i, left in enumerate(current):
            for right in current[i + 1:]:
                for pivot in range(1, max(map(abs, left + right), default=0) + 1):
                    for got in C2.oriented_resolvents(left, right, pivot):
                        if got in clauses:
                            continue
                        node_id = len(nodes)
                        nodes.append({"id": node_id, "rule": "RES",
                                      "left": clauses[left], "right": clauses[right],
                                      "pivot": pivot, "clause": list(got)})
                        clauses[got] = {"node": node_id, "view": "clause"}
                        parents[got] = (left, right, pivot)
                        changed = True
    return clauses, parents


def ancestry_nodes(clause, parents, seen=None):
    if seen is None:
        seen = set()
    if clause in seen or parents[clause] is None:
        return 0
    seen.add(clause)
    left, right, _ = parents[clause]
    return 1 + ancestry_nodes(left, parents, seen) + ancestry_nodes(right, parents, seen)


def trim_and_renumber(nodes, root_refs):
    """Keep DEF owners plus the union of actual referenced RES ancestry once."""
    by_id = {n["id"]: n for n in nodes}
    needed = {n["id"] for n in nodes if n["rule"] == "DEF"}
    stack = [r["node"] for r in root_refs if "node" in r]
    while stack:
        i = stack.pop()
        if i in needed:
            continue
        needed.add(i)
        n = by_id[i]
        if n["rule"] == "RES":
            for side in (n["left"], n["right"]):
                if "node" in side:
                    stack.append(side["node"])
    order = sorted(needed)
    ren = {old: new for new, old in enumerate(order)}

    def rr(ref):
        out = copy.deepcopy(ref)
        if "node" in out:
            out["node"] = ren[out["node"]]
        return out

    trimmed = []
    for old in order:
        n = copy.deepcopy(by_id[old]); n["id"] = ren[old]
        if n["rule"] == "RES":
            n["left"], n["right"] = rr(n["left"]), rr(n["right"])
        trimmed.append(n)
    return trimmed, [rr(r) for r in root_refs]


def compile_table(table: int, template):
    nodes = []
    output, seed, defs = add_def_network(template, nodes)
    closure, parents = resolution_closure(seed, nodes)
    # REFEREE371 bit positions use 2*a+b; CANON2 row positions use a+2*b.
    # This explicit permutation is load-bearing byte authentication.
    old_truth = tuple(int(R371.expected(table, bool(a), bool(b)))
                      for b in (0, 1) for a in (0, 1))
    old_facets = C2.def_facets(1, 2, output, old_truth)
    mapped = []
    for index, target in enumerate(old_facets):
        candidates = [c for c in closure if set(c).issubset(target)]
        assert candidates, (table, index, target)
        representative = min(candidates, key=lambda c: (len(c), ancestry_nodes(c, parents)))
        mapped.append({"old_facet": index, "target": list(target),
                       "representative": list(representative),
                       "exact_target_in_strict_resolution_closure": target in closure,
                       "reference": closure[representative],
                       "resolution_ancestry_nodes": ancestry_nodes(representative, parents)})

    # The checker insists on a contradiction.  The final core is native and
    # deliberately independent of the local normalizer trace; every local node
    # is nevertheless parsed and checked.  No minimum-cost claim uses this file.
    final_id = len(nodes)
    nodes.append({"id": final_id, "rule": "RES",
                  "left": {"src": 0, "view": "clause"},
                  "right": {"src": 1, "view": "clause"},
                  "pivot": 1, "clause": []})
    roots = [x["reference"] for x in mapped] + [{"node": final_id, "view": "clause"}]
    nodes, new_roots = trim_and_renumber(nodes, roots)
    for item, ref in zip(mapped, new_roots[:-1]):
        item["reference"] = ref
    final_ref = new_roots[-1]
    proof = C2.doc(SOURCE, nodes, final_ref)
    stats = C2.Checker(proof, SOURCE).run()
    wrapper = C2R.wrap(RAW_SOURCE, proof)
    wrapper_stats = C2R.check_wrapper(wrapper)
    assert stats["paid_nodes"] == wrapper_stats["paid_nodes"]
    return proof, wrapper, {"table": f"{table:04b}", "old_truth": list(old_truth),
                            "compiled_definitions": len(defs),
                            "compiled_definition_records": defs,
                            "closure_clause_count": len(closure),
                            "projected_old_facets": mapped,
                            "paid_nodes_in_validation_trace": stats["paid_nodes"],
                            "certificate_bytes": stats["certificate_bytes"],
                            "wrapper_bytes": wrapper_stats["wrapper_bytes"],
                            "references": stats["references"]}


def accepted_old_gate(table: int):
    truth = [int(R371.expected(table, bool(a), bool(b)))
             for b in (0, 1) for a in (0, 1)]
    nodes = [{"id": 0, "rule": "DEF", "var": 3, "inputs": [1, 2], "truth": truth},
             {"id": 1, "rule": "RES", "left": {"src": 0, "view": "clause"},
              "right": {"src": 1, "view": "clause"}, "pivot": 1, "clause": []}]
    proof = C2.doc(SOURCE, nodes, {"node": 1, "view": "clause"})
    stats = C2.Checker(proof, SOURCE).run()
    wrapper = C2R.wrap(RAW_SOURCE, proof); C2R.check_wrapper(wrapper)
    assert stats["paid_nodes"] == 2
    return proof, wrapper


def reject(fn, needle):
    try:
        fn()
    except (C2.Reject, C2R.RawReject) as exc:
        assert needle in str(exc), (needle, str(exc))
        return "REJECTED: " + str(exc)
    raise AssertionError("hostile control accepted")


def controls(proofs, wrappers):
    corrupt_truth = copy.deepcopy(proofs[6])
    corrupt_truth["nodes"][0]["truth"][0] ^= 1
    truth_reject = reject(lambda: C2.Checker(corrupt_truth, SOURCE).run(), "oriented resolvent")

    nonfresh = copy.deepcopy(proofs[6])
    nonfresh["nodes"][0]["var"] += 1
    nonfresh_reject = reject(lambda: C2.Checker(nonfresh, SOURCE).run(), "nonfresh DEF")

    bad_pivot = copy.deepcopy(proofs[6])
    rr = next(n for n in bad_pivot["nodes"] if n["rule"] == "RES" and n["clause"])
    rr["pivot"] = 999
    pivot_reject = reject(lambda: C2.Checker(bad_pivot, SOURCE).run(), "bad RES types")

    extra_key = copy.deepcopy(proofs[6])
    extra_key["nodes"][0]["semantic_oracle"] = True
    payload_reject = reject(lambda: C2.Checker(extra_key, SOURCE).run(), "wrong keys")

    bad_raw = copy.deepcopy(wrappers[6])
    bad_raw["source_raw_sha256"] = "0" * 64
    raw_reject = reject(lambda: C2R.check_wrapper(bad_raw), "raw hash mismatch")

    sat = copy.deepcopy(proofs[6])
    sat["source"]["clauses"] = [[1], [1]]
    sat["source_sha256"] = C2.source_hash(sat["source"])
    sat_final = sat["nodes"][-1]
    sat_reject = reject(lambda: C2.Checker(sat, sat["source"]).run(), "not an oriented resolvent")
    return {"corrupt_gate_truth": truth_reject, "nonfresh_output": nonfresh_reject,
            "corrupt_pivot": pivot_reject, "hidden_payload": payload_reject,
            "raw_hash_mismatch": raw_reject, "sat_same_sign_source": sat_reject}


def main():
    started = time.perf_counter()
    templates, bfs_states = R371.bfs_templates()
    proofs, wrappers, summaries, old_proofs, old_wrappers = [], [], [], [], []
    for table in range(16):
        proof, wrapper, summary = compile_table(table, templates[table])
        proofs.append(proof); wrappers.append(wrapper); summaries.append(summary)
        old, oldw = accepted_old_gate(table); old_proofs.append(old); old_wrappers.append(oldw)
    hostile = controls(proofs, wrappers)
    cert_payload = {"artifact": "REFEREE372-CANON2R-CERTIFICATES",
                    "old_arbitrary_gate_proofs": old_proofs, "old_arbitrary_gate_wrappers": old_wrappers,
                    "normalized_and_only_proofs": proofs, "normalized_and_only_wrappers": wrappers}
    CERTS.parent.mkdir(parents=True, exist_ok=True)
    CERTS.write_text(json.dumps(cert_payload, indent=2, sort_keys=True) + "\n")

    total_facets = sum(len(x["projected_old_facets"]) for x in summaries)
    exact_facets = sum(y["exact_target_in_strict_resolution_closure"]
                       for x in summaries for y in x["projected_old_facets"])
    payload = {
        "artifact": "REFEREE372", "status": "PASS",
        "scope": "actual frozen CANON2/CANON2R accepted bytes; not historical /341 authority",
        "function_tables": 16, "bfs_states": bfs_states,
        "all_four_old_facets_checked": total_facets,
        "exact_old_facets_in_strict_resolution_closure": exact_facets,
        "subclause_only_old_facets": total_facets - exact_facets,
        "minimal_exact_facet_counterexample": {
            "old_gate": "constant-0 truth table 0000 on distinct inputs a,b",
            "old_facet_0": [1, 2, -3],
            "and_only_replacement": "z=(b AND (NOT b)) with aliased input id 2",
            "derived_strict_subclause": [-3],
            "claim_falsified": "every old positional facet is exactly derivable by strict RES from the AND-only replacement"
        },
        "maximum_compiled_definitions": max(x["compiled_definitions"] for x in summaries),
        "maximum_facet_resolution_ancestry": max(y["resolution_ancestry_nodes"] for x in summaries for y in x["projected_old_facets"]),
        "validation_trace_paid_nodes_range": [min(x["paid_nodes_in_validation_trace"] for x in summaries), max(x["paid_nodes_in_validation_trace"] for x in summaries)],
        "certificate_bytes_range": [min(x["certificate_bytes"] for x in summaries), max(x["certificate_bytes"] for x in summaries)],
        "wrapper_bytes_range": [min(x["wrapper_bytes"] for x in summaries), max(x["wrapper_bytes"] for x in summaries)],
        "summaries": summaries, "hostile_controls": hostile,
        "resource_ledger": {"construction_and_actual_checker_seconds": round(time.perf_counter()-started, 6),
                            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                            "proof_search": "finite BFS synthesis plus exhaustive Resolution closure; charged offline",
                            "logical_xor_trace": "not used"},
        "status_ledger": {"canon2r_byte_normalization": "PROVED/COMPUTATIONAL subclause normalization for all 16 binary gate tags and four exposed facets; exact facet identity falsified for 24/64",
                          "historical_rmix341_bytes": "OPEN",
                          "same_R_B3": "OPEN", "P_vs_NP": "OPEN"}
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
