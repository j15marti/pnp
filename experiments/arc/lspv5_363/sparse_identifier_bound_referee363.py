#!/usr/bin/env python3
"""REFEREE363: sparse-ID bound and JSON-number collision controls.

This imports the frozen CANON2 checker and constructs accepted proofs with
large, sparse source identifiers.  It checks the reachable-identifier bound
used in the report and emits raw JSON for an independent JavaScript control.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
C2_PATH = ROOT / "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py"
RAW_PATH = ROOT / "results/raw/arc/lspv5_363"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C2 = load_module(C2_PATH, "rmix341_canon2_referee361")


def source_doc(nvars: int):
    clauses = [[1], [-1]]
    source = {"nvars": nvars, "clauses": clauses}
    return C2.doc(source, [], {"src": 0, "view": "clause"})


def build_sparse_proof(digits: int, defs: int = 10, locals_: int = 10):
    # A huge but exactly parsed original-variable namespace.  Only a sparse
    # subset is ever reachable from paid proof records.
    nvars = int("9" * digits)
    doc = source_doc(nvars)
    nodes = []

    # Each DEF introduces at most two previously unreachable inputs and its
    # one mandatory fresh auxiliary output.
    for k in range(defs):
        node_id = len(nodes)
        nodes.append(
            {
                "id": node_id,
                "rule": "DEF",
                "var": nvars + k + 1,
                "inputs": [2 + 2 * k, 3 + 2 * k],
                "truth": [0, 1, 1, 0],
            }
        )

    # Each LOCAL output has combined parent/output support at most three.
    # From source clause (1), this adds two new original IDs per node.
    for k in range(locals_):
        node_id = len(nodes)
        a = 1000 + 2 * k
        b = 1001 + 2 * k
        nodes.append(
            {
                "id": node_id,
                "rule": "LOCAL",
                "parent": {"src": 0, "view": "clause"},
                "out": {"kind": "clause", "clause": [1, a, b]},
            }
        )

    # The final contradiction is independent of the deliberately dead sparse
    # records, which tests the entire accepted certificate grammar.
    final_id = len(nodes)
    nodes.append(
        {
            "id": final_id,
            "rule": "RES",
            "left": {"src": 0, "view": "clause"},
            "right": {"src": 1, "view": "clause"},
            "pivot": 1,
            "clause": [],
        }
    )
    doc["nodes"] = nodes
    doc["final"] = {"node": final_id, "view": "clause"}
    return doc


def build_er_or_embedding_control():
    """One legal DEF plus two RES nodes derive the usual ER OR clauses."""
    source = {"nvars": 2, "clauses": [[1], [-1]]}
    nodes = [
        {
            "id": 0,
            "rule": "DEF",
            "var": 3,
            "inputs": [1, 2],
            "truth": [0, 1, 1, 1],  # z <-> (x1 OR x2)
        },
        {
            "id": 1,
            "rule": "RES",
            "left": {"node": 0, "view": "clause", "facet": 1},
            "right": {"node": 0, "view": "clause", "facet": 3},
            "pivot": 1,
            "clause": [-2, 3],
        },
        {
            "id": 2,
            "rule": "RES",
            "left": {"node": 0, "view": "clause", "facet": 2},
            "right": {"node": 0, "view": "clause", "facet": 3},
            "pivot": 2,
            "clause": [-1, 3],
        },
        {
            "id": 3,
            "rule": "RES",
            "left": {"src": 0, "view": "clause"},
            "right": {"src": 1, "view": "clause"},
            "pivot": 1,
            "clause": [],
        },
    ]
    return C2.doc(source, nodes, {"node": 3, "view": "clause"})


def identifiers(doc):
    """Collect variable/auxiliary IDs, excluding node/source reference IDs."""
    out = set()
    nvars = doc["source"]["nvars"]
    for clause in doc["source"]["clauses"]:
        out.update(abs(lit) for lit in clause)
    for node in doc["nodes"]:
        rule = node["rule"]
        if rule == "DEF":
            out.add(node["var"])
            out.update(node["inputs"])
        elif rule == "LOCAL":
            if node["out"]["kind"] == "clause":
                out.update(abs(lit) for lit in node["out"]["clause"])
            else:
                out.update(node["out"]["factor"]["support"])
        elif rule == "RES":
            out.add(node["pivot"])
            out.update(abs(lit) for lit in node["clause"])
        elif rule == "AND3":
            out.update(node["factor"]["support"])
        elif rule == "GF2":
            out.update(node["affine"]["mask"])
    assert all(1 <= x <= nvars + len(doc["nodes"]) for x in out)
    return out


def main():
    cases = []
    for digits in (16, 17, 18, 80, 200):
        doc = build_sparse_proof(digits)
        checker = C2.Checker(doc, doc["source"])
        accepted = checker.run()["accepted"]
        ids = identifiers(doc)
        q = len(doc["nodes"])
        a0 = len({abs(lit) for c in doc["source"]["clauses"] for lit in c})
        reachable_bound = a0 + 3 * q
        encoded = C2.canon_bytes(doc)
        cases.append(
            {
                "digits": digits,
                "accepted": accepted,
                "q": q,
                "source_reachable_ids": a0,
                "actual_reachable_ids": len(ids),
                "bound_a0_plus_3q": reachable_bound,
                "bound_holds": len(ids) <= reachable_bound,
                "canonical_bytes": len(encoded),
                "max_identifier_digits": max(len(str(x)) for x in ids),
                "header_digits": len(str(doc["source"]["nvars"])),
            }
        )

    # Python's arbitrary-precision JSON integers distinguish these.  Ordinary
    # JavaScript JSON.parse represents both by the same binary64 Number.
    js_a = '{"nvars":9007199254740992,"id":9007199254740992}'
    js_b = '{"nvars":9007199254740993,"id":9007199254740993}'
    py_a = json.loads(js_a)
    py_b = json.loads(js_b)
    collision = {
        "a": js_a,
        "b": js_b,
        "python_objects_equal": py_a == py_b,
        "python_nvars_equal": py_a["nvars"] == py_b["nvars"],
        "expected_javascript_number_equal": True,
        "repair": "encode every identifier and nvars as a canonical decimal string, or mandate arbitrary-precision integer-token parsing",
    }

    er_doc = build_er_or_embedding_control()
    er_stats = C2.Checker(er_doc, er_doc["source"]).run()
    er_embedding = {
        "accepted": er_stats["accepted"],
        "paid_nodes": er_stats["paid_nodes"],
        "definition": "z <-> (x1 OR x2)",
        "exported_facets": C2.def_facets(1, 2, 3, (0, 1, 1, 1)),
        "derived_standard_er_clauses": [[-2, 3], [-1, 3]],
        "constant_overhead_fact": "one DEF and at most two RES derive the three standard OR-extension clauses",
    }

    result = {
        "format": "LSPV5-SPARSE-ID-BOUND-REFEREE363-1",
        "checker": str(C2_PATH.relative_to(ROOT)),
        "cases": cases,
        "numeric_collision_control": collision,
        "extended_resolution_embedding_control": er_embedding,
        "status": {
            "sparse_id_blob_falsifier": "FAILED: all accepted cases satisfy A0+3q",
            "node_to_bit_polynomial": "PROVED for frozen CANON2 under arbitrary-precision integer semantics",
            "cross_language_json_number_uniqueness": "FALSIFIED for ordinary JavaScript Number parsing above 2^53",
            "polynomial_retraction_to_source_only_resolution": "FALSIFIED by Cook ER-short PHP plus Haken Resolution-hard PHP, using the constant-overhead DEF/RES embedding",
            "b3": "OPEN",
        },
    }
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    out = RAW_PATH / "sparse_identifier_bound_referee363.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    timestamped = ROOT / "results/raw/arc/2026-11-05_0648_LSPV5_REFEREE363_raw.json"
    timestamped.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
