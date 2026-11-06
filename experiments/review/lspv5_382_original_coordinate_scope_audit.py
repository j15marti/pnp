#!/usr/bin/env python3
"""REFEREE382: audit REFEREE381 against historical original-coordinate scope.

This is a provenance audit, not an authoritative R_mix341 checker.  It reads
the exact published REFEREE381 trace and classifies every AND3/LOCAL node under
two explicitly distinct grammars: WIRE (fresh DEF outputs allowed) and ORIG
(support must be source-coordinate variables).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACE = ROOT / "results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json"
OUT = ROOT / "results/raw/review/2026-11-06_0148_LSPV5_ORIGINAL_COORDINATE_SCOPE382.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    raw = TRACE.read_bytes()
    doc = json.loads(raw)
    assert doc["run"] == "LSPV-5/REFEREE381"
    assert sha256(raw) == "f3200e609df200d892ff630103c3490961094d705585880daf4df3befa7254a3"

    rows = []
    for inst in doc["instances"]:
        source_max = inst["source_variables"]
        nodes = inst["trace"]["nodes"]
        by_id = {n["id"]: n for n in nodes}
        def_outputs = {n["out"] for n in nodes if n["kind"] == "DEF"}
        assert def_outputs and min(def_outputs) > source_max

        and3_bad, local_bad = [], []
        for n in nodes:
            if n["kind"] == "AND3":
                support = n["support"]
                assert 0 < len(support) <= 3
                assert set(support) <= def_outputs
                and3_bad.append({
                    "id": n["id"],
                    "support": support,
                    "all_fresh_def_outputs": True,
                    "wire_support_legal": True,
                    "original_support_legal": False,
                })
            elif n["kind"] == "LOCAL":
                parent = by_id[n["parent"]]
                assert parent["kind"] == "XOR"
                support = parent["affine"]["vars"]
                assert len(support) == 3
                assert set(support) <= def_outputs
                assert set(map(abs, n["clause"])) <= set(support)
                local_bad.append({
                    "id": n["id"],
                    "parent": n["parent"],
                    "support": support,
                    "all_fresh_def_outputs": True,
                    "wire_support_legal": True,
                    "original_support_legal": False,
                })

        h = inst["vertices"]
        assert len(and3_bad) == 3 * (h - 1)
        assert len(local_bad) == 4
        rows.append({
            "graph": inst["graph"],
            "h": h,
            "source_variables": source_max,
            "final_variables": inst["final_variables"],
            "paid_nodes": inst["paid_nodes"],
            "wire_grammar_accepts_affected_nodes": True,
            "original_coordinate_grammar_accepts_trace": False,
            "and3_original_scope_rejections": and3_bad,
            "local_original_scope_rejections": local_bad,
            "rejection_count": len(and3_bad) + len(local_bad),
        })

    # A tiny classifier control: the same parity implication is legal over
    # source coordinates in both policies, but over fresh coordinates only in
    # the explicitly proposed WIRE completion.
    controls = {
        "original_row": {
            "source_max": 3,
            "affine": {"vars": [1, 2, 3], "rhs": 0},
            "implied_clause": [1, 2, -3],
            "wire_legal": True,
            "original_legal": True,
        },
        "fresh_wire_row": {
            "source_max": 3,
            "affine": {"vars": [4, 5, 6], "rhs": 0},
            "implied_clause": [4, 5, -6],
            "wire_legal": True,
            "original_legal": False,
        },
        "large_id_wire_row": {
            "source_max": 3,
            "affine": {"vars": [2**40 + 1, 2**40 + 2, 2**40 + 3], "rhs": 0},
            "implied_clause": [2**40 + 1, 2**40 + 2, -(2**40 + 3)],
            "wire_legal": True,
            "original_legal": False,
        },
    }

    out = {
        "run": "LSPV-5/REFEREE382",
        "timestamp_PST": "2026-11-06 01:48",
        "status": [
            "PROVED/EXACT trace-coordinate classification",
            "FALSIFIED historical-original-coordinate acceptance of REFEREE381",
            "CONDITIONAL acceptance in distinct WIRE-MIX completion",
            "OPEN authoritative historical byte grammar and full mixed minimum",
        ],
        "input_trace_path": str(TRACE.relative_to(ROOT)),
        "input_trace_sha256": sha256(raw),
        "historical_rule_source": {
            "path": "research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex",
            "git_blob": "c87acd11d32ccfc3b7acd3667ef11daeb60079cb",
            "and3_scope": "combined support has at most three original variables",
            "local_text": "from one already derived local factor/equation derive an implied bounded-support condition by explicit constant-support truth table",
        },
        "later_scope_audit": {
            "path": "research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md",
            "interpretation": "literal at-most-three-original-support LOCAL-CONVERT",
        },
        "grammars": {
            "ORIG341": "AND3 and LOCAL support restricted to source-coordinate variables",
            "WIRE_MIX_PROPOSED": "support may contain globally fresh paid DEF outputs; semantic checks unchanged",
        },
        "instances": rows,
        "controls": controls,
        "totals": {
            "instances": len(rows),
            "and3_original_scope_rejections": sum(len(x["and3_original_scope_rejections"]) for x in rows),
            "local_original_scope_rejections": sum(len(x["local_original_scope_rejections"]) for x in rows),
            "all_original_scope_rejections": sum(x["rejection_count"] for x in rows),
        },
        "conclusion": "51h/2+6 remains a checked WIRE-MIX candidate upper bound, but is not an established historical ORIG341 upper bound.",
    }
    assert [x["rejection_count"] for x in rows] == [13, 19, 25]
    assert out["totals"] == {
        "instances": 3,
        "and3_original_scope_rejections": 45,
        "local_original_scope_rejections": 12,
        "all_original_scope_rejections": 57,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"run": out["run"], "trace_sha256": out["input_trace_sha256"], "rejections": [x["rejection_count"] for x in rows], "totals": out["totals"]}, indent=2))


if __name__ == "__main__":
    main()
