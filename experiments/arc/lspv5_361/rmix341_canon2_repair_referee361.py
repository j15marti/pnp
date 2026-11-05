#!/usr/bin/env python3
"""REFEREE361: repair and adversarial audit of Rmix341-CANON1.

CANON2 changes no R_mix341 semantic rule or weight.  Relative to CANON1 it:
  (1) uses oriented Resolution and never deletes both pivot signs;
  (2) permits an affine annotation whose mask is a subset of factor support;
  (3) requires exact comparison with an externally supplied original source;
  (4) measures sparse identifiers, not the numeric DIMACS header value.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from itertools import product
from pathlib import Path
from typing import Any


class Reject(ValueError):
    pass


def exact_keys(x: Any, keys: set[str], where: str) -> None:
    if not isinstance(x, dict) or set(x) != keys:
        raise Reject(f"{where}: wrong keys")


def canon_bytes(x: Any) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def source_hash(x: dict) -> str:
    return hashlib.sha256(canon_bytes(x)).hexdigest()


def canonical_clause(lits, maxvar: int, where: str) -> tuple[int, ...]:
    if not isinstance(lits, list) or any(type(x) is not int or x == 0 or abs(x) > maxvar for x in lits):
        raise Reject(f"{where}: invalid literal")
    want = sorted(set(lits), key=lambda x: (abs(x), x < 0))
    if lits != want:
        raise Reject(f"{where}: clause must be a sorted literal set")
    # Complementary literals are allowed: aliased DEF impossible-row facets
    # are tautologies.  Oriented RES remains sound on them.
    return tuple(lits)


def simplify_clause(lits) -> tuple[int, ...]:
    return tuple(sorted(set(lits), key=lambda x: (abs(x), x < 0)))


def norm_affine(a, maxvar: int, where: str):
    exact_keys(a, {"mask", "rhs"}, where)
    m = a["mask"]
    if not isinstance(m, list) or m != sorted(set(m)) or any(type(v) is not int or not 1 <= v <= maxvar for v in m):
        raise Reject(f"{where}: bad mask")
    if type(a["rhs"]) is not int or a["rhs"] not in (0, 1):
        raise Reject(f"{where}: bad rhs")
    return tuple(m), a["rhs"]


def norm_factor(f, nvars: int, where: str):
    exact_keys(f, {"support", "truth"}, where)
    s, t = f["support"], f["truth"]
    if not isinstance(s, list) or s != sorted(set(s)) or len(s) > 3 or any(type(v) is not int or not 1 <= v <= nvars for v in s):
        raise Reject(f"{where}: bad support")
    if not isinstance(t, list) or len(t) != 1 << len(s) or any(type(b) is not int or b not in (0, 1) for b in t):
        raise Reject(f"{where}: bad truth table")
    return tuple(s), tuple(t)


def eval_clause(c, env):
    return int(any(env[abs(x)] == int(x > 0) for x in c))


def eval_factor(f, env):
    s, t = f
    return t[sum(env[v] << i for i, v in enumerate(s))]


def eval_affine(a, env):
    m, rhs = a
    return int(sum(env[v] for v in m) % 2 == rhs)


def support(rel):
    return {abs(x) for x in rel[1]} if rel[0] == "clause" else set(rel[1][0])


def evaluate(rel, env):
    return {"clause": eval_clause, "factor": eval_factor, "affine": eval_affine}[rel[0]](rel[1], env)


def def_facets(a: int, b: int, z: int, truth: tuple[int, ...]):
    out = []
    for av in (0, 1):
        for bv in (0, 1):
            zv = 1 - truth[av | (bv << 1)]
            out.append(simplify_clause([a if av == 0 else -a,
                                        b if bv == 0 else -b,
                                        z if zv == 0 else -z]))
    return out


def oriented_resolvents(a: tuple[int, ...], b: tuple[int, ...], p: int):
    ans = set()
    if p in a and -p in b:
        ans.add(simplify_clause((set(a) - {p}) | (set(b) - {-p})))
    if -p in a and p in b:
        ans.add(simplify_clause((set(a) - {-p}) | (set(b) - {p})))
    return ans


class Checker:
    def __init__(self, doc: dict, external_source: dict):
        self.doc, self.external_source = doc, external_source
        self.views = {}
        self.refs = self.nodes = self.rows = 0
        self.nvars = self.maxvar = self.next_def = 0

    def add(self, k, v):
        if k in self.views: raise Reject("duplicate view")
        self.views[k] = v

    def ref(self, r, before):
        if not isinstance(r, dict) or "wire" in r or "selector" in r:
            raise Reject("bad/private reference")
        self.refs += 1
        if "src" in r:
            exact_keys(r, {"src", "view"}, "source ref")
            if type(r["src"]) is not int or r["view"] != "clause": raise Reject("bad source ref")
            k = ("s", r["src"], "clause")
        else:
            exact_keys(r, {"node", "view"} | ({"facet"} if "facet" in r else set()), "node ref")
            if type(r["node"]) is not int or not 0 <= r["node"] < before: raise Reject("forward/missing ref")
            if "facet" in r:
                if r["view"] != "clause" or type(r["facet"]) is not int: raise Reject("bad facet ref")
                k = ("n", r["node"], "clause", r["facet"])
            else:
                k = ("n", r["node"], r["view"])
        if k not in self.views: raise Reject(f"unavailable view {k}")
        return self.views[k]

    def run(self):
        exact_keys(self.doc, {"format", "source", "source_sha256", "nodes", "final"}, "doc")
        if self.doc["format"] != "Rmix341-CANON2": raise Reject("wrong format")
        src = self.doc["source"]
        exact_keys(src, {"nvars", "clauses"}, "source")
        if canon_bytes(src) != canon_bytes(self.external_source):
            raise Reject("embedded source differs from externally supplied original")
        if self.doc["source_sha256"] != source_hash(src): raise Reject("source hash mismatch")
        if type(src["nvars"]) is not int or src["nvars"] < 0 or not isinstance(src["clauses"], list): raise Reject("bad header")
        self.nvars = self.maxvar = src["nvars"]; self.next_def = self.nvars + 1
        for i, c in enumerate(src["clauses"]):
            self.add(("s", i, "clause"), ("clause", canonical_clause(c, self.nvars, f"source {i}")))
        nodes = self.doc["nodes"]
        if not isinstance(nodes, list): raise Reject("nodes not list")
        for i, r in enumerate(nodes):
            if not isinstance(r, dict) or type(r.get("id")) is not int or r["id"] != i: raise Reject("bad node id")
            rule = r.get("rule")
            if rule == "RES":
                exact_keys(r, {"id", "rule", "left", "right", "pivot", "clause"}, f"RES {i}")
                a, b = self.ref(r["left"], i), self.ref(r["right"], i)
                if a[0] != "clause" or b[0] != "clause" or type(r["pivot"]) is not int or not 1 <= r["pivot"] <= self.maxvar: raise Reject("bad RES types")
                got = canonical_clause(r["clause"], self.maxvar, f"RES {i} output")
                if got not in oriented_resolvents(a[1], b[1], r["pivot"]): raise Reject(f"RES {i}: not an oriented resolvent")
                self.add(("n", i, "clause"), ("clause", got))
            elif rule == "AND3":
                exact_keys(r, {"id", "rule", "left", "right", "factor"} | ({"affine"} if "affine" in r else set()), f"AND3 {i}")
                a, b = self.ref(r["left"], i), self.ref(r["right"], i)
                if a[0] not in ("clause", "factor") or b[0] not in ("clause", "factor"): raise Reject("bad AND3 parents")
                s = sorted(support(a) | support(b))
                if len(s) > 3 or any(v > self.nvars for v in s): raise Reject("AND3 support")
                f = norm_factor(r["factor"], self.nvars, f"AND3 {i}")
                want = []
                for z in range(1 << len(s)):
                    env = {v: (z >> j) & 1 for j, v in enumerate(s)}
                    want.append(evaluate(a, env) & evaluate(b, env)); self.rows += 1
                if f != (tuple(s), tuple(want)): raise Reject("wrong AND3 table")
                self.add(("n", i, "factor"), ("factor", f))
                if "affine" in r:
                    q = norm_affine(r["affine"], self.maxvar, f"AND3 {i} affine")
                    if not set(q[0]).issubset(s): raise Reject("affine mask outside factor support")
                    for z in range(1 << len(s)):
                        env = {v: (z >> j) & 1 for j, v in enumerate(s)}
                        if eval_factor(f, env) != eval_affine(q, env): raise Reject("false affine annotation")
                        self.rows += 1
                    self.add(("n", i, "affine"), ("affine", q))
            elif rule == "GF2":
                exact_keys(r, {"id", "rule", "left", "right", "affine"}, f"GF2 {i}")
                a, b = self.ref(r["left"], i), self.ref(r["right"], i)
                if a[0] != "affine" or b[0] != "affine": raise Reject("nonaffine GF2 parent")
                q = norm_affine(r["affine"], self.maxvar, f"GF2 {i}")
                want = (tuple(sorted(set(a[1][0]) ^ set(b[1][0]))), a[1][1] ^ b[1][1])
                if q != want: raise Reject("wrong GF2 sum")
                self.add(("n", i, "affine"), ("affine", q))
            elif rule == "LOCAL":
                exact_keys(r, {"id", "rule", "parent", "out"}, f"LOCAL {i}")
                a, o = self.ref(r["parent"], i), r["out"]
                if not isinstance(o, dict) or o.get("kind") not in ("clause", "factor"): raise Reject("bad LOCAL out")
                if o["kind"] == "clause":
                    exact_keys(o, {"kind", "clause"}, "LOCAL clause")
                    rel = ("clause", canonical_clause(o["clause"], self.nvars, "LOCAL clause"))
                else:
                    exact_keys(o, {"kind", "factor"}, "LOCAL factor")
                    rel = ("factor", norm_factor(o["factor"], self.nvars, "LOCAL factor"))
                s = sorted(support(a) | support(rel))
                if len(s) > 3 or any(v > self.nvars for v in s): raise Reject("LOCAL support")
                for z in range(1 << len(s)):
                    env = {v: (z >> j) & 1 for j, v in enumerate(s)}
                    if evaluate(a, env) and not evaluate(rel, env): raise Reject("false LOCAL implication")
                    self.rows += 1
                self.add(("n", i, o["kind"]), rel)
            elif rule == "DEF":
                exact_keys(r, {"id", "rule", "var", "inputs", "truth"}, f"DEF {i}")
                z, ins, t = r["var"], r["inputs"], r["truth"]
                if type(z) is not int or z != self.next_def or not isinstance(ins, list) or len(ins) != 2: raise Reject("nonfresh DEF")
                if any(type(v) is not int or not 1 <= v < z for v in ins): raise Reject("bad DEF input")
                if not isinstance(t, list) or len(t) != 4 or any(type(x) is not int or x not in (0, 1) for x in t): raise Reject("bad DEF truth")
                self.maxvar = z; self.next_def += 1
                for j, c in enumerate(def_facets(ins[0], ins[1], z, tuple(t))):
                    self.add(("n", i, "clause", j), ("clause", c))
            else: raise Reject(f"unknown rule {rule}")
            self.nodes += 1
        fin = self.ref(self.doc["final"], len(nodes))
        contradiction = (fin[0] == "clause" and not fin[1]) or (fin[0] == "affine" and fin[1] == ((), 1)) or (fin[0] == "factor" and not any(fin[1][1]))
        if not contradiction: raise Reject("final is not contradiction")
        active = set()
        for c in src["clauses"]: active |= {abs(x) for x in c}
        return {"accepted": True, "paid_nodes": self.nodes, "references": self.refs, "truth_rows": self.rows,
                "source_bytes": len(canon_bytes(src)), "certificate_bytes": len(canon_bytes(self.doc)),
                "active_original_ids": len(active), "header_decimal_digits": len(str(self.nvars))}


def doc(source, nodes, final):
    return {"format": "Rmix341-CANON2", "source": source, "source_sha256": source_hash(source), "nodes": nodes, "final": final}


def alias_attack():
    s = {"nvars": 1, "clauses": [[1]]}
    ns = [{"id": 0, "rule": "DEF", "var": 2, "inputs": [1, 1], "truth": [0, 1, 0, 1]},
          {"id": 1, "rule": "RES", "left": {"node": 0, "view": "clause", "facet": 1}, "right": {"src": 0, "view": "clause"}, "pivot": 1, "clause": [-2]},
          {"id": 2, "rule": "RES", "left": {"node": 0, "view": "clause", "facet": 2}, "right": {"src": 0, "view": "clause"}, "pivot": 1, "clause": [2]},
          {"id": 3, "rule": "RES", "left": {"node": 1, "view": "clause"}, "right": {"node": 2, "view": "clause"}, "pivot": 2, "clause": []}]
    return doc(s, ns, {"node": 3, "view": "clause"})


def affine_subsupport():
    s = {"nvars": 2, "clauses": [[1, 2], [1, -2], [-1], [-1, 2]]}
    ns = [{"id": 0, "rule": "AND3", "left": {"src": 0, "view": "clause"}, "right": {"src": 1, "view": "clause"},
           "factor": {"support": [1, 2], "truth": [0, 1, 0, 1]}, "affine": {"mask": [1], "rhs": 1}},
          {"id": 1, "rule": "AND3", "left": {"src": 2, "view": "clause"}, "right": {"src": 3, "view": "clause"},
           "factor": {"support": [1, 2], "truth": [1, 0, 1, 0]}, "affine": {"mask": [1], "rhs": 0}},
          {"id": 2, "rule": "GF2", "left": {"node": 0, "view": "affine"}, "right": {"node": 1, "view": "affine"},
           "affine": {"mask": [], "rhs": 1}}]
    return doc(s, ns, {"node": 2, "view": "affine"})


def load_base():
    p = Path("experiments/arc/lspv5_360/rmix341_canon1_referee360.py")
    spec = importlib.util.spec_from_file_location("canon1", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def reject(d, external):
    try: Checker(d, external).run()
    except Reject as e: return str(e)
    raise AssertionError("unexpected acceptance")


def main():
    base = load_base()
    old = alias_attack(); old1 = copy.deepcopy(old); old1["format"] = "Rmix341-CANON1"
    old_accept = base.Checker(old1).run()
    attack_reject = reject(old, old["source"])

    cov = affine_subsupport(); cov_stats = Checker(cov, cov["source"]).run()
    odd1 = base.k4_tseitin([1, 0, 0, 0]); odd = copy.deepcopy(odd1); odd["format"] = "Rmix341-CANON2"
    odd_stats = Checker(odd, odd["source"]).run()

    # Exact external-source authentication: a self-consistent embedded rewrite fails.
    external = {"nvars": 1, "clauses": [[1], [-1]]}
    replacement = {"nvars": 1, "clauses": [[1], [1]]}
    forged = doc(replacement, [], {"src": 0, "view": "clause"})
    source_reject = reject(forged, external)

    huge = 10 ** 80
    hs = {"nvars": huge, "clauses": [[1], [-1]]}
    hn = [{"id": 0, "rule": "RES", "left": {"src": 0, "view": "clause"}, "right": {"src": 1, "view": "clause"}, "pivot": 1, "clause": []}]
    huge_stats = Checker(doc(hs, hn, {"node": 0, "view": "clause"}), hs).run()

    # Valid aliased facet oriented result: taut facet (x or !x or !z) with (x)
    # resolves to (x or !z), not the false unit (!z).
    p = alias_attack(); p["nodes"] = p["nodes"][:2]; p["nodes"][1]["clause"] = [1, -2]; p["final"] = {"node": 1, "view": "clause"}
    prefix_reason = reject(p, p["source"])

    raw = {
        "run": "REFEREE361",
        "status": {"REFEREE360_soundness": "FALSIFIED_RETIRED", "CANON2_checker_soundness": "PROVED_FOR_FROZEN_COMPLETION",
                   "CANON2_coverage": "REPAIRED_FOR_ALIAS_RES_AFFINE_SUBSUPPORT_EXTERNAL_SOURCE_SPARSE_HEADER",
                   "historical_native_byte_uniqueness": "OPEN", "same_R_B3": "OPEN", "P_vs_NP": "OPEN"},
        "old_checker_unsound_attack": {"source_models": [{"x": 1}], "bytes": len(canon_bytes(old1)), "old_accept": old_accept,
                                       "new_reject": attack_reject, "paid_nodes": 4},
        "legal_affine_subsupport": cov_stats,
        "odd_k4": odd_stats,
        "external_source_replacement_reject": source_reject,
        "huge_sparse_header": huge_stats,
        "oriented_alias_prefix": {"expected_clause": [1, -2], "validated_prefix_then": prefix_reason},
        "normalization_bound": "O(N + q(N+q)(N+log(q+2))) sparse bits; independent of numeric header value",
        "b3_weakest_exact_contract": {
            "assumption": "one fixed uniform polynomial-time correct SAT decider A",
            "decider_system": "P_A proof of UNSAT F is the canonical string F; verifier reruns A(F) and syntax checks",
            "equivalent_missing_statement": "CANON2 size-simulates P_A with a polynomial length bound",
            "not_required_by_W_minimum": "polynomial-time proof translation or proof search",
            "still_circular": "choosing a minimum CANON2 proof without independently proving its polynomial bound"
        },
        "physical_cost_note": "Logical paid nodes exclude parsing, external-source acquisition/comparison, hashing, table checks, reads, writes, output and peak storage."
    }
    out = Path("results/raw/arc/2026-11-05_0448_LSPV5_REFEREE361_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"raw": str(out), "old_attack": old_accept, "new_reject": attack_reject,
                      "coverage": cov_stats, "odd": odd_stats, "huge": huge_stats}, sort_keys=True))


if __name__ == "__main__": main()
