#!/usr/bin/env python3
"""Audit the /449 packet against the declarative R_mix341 source/DEF boundary.

This is an independent typed adapter for a proposed facet-addressable grammar.
It is not an implementation of an authoritative historical byte checker.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import resource
import time
from pathlib import Path


def canon_clause(xs):
    if 0 in xs or any(-x in xs for x in xs):
        raise ValueError("zero or tautological clause")
    return sorted(set(xs), key=lambda z: (abs(z), z < 0))


def resolve(a, b, pivot):
    if pivot not in a or -pivot not in b:
        raise ValueError("oriented pivot absent")
    return canon_clause([x for x in a if x != pivot] + [x for x in b if x != -pivot])


def lit_value(lit, assignment):
    value = assignment[abs(lit)]
    return value if lit > 0 else not value


def extract_defs(cert):
    grouped = {}
    for line in cert:
        label = line.get("label", "")
        if not label.startswith("DEF:"):
            continue
        name, facet = label[4:].rsplit(":", 1)
        grouped.setdefault(name, {})[facet] = line

    defs = []
    for owner, name in enumerate(sorted(grouped, key=lambda n: min(x["id"] for x in grouped[n].values()))):
        fs = grouped[name]
        if set(fs) != {"left", "right", "back"}:
            raise ValueError(f"incomplete facets for {name}")
        left, right, back = fs["left"], fs["right"], fs["back"]
        common = set(left["clause"]) & set(right["clause"])
        candidates = [z for z in common if -z in back["clause"]]
        if len(candidates) != 1:
            raise ValueError(f"cannot recover output for {name}")
        neg_out = candidates[0]
        out = -neg_out
        left_lit = next(z for z in left["clause"] if z != neg_out)
        right_lit = next(z for z in right["clause"] if z != neg_out)
        expected = {
            "left": canon_clause([left_lit, -out]),
            "right": canon_clause([right_lit, -out]),
            "back": canon_clause([-left_lit, -right_lit, out]),
        }
        for facet in expected:
            if canon_clause(fs[facet]["clause"]) != expected[facet]:
                raise ValueError(f"wrong {facet} facet for {name}")
        if abs(left_lit) == abs(right_lit):
            raise ValueError(f"repeated input ID for {name}")
        if out <= max(abs(left_lit), abs(right_lit)):
            raise ValueError(f"nonfresh/topologically early output for {name}")

        truth = []
        for av, bv in [(False, False), (False, True), (True, False), (True, True)]:
            assignment = {abs(left_lit): av, abs(right_lit): bv}
            truth.append(int(lit_value(left_lit, assignment) and lit_value(right_lit, assignment)))
        defs.append({
            "owner": owner,
            "name": name,
            "output": out,
            "left_lit": left_lit,
            "right_lit": right_lit,
            "unsigned_input_ids": [abs(left_lit), abs(right_lit)],
            "truth_table_00_01_10_11": truth,
            "facets": {k: {"line_id": fs[k]["id"], "clause": expected[k]} for k in expected},
        })
    return defs


def ref_for(line_id, facet_owner):
    if line_id < 8:
        return {"kind": "original", "line_id": line_id}
    if line_id in facet_owner:
        owner, facet = facet_owner[line_id]
        return {"kind": "facet", "owner": owner, "facet": facet, "line_id": line_id}
    return {"kind": "res", "line_id": line_id}


def replay_ownerized(ownerized):
    clauses = {}
    for src in ownerized["original_sources"]:
        clauses[src["line_id"]] = canon_clause(src["clause"])

    outputs = set()
    for d in ownerized["defs"]:
        if d["output"] in outputs:
            raise ValueError("duplicate DEF output")
        outputs.add(d["output"])
        if abs(d["left_lit"]) == abs(d["right_lit"]):
            raise ValueError("repeated DEF input")
        expected = {
            "left": canon_clause([d["left_lit"], -d["output"]]),
            "right": canon_clause([d["right_lit"], -d["output"]]),
            "back": canon_clause([-d["left_lit"], -d["right_lit"], d["output"]]),
        }
        for facet, item in d["facets"].items():
            if canon_clause(item["clause"]) != expected[facet]:
                raise ValueError("facet not owned by declared DEF")
            clauses[item["line_id"]] = expected[facet]

    for node in ownerized["resolution"]:
        if node["left"]["line_id"] not in clauses or node["right"]["line_id"] not in clauses:
            raise ValueError("missing parent/facet view")
        got = resolve(clauses[node["left"]["line_id"]], clauses[node["right"]["line_id"]], node["pivot"])
        if got != canon_clause(node["clause"]):
            raise ValueError("wrong resolvent")
        clauses[node["line_id"]] = got
    return clauses


def must_reject(ownerized, mutation):
    bad = copy.deepcopy(ownerized)
    mutation(bad)
    try:
        replay_ownerized(bad)
    except (ValueError, KeyError, StopIteration):
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    started = time.perf_counter()
    packet_bytes = Path(args.packet).read_bytes()
    packet = json.loads(packet_bytes)
    cert = packet["certificate"]
    if [x["id"] for x in cert] != list(range(len(cert))):
        raise ValueError("noncanonical line IDs")
    compact = json.dumps({"lines": cert, "targets": packet["compact_target_line_ids"]},
                         sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(compact).hexdigest() != packet["certificate_sha256"]:
        raise ValueError("certificate digest mismatch")

    originals = cert[:8]
    original_clauses = {tuple(canon_clause(x["clause"])) for x in originals}
    alleged_sources = [x for x in cert if x["kind"] == "SOURCE"]
    nonoriginal_free_sources = [x for x in alleged_sources if tuple(canon_clause(x["clause"])) not in original_clauses]
    if len(nonoriginal_free_sources) != 45:
        raise ValueError("expected 45 nonoriginal free facet records")

    defs = extract_defs(cert)
    if len(defs) != 15:
        raise ValueError("expected 15 DEF owners")
    facet_owner = {}
    for d in defs:
        for facet, item in d["facets"].items():
            facet_owner[item["line_id"]] = (d["owner"], facet)
    resolution = []
    for n in cert[53:]:
        if n["kind"] != "RES":
            raise ValueError("unexpected non-RES tail")
        resolution.append({
            "line_id": n["id"], "left": ref_for(n["left"], facet_owner),
            "right": ref_for(n["right"], facet_owner), "pivot": n["pivot"],
            "clause": canon_clause(n["clause"]),
        })
    ownerized = {
        "grammar": "PROPOSED-FACET-OWNER-450",
        "original_sources": [{"line_id": x["id"], "label": x["label"], "clause": canon_clause(x["clause"])} for x in originals],
        "defs": defs,
        "resolution": resolution,
        "targets": packet["compact_target_line_ids"],
    }
    clauses = replay_ownerized(ownerized)
    for target, line_id in ownerized["targets"].items():
        if tuple(clauses[line_id]) != tuple(json.loads(target.replace("(", "[").replace(")", "]"))):
            raise ValueError("target mismatch")

    controls = {
        "raw_historical_source_boundary_rejects_45_nonoriginal_free_sources": len(nonoriginal_free_sources) == 45,
        "ownerized_bad_facet_rejected": must_reject(ownerized, lambda x: x["defs"][0]["facets"]["left"]["clause"].append(999)),
        "ownerized_missing_facet_rejected": must_reject(ownerized, lambda x: x["defs"][0]["facets"].pop("left")),
        "ownerized_wrong_res_pivot_rejected": must_reject(ownerized, lambda x: x["resolution"][0].__setitem__("pivot", 999)),
        "ownerized_repeated_input_rejected": must_reject(ownerized, lambda x: x["defs"][0].__setitem__("right_lit", x["defs"][0]["left_lit"])),
    }
    if not all(controls.values()):
        raise ValueError("hostile control failed")

    elapsed = time.perf_counter() - started
    result = {
        "run": "LSPV5_450_DEF_FACET_OWNER_AUDIT",
        "status": "PASS",
        "scope": "declarative /341 semantic DEF plus proposed facet-owner adapter; not authoritative historical bytes",
        "input_packet_sha256": hashlib.sha256(packet_bytes).hexdigest(),
        "compact_certificate_sha256": packet["certificate_sha256"],
        "raw_packet": {
            "total_lines": len(cert), "records_marked_SOURCE": len(alleged_sources),
            "actual_original_sources": len(originals), "nonoriginal_DEF_facets_marked_SOURCE": len(nonoriginal_free_sources),
            "DEF_records": sum(x["kind"] == "DEF" for x in cert), "RES_records": len(resolution),
        },
        "semantic_signed_gate_compiler": {
            "gates": len(defs), "all_distinct_input_ids": True, "all_fresh_outputs": True,
            "polarity_patterns": {p: sum((d["left_lit"] > 0, d["right_lit"] > 0) == q for d in defs) for p, q in {
                "++": (True, True), "+-": (True, False), "-+": (False, True), "--": (False, False)}.items()},
            "truth_tables": sorted({tuple(d["truth_table_00_01_10_11"]) for d in defs}),
        },
        "proposed_ownerized_packet": ownerized,
        "cost": {"paid_DEF": len(defs), "paid_RES": len(resolution), "distinct_paid_nodes": len(defs) + len(resolution)},
        "controls": controls,
        "resource": {"elapsed_seconds": elapsed, "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "conclusion": {
            "signed_input_semantic_obstruction": "FALSIFIED for declarative arbitrary two-input DEF",
            "raw_449_native_historical_trace": "REJECTED by original-source boundary",
            "facet_owner_serialization": "OPEN for historical bytes; accepted only in proposed adapter",
        },
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
