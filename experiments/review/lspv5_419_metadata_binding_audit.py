#!/usr/bin/env python3
"""LSPV-5/419: source/proof metadata binding audit of recovered /341 checker."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
CHECKER = ROOT / "replay/413/lspv2_341_independent_verify.js"
OUT = ROOT / "results/raw/review/2026-11-07_1548_LSPV5_METADATA_BINDING419.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_checker(obj):
    raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        fh.write(raw)
        name = fh.name
    try:
        cp = subprocess.run(
            ["node", str(CHECKER), name], capture_output=True, text=True, timeout=30
        )
        return {
            "accepted": cp.returncode == 0,
            "returncode": cp.returncode,
            "stdout_sha256": sha256(cp.stdout.encode()),
            "stderr_first_line": cp.stderr.splitlines()[0] if cp.stderr else "",
            "raw_sha256": sha256(raw.encode()),
            "raw_bytes": len(raw.encode()),
        }
    finally:
        Path(name).unlink(missing_ok=True)


def strict_metadata(obj, baseline):
    """Independent consistency check for fields the recovered checker partly ignores."""
    try:
        if obj.get("version") != baseline["version"]:
            return False, "version"
        if obj.get("definition") != baseline["definition"]:
            return False, "definition"
        fixtures, summary = obj["fixtures"], obj["summary"]
        if len(fixtures) != len(summary):
            return False, "summary length"
        for i, f in enumerate(fixtures):
            g, props, sm = f["graph"], f["properties"], summary[i]
            v, e = g["n"], len(g["edges"])
            if len(f["charges"]) != v or not all(x in (0, 1) for x in f["charges"]):
                return False, "charges"
            if sum(f["charges"]) % 2 != 1:
                return False, "charge parity"
            degree, edge_keys = [0] * v, set()
            for a, b in g["edges"]:
                if not (isinstance(a, int) and isinstance(b, int) and 0 <= a < v and 0 <= b < v and a != b):
                    return False, "graph edge"
                key = tuple(sorted((a, b)))
                if key in edge_keys:
                    return False, "duplicate edge"
                edge_keys.add(key); degree[a] += 1; degree[b] += 1
            if any(d != 3 for d in degree):
                return False, "graph degree"
            if sm.get("name") != g["name"]:
                return False, "summary name"
            expected_summary = {
                "vertices": v,
                "variables": e,
                "clauses": len(f["clauses"]),
                "essential": props["essential"],
                "inferences": len(f["proof"]),
                "predictedMinimum": props["predictedMinimum"],
                "allEssential": props["essential"] == len(f["clauses"]),
            }
            if any(sm.get(k) != val for k, val in expected_summary.items()):
                return False, "summary contents"
            expected_props = {
                "variables": e,
                "sourceClauses": len(f["clauses"]),
                "inferences": len(f["proof"]),
                "oddUnsat": True,
                "evenSat": True,
                "predictedMinimum": len(f["proof"]) if props["essential"] == len(f["clauses"]) else None,
            }
            if any(props.get(k) != val for k, val in expected_props.items()):
                return False, "properties"
            incid = [[] for _ in range(v)]
            for edge, (a, b) in enumerate(g["edges"]):
                incid[a].append(edge)
                incid[b].append(edge)
            source_ids = set()
            for c in f["clauses"]:
                if c["id"] in source_ids or not isinstance(c["vertex"], int) or not 0 <= c["vertex"] < v:
                    return False, "source identity"
                source_ids.add(c["id"])
                pattern = 0
                for bit, edge in enumerate(incid[c["vertex"]]):
                    lit = next(x for x in c["literals"] if abs(x) == edge + 1)
                    if lit < 0:
                        pattern |= 1 << bit
                if c.get("pattern") != pattern:
                    return False, "clause pattern"
            if len(f["deleted"]) != len(f["clauses"]):
                return False, "deletion arity"
            if any(d.get("sourceId") != c["id"] for d, c in zip(f["deleted"], f["clauses"])):
                return False, "deletion provenance"
            if props["essential"] != sum(d.get("assignment") is not None for d in f["deleted"]):
                return False, "essential count"
            witness = f["evenWitness"]
            if not isinstance(witness, str) or len(witness) != e or set(witness) - {"0", "1"}:
                return False, "even witness syntax"
            for edges in incid:
                if sum(int(witness[x]) for x in edges) % 2:
                    return False, "even witness parity"
            known = set(source_ids)
            for pnode in f["proof"]:
                if pnode["id"] in known or len(pnode.get("parents", [])) != 2 or any(x not in known for x in pnode["parents"]):
                    return False, "proof dependency"
                known.add(pnode["id"])
        return True, ""
    except (KeyError, IndexError, StopIteration, TypeError, ValueError):
        return False, "malformed metadata"


def mutate(base, scope, path, value):
    obj = copy.deepcopy(base)
    cur = obj if scope == "root" else obj["fixtures"][0]
    for step in path[:-1]:
        cur = cur[step]
    cur[path[-1]] = value
    return obj


def main():
    base = json.loads(PACKET.read_text())
    baseline = run_checker(base)
    strict_base = strict_metadata(base, base)
    if not baseline["accepted"] or not strict_base[0]:
        raise AssertionError("baseline failed")

    f = base["fixtures"][0]
    flipped_even = ("1" if f["evenWitness"][0] == "0" else "0") + f["evenWitness"][1:]
    specs = [
        ("unbound_root_version", "root", ["version"], "FORGED/v99", True, "root declaration"),
        ("unbound_root_definition", "root", ["definition"], "FORGED: RES and DEF are free", True, "grammar declaration"),
        ("unbound_summary_contents", "root", ["summary", 0], {}, True, "summary record"),
        ("unbound_clause_pattern", "fixture", ["clauses", 0, "pattern"], 7, True, "source pattern provenance"),
        ("unbound_property_variables", "fixture", ["properties", "variables"], 999, True, "reported variable count"),
        ("unbound_property_source_clauses", "fixture", ["properties", "sourceClauses"], 0, True, "reported source count"),
        ("unbound_property_inferences", "fixture", ["properties", "inferences"], 0, True, "reported inference count"),
        ("unbound_property_odd_unsat", "fixture", ["properties", "oddUnsat"], False, True, "reported odd status"),
        ("unbound_property_even_sat", "fixture", ["properties", "evenSat"], False, True, "reported even status"),
        ("unbound_property_predicted_minimum", "fixture", ["properties", "predictedMinimum"], 0, True, "reported minimum"),
        ("bound_graph_self_loop", "fixture", ["graph", "edges", 0], [0, 0], False, "graph structure"),
        ("bound_charge_parity", "fixture", ["charges", 0], f["charges"][0] ^ 1, False, "charge parity"),
        ("bound_clause_vertex", "fixture", ["clauses", 0, "vertex"], 999, False, "clause owner"),
        ("bound_clause_literal", "fixture", ["clauses", 0, "literals", 0], 999, False, "source literal"),
        ("bound_source_id_uniqueness", "fixture", ["clauses", 1, "id"], f["clauses"][0]["id"], False, "source ID"),
        ("bound_deleted_source", "fixture", ["deleted", 0, "sourceId"], "forged", False, "deletion provenance"),
        ("bound_even_witness", "fixture", ["evenWitness"], flipped_even, False, "even witness"),
        ("bound_proof_parent", "fixture", ["proof", 0, "parents", 0], "forged", False, "proof edge"),
        ("bound_property_essential", "fixture", ["properties", "essential"], 0, False, "essential count"),
        ("bound_summary_length", "root", ["summary"], base["summary"][:-1], False, "fixture-summary arity"),
    ]

    cases = []
    for name, scope, path, value, expected, classification in specs:
        obj = mutate(base, scope, path, value)
        result = run_checker(obj)
        strict_ok, strict_reason = strict_metadata(obj, base)
        result.update({
            "name": name,
            "scope": scope,
            "path": path,
            "classification": classification,
            "expected_checker_accept": expected,
            "strict_metadata_accept": strict_ok,
            "strict_metadata_reason": strict_reason,
            "same_stdout_as_baseline": result["stdout_sha256"] == baseline["stdout_sha256"],
        })
        if result["accepted"] != expected:
            raise AssertionError(f"unexpected checker result: {result}")
        if strict_ok:
            raise AssertionError(f"strict metadata verifier accepted mutation: {name}")
        if expected and not result["same_stdout_as_baseline"]:
            raise AssertionError(f"accepted ignored-field mutation changed output: {name}")
        cases.append(result)

    record = {
        "experiment": "LSPV-5/419 recovered-checker metadata binding audit",
        "timestamp_pst": "2026-11-07 15:48 PST",
        "status": "COMPUTATIONAL/PROVED-RESTRICTED",
        "scope": "recovered SOURCE/AND3/XOR checker and declared packet schema only",
        "packet": str(PACKET.relative_to(ROOT)),
        "packet_sha256": sha256(PACKET.read_bytes()),
        "checker": str(CHECKER.relative_to(ROOT)),
        "checker_sha256": sha256(CHECKER.read_bytes()),
        "baseline": baseline,
        "case_count": len(cases),
        "accepted_unbound_count": sum(c["accepted"] for c in cases),
        "rejected_bound_control_count": sum(not c["accepted"] for c in cases),
        "strict_metadata_rejection_count": sum(not c["strict_metadata_accept"] for c in cases),
        "cases": cases,
        "limitations": [
            "The checker strongly binds graph edges, charges, clause owners/literals/IDs, deletion witnesses, proof edges and the essential count in the tested controls.",
            "Ignored report/provenance fields do not create a satisfiable accepted source or shorter proof.",
            "Whether ignored fields are normative historical grammar or informational metadata remains an authority question.",
            "RES, LOCAL-CONVERT, DEF facets, branching and full historical grammar remain unauthenticated.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS",
        "cases": len(cases),
        "accepted_unbound": record["accepted_unbound_count"],
        "rejected_bound_controls": record["rejected_bound_control_count"],
        "strict_metadata_rejected": record["strict_metadata_rejection_count"],
        "baseline_stdout_sha256": baseline["stdout_sha256"],
        "output": str(OUT.relative_to(ROOT)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
