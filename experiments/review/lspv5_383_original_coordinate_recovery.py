#!/usr/bin/env python3
"""REFEREE383: exact original-coordinate recovery of the known /436 shortcut.

This independently instantiates an already published construction; it does not
claim novelty.  The input source bytes are the exact REFEREE381 guarded
Tseitin instances.  The proof uses only historical /341 rule-level RES, AND3,
and XOR: no DEF, LOCAL, split, discharge, or weakening.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json"
OUT = ROOT / "results/raw/review/2026-11-06_0248_LSPV5_ORIGINAL_COORDINATE_RECOVERY383.json"
INPUT_SHA = "f3200e609df200d892ff630103c3490961094d705585880daf4df3befa7254a3"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(clause):
    out = sorted(set(clause), key=lambda z: (abs(z), 0 if z < 0 else 1))
    assert not any(-z in out for z in out)
    return out


def lit_value(lit: int, assignment: dict[int, int]) -> bool:
    return bool(assignment[abs(lit)]) == (lit > 0)


def clause_value(clause, assignment) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


class Proof:
    def __init__(self, instance):
        self.I = instance
        self.h = instance["vertices"]
        self.edges = [tuple(e) for e in instance["edges"]]
        self.edge_count = len(self.edges)
        self.g = self.edge_count + 1
        self.source_max = instance["source_variables"]
        self.sources = instance["trace"]["sources"]
        self.source = {s["id"]: s for s in self.sources}
        self.clause = {s["id"]: norm(s["clause"]) for s in self.sources}
        self.factor = {}
        self.affine = {}
        self.nodes = []
        self.deps = {s["id"]: [] for s in self.sources}
        self.depth = {s["id"]: 0 for s in self.sources}
        self.next_node = 0
        self.inc = [[] for _ in range(self.h)]
        for eid, (u, v) in enumerate(self.edges, start=1):
            self.inc[u].append(eid)
            self.inc[v].append(eid)
        assert all(len(x) == 3 for x in self.inc)

    def add(self, kind, parents, **fields):
        self.next_node += 1
        nid = f"R{self.next_node}"
        node = {"id": nid, "kind": kind, **fields}
        self.nodes.append(node)
        self.deps[nid] = list(parents)
        self.depth[nid] = 1 + max(self.depth[p] for p in parents)
        return nid

    def res(self, left, right, pivot, tag):
        a, b = self.clause[left], self.clause[right]
        assert pivot in a and -pivot in b, (tag, a, b, pivot)
        z = norm([x for x in a if x != pivot] + [x for x in b if x != -pivot])
        nid = self.add("RES", [left, right], left=left, right=right,
                       pivot=pivot, clause=z, tag=tag)
        self.clause[nid] = z
        return nid

    def condition_support(self, ref):
        if ref in self.clause:
            return sorted({abs(x) for x in self.clause[ref]})
        return self.factor[ref]["support"]

    def condition_value(self, ref, assignment):
        if ref in self.clause:
            return clause_value(self.clause[ref], assignment)
        f = self.factor[ref]
        mask = sum((assignment[v] << i) for i, v in enumerate(f["support"]))
        return bool(f["truth"][mask])

    def and3(self, left, right, tag, affine=None):
        support = sorted(set(self.condition_support(left)) | set(self.condition_support(right)))
        assert 0 < len(support) <= 3
        assert all(1 <= v <= self.source_max for v in support)
        truth = []
        for mask in range(1 << len(support)):
            a = {v: (mask >> i) & 1 for i, v in enumerate(support)}
            truth.append(int(self.condition_value(left, a) and self.condition_value(right, a)))
        fields = {"left": left, "right": right, "support": support,
                  "truth": truth, "tag": tag, "original_coordinate_legal": True}
        if affine is not None:
            expected = [int((sum((mask >> i) & 1 for i in range(len(support))) & 1) == affine["rhs"])
                        for mask in range(1 << len(support))]
            assert truth == expected
            assert affine["vars"] == support
            fields["affine"] = affine
        nid = self.add("AND3", [left, right], **fields)
        self.factor[nid] = {"support": support, "truth": truth}
        if affine is not None:
            self.affine[nid] = affine
        return nid

    def xor(self, left, right, tag):
        a, b = self.affine[left], self.affine[right]
        av, bv = set(a["vars"]), set(b["vars"])
        row = {"vars": sorted(av ^ bv), "rhs": a["rhs"] ^ b["rhs"]}
        nid = self.add("XOR", [left, right], left=left, right=right,
                       affine=row, tag=tag)
        self.affine[nid] = row
        return nid

    def balanced_xor(self, rows):
        layer = list(rows)
        round_no = 0
        while len(layer) > 1:
            nxt = []
            for i in range(0, len(layer), 2):
                if i + 1 == len(layer):
                    nxt.append(layer[i])
                else:
                    nxt.append(self.xor(layer[i], layer[i + 1], f"xor:{round_no}:{i//2}"))
            layer = nxt
            round_no += 1
        return layer[0]

    def backward(self, root):
        live, stack = set(), [root]
        while stack:
            x = stack.pop()
            if x in live:
                continue
            live.add(x)
            stack.extend(self.deps[x])
        return live

    def source_blocks(self):
        blocks = {}
        pads = {}
        for s in self.sources:
            meta = s["meta"]
            if "pad" in meta:
                pads[tuple(meta["pad"])] = s["id"]
            else:
                key = (meta["vertex"], tuple(meta["wrong"]))
                blocks.setdefault(key, {})[meta["side"]] = s["id"]
        assert len(blocks) == 4 * self.h and len(pads) == 4
        assert all(set(x) == {0, 1} for x in blocks.values())
        return blocks, pads

    def build(self):
        blocks, pads = self.source_blocks()
        p, q = self.source_max - 1, self.source_max

        # Three shared RES nodes derive not-g from all four pad clauses.
        pq0 = self.res(pads[(0, 0)], pads[(0, 1)], q, "pad:q0")
        pq1 = self.res(pads[(1, 0)], pads[(1, 1)], q, "pad:q1")
        not_g = self.res(pq0, pq1, p, "pad:not-g")
        assert self.clause[not_g] == [-self.g]

        recovered = {v: [] for v in range(self.h)}
        for (v, wrong), pair in sorted(blocks.items()):
            s0, s1 = pair[0], pair[1]
            y = next(x for x in self.clause[s0] if x > self.g)
            guarded = self.res(s0, s1, y, f"recover:{v}:{''.join(map(str,wrong))}:y")
            base = self.res(guarded, not_g, self.g, f"recover:{v}:{''.join(map(str,wrong))}:g")
            expected = norm([x if bit == 0 else -x for x, bit in zip(self.inc[v], wrong)])
            assert self.clause[base] == expected
            recovered[v].append((wrong, base))

        rows = []
        for v in range(self.h):
            parts = [ref for _, ref in sorted(recovered[v])]
            assert len(parts) == 4
            a = self.and3(parts[0], parts[1], f"v{v}:and-a")
            b = self.and3(parts[2], parts[3], f"v{v}:and-b")
            support = sorted(self.inc[v])
            row = self.and3(a, b, f"v{v}:row",
                            affine={"vars": support, "rhs": self.I["charges"][v]})
            rows.append(row)

        root = self.balanced_xor(rows)
        assert self.affine[root] == {"vars": [], "rhs": 1}
        live = self.backward(root)
        assert all(s["id"] in live for s in self.sources)
        assert all(n["id"] in live for n in self.nodes)

        counts = {k: sum(n["kind"] == k for n in self.nodes) for k in ("RES", "AND3", "XOR")}
        assert counts == {"RES": 8 * self.h + 3, "AND3": 3 * self.h, "XOR": self.h - 1}
        assert len(self.nodes) == 12 * self.h + 2

        deletions = self.deletion_witnesses(blocks, pads)
        assert len(deletions) == len(self.sources)

        return {
            "graph": self.I["graph"],
            "h": self.h,
            "edges": [list(e) for e in self.edges],
            "charges": self.I["charges"],
            "source_variables": self.source_max,
            "source_clauses": len(self.sources),
            "source_bytes": self.I["source_bytes"],
            "source_sha256": self.I["source_sha256"],
            "dimacs": self.I["dimacs"],
            "work": len(self.nodes),
            "work_formula": 12 * self.h + 2,
            "known_binary_source_floor": 8 * self.h + 3,
            "counts": counts,
            "span": self.depth[root],
            "span_bound": 5 + (self.h - 1).bit_length(),
            "root": root,
            "root_affine": self.affine[root],
            "not_g": not_g,
            "all_sources_and_nodes_live": True,
            "uses": ["RES", "AND3", "XOR"],
            "excludes": ["DEF", "LOCAL", "SPLIT", "DISCHARGE", "WEAKENING"],
            "sources": self.sources,
            "nodes": self.nodes,
            "deletion_witnesses": deletions,
            "even_charge_control": self.I["even_charge_control"],
        }

    def edge_model_for_deleted_block(self, vertex, wrong):
        for mask in range(1 << self.edge_count):
            bits = {e: (mask >> (e - 1)) & 1 for e in range(1, self.edge_count + 1)}
            if tuple(bits[e] for e in self.inc[vertex]) != tuple(wrong):
                continue
            if all(v == vertex or (sum(bits[e] for e in self.inc[v]) & 1) == self.I["charges"][v]
                   for v in range(self.h)):
                return bits
        raise AssertionError((vertex, wrong))

    def deletion_witnesses(self, blocks, pads):
        out = []
        for deleted in self.sources:
            sid = deleted["id"]
            A = {v: 0 for v in range(1, self.source_max + 1)}
            meta = deleted["meta"]
            if "pad" in meta:
                A[self.g] = 1
                s, t = meta["pad"]
                A[self.source_max - 1], A[self.source_max] = s, t
                for pair in blocks.values():
                    y = next(x for x in self.clause[pair[0]] if x > self.g)
                    A[y] = 0
            else:
                target = (meta["vertex"], tuple(meta["wrong"]))
                A.update(self.edge_model_for_deleted_block(*target))
                A[self.g] = 0
                for key, pair in blocks.items():
                    s0 = pair[0]
                    y = next(x for x in self.clause[s0] if x > self.g)
                    if key == target:
                        A[y] = 0 if meta["side"] == 0 else 1
                    else:
                        edge_lit = next(x for x in self.clause[s0] if abs(x) <= self.edge_count)
                        A[y] = 0 if lit_value(edge_lit, A) else 1
            assert not clause_value(self.clause[sid], A)
            assert all(s["id"] == sid or clause_value(self.clause[s["id"]], A) for s in self.sources)
            out.append({"deleted": sid, "assignment": [A[v] for v in range(1, self.source_max + 1)]})
        return out


def main():
    raw = INPUT.read_bytes()
    assert sha256(raw) == INPUT_SHA
    src = json.loads(raw)
    assert src["run"] == "LSPV-5/REFEREE381"
    instances = [Proof(i).build() for i in src["instances"]]
    malformed = [
        {"name": "empty", "text": ""},
        {"name": "bad-header", "text": "p cnd 1 1\n1 0\n"},
        {"name": "count-mismatch", "text": "p cnf 1 2\n1 0\n"},
        {"name": "unterminated", "text": "p cnf 1 1\n1\n"},
        {"name": "out-of-range", "text": "p cnf 1 1\n2 0\n"},
        {"name": "nonnumeric", "text": "p cnf 1 1\nx 0\n"},
        {"name": "trailing-junk", "text": "p cnf 1 1\n1 0\njunk\n"},
        {"name": "negative-count", "text": "p cnf -1 0\n"},
    ]
    doc = {
        "run": "LSPV-5/REFEREE383",
        "timestamp_PST": "2026-11-06 02:48",
        "status": [
            "PROVED/EXACT rule-level historical RES/AND3/XOR construction",
            "COMPUTATIONAL finite source/certificate/deletion controls",
            "KNOWN/DUPLICATE construction from LSPV-1/436",
            "OPEN authoritative accepted-byte checker and all-rule superpolynomial hardness/B3",
        ],
        "input_trace_path": str(INPUT.relative_to(ROOT)),
        "input_trace_sha256": INPUT_SHA,
        "historical_grammar": {
            "path": "research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex",
            "blob": "c87acd11d32ccfc3b7acd3667ef11daeb60079cb",
            "rules_used": ["RES", "AND3", "XOR"],
            "weights": "one per derived node; shared node charged once",
        },
        "prior_source": {
            "path": "research/agents/lspv-1/2026-11-05_2226_LSPV1_COMPACT_GUARD_STRICT3_TRANSFER436.md",
            "blob": "2c72bdf3934f91188e330fa628207ac1a02c5d68",
            "claim": "known 12h+2 upper construction; independently instantiated here",
        },
        "instances": instances,
        "malformed_controls": malformed,
        "conclusion": "REFEREE382 retires the fresh-wire proof, not the earlier original-coordinate 12h+2 proof; the guarded family remains a linear-work failure for mixed hardness at the rule level.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "run": doc["run"],
        "input_sha256": INPUT_SHA,
        "instances": [{"graph": x["graph"], "h": x["h"], "work": x["work"],
                       "span": x["span"], "deletions": len(x["deletion_witnesses"])} for x in instances],
    }, indent=2))


if __name__ == "__main__":
    main()
