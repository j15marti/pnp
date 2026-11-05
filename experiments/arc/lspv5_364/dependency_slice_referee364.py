#!/usr/bin/env python3
"""REFEREE364: dependency-closed proof slicing for frozen CANON2.

The adversarial family has a chain of paid definitions whose outputs are used
only as numeric inputs to later definitions. Ordinary reference-only backward
slicing drops the owners and produces an invalid certificate. Adding
auxiliary-owner edges and order-preserving alpha-renaming repairs it.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
C2_PATH = ROOT / "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py"
RAW_PATH = ROOT / "results/raw/arc/2026-11-05_0748_LSPV5_REFEREE364_raw.json"
MIXED_FIXTURE = ROOT / "results/raw/arc/2026-11-05_0512_LSPV2_MIXED_DEF_PORT416.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C2 = load_module(C2_PATH, "rmix341_canon2_referee364")


def ref_nodes(node: dict):
    fields = {
        "RES": ("left", "right"),
        "AND3": ("left", "right"),
        "GF2": ("left", "right"),
        "LOCAL": ("parent",),
        "DEF": (),
    }[node["rule"]]
    for field in fields:
        ref = node[field]
        if "node" in ref:
            yield ref["node"]


def semantic_vars(node: dict):
    rule = node["rule"]
    if rule == "DEF":
        yield node["var"]
        yield from node["inputs"]
    elif rule == "RES":
        yield node["pivot"]
        yield from (abs(x) for x in node["clause"])
    elif rule == "AND3":
        yield from node["factor"]["support"]
        if "affine" in node:
            yield from node["affine"]["mask"]
    elif rule == "GF2":
        yield from node["affine"]["mask"]
    elif rule == "LOCAL":
        out = node["out"]
        if out["kind"] == "clause":
            yield from (abs(x) for x in out["clause"])
        else:
            yield from out["factor"]["support"]


def explicit_ancestors(doc: dict):
    todo = [doc["final"]["node"]] if "node" in doc["final"] else []
    keep = set()
    while todo:
        i = todo.pop()
        if i in keep:
            continue
        keep.add(i)
        todo.extend(ref_nodes(doc["nodes"][i]))
    return keep


def dependency_closed_ancestors(doc: dict):
    keep = explicit_ancestors(doc)
    nvars = doc["source"]["nvars"]
    owner = {
        node["var"]: node["id"]
        for node in doc["nodes"]
        if node["rule"] == "DEF"
    }
    changed = True
    while changed:
        changed = False
        additions = set()
        for i in tuple(keep):
            additions.update(ref_nodes(doc["nodes"][i]))
            for v in semantic_vars(doc["nodes"][i]):
                if v > nvars:
                    if v not in owner:
                        raise ValueError(f"auxiliary {v} has no paid DEF owner")
                    additions.add(owner[v])
        additions -= keep
        if additions:
            keep |= additions
            changed = True
    return keep


def remap_ref(ref: dict, node_map: dict):
    out = copy.deepcopy(ref)
    if "node" in out:
        out["node"] = node_map[out["node"]]
    return out


def canonical_lits(lits):
    return sorted(set(lits), key=lambda x: (abs(x), x < 0))


def slice_and_rename(doc: dict, keep: set[int]):
    nvars = doc["source"]["nvars"]
    ordered = sorted(keep)
    node_map = {old: new for new, old in enumerate(ordered)}
    def_nodes = [i for i in ordered if doc["nodes"][i]["rule"] == "DEF"]
    var_map = {
        doc["nodes"][old]["var"]: nvars + rank + 1
        for rank, old in enumerate(def_nodes)
    }

    def mv(v):
        if v <= nvars:
            return v
        return var_map.get(v, v)

    new_nodes = []
    for old in ordered:
        node = copy.deepcopy(doc["nodes"][old])
        node["id"] = node_map[old]
        rule = node["rule"]
        if rule == "DEF":
            node["var"] = mv(node["var"])
            node["inputs"] = [mv(v) for v in node["inputs"]]
        elif rule == "RES":
            node["left"] = remap_ref(node["left"], node_map)
            node["right"] = remap_ref(node["right"], node_map)
            node["pivot"] = mv(node["pivot"])
            node["clause"] = canonical_lits(
                (mv(abs(lit)) if lit > 0 else -mv(abs(lit)))
                for lit in node["clause"]
            )
        elif rule == "AND3":
            node["left"] = remap_ref(node["left"], node_map)
            node["right"] = remap_ref(node["right"], node_map)
            node["factor"]["support"] = sorted(mv(v) for v in node["factor"]["support"])
            if "affine" in node:
                node["affine"]["mask"] = sorted(mv(v) for v in node["affine"]["mask"])
        elif rule == "GF2":
            node["left"] = remap_ref(node["left"], node_map)
            node["right"] = remap_ref(node["right"], node_map)
            node["affine"]["mask"] = sorted(mv(v) for v in node["affine"]["mask"])
        elif rule == "LOCAL":
            node["parent"] = remap_ref(node["parent"], node_map)
            out = node["out"]
            if out["kind"] == "clause":
                out["clause"] = canonical_lits(
                    (mv(abs(lit)) if lit > 0 else -mv(abs(lit)))
                    for lit in out["clause"]
                )
            else:
                out["factor"]["support"] = sorted(mv(v) for v in out["factor"]["support"])
        new_nodes.append(node)

    result = copy.deepcopy(doc)
    result["nodes"] = new_nodes
    result["final"] = remap_ref(result["final"], node_map)
    return result


def build_hidden_owner_chain(chain: int, dead_after: int = 0, sat_control=False):
    assert chain >= 2
    source = {"nvars": 1, "clauses": [[1], [1] if sat_control else [-1]]}
    nodes = [
        {"id": 0, "rule": "DEF", "var": 2, "inputs": [1, 1],
         "truth": [0, 0, 0, 0]}
    ]
    for j in range(2, chain + 1):
        nodes.append(
            {"id": len(nodes), "rule": "DEF", "var": j + 1,
             "inputs": [j, 1], "truth": [0, 0, 1, 1]}
        )
    final_var = chain + 1
    final_def = chain - 1

    for _ in range(dead_after):
        z = 2 + len([n for n in nodes if n["rule"] == "DEF"])
        nodes.append(
            {"id": len(nodes), "rule": "DEF", "var": z,
             "inputs": [1, 1], "truth": [0, 1, 1, 0]}
        )

    k = len(nodes)
    nodes.extend(
        [
            {"id": k, "rule": "RES",
             "left": {"node": final_def, "view": "clause", "facet": 1},
             "right": {"node": final_def, "view": "clause", "facet": 3},
             "pivot": chain, "clause": [-1, final_var]},
            {"id": k + 1, "rule": "RES",
             "left": {"node": k, "view": "clause"},
             "right": {"src": 0, "view": "clause"},
             "pivot": 1, "clause": [final_var]},
            {"id": k + 2, "rule": "RES",
             "left": {"node": final_def, "view": "clause", "facet": 0},
             "right": {"node": final_def, "view": "clause", "facet": 2},
             "pivot": chain, "clause": [1, -final_var]},
            {"id": k + 3, "rule": "RES",
             "left": {"node": k + 2, "view": "clause"},
             "right": {"src": 1, "view": "clause"},
             "pivot": 1, "clause": [-final_var]},
            {"id": k + 4, "rule": "RES",
             "left": {"node": k + 1, "view": "clause"},
             "right": {"node": k + 3, "view": "clause"},
             "pivot": final_var, "clause": []},
        ]
    )
    return C2.doc(source, nodes, {"node": len(nodes) - 1, "view": "clause"})


def reject_reason(doc):
    try:
        C2.Checker(doc, doc["source"]).run()
    except Exception as exc:
        return str(exc)
    raise AssertionError("unexpected acceptance")


def main():
    cases = []
    assertions = 0
    for chain in (2, 3, 10, 50):
        for dead in (0, 1, 7):
            doc = build_hidden_owner_chain(chain, dead)
            original = C2.Checker(doc, doc["source"]).run()
            assertions += 1
            explicit = explicit_ancestors(doc)
            naive = slice_and_rename(doc, explicit)
            naive_reject = reject_reason(naive)
            assertions += 1
            closed = dependency_closed_ancestors(doc)
            repaired = slice_and_rename(doc, closed)
            repaired_stats = C2.Checker(repaired, repaired["source"]).run()
            assertions += 1
            assert len(explicit) == 6
            assert len(closed) == chain + 5
            assert len(repaired["nodes"]) == chain + 5
            assert repaired["source"] == doc["source"]
            assert repaired["source_sha256"] == doc["source_sha256"]
            assertions += 5
            cases.append(
                {"chain": chain, "dead_definitions": dead,
                 "original_nodes": original["paid_nodes"],
                 "reference_only_nodes": len(explicit),
                 "reference_only_reject": naive_reject,
                 "dependency_closed_nodes": repaired_stats["paid_nodes"],
                 "pruned_nodes": original["paid_nodes"] - repaired_stats["paid_nodes"],
                 "source_hash_preserved": repaired["source_sha256"] == doc["source_sha256"],
                 "accepted_after_repair": repaired_stats["accepted"]}
            )

    sat_reason = reject_reason(build_hidden_owner_chain(3, 2, sat_control=True))
    assertions += 1

    # Full DEF/RES/AND3/LOCAL/GF2 peer fixture with two trailing dead DEFs.
    mixed_raw = json.loads(MIXED_FIXTURE.read_text())
    mixed = copy.deepcopy(mixed_raw["complete_certificate"])
    mixed["nodes"].append(
        {"id": 17, "rule": "DEF", "var": 5, "inputs": [1, 1],
         "truth": [0, 1, 1, 0]}
    )
    mixed["nodes"].append(
        {"id": 18, "rule": "DEF", "var": 6, "inputs": [5, 1],
         "truth": [0, 0, 1, 1]}
    )
    mixed_before = C2.Checker(mixed, mixed["source"]).run()
    mixed_keep = dependency_closed_ancestors(mixed)
    mixed_after_doc = slice_and_rename(mixed, mixed_keep)
    mixed_after = C2.Checker(mixed_after_doc, mixed_after_doc["source"]).run()
    assert mixed_before["paid_nodes"] == 19
    assert mixed_after["paid_nodes"] == 17
    assert mixed_after_doc["source_sha256"] == mixed["source_sha256"]
    assertions += 5
    base = build_hidden_owner_chain(2)
    bad_fresh = copy.deepcopy(base)
    bad_fresh["nodes"][0]["var"] = 3
    bad_input = copy.deepcopy(base)
    bad_input["nodes"][1]["inputs"][0] = 3
    bad_output = copy.deepcopy(base)
    bad_output["nodes"][-1]["clause"] = [1]
    controls = {
        "sat_same_sign_source_reject": sat_reason,
        "malformed_nonfresh_def_reject": reject_reason(bad_fresh),
        "malformed_forward_self_input_reject": reject_reason(bad_input),
        "malformed_final_output_reject": reject_reason(bad_output),
    }
    assertions += 3
    result = {
        "format": "LSPV5-DEPENDENCY-SLICE-REFEREE364-1",
        "checker": str(C2_PATH.relative_to(ROOT)),
        "cases": cases,
        "full_mixed_fixture": {
            "rules": ["DEF", "RES", "AND3", "LOCAL", "GF2"],
            "before_nodes": mixed_before["paid_nodes"],
            "after_nodes": mixed_after["paid_nodes"],
            "pruned_dead_definitions": 2,
            "source_hash_preserved":
                mixed_after_doc["source_sha256"] == mixed["source_sha256"],
            "accepted_after_repair": mixed_after["accepted"],
        },
        "controls": controls,
        "assertions": assertions,
        "status": {
            "reference_only_backward_slice": "FALSIFIED by a 7-node legal proof",
            "dependency_closed_slice_alpha_rename": "PROVED for frozen CANON2R",
            "paid_nodes": "never increase; dead records may be removed",
            "b3": "OPEN; slicing does not generate a proof from a decider trace",
            "p_vs_np": "OPEN",
        },
    }
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
