#!/usr/bin/env python3
"""REFEREE379: complete Cook ER suffix over REFEREE378 FACET-A traces.

This is a declared FACET-A certificate producer, not an execution of the
unavailable historical R_mix341 checker.  Every Cook extension
q = a OR (b AND c) is represented by two fresh signed-AND2 owners:
w = b AND c, r = (NOT a) AND (NOT w), with q represented by NOT r.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "experiments/review/lspv5_378_strict3_bphp_facet_a.py"
OUT = ROOT / "results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json"

spec = importlib.util.spec_from_file_location("ref378", BASE_PATH)
ref378 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ref378)


def norm(c):
    return sorted(set(c), key=lambda x: (abs(x), 0 if x < 0 else 1))


class FullCook:
    def __init__(self, ell: int):
        self.base = ref378.Builder(ell)
        self.base_summary = self.base.trace()
        self.ell = ell
        self.n = 2**ell
        self.m = self.n + 1
        self.sources = self.base.sources
        self.nodes = self.base.nodes
        self.clauses = self.base.clauses
        self.depth = self.base.depth
        self.defs = self.base.defs
        self.next_var = self.base.next_var
        self.var_owner = {d["out"]: did for did, d in self.defs.items()}
        self.ext_def_count = 0
        self.ext_res_count = 0
        self.q = {}
        self.q_owner = {}
        self.alo = {}
        self.coll = {}
        self.stage_records = []

    def ref_clause(self, ref: str):
        if "#f" in ref:
            owner, fi = ref.split("#f")
            return self.defs[owner]["facets"][int(fi)]
        return self.clauses[ref]

    def ref_depth(self, ref: str):
        return self.depth[ref.split("#f")[0]]

    def add_def(self, a: int, b: int, tag: str):
        z = self.next_var
        self.next_var += 1
        self.ext_def_count += 1
        did = f"E_D{self.ext_def_count}"
        owners = sorted({self.var_owner[abs(x)] for x in (a, b) if abs(x) in self.var_owner})
        facets = [norm([-z, a]), norm([-z, b]), norm([z, -a, -b])]
        node = {"id": did, "kind": "def", "out": z, "a": a, "b": b,
                "facets": facets, "input_owners": owners, "tag": tag}
        self.nodes.append(node)
        self.defs[did] = node
        self.var_owner[z] = did
        self.depth[did] = 1 + max([self.depth[x] for x in owners] or [0])
        return did

    def add_res(self, left: str, right: str, pivot: int, tag: str):
        c1, c2 = self.ref_clause(left), self.ref_clause(right)
        if pivot not in c1:
            left, right, c1, c2 = right, left, c2, c1
        assert pivot in c1 and -pivot in c2
        out = norm([x for x in c1 if x != pivot] + [x for x in c2 if x != -pivot])
        assert not any(-x in out for x in out)
        self.ext_res_count += 1
        rid = f"E_R{self.ext_res_count}"
        node = {"id": rid, "kind": "res", "left": left, "right": right,
                "pivot": pivot, "clause": out, "tag": tag}
        self.nodes.append(node)
        self.clauses[rid] = out
        self.depth[rid] = 1 + max(self.ref_depth(left), self.ref_depth(right))
        return rid

    def initialize_unary_php(self):
        # q^n_(i,j) is the positive bit-PHP leaf variable y_(i,j).
        for i in range(self.m):
            for j in range(self.n):
                owner = self.base.leaf[(i, j)]
                self.q[(self.n, i, j)] = self.defs[owner]["out"]
                self.q_owner[(self.n, i, j)] = owner
            self.alo[(self.n, i)] = self.base.outputs["at_least_one"][i]
        z = 0
        for i in range(self.m):
            for r in range(i + 1, self.m):
                for j in range(self.n):
                    self.coll[(self.n, i, r, j)] = self.base.outputs["collisions"][z]
                    z += 1
        assert z == len(self.base.outputs["collisions"])

    def extension(self, k: int, i: int, j: int):
        a = self.q[(k + 1, i, j)]
        b = self.q[(k + 1, i, k)]
        c = self.q[(k + 1, k + 1, j)]
        assert len({abs(a), abs(b), abs(c)}) == 3
        wd = self.add_def(b, c, f"cook:w:{k},{i},{j}")
        w = self.defs[wd]["out"]
        rd = self.add_def(-a, -w, f"cook:r:{k},{i},{j}")
        r = self.defs[rd]["out"]
        q = -r
        # Four Cook extension clauses; E0 is a direct facet, E1-E3 paid RES.
        e0 = f"{rd}#f0"                         # q | !a
        e1 = self.add_res(f"{wd}#f2", f"{rd}#f1", w, f"cook:E1:{k},{i},{j}")
        e2 = self.add_res(f"{rd}#f2", f"{wd}#f0", w, f"cook:E2:{k},{i},{j}")
        e3 = self.add_res(f"{rd}#f2", f"{wd}#f1", w, f"cook:E3:{k},{i},{j}")
        assert self.ref_clause(e0) == norm([q, -a])
        assert self.ref_clause(e1) == norm([q, -b, -c])
        assert self.ref_clause(e2) == norm([-q, a, b])
        assert self.ref_clause(e3) == norm([-q, a, c])
        self.q[(k, i, j)] = q
        self.q_owner[(k, i, j)] = rd
        return (e0, e1, e2, e3)

    def derive_collision(self, k, i, r, j, Ei, Er):
        qi, qr = self.q[(k, i, j)], self.q[(k, r, j)]
        ai, bi = self.q[(k + 1, i, j)], self.q[(k + 1, i, k)]
        ar, br = self.q[(k + 1, r, j)], self.q[(k + 1, r, k)]
        c = self.q[(k + 1, k + 1, j)]
        ai_ar = self.coll[(k + 1, i, r, j)]
        ai_c = self.coll[(k + 1, i, k + 1, j)]
        ar_c = self.coll[(k + 1, r, k + 1, j)]
        bi_br = self.coll[(k + 1, i, r, k)]
        # Exhaustively found nine-step weakening-free Resolution template.
        x1 = self.add_res(ai_ar, Ei[3], ai, f"cook:col1:{k},{i},{r},{j}")
        x2 = self.add_res(x1, ar_c, c, f"cook:col2:{k},{i},{r},{j}")
        x3 = self.add_res(bi_br, Er[2], br, f"cook:col3:{k},{i},{r},{j}")
        x4 = self.add_res(x2, x3, ar, f"cook:col4:{k},{i},{r},{j}")
        x5 = self.add_res(ai_ar, Ei[2], ai, f"cook:col5:{k},{i},{r},{j}")
        x6 = self.add_res(x5, Er[3], ar, f"cook:col6:{k},{i},{r},{j}")
        x7 = self.add_res(ai_c, Ei[2], ai, f"cook:col7:{k},{i},{r},{j}")
        x8 = self.add_res(x6, x7, c, f"cook:col8:{k},{i},{r},{j}")
        x9 = self.add_res(x4, x8, bi, f"cook:col9:{k},{i},{r},{j}")
        assert self.ref_clause(x9) == norm([-qi, -qr])
        return x9

    def derive_stage(self, k: int):
        start_d, start_r = self.ext_def_count, self.ext_res_count
        ext = {}
        for i in range(k + 1):
            for j in range(k):
                ext[(i, j)] = self.extension(k, i, j)

        # Totality clauses for k+1 pigeons and k holes.
        for i in range(k + 1):
            left = self.alo[(k + 1, i)]
            for j in range(k):
                left = self.add_res(left, ext[(i, j)][0], self.q[(k + 1, i, j)],
                                    f"cook:alo-left:{k},{i},{j}")
            b = self.q[(k + 1, i, k)]
            d = self.q[(k + 1, k + 1, k)]
            right = self.add_res(self.alo[(k + 1, k + 1)],
                                 self.coll[(k + 1, i, k + 1, k)], d,
                                 f"cook:alo-right0:{k},{i}")
            for j in range(k):
                right = self.add_res(right, ext[(i, j)][1],
                                     self.q[(k + 1, k + 1, j)],
                                     f"cook:alo-right:{k},{i},{j}")
            out = self.add_res(left, right, b, f"cook:alo-out:{k},{i}")
            assert self.ref_clause(out) == norm([self.q[(k, i, j)] for j in range(k)])
            self.alo[(k, i)] = out

        for i in range(k + 1):
            for r in range(i + 1, k + 1):
                for j in range(k):
                    self.coll[(k, i, r, j)] = self.derive_collision(
                        k, i, r, j, ext[(i, j)], ext[(r, j)])

        d = self.ext_def_count - start_d
        rr = self.ext_res_count - start_r
        expected_d = 2 * k * (k + 1)
        expected_r = 3 * k * (k + 1) + 2 * (k + 1) ** 2 + 9 * k * k * (k + 1) // 2
        assert d == expected_d and rr == expected_r
        self.stage_records.append({"k": k, "definitions": d, "resolution": rr,
                                   "work": d + rr,
                                   "alo_outputs": [self.alo[(k, i)] for i in range(k + 1)],
                                   "collision_outputs": [self.coll[(k, i, r, j)]
                                       for i in range(k + 1) for r in range(i + 1, k + 1)
                                       for j in range(k)]})

    def finish(self):
        self.initialize_unary_php()
        for k in range(self.n - 1, 0, -1):
            self.derive_stage(k)
        q0, q1 = self.q[(1, 0, 0)], self.q[(1, 1, 0)]
        unit = self.add_res(self.alo[(1, 0)], self.coll[(1, 0, 1, 0)], q0,
                            "cook:final-unit")
        empty = self.add_res(self.alo[(1, 1)], unit, q1, "cook:empty")
        assert self.ref_clause(empty) == []
        suffix_formula = self.n * (self.n + 1) * (27 * self.n**2 + 11 * self.n - 14) // 24
        suffix_work = self.ext_def_count + self.ext_res_count
        assert suffix_work == suffix_formula
        base_work = self.base_summary["paid_work_pre_php"]
        span_formula = max(self.n - 1, 4 * self.ell - 3) + (self.n - 1) * (self.n + 4) // 2 + 2
        assert self.depth[empty] == span_formula
        compact_nodes = []
        for x in self.nodes:
            if x["kind"] == "def":
                y = {k: x[k] for k in ("id", "kind", "out", "a", "b")}
                if "parent_owner" in x:
                    y["parent_owner"] = x["parent_owner"]
                if "input_owners" in x:
                    y["input_owners"] = x["input_owners"]
            else:
                y = {k: x[k] for k in ("id", "kind", "left", "right", "pivot")}
            compact_nodes.append(y)
        return {
            "grammar": "FACET-A379-v1: REFEREE378 strict3/FACET-A plus fresh signed-AND2 and oriented binary RES",
            "ell": self.ell,
            "holes": self.n,
            "pigeons": self.m,
            "source_variables": self.base_summary["source_variables"],
            "final_variables_after_def": self.next_var - 1,
            "strict3_source_clauses": len(self.sources),
            "source_sha256": self.base_summary["source_sha256"],
            "source_bytes": self.base_summary["source_bytes"],
            "dimacs": self.base_summary["dimacs"],
            "base_pre_php_work": base_work,
            "cook_suffix_def": self.ext_def_count,
            "cook_suffix_res": self.ext_res_count,
            "cook_suffix_work": suffix_work,
            "cook_suffix_formula": suffix_formula,
            "paid_full_refutation_work": base_work + suffix_work,
            "critical_path_full": self.depth[empty],
            "critical_path_formula": span_formula,
            "final_empty": empty,
            "stages": self.stage_records,
            "trace": {"sources": self.sources, "nodes": compact_nodes},
        }


def sat_control(ell):
    n = 2**ell
    return {"ell": ell, "pigeons": n, "holes": n,
            "distinct_addresses": list(range(n)), "satisfies_unary_php": True}


def main():
    traces = [FullCook(ell).finish() for ell in (2, 3)]
    out = {
        "run": "LSPV-5/REFEREE379",
        "timestamp_PST": "2026-11-05 22:53",
        "status": "PROVED/RESTRICTED complete FACET-A refutation; COMPUTATIONAL finite accepted declared bytes",
        "historical_authoritative_checker": False,
        "full_empty_clause_refutation": True,
        "lower_bound_transfer": False,
        "traces": traces,
        "sat_controls": [sat_control(e) for e in (2, 3, 4)],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "run": out["run"],
        "traces": [{k: t[k] for k in ("ell", "strict3_source_clauses", "source_variables",
                    "final_variables_after_def", "base_pre_php_work", "cook_suffix_def",
                    "cook_suffix_res", "cook_suffix_work", "paid_full_refutation_work",
                    "critical_path_full", "final_empty")} for t in traces],
        "raw_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "raw_bytes": OUT.stat().st_size,
    }, indent=2))


if __name__ == "__main__":
    main()
