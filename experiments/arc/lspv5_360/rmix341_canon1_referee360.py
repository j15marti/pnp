#!/usr/bin/env python3
"""REFEREE360: proposed exact finite-alphabet checker for literal R_mix341.

Rmix341-CANON1 does not add an inference rule or change a weight.  It freezes
the root-only/fixed-facet completion audited in REFEREE359: every record is one
paid node; LOCAL internal wires are never addressable; a DEF has four fixed
CNF facets; AND3/LOCAL factors have at most three original variables; and GF2
rows are explicit sorted masks with an RHS bit.
"""
from __future__ import annotations

import copy
import hashlib
import json
from itertools import product
from pathlib import Path
from typing import Any


class Reject(ValueError):
    pass


def exact_keys(x: dict, keys: set[str], where: str) -> None:
    if not isinstance(x, dict) or set(x) != keys:
        raise Reject(f"{where}: expected keys {sorted(keys)}, got {sorted(x) if isinstance(x, dict) else type(x).__name__}")


def canon_bytes(x: Any) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def source_hash(source: dict) -> str:
    return hashlib.sha256(canon_bytes(source)).hexdigest()


def strict_loads(s: str) -> Any:
    def hook(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise Reject(f"duplicate JSON key: {k}")
            out[k] = v
        return out
    try:
        return json.loads(s, object_pairs_hook=hook)
    except json.JSONDecodeError as e:
        raise Reject(f"invalid JSON: {e}") from e


def norm_clause(c: Any, maxvar: int, where: str) -> tuple[int, ...]:
    if not isinstance(c, list) or any(type(l) is not int or l == 0 or abs(l) > maxvar for l in c):
        raise Reject(f"{where}: invalid literal")
    if c != sorted(c, key=lambda z: (abs(z), z < 0)):
        raise Reject(f"{where}: clause is not canonical")
    if len({abs(l) for l in c}) != len(c):
        raise Reject(f"{where}: repeated/complementary variable")
    return tuple(c)


def norm_affine(a: Any, maxvar: int, where: str) -> tuple[tuple[int, ...], int]:
    exact_keys(a, {"mask", "rhs"}, where)
    m = a["mask"]
    if not isinstance(m, list) or any(type(v) is not int or not 1 <= v <= maxvar for v in m):
        raise Reject(f"{where}: invalid mask")
    if m != sorted(set(m)):
        raise Reject(f"{where}: mask is not strictly sorted")
    if type(a["rhs"]) is not int or a["rhs"] not in (0, 1):
        raise Reject(f"{where}: rhs is not a bit")
    return tuple(m), a["rhs"]


def norm_factor(f: Any, nvars: int, where: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    exact_keys(f, {"support", "truth"}, where)
    s, t = f["support"], f["truth"]
    if not isinstance(s, list) or any(type(v) is not int or not 1 <= v <= nvars for v in s):
        raise Reject(f"{where}: bad support")
    if s != sorted(set(s)) or len(s) > 3:
        raise Reject(f"{where}: support must be sorted, unique, and <=3")
    if not isinstance(t, list) or len(t) != (1 << len(s)) or any(type(b) is not int or b not in (0, 1) for b in t):
        raise Reject(f"{where}: bad truth table")
    return tuple(s), tuple(t)


def eval_clause(c: tuple[int, ...], env: dict[int, int]) -> int:
    return int(any(env[abs(l)] == int(l > 0) for l in c))


def eval_factor(f: tuple[tuple[int, ...], tuple[int, ...]], env: dict[int, int]) -> int:
    s, t = f
    idx = sum(env[v] << i for i, v in enumerate(s))
    return t[idx]


def eval_affine(a: tuple[tuple[int, ...], int], env: dict[int, int]) -> int:
    m, rhs = a
    return int(sum(env[v] for v in m) % 2 == rhs)


def relation_support(rel) -> set[int]:
    kind, body = rel
    if kind == "clause":
        return {abs(l) for l in body}
    return set(body[0])


def relation_eval(rel, env: dict[int, int]) -> int:
    kind, body = rel
    return {"clause": eval_clause, "factor": eval_factor, "affine": eval_affine}[kind](body, env)


def truth_from_rel(rel, support: list[int]) -> list[int]:
    out = []
    for bits in product((0, 1), repeat=len(support)):
        out.append(relation_eval(rel, dict(zip(support, bits))))
    # product order is big-endian; canonical tables index support[0] as LSB.
    if support:
        corrected = [0] * (1 << len(support))
        for bits in product((0, 1), repeat=len(support)):
            idx = sum(bits[i] << i for i in range(len(support)))
            corrected[idx] = relation_eval(rel, dict(zip(support, bits)))
        return corrected
    return out


def xor_affines(a, b):
    am, ar = a
    bm, br = b
    return tuple(sorted(set(am) ^ set(bm))), ar ^ br


def def_facets(a: int, b: int, z: int, truth: tuple[int, ...]) -> list[tuple[int, ...]]:
    facets = []
    for av in (0, 1):
        for bv in (0, 1):
            zv = 1 - truth[av | (bv << 1)]
            row = ((a, av), (b, bv), (z, zv))
            clause = tuple(sorted((v if bit == 0 else -v for v, bit in row), key=lambda q: (abs(q), q < 0)))
            facets.append(clause)
    return facets


class Checker:
    def __init__(self, doc: dict):
        self.doc = doc
        self.views: dict[tuple, tuple[str, Any]] = {}
        self.nodes = 0
        self.truth_assignments = 0
        self.refs = 0
        self.next_def = 0
        self.maxvar = 0
        self.nvars = 0

    def ref(self, r: Any, before: int):
        if not isinstance(r, dict):
            raise Reject("reference is not an object")
        if "wire" in r or "selector" in r:
            raise Reject("internal wire/selector references are forbidden")
        self.refs += 1
        if "src" in r:
            exact_keys(r, {"src", "view"}, "source ref")
            if type(r["src"]) is not int or r["view"] != "clause":
                raise Reject("bad source reference")
            key = ("src", r["src"], "clause")
        else:
            allowed = {"node", "view"} | ({"facet"} if "facet" in r else set())
            exact_keys(r, allowed, "node ref")
            if type(r["node"]) is not int or r["node"] < 0 or r["node"] >= before:
                raise Reject("forward/missing node reference")
            if r["view"] == "clause" and "facet" in r:
                if type(r["facet"]) is not int:
                    raise Reject("facet is not integer")
                key = ("node", r["node"], "clause", r["facet"])
            elif "facet" not in r:
                key = ("node", r["node"], r["view"])
            else:
                raise Reject("facet only allowed on clause view")
        if key not in self.views:
            raise Reject(f"unavailable view {key}")
        return self.views[key]

    def add(self, key, rel):
        if key in self.views:
            raise Reject(f"duplicate view {key}")
        self.views[key] = rel

    def run(self) -> dict:
        exact_keys(self.doc, {"format", "source", "source_sha256", "nodes", "final"}, "document")
        if self.doc["format"] != "Rmix341-CANON1":
            raise Reject("wrong format")
        src = self.doc["source"]
        exact_keys(src, {"nvars", "clauses"}, "source")
        if type(src["nvars"]) is not int or src["nvars"] < 0 or not isinstance(src["clauses"], list):
            raise Reject("bad source header")
        self.nvars = src["nvars"]
        self.maxvar = self.nvars
        self.next_def = self.nvars + 1
        if self.doc["source_sha256"] != source_hash(src):
            raise Reject("source SHA-256 mismatch")
        for i, c in enumerate(src["clauses"]):
            cc = norm_clause(c, self.nvars, f"source clause {i}")
            self.add(("src", i, "clause"), ("clause", cc))
        nodes = self.doc["nodes"]
        if not isinstance(nodes, list):
            raise Reject("nodes is not a list")
        for i, rec in enumerate(nodes):
            if not isinstance(rec, dict) or rec.get("id") != i or type(rec.get("id")) is not int:
                raise Reject(f"node {i}: nonsequential id")
            rule = rec.get("rule")
            if rule == "RES":
                exact_keys(rec, {"id", "rule", "left", "right", "pivot", "clause"}, f"RES {i}")
                l = self.ref(rec["left"], i); r = self.ref(rec["right"], i)
                if l[0] != "clause" or r[0] != "clause" or type(rec["pivot"]) is not int or not 1 <= rec["pivot"] <= self.maxvar:
                    raise Reject(f"RES {i}: bad types/pivot")
                p = rec["pivot"]
                if not ((p in l[1] and -p in r[1]) or (-p in l[1] and p in r[1])):
                    raise Reject(f"RES {i}: pivot absent")
                want = sorted(({x for x in l[1] if abs(x) != p} | {x for x in r[1] if abs(x) != p}), key=lambda z: (abs(z), z < 0))
                if len({abs(x) for x in want}) != len(want):
                    raise Reject(f"RES {i}: tautological resolvent")
                got = norm_clause(rec["clause"], self.maxvar, f"RES {i} output")
                if tuple(want) != got: raise Reject(f"RES {i}: wrong resolvent")
                self.add(("node", i, "clause"), ("clause", got))
            elif rule == "AND3":
                keys = {"id", "rule", "left", "right", "factor"} | ({"affine"} if "affine" in rec else set())
                exact_keys(rec, keys, f"AND3 {i}")
                l = self.ref(rec["left"], i); r = self.ref(rec["right"], i)
                if l[0] not in ("clause", "factor") or r[0] not in ("clause", "factor"):
                    raise Reject(f"AND3 {i}: inputs must be Boolean conditions")
                support = sorted(relation_support(l) | relation_support(r))
                if len(support) > 3 or any(v > self.nvars for v in support):
                    raise Reject(f"AND3 {i}: support not <=3 original variables")
                got = norm_factor(rec["factor"], self.nvars, f"AND3 {i} factor")
                want = []
                for idx in range(1 << len(support)):
                    env = {v: (idx >> j) & 1 for j, v in enumerate(support)}
                    want.append(relation_eval(l, env) & relation_eval(r, env)); self.truth_assignments += 1
                if got != (tuple(support), tuple(want)):
                    raise Reject(f"AND3 {i}: wrong conjunction table")
                self.add(("node", i, "factor"), ("factor", got))
                if "affine" in rec:
                    aff = norm_affine(rec["affine"], self.maxvar, f"AND3 {i} affine")
                    if set(aff[0]) != set(support):
                        raise Reject(f"AND3 {i}: affine support mismatch")
                    for idx in range(1 << len(support)):
                        env = {v: (idx >> j) & 1 for j, v in enumerate(support)}
                        if eval_factor(got, env) != eval_affine(aff, env):
                            raise Reject(f"AND3 {i}: false affine annotation")
                        self.truth_assignments += 1
                    self.add(("node", i, "affine"), ("affine", aff))
            elif rule == "GF2":
                exact_keys(rec, {"id", "rule", "left", "right", "affine"}, f"GF2 {i}")
                l = self.ref(rec["left"], i); r = self.ref(rec["right"], i)
                if l[0] != "affine" or r[0] != "affine": raise Reject(f"GF2 {i}: nonaffine parent")
                got = norm_affine(rec["affine"], self.maxvar, f"GF2 {i} output")
                if got != xor_affines(l[1], r[1]): raise Reject(f"GF2 {i}: wrong row addition")
                self.add(("node", i, "affine"), ("affine", got))
            elif rule == "LOCAL":
                exact_keys(rec, {"id", "rule", "parent", "out"}, f"LOCAL {i}")
                parent = self.ref(rec["parent"], i)
                out = rec["out"]
                if not isinstance(out, dict) or out.get("kind") not in ("clause", "factor"):
                    raise Reject(f"LOCAL {i}: bad output")
                if out["kind"] == "clause":
                    exact_keys(out, {"kind", "clause"}, f"LOCAL {i} out")
                    body = norm_clause(out["clause"], self.nvars, f"LOCAL {i} clause")
                    rel = ("clause", body)
                else:
                    exact_keys(out, {"kind", "factor"}, f"LOCAL {i} out")
                    body = norm_factor(out["factor"], self.nvars, f"LOCAL {i} factor")
                    rel = ("factor", body)
                support = sorted(relation_support(parent) | relation_support(rel))
                if len(support) > 3 or any(v > self.nvars for v in support):
                    raise Reject(f"LOCAL {i}: implication support not <=3 originals")
                for idx in range(1 << len(support)):
                    env = {v: (idx >> j) & 1 for j, v in enumerate(support)}
                    if relation_eval(parent, env) and not relation_eval(rel, env):
                        raise Reject(f"LOCAL {i}: implication fails")
                    self.truth_assignments += 1
                self.add(("node", i, out["kind"]), rel)
            elif rule == "DEF":
                exact_keys(rec, {"id", "rule", "var", "inputs", "truth"}, f"DEF {i}")
                z, ins, truth = rec["var"], rec["inputs"], rec["truth"]
                if type(z) is not int or z != self.next_def or not isinstance(ins, list) or len(ins) != 2:
                    raise Reject(f"DEF {i}: nonfresh/noncanonical definition")
                if any(type(v) is not int or not 1 <= v < z for v in ins): raise Reject(f"DEF {i}: bad input")
                if not isinstance(truth, list) or len(truth) != 4 or any(type(b) is not int or b not in (0, 1) for b in truth):
                    raise Reject(f"DEF {i}: truth is not four bits")
                self.maxvar = z; self.next_def += 1
                facets = def_facets(ins[0], ins[1], z, tuple(truth))
                for j, c in enumerate(facets): self.add(("node", i, "clause", j), ("clause", c))
            else:
                raise Reject(f"node {i}: unknown rule {rule}")
            self.nodes += 1
        final = self.ref(self.doc["final"], len(nodes))
        contradiction = (final[0] == "clause" and len(final[1]) == 0) or (final[0] == "affine" and final[1] == ((), 1)) or (final[0] == "factor" and not any(final[1][1]))
        if not contradiction: raise Reject("final view is not contradiction")
        return {"accepted": True, "paid_nodes": self.nodes, "references": self.refs,
                "truth_assignments": self.truth_assignments, "source_bytes": len(canon_bytes(src)),
                "certificate_bytes": len(canon_bytes(self.doc)), "max_variable": self.maxvar}


def make_doc(source: dict, nodes: list[dict], final: dict) -> dict:
    return {"format": "Rmix341-CANON1", "source": source, "source_sha256": source_hash(source), "nodes": nodes, "final": final}


def parity_clauses(vars3: list[int], rhs: int) -> list[list[int]]:
    out = []
    for bits in product((0, 1), repeat=3):
        if sum(bits) % 2 != rhs:
            out.append(sorted([v if b == 0 else -v for v, b in zip(vars3, bits)], key=lambda z: (abs(z), z < 0)))
    return out


def k4_tseitin(charges: list[int]) -> dict:
    # edges 12,13,14,23,24,34; four degree-3 vertex equations.
    rows = [[1, 2, 3], [1, 4, 5], [2, 4, 6], [3, 5, 6]]
    clauses = []
    groups = []
    for vs, rhs in zip(rows, charges):
        g = list(range(len(clauses), len(clauses) + 4)); groups.append(g)
        clauses.extend(parity_clauses(vs, rhs))
    source = {"nvars": 6, "clauses": clauses}
    nodes = []
    affine_nodes = []
    for vs, rhs, group in zip(rows, charges, groups):
        left = {"src": group[0], "view": "clause"}
        for k in range(1, 4):
            right = {"src": group[k], "view": "clause"}
            support = sorted(vs)
            parents = []
            # Compute declared factor directly from conjunction of first k+1 clauses.
            truth = []
            for idx in range(8):
                env = {v: (idx >> j) & 1 for j, v in enumerate(support)}
                truth.append(int(all(eval_clause(tuple(clauses[group[t]]), env) for t in range(k + 1))))
            rec = {"id": len(nodes), "rule": "AND3", "left": left, "right": right,
                   "factor": {"support": support, "truth": truth}}
            if k == 3:
                rec["affine"] = {"mask": support, "rhs": rhs}
            nodes.append(rec)
            left = {"node": rec["id"], "view": "factor"}
        affine_nodes.append(nodes[-1]["id"])
    def gf2(a, b, mask, rhs):
        rec = {"id": len(nodes), "rule": "GF2", "left": {"node": a, "view": "affine"},
               "right": {"node": b, "view": "affine"}, "affine": {"mask": mask, "rhs": rhs}}
        nodes.append(rec); return rec["id"]
    a = gf2(affine_nodes[0], affine_nodes[1], [2, 3, 4, 5], charges[0] ^ charges[1])
    b = gf2(affine_nodes[2], affine_nodes[3], [2, 3, 4, 5], charges[2] ^ charges[3])
    c = gf2(a, b, [], sum(charges) % 2)
    return make_doc(source, nodes, {"node": c, "view": "affine"})


def res_control() -> dict:
    source = {"nvars": 1, "clauses": [[1], [-1]]}
    node = {"id": 0, "rule": "RES", "left": {"src": 0, "view": "clause"},
            "right": {"src": 1, "view": "clause"}, "pivot": 1, "clause": []}
    return make_doc(source, [node], {"node": 0, "view": "clause"})


def local_control() -> dict:
    source = {"nvars": 1, "clauses": [[]]}
    node = {"id": 0, "rule": "LOCAL", "parent": {"src": 0, "view": "clause"},
            "out": {"kind": "factor", "factor": {"support": [], "truth": [0]}}}
    return make_doc(source, [node], {"node": 0, "view": "factor"})


def def_local_control() -> dict:
    # DEF z=x1 AND x2, then use fixed facet 3 with source units x1,x2,zbar.
    source = {"nvars": 2, "clauses": [[1], [2]]}
    nodes = [{"id": 0, "rule": "DEF", "var": 3, "inputs": [1, 2], "truth": [0, 0, 0, 1]},
             {"id": 1, "rule": "RES", "left": {"node": 0, "view": "clause", "facet": 3},
              "right": {"src": 0, "view": "clause"}, "pivot": 1, "clause": [-2, 3]},
             {"id": 2, "rule": "RES", "left": {"node": 1, "view": "clause"},
              "right": {"src": 1, "view": "clause"}, "pivot": 2, "clause": [3]}]
    # This is rule-valid but not a refutation; retain as partial grammar control.
    return {"format": "Rmix341-CANON1", "source": source, "source_sha256": source_hash(source), "nodes": nodes,
            "final": {"node": 2, "view": "clause"}}


def reject_reason(doc: dict) -> str:
    try:
        Checker(doc).run()
    except Reject as e:
        return str(e)
    raise AssertionError("corruption unexpectedly accepted")


def main() -> None:
    odd = k4_tseitin([1, 0, 0, 0])
    even = k4_tseitin([0, 0, 0, 0])
    res = res_control()
    local = local_control()
    odd_stats = Checker(odd).run()
    res_stats = Checker(res).run()
    local_stats = Checker(local).run()
    controls = []
    # Even charge has a valid 15-node derivation ending 0=0, hence is not a refutation.
    controls.append({"name": "even_tseitin_not_refutation", "reason": reject_reason(even)})
    mutations = []
    def mut(name, fn):
        d = copy.deepcopy(odd); fn(d); mutations.append({"name": name, "reason": reject_reason(d)})
    mut("wrong_source_hash", lambda d: d.__setitem__("source_sha256", "0" * 64))
    mut("forward_reference", lambda d: d["nodes"][0].__setitem__("left", {"node": 1, "view": "factor"}))
    mut("hidden_wire_selector", lambda d: d["nodes"][1].__setitem__("left", {"node": 0, "view": "factor", "wire": "g0"}))
    mut("bad_and3_table", lambda d: d["nodes"][0]["factor"]["truth"].__setitem__(0, 1 - d["nodes"][0]["factor"]["truth"][0]))
    mut("false_affine_annotation", lambda d: d["nodes"][2]["affine"].__setitem__("rhs", 0))
    mut("bad_gf2", lambda d: d["nodes"][12]["affine"].__setitem__("rhs", 0))
    mut("noncanonical_source_clause", lambda d: d["source"]["clauses"][0].reverse())
    # Rehash the noncanonical source so rejection is grammatical, not hash-only.
    d = copy.deepcopy(odd); d["source"]["clauses"][0].reverse(); d["source_sha256"] = source_hash(d["source"])
    mutations[-1] = {"name": "noncanonical_source_clause", "reason": reject_reason(d)}

    partial = def_local_control()
    try:
        Checker(partial).run()
        raise AssertionError("noncontradictory partial proof accepted as refutation")
    except Reject as e:
        controls.append({"name": "def_fixed_facet_partial_trace", "reason": str(e),
                         "rule_prefix_nodes": len(partial["nodes"])})
    badfacet = copy.deepcopy(partial); badfacet["nodes"][1]["left"]["facet"] = 4
    controls.append({"name": "bad_def_facet", "reason": reject_reason(badfacet)})
    nonfresh = copy.deepcopy(partial); nonfresh["nodes"][0]["var"] = 2
    controls.append({"name": "nonfresh_def", "reason": reject_reason(nonfresh)})
    badlocal = make_doc({"nvars": 1, "clauses": [[1]]},
                        [{"id": 0, "rule": "LOCAL", "parent": {"src": 0, "view": "clause"},
                          "out": {"kind": "clause", "clause": [-1]}}],
                        {"node": 0, "view": "clause"})
    controls.append({"name": "false_local_implication", "reason": reject_reason(badlocal)})

    sat_source = {"nvars": 2, "clauses": [[1, 2]]}
    sat_doc = make_doc(sat_source, [], {"src": 0, "view": "clause"})
    controls.append({"name": "SAT_source_no_refutation", "reason": reject_reason(sat_doc)})
    malformed_text = '{"a":1,"a":2}'
    try:
        strict_loads(malformed_text); raise AssertionError("duplicate key accepted")
    except Reject as e:
        controls.append({"name": "duplicate_json_key", "reason": str(e)})

    result = {
        "run": "REFEREE360",
        "format": "Rmix341-CANON1",
        "status": {
            "exact_finite_alphabet_parser": "PROPOSED_AND_EXECUTABLE_NOT_HISTORICALLY_AUTHORITATIVE",
            "rule_by_rule_checker_soundness": "PROVED_FOR_LITERAL_ROOT_ONLY_FIXED_FACET_COMPLETION",
            "normalization": "POLYNOMIAL_BY_REFEREE359_PLUS_THIS_EXACT_SERIALIZATION",
            "same_R_B3": "OPEN_PSIMULATION_OR_REFLECTION_MISSING",
            "P_vs_NP": "OPEN"
        },
        "odd_k4": odd_stats,
        "resolution": res_stats,
        "local": local_stats,
        "mutations": mutations,
        "controls": controls,
        "odd_certificate": odd,
        "resource_model": {
            "logical_weight": odd_stats["paid_nodes"],
            "encoded_input_bytes": odd_stats["source_bytes"],
            "encoded_certificate_bytes": odd_stats["certificate_bytes"],
            "checker_truth_assignments": odd_stats["truth_assignments"],
            "checker_references": odd_stats["references"],
            "physical_note": "Python counters are reproducible implementation work, not a universal TM or FLMV time/space theorem; parsing, hashing, reads, writes, allocation, and output remain charged."
        }
    }
    out = Path("results/raw/arc/2026-11-05_0348_LSPV5_REFEREE360_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"raw": str(out), "odd": odd_stats, "mutations": len(mutations), "controls": len(controls)}, sort_keys=True))


if __name__ == "__main__":
    main()
