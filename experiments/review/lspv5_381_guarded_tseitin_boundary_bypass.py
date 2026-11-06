#!/usr/bin/env python3
"""REFEREE381: guarded Tseitin boundary-row bypass certificate producer.

Declared semantic R_mix341 candidate only: owner-qualified DEF facets,
AND3 exact factors, XOR rows, LOCAL equation-to-clause, and oriented RES.
This is not an execution of an authoritative historical byte checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json"


def norm(clause):
    out = sorted(set(clause), key=lambda z: (abs(z), 0 if z < 0 else 1))
    assert not any(-z in out for z in out)
    return out


def parity(bits):
    return sum(bits) & 1


def graphs():
    k4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    k33 = [(u, v) for u in range(3) for v in range(3, 6)]
    cube = []
    for u in range(8):
        for bit in (1, 2, 4):
            v = u ^ bit
            if u < v:
                cube.append((u, v))
    return [("K4", 4, k4), ("K33", 6, k33), ("cube", 8, cube)]


def dimacs(vmax, clauses):
    return "p cnf %d %d\n%s\n" % (
        vmax,
        len(clauses),
        "\n".join(" ".join(map(str, c)) + " 0" for c in clauses),
    )


class Build:
    def __init__(self, name, h, edges):
        self.name, self.h, self.edges = name, h, edges
        assert len(edges) * 2 == 3 * h
        self.inc = [[] for _ in range(h)]
        for eid, (u, v) in enumerate(edges, start=1):
            self.inc[u].append(eid)
            self.inc[v].append(eid)
        assert all(len(x) == 3 for x in self.inc)
        self.g = len(edges) + 1
        self.y_next = self.g + 1
        self.sources, self.nodes = [], []
        self.clause = {}
        self.dep = {}
        self.node_id = 0
        self.local = {}
        self.exceptional = 0

    def source(self, sid, clause, meta):
        c = norm(clause)
        self.sources.append({"id": sid, "clause": c, "meta": meta})
        self.clause[sid] = c
        self.dep[sid] = []
        return sid

    def node(self, kind, **kw):
        self.node_id += 1
        nid = f"N{self.node_id}"
        z = {"id": nid, "kind": kind, **kw}
        self.nodes.append(z)
        return nid

    def facet(self, did, which):
        d = next(x for x in self.nodes if x["id"] == did)
        w, a, b = d["out"], d["a"], d["b"]
        facets = [norm([-w, a]), norm([-w, b]), norm([w, -a, -b])]
        return facets[which]

    def ref_clause(self, ref):
        if "#f" in ref:
            did, f = ref.split("#f")
            return self.facet(did, int(f))
        return self.clause[ref]

    def res(self, left, right, pivot, tag):
        a, b = self.ref_clause(left), self.ref_clause(right)
        assert pivot in a and -pivot in b, (tag, a, b, pivot)
        c = norm([x for x in a if x != pivot] + [x for x in b if x != -pivot])
        nid = self.node("RES", left=left, right=right, pivot=pivot, tag=tag, clause=c)
        self.clause[nid] = c
        self.dep[nid] = [left.split("#f")[0], right.split("#f")[0]]
        return nid

    def build(self):
        # One odd charge, at vertex zero.  This is a standard hard-family charge
        # representative under literal gauge renaming.
        charges = [1] + [0] * (self.h - 1)
        block = {}
        for v in range(self.h):
            xs = self.inc[v]
            wrong = [b for b in itertools.product((0, 1), repeat=3) if parity(b) != charges[v]]
            block[v] = {}
            for b in wrong:
                bs = "".join(map(str, b))
                y = self.y_next
                self.y_next += 1
                lits = [x if bit == 0 else -x for x, bit in zip(xs, b)]
                s0 = self.source(f"S{v}_{bs}_0", [self.g, lits[0], y], {"vertex": v, "wrong": list(b), "side": 0})
                s1 = self.source(f"S{v}_{bs}_1", [-y, lits[1], lits[2]], {"vertex": v, "wrong": list(b), "side": 1})
                block[v][b] = (s0, s1)

        self.p, self.q = self.y_next, self.y_next + 1
        self.source_max = self.q
        pads = {}
        for s, t in itertools.product((0, 1), repeat=2):
            ps = self.p if s == 0 else -self.p
            qt = self.q if t == 0 else -self.q
            pads[(s, t)] = self.source(f"P{s}{t}", [-self.g, ps, qt], {"pad": [s, t]})

        # Globally shared owner per edge: w_e = (not g) AND x_e.
        defs, w_by_edge = {}, {}
        next_var = self.source_max + 1
        for eid in range(1, len(self.edges) + 1):
            w = next_var
            next_var += 1
            did = self.node("DEF", out=w, a=-self.g, b=eid, edge=eid)
            self.dep[did] = []
            defs[eid], w_by_edge[eid] = did, w

        charge0_rows, charge1_B = [], {}
        for v in range(self.h):
            xs = self.inc[v]
            ws = [w_by_edge[e] for e in xs]
            blockers = []
            for b, (s0, s1) in sorted(block[v].items()):
                bs = "".join(map(str, b))
                cur = self.res(s0, s1, self.y_for_source(s0), f"v{v}:{bs}:guard")
                for j, (x, w, bit) in enumerate(zip(xs, ws, b)):
                    did = defs[x]
                    if bit == 0:
                        cur = self.res(cur, f"{did}#f2", x, f"v{v}:{bs}:x{j}")
                    else:
                        cur = self.res(f"{did}#f1", cur, x, f"v{v}:{bs}:x{j}")
                if charges[v] == 0:
                    j = next(k for k, bit in enumerate(b) if bit == 1)
                    cur = self.res(cur, f"{defs[xs[j]]}#f0", self.g, f"v{v}:{bs}:drop-g")
                    assert self.clause[cur] == norm([w if bit == 0 else -w for w, bit in zip(ws, b)])
                    blockers.append(cur)
                else:
                    assert self.clause[cur] == norm([self.g] + [w if bit == 0 else -w for w, bit in zip(ws, b)])
                    charge1_B[b] = cur

            if charges[v] == 0:
                assert len(blockers) == 4
                a1 = self.and3(blockers[0], blockers[1], ws, f"v{v}:and-a")
                a2 = self.and3(blockers[2], blockers[3], ws, f"v{v}:and-b")
                row = self.and3(a1, a2, ws, f"v{v}:parity0", affine={"vars": sorted(ws), "rhs": 0})
                charge0_rows.append(row)

        assert len(charge0_rows) == self.h - 1 and len(charge1_B) == 4
        boundary = charge0_rows[0]
        for k, row in enumerate(charge0_rows[1:], start=1):
            boundary = self.xor(boundary, row, f"sum{k}")
        bvars = sorted(w_by_edge[e] for e in self.inc[self.exceptional])
        assert self.nodes_by_id(boundary)["affine"] == {"vars": bvars, "rhs": 0}

        local = {}
        for b in itertools.product((0, 1), repeat=3):
            if parity(b) == 1:
                c = norm([w if bit == 0 else -w for w, bit in zip([w_by_edge[e] for e in self.inc[0]], b)])
                local[b] = self.local_clause(boundary, c, f"boundary:{''.join(map(str,b))}")

        # Seven-node clausal elimination: parity(w)=0 plus the exceptional
        # vertex's guarded even blockers yields g without a four-variable row.
        w0, w1, w2 = [w_by_edge[e] for e in self.inc[0]]
        e1 = self.res(charge1_B[(0, 0, 0)], local[(0, 0, 1)], w2, "bridge:1")
        e2 = self.res(local[(0, 1, 0)], charge1_B[(0, 1, 1)], w2, "bridge:2")
        e3 = self.res(e1, e2, w1, "bridge:3")
        e4 = self.res(local[(1, 0, 0)], charge1_B[(1, 0, 1)], w2, "bridge:4")
        e5 = self.res(charge1_B[(1, 1, 0)], local[(1, 1, 1)], w2, "bridge:5")
        e6 = self.res(e4, e5, w1, "bridge:6")
        unit_g = self.res(e3, e6, w0, "bridge:g")
        assert self.clause[unit_g] == [self.g]

        p1 = self.res(pads[(0, 0)], pads[(0, 1)], self.q, "pad:q0")
        p2 = self.res(pads[(1, 0)], pads[(1, 1)], self.q, "pad:q1")
        not_g = self.res(p1, p2, self.p, "pad:not-g")
        final = self.res(unit_g, not_g, self.g, "final")
        assert self.clause[final] == []

        clauses = [s["clause"] for s in self.sources]
        text = dimacs(self.source_max, clauses)
        expected = 51 * self.h // 2 + 6
        assert len(self.nodes) == expected
        assert len(self.sources) == 8 * self.h + 4
        live = self.backward(final)
        assert all(s["id"] in live for s in self.sources)
        assert all(n["id"] in live for n in self.nodes)

        even_control = self.even_control()
        return {
            "graph": self.name,
            "vertices": self.h,
            "edges": [list(e) for e in self.edges],
            "charges": charges,
            "source_variables": self.source_max,
            "final_variables": next_var - 1,
            "source_clauses": len(self.sources),
            "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "source_bytes": len(text.encode()),
            "dimacs": text,
            "paid_nodes": len(self.nodes),
            "paid_formula": expected,
            "work_breakdown": {
                "DEF": 3 * self.h // 2,
                "charge0_RES": 20 * (self.h - 1),
                "charge0_AND3": 3 * (self.h - 1),
                "XOR": self.h - 2,
                "LOCAL": 4,
                "charge1_RES": 16,
                "bridge_RES": 7,
                "pad_RES": 3,
                "final_RES": 1,
            },
            "boundary_equation": self.nodes_by_id(boundary)["affine"],
            "unit_g": unit_g,
            "final_empty": final,
            "all_sources_and_nodes_live": True,
            "even_charge_control": even_control,
            "trace": {"sources": self.sources, "nodes": self.nodes},
        }

    def y_for_source(self, sid):
        c = self.clause[sid]
        return next(abs(x) for x in c if abs(x) > self.g and abs(x) < self.p if x > 0)

    def nodes_by_id(self, nid):
        return next(x for x in self.nodes if x["id"] == nid)

    def and3(self, left, right, support, tag, affine=None):
        z = {"left": left, "right": right, "support": sorted(support), "tag": tag}
        if affine is not None:
            z["affine"] = affine
        nid = self.node("AND3", **z)
        self.dep[nid] = [left.split("#f")[0], right.split("#f")[0]]
        return nid

    def xor(self, left, right, tag):
        a = self.nodes_by_id(left)["affine"]
        b = self.nodes_by_id(right)["affine"]
        av, bv = set(a["vars"]), set(b["vars"])
        aff = {"vars": sorted(av ^ bv), "rhs": a["rhs"] ^ b["rhs"]}
        nid = self.node("XOR", left=left, right=right, affine=aff, tag=tag)
        self.dep[nid] = [left, right]
        return nid

    def local_clause(self, parent, clause, tag):
        nid = self.node("LOCAL", parent=parent, clause=clause, tag=tag)
        self.clause[nid] = clause
        self.dep[nid] = [parent]
        return nid

    def backward(self, root):
        live, stack = set(), [root]
        while stack:
            x = stack.pop()
            if x in live:
                continue
            live.add(x)
            stack.extend(self.dep.get(x, []))
        return live

    def even_control(self):
        # Same graph/encoding with all charges zero.  Set g=0 and all edges
        # zero; every wrong odd triple differs from that address, so the
        # private split can be satisfied.  Padding is true by not g.
        clauses, rows = [], []
        y = self.g + 1
        A = {str(i): 0 for i in range(1, self.source_max + 1)}
        for v in range(self.h):
            xs = self.inc[v]
            for b in [z for z in itertools.product((0, 1), repeat=3) if parity(z) == 1]:
                lits = [x if bit == 0 else -x for x, bit in zip(xs, b)]
                c0, c1 = norm([self.g, lits[0], y]), norm([-y, lits[1], lits[2]])
                aval = (A[str(abs(lits[0]))] == 1) == (lits[0] > 0)
                A[str(y)] = 0 if aval else 1
                clauses.extend([c0, c1])
                rows.append({"vertex": v, "wrong": list(b), "y": y})
                y += 1
        assert y == self.p
        for s, t in itertools.product((0, 1), repeat=2):
            clauses.append(norm([-self.g, self.p if s == 0 else -self.p, self.q if t == 0 else -self.q]))
        assert len(clauses) == 8 * self.h + 4
        assert all(any((A[str(abs(l))] == 1) == (l > 0) for l in c) for c in clauses)
        text = dimacs(self.source_max, clauses)
        return {
            "charges": [0] * self.h,
            "clauses": clauses,
            "rows": rows,
            "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "source_bytes": len(text.encode()),
            "witness": A,
        }

    def final_variables(self):
        return max([self.source_max] + [n.get("out", 0) for n in self.nodes])


def main():
    instances = [Build(*g).build() for g in graphs()]
    doc = {
        "run": "LSPV-5/REFEREE381",
        "timestamp_PST": "2026-11-06 00:52",
        "status": "PROVED/RESTRICTED semantic-R_mix341 boundary bypass; COMPUTATIONAL finite complete DAGs",
        "historical_authoritative_checker": False,
        "grammar": "declared source + paid owner facets + AND3 + XOR + LOCAL + oriented RES",
        "theorem": "one-charge guarded cubic Tseitin has exhibited work 51h/2+6 without a four-variable row exporter",
        "instances": instances,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"run": doc["run"], "instances": [{"graph": x["graph"], "h": x["vertices"], "sources": x["source_clauses"], "paid": x["paid_nodes"], "final": x["final_empty"]} for x in instances]}, indent=2))


if __name__ == "__main__":
    main()
