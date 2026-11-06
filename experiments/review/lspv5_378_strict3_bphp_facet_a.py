#!/usr/bin/env python3
"""REFEREE378: strict-3 bit-PHP -> unary-PHP FACET-A trace producer.

The emitted grammar is a separately declared, source-authenticated FACET-A
completion.  It is not the unavailable authoritative historical R_mix341
byte grammar and it stops after producing the unary PHP premises.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import time
import tracemalloc

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-11-05_2153_LSPV5_STRICT3_BPHP_FACETA378.json"


def norm(clause):
    return sorted(set(clause), key=lambda x: (abs(x), 0 if x < 0 else 1))


def resolve(c1, c2, pivot):
    assert pivot in c1 and -pivot in c2
    out = norm([x for x in c1 if x != pivot] + [x for x in c2 if x != -pivot])
    assert not any(-x in out for x in out)
    return out


class Builder:
    def __init__(self, ell):
        self.ell = ell
        self.n = 2**ell
        self.m = self.n + 1
        self.next_var = self.m * ell + 1
        self.sources = []
        self.nodes = []
        self.clauses = {}
        self.depth = {}
        self.defs = {}
        self.wide_refs = {}
        self.imp = {}
        self.leaf = {}
        self.outputs = {"at_least_one": [], "collisions": []}
        self.source_max_var = None

    def bit(self, i, t):
        return 1 + i * self.ell + t

    def eq_lit(self, i, t, bit):
        v = self.bit(i, t)
        return v if bit else -v

    def add_source(self, clause):
        sid = f"S{len(self.sources) + 1}"
        c = norm(clause)
        assert len(c) == 3 and len({abs(x) for x in c}) == 3
        self.sources.append({"id": sid, "clause": c})
        self.clauses[sid] = c
        self.depth[sid] = 0
        return sid

    def ref_clause(self, ref):
        if "#f" in ref:
            owner, fi = ref.split("#f")
            return self.defs[owner]["facets"][int(fi)]
        return self.clauses[ref]

    def ref_depth(self, ref):
        return self.depth[ref.split("#f")[0]]

    def add_res(self, left, right, pivot, tag):
        c1, c2 = self.ref_clause(left), self.ref_clause(right)
        # Orient so pivot is positive in left.
        if pivot not in c1:
            left, right = right, left
            c1, c2 = c2, c1
        out = resolve(c1, c2, pivot)
        rid = f"R{1 + sum(1 for n in self.nodes if n['kind'] == 'res')}"
        node = {"id": rid, "kind": "res", "left": left, "right": right,
                "pivot": pivot, "clause": out, "tag": tag}
        self.nodes.append(node)
        self.clauses[rid] = out
        self.depth[rid] = max(self.ref_depth(left), self.ref_depth(right)) + 1
        return rid

    def add_def(self, a, b, parent_owner, tag):
        z = self.next_var
        self.next_var += 1
        did = f"D{1 + sum(1 for n in self.nodes if n['kind'] == 'def')}"
        facets = [norm([-z, a]), norm([-z, b]), norm([z, -a, -b])]
        node = {"id": did, "kind": "def", "out": z, "a": a, "b": b,
                "facets": facets, "parent_owner": parent_owner, "tag": tag}
        self.nodes.append(node)
        self.defs[did] = node
        self.depth[did] = 1 + (self.depth[parent_owner] if parent_owner else 0)
        return did

    def split_wide_clause(self, wide, tag):
        k = len(wide)
        assert k == 2 * self.ell >= 4
        aux = list(range(self.next_var, self.next_var + k - 3))
        self.next_var += k - 3
        parts = [[wide[0], wide[1], aux[0]]]
        for j in range(k - 4):
            parts.append([-aux[j], wide[j + 2], aux[j + 1]])
        parts.append([-aux[-1], wide[-2], wide[-1]])
        refs = [self.add_source(c) for c in parts]
        current = refs[0]
        for j in range(1, len(refs)):
            current = self.add_res(current, refs[j], aux[j - 1], f"reconstruct:{tag}")
        assert self.ref_clause(current) == norm(wide)
        return current

    def make_sources(self):
        for i in range(self.m):
            for j in range(i + 1, self.m):
                for a in range(self.n):
                    bits = [(a >> (self.ell - 1 - t)) & 1 for t in range(self.ell)]
                    wide = [-self.eq_lit(i, t, bits[t]) for t in range(self.ell)]
                    wide += [-self.eq_lit(j, t, bits[t]) for t in range(self.ell)]
                    ref = self.split_wide_clause(wide, f"{i},{j},{a}")
                    self.wide_refs[(i, j, a)] = ref
        self.source_max_var = self.next_var - 1

    def make_defs_and_implications(self):
        for i in range(self.m):
            owner = {}
            for d in range(2, self.ell + 1):
                for p in range(2**d):
                    bits = [(p >> (d - 1 - t)) & 1 for t in range(d)]
                    if d == 2:
                        a = self.eq_lit(i, 0, bits[0])
                        b = self.eq_lit(i, 1, bits[1])
                        parent = None
                    else:
                        parent = owner[(d - 1, p >> 1)]
                        a = self.defs[parent]["out"]
                        b = self.eq_lit(i, d - 1, bits[-1])
                    did = self.add_def(a, b, parent, f"prefix:{i},{d},{p}")
                    owner[(d, p)] = did
                    z = self.defs[did]["out"]
                    if d == 2:
                        self.imp[(i, d, p, 0)] = f"{did}#f0"
                    else:
                        for t in range(d - 1):
                            parent_imp = self.imp[(i, d - 1, p >> 1, t)]
                            eq = self.eq_lit(i, t, bits[t])
                            rid = self.add_res(f"{did}#f0", parent_imp,
                                               self.defs[parent]["out"],
                                               f"imp:{i},{d},{p},{t}")
                            assert self.ref_clause(rid) == norm([-z, eq])
                            self.imp[(i, d, p, t)] = rid
                    self.imp[(i, d, p, d - 1)] = f"{did}#f1"
                    if d == self.ell:
                        self.leaf[(i, p)] = did

            # Two length-one bridges and their root resolution.
            bridges = []
            for bit0 in (0, 1):
                c0, c1 = owner[(2, 2 * bit0)], owner[(2, 2 * bit0 + 1)]
                pivot = self.bit(i, 1)
                bridge = self.add_res(f"{c1}#f2", f"{c0}#f2", pivot,
                                      f"bridge:{i},1,{bit0}")
                bridges.append(bridge)
            current = self.add_res(bridges[1], bridges[0], self.bit(i, 0),
                                   f"root:{i}")
            # Sequentially replace each frontier prefix; bridges are independent.
            for d in range(2, self.ell):
                for p in range(2**d):
                    c0, c1 = owner[(d + 1, 2 * p)], owner[(d + 1, 2 * p + 1)]
                    bridge = self.add_res(f"{c1}#f2", f"{c0}#f2",
                                          self.bit(i, d), f"bridge:{i},{d},{p}")
                    current = self.add_res(current, bridge, self.defs[owner[(d, p)]]["out"],
                                           f"expand:{i},{d},{p}")
            expected = norm([self.defs[owner[(self.ell, a)]]["out"] for a in range(self.n)])
            assert self.ref_clause(current) == expected
            self.outputs["at_least_one"].append(current)

    def make_collisions(self):
        for (i, j, a), wide_ref in self.wide_refs.items():
            current = wide_ref
            bits = [(a >> (self.ell - 1 - t)) & 1 for t in range(self.ell)]
            for pigeon in (i, j):
                leaf = self.leaf[(pigeon, a)]
                for t in range(self.ell):
                    eq = self.eq_lit(pigeon, t, bits[t])
                    current = self.add_res(self.imp[(pigeon, self.ell, a, t)],
                                           current, eq,
                                           f"collision:{i},{j},{a},{pigeon},{t}")
            yi, yj = self.defs[self.leaf[(i, a)]]["out"], self.defs[self.leaf[(j, a)]]["out"]
            assert self.ref_clause(current) == norm([-yi, -yj])
            self.outputs["collisions"].append(current)

    def trace(self):
        self.make_sources()
        self.make_defs_and_implications()
        self.make_collisions()
        paid_def = sum(n["kind"] == "def" for n in self.nodes)
        paid_res = sum(n["kind"] == "res" for n in self.nodes)
        M = self.n * self.m * (self.m - 1) // 2
        source_res = M * (2 * self.ell - 3)
        implication_res = self.m * sum(2**d * (d - 1) for d in range(3, self.ell + 1))
        at_least_res = self.m * (2 * self.n - 5)
        collision_res = 2 * self.ell * M
        expected_def = self.m * (2 * self.n - 4)
        expected_res = source_res + implication_res + at_least_res + collision_res
        assert paid_def == expected_def
        assert paid_res == expected_res
        span = max(self.depth[x] for x in self.outputs["at_least_one"] + self.outputs["collisions"])
        assert span == max(self.n - 1, 4 * self.ell - 3)
        assert self.source_max_var is not None
        dimacs = f"p cnf {self.source_max_var} {len(self.sources)}\n" + "".join(
            " ".join(map(str, s["clause"])) + " 0\n" for s in self.sources)
        return {
            "grammar": "FACET-A378-v1: free strict3 source; unit fresh signed-AND2 owner with facets f0/f1/f2; unit oriented binary RES",
            "ell": self.ell,
            "holes": self.n,
            "pigeons": self.m,
            "original_wide_clauses": M,
            "strict3_source_clauses": len(self.sources),
            "source_variables": self.source_max_var,
            "final_variables_after_def": self.next_var - 1,
            "source_sha256": hashlib.sha256(dimacs.encode()).hexdigest(),
            "source_bytes": len(dimacs.encode()),
            "source_res": source_res,
            "paid_def": paid_def,
            "compiler_res_without_source_reconstruction": paid_res - source_res,
            "paid_res_total": paid_res,
            "paid_work_pre_php": paid_def + paid_res,
            "critical_path_pre_php": span,
            "at_least_one_outputs": len(self.outputs["at_least_one"]),
            "collision_outputs": len(self.outputs["collisions"]),
            "trace": {"sources": self.sources, "nodes": self.nodes, "outputs": self.outputs},
            "dimacs": dimacs,
        }


def sat_control(ell):
    n = 2**ell
    # n pigeons in n holes: pigeon i uses distinct address i.
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(n):
                bits_a = [(a >> (ell - 1 - t)) & 1 for t in range(ell)]
                bits_i = [(i >> (ell - 1 - t)) & 1 for t in range(ell)]
                bits_j = [(j >> (ell - 1 - t)) & 1 for t in range(ell)]
                assert any(bits_i[t] != bits_a[t] for t in range(ell)) or any(
                    bits_j[t] != bits_a[t] for t in range(ell)
                )
    return {"ell": ell, "pigeons": n, "holes": n, "distinct_address_witness": True}


def main():
    tracemalloc.start()
    start = time.perf_counter()
    traces = [Builder(ell).trace() for ell in (2, 3)]
    controls = [sat_control(ell) for ell in (2, 3, 4)]
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    out = {
        "run": "LSPV-5/REFEREE378",
        "timestamp_PST": "2026-11-05 21:53",
        "status": "PROVED/RESTRICTED FACET-A work/span theorem; COMPUTATIONAL accepted declared bytes",
        "historical_authoritative_checker": False,
        "full_empty_clause_refutation": False,
        "published_hard_family": {
            "name": "Braun bit-PHP",
            "model": "DAG-like Res(XOR), no extension axioms",
            "theorem_range": "ell >= 32",
            "lower_bound": "> exp(n/(32768 ell^2))",
            "strict3_lower_bound_transfer": False,
        },
        "traces": traces,
        "sat_controls": controls,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8")
    summary = {k: v for k, v in out.items() if k != "traces"}
    # Host timing and allocator observations are deliberately excluded from the
    # persisted certificate so identical logical traces have stable bytes.
    summary["producer_elapsed_seconds_observed"] = elapsed
    summary["producer_tracemalloc_peak_bytes_observed"] = peak
    summary["trace_summaries"] = [
        {k: v for k, v in t.items() if k not in {"trace", "dimacs"}} for t in traces
    ]
    print(json.dumps(summary, indent=2))
    print(f"raw={OUT}")


if __name__ == "__main__":
    main()
