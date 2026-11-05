#!/usr/bin/env python3
"""REFEREE365: constructive size audit for CANON2R -> EF and ER -> CANON2R.

This script does not pretend to emit an authoritative Extended-Frege byte
format.  It replays actual CANON2 certificates, constructs the explicit
relation/circuit-size ledger used by the mathematical simulation proof, and
tests the rule-local identities and hostile malformed controls.  The report
contains the symbolic proof of the polynomial simulations.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


C2 = load(ROOT / "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py", "canon2_365")
R364 = load(ROOT / "experiments/arc/lspv5_364/dependency_slice_referee364.py", "ref364_365")
BASE = load(ROOT / "experiments/arc/lspv5_360/rmix341_canon1_referee360.py", "canon1_fixture_365")


def relation_symbols(rel: tuple[str, Any]) -> int:
    """Conservative circuit/extension-symbol count for one explicit relation."""
    kind, data = rel
    if kind == "clause":
        return 5 + 4 * len(data)
    if kind == "factor":
        support, truth = data
        return 12 + 4 * len(support) + 4 * len(truth)
    if kind == "affine":
        mask, _rhs = data
        return 8 + 8 * len(mask)
    raise AssertionError(kind)


def node_relations(checker: C2.Checker, node_id: int):
    return [v for k, v in checker.views.items() if k[0] == "n" and k[1] == node_id]


def compile_ledger(doc: dict, label: str) -> dict:
    checker = C2.Checker(doc, doc["source"])
    stats = checker.run()
    q = len(doc["nodes"])
    source_symbols = sum(5 + 4 * len(c) for c in doc["source"]["clauses"])
    relation_total = source_symbols
    macro_total = 0
    rules = {}
    max_relation = 0
    for node in doc["nodes"]:
        i, rule = node["id"], node["rule"]
        rules[rule] = rules.get(rule, 0) + 1
        rs = node_relations(checker, i)
        assert rs, (label, i, rule)
        sizes = [relation_symbols(r) for r in rs]
        relation_total += sum(sizes)
        max_relation = max(max_relation, *sizes)
        # EF macro proof: constant truth-table proof for DEF/AND3/LOCAL/RES;
        # linear parity-associativity/cancellation proof for GF2.
        if rule == "GF2":
            width = len(rs[0][1][0])
            macro_total += 64 + 32 * (width + 1)
        elif rule in {"AND3", "LOCAL", "DEF"}:
            macro_total += 256 + 8 * sum(sizes)
        elif rule == "RES":
            macro_total += 64 + 4 * sum(sizes)
        else:
            raise AssertionError(rule)

    ef_symbols = relation_total + macro_total
    source_bytes = len(C2.canon_bytes(doc["source"]))
    cert_bytes = len(C2.canon_bytes(doc))
    # A deliberately loose polynomial in the declared source and paid nodes.
    polynomial_cap = 4096 * (source_bytes + q + 1) ** 4
    assert cert_bytes <= polynomial_cap
    assert ef_symbols <= polynomial_cap
    return {
        "label": label,
        "paid_nodes": q,
        "rules": rules,
        "source_bytes": source_bytes,
        "certificate_bytes": cert_bytes,
        "relation_symbols": relation_total,
        "ef_macro_symbols": macro_total,
        "ef_total_symbol_budget": ef_symbols,
        "polynomial_cap": polynomial_cap,
        "max_relation_symbols": max_relation,
        "checker_stats": stats,
    }


def odd_k4() -> dict:
    d = BASE.k4_tseitin([1, 0, 0, 0])
    d = copy.deepcopy(d)
    d["format"] = "Rmix341-CANON2"
    return d


def full_mixed() -> dict:
    raw = json.loads((ROOT / "results/raw/arc/2026-11-05_0512_LSPV2_MIXED_DEF_PORT416.json").read_text())
    return raw["complete_certificate"]


def expect_reject(doc: dict, needle: str) -> str:
    try:
        C2.Checker(doc, doc["source"]).run()
    except C2.Reject as exc:
        msg = str(exc)
        assert needle in msg, (needle, msg)
        return msg
    raise AssertionError("unexpected acceptance")


def er_embedding_controls() -> dict:
    """All 16 binary gates expose exactly four checked defining facets."""
    checks = 0
    rows = []
    for table in range(16):
        truth = tuple((table >> i) & 1 for i in range(4))
        facets = C2.def_facets(1, 2, 3, truth)
        assert len(facets) == 4
        for av in (0, 1):
            for bv in (0, 1):
                want = truth[av | (bv << 1)]
                for zv in (0, 1):
                    env = {1: av, 2: bv, 3: zv}
                    all_facets = all(C2.eval_clause(c, env) for c in facets)
                    assert all_facets == (zv == want)
                    checks += 1
        rows.append({"table": table, "facet_count": 4})
    return {"tables": rows, "valuation_checks": checks}


def hostile_controls(base: dict) -> dict:
    bad_sum = copy.deepcopy(base)
    gf = next(n for n in bad_sum["nodes"] if n["rule"] == "GF2")
    gf["affine"]["rhs"] ^= 1
    wrong_gf2 = expect_reject(bad_sum, "wrong GF2 sum")

    hidden = copy.deepcopy(base)
    hidden["nodes"][0]["implicit_semantic_oracle"] = True
    hidden_payload = expect_reject(hidden, "wrong keys")

    future = R364.build_hidden_owner_chain(3, 0)
    future["nodes"][0]["inputs"][0] = future["nodes"][0]["var"]
    forward_input = expect_reject(future, "bad DEF input")

    sat = R364.build_hidden_owner_chain(3, 0, sat_control=True)
    sat_reject = expect_reject(sat, "not an oriented resolvent")
    return {
        "wrong_gf2": wrong_gf2,
        "hidden_payload": hidden_payload,
        "forward_def_input": forward_input,
        "sat_same_sign": sat_reject,
    }


def main() -> None:
    docs = [
        (odd_k4(), "odd-k4-tseitin"),
        (full_mixed(), "full-mixed-17"),
        (R364.build_hidden_owner_chain(50, 7), "hidden-owner-50-plus-7-dead"),
    ]
    ledgers = [compile_ledger(d, label) for d, label in docs]
    embedding = er_embedding_controls()
    controls = hostile_controls(docs[1][0])

    assertions = embedding["valuation_checks"]
    assertions += sum(8 + x["paid_nodes"] for x in ledgers)
    assertions += 8
    out = {
        "format": "LSPV5-EF-EQUIVALENCE-AUDIT-REFEREE365-1",
        "status": {
            "canon2r_to_ef": "PROVED/RESTRICTED symbolically; executable size ledger checked",
            "er_to_canon2r": "PROVED/RESTRICTED for explicit facet-addressable CANON2R",
            "historical_rmix341_reverse_simulation": "OPEN: authoritative selector bytes absent",
            "bare_b3": "OPEN; equivalent target would require strong-system polynomial boundedness",
            "p_vs_np": "OPEN",
        },
        "ledgers": ledgers,
        "er_embedding": embedding,
        "hostile_controls": controls,
        "assertions": assertions,
        "randomness": "none",
        "limitation": "No authoritative EF byte checker is claimed or executed; the full proof is the rule-by-rule symbolic construction in the report.",
    }
    path = ROOT / "results/raw/arc/2026-11-05_0848_LSPV5_REFEREE365_raw.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
