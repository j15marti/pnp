#!/usr/bin/env python3
"""REFEREE367: context-typed branch DAG -> ordinary DAG Resolution.

This is an independent, declared experimental calculus, not the historical
R_mix341 checker.  It constructs the K4 odd-charge Tseitin 3-CNF, a fully
branched shared refutation, a Resolution+Weakening+Tautology compilation, and
then eliminates weakening/tautologies without unfolding the DAG.
"""

from __future__ import annotations

import hashlib
import json
import os
import resource
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
RAW = ROOT / "results/raw/arc/2026-11-05_1048_LSPV5_REFEREE367_raw.json"


def canon_clause(xs):
    out = sorted(set(int(x) for x in xs), key=lambda z: (abs(z), z < 0))
    return tuple(out)


def taut(c):
    s = set(c)
    return any(-x in s for x in s)


def guard(ctx, clause):
    return canon_clause([-x for x in ctx] + list(clause))


def resolve_exact(left, right, pivot):
    if pivot not in left or -pivot not in right:
        raise ValueError("oriented pivot absent")
    return canon_clause([x for x in left if x != pivot] + [x for x in right if x != -pivot])


def parse_dimacs(src: bytes):
    try:
        text = src.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("non-ASCII DIMACS") from exc
    header = None
    clauses = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            parts = line.split()
            if len(parts) != 4 or parts[:2] != ["p", "cnf"]:
                raise ValueError("bad header")
            header = (int(parts[2]), int(parts[3]))
            continue
        vals = [int(x) for x in line.split()]
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            raise ValueError("bad clause terminator")
        c = canon_clause(vals[:-1])
        if taut(c):
            raise ValueError("source tautology")
        clauses.append(c)
    if header is None or header[1] != len(clauses):
        raise ValueError("header/count mismatch")
    if any(abs(x) > header[0] for c in clauses for x in c):
        raise ValueError("variable out of range")
    return header[0], clauses


def k4_tseitin(charge=(1, 0, 0, 0)):
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    incident = [[] for _ in range(4)]
    for var, (u, v) in enumerate(edges, 1):
        incident[u].append(var)
        incident[v].append(var)
    clauses = []
    for vertex, row in enumerate(incident):
        for mask in range(8):
            bits = [(mask >> i) & 1 for i in range(3)]
            if sum(bits) % 2 != charge[vertex]:
                clauses.append(canon_clause(v if b == 0 else -v for v, b in zip(row, bits)))
    clauses = sorted(set(clauses))
    src = "p cnf 6 16\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
    return src.encode("ascii"), clauses, edges


def sat_masks(clauses, nvars):
    good = []
    for mask in range(1 << nvars):
        if all(any(((mask >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in clauses):
            good.append(mask)
    return good


@dataclass
class Node:
    rule: str
    ctx: tuple[int, ...]
    clause: tuple[int, ...]
    parents: tuple[int, ...] = ()
    pivot: Optional[int] = None
    source_index: Optional[int] = None

    def obj(self):
        d: dict[str, Any] = {"rule": self.rule, "ctx": list(self.ctx), "clause": list(self.clause)}
        if self.parents:
            d["parents"] = list(self.parents)
        if self.pivot is not None:
            d["pivot"] = self.pivot
        if self.source_index is not None:
            d["source_index"] = self.source_index
        return d


def build_typed(clauses):
    nodes: list[Node] = []
    src_ids = []
    for i, c in enumerate(clauses):
        src_ids.append(len(nodes))
        nodes.append(Node("SRC", (), c, source_index=i))
    assume = {}
    for v in range(1, 7):
        for lit in (v, -v):
            assume[lit] = len(nodes)
            nodes.append(Node("ASSUME", (lit,), (lit,)))

    leaf_count = 0

    def rec(prefix, depth):
        nonlocal leaf_count
        if depth == 6:
            leaf_count += 1
            assignment = {abs(l): l > 0 for l in prefix}
            falsified = next(i for i, c in enumerate(clauses)
                              if not any(assignment[abs(l)] == (l > 0) for l in c))
            cur = src_ids[falsified]
            current_clause = clauses[falsified]
            fullctx = canon_clause(prefix)
            for lit in list(current_clause):
                # Falsity of lit means the live assumption is -lit.
                aid = assume[-lit]
                nxt = resolve_exact(current_clause, (-lit,), lit)
                nodes.append(Node("RES", fullctx, nxt, (cur, aid), pivot=lit))
                cur = len(nodes) - 1
                current_clause = nxt
            assert current_clause == ()
            return cur
        v = depth + 1
        pos = rec(prefix + (v,), depth + 1)
        neg = rec(prefix + (-v,), depth + 1)
        ctx = canon_clause(prefix)
        nodes.append(Node("MERGE", ctx, (), (pos, neg), pivot=v))
        return len(nodes) - 1

    final = rec((), 0)
    return nodes, final, leaf_count


def verify_typed(nodes, final, clauses):
    counts = {"source_reads": 0, "parent_reads": 0, "context_subset_tests": 0,
              "literal_scans": 0, "nodes": len(nodes)}
    for i, n in enumerate(nodes):
        if len(set(abs(x) for x in n.ctx)) != len(n.ctx):
            raise ValueError(f"inconsistent/duplicate context {i}")
        if taut(n.clause):
            raise ValueError(f"taut stored clause {i}")
        counts["literal_scans"] += len(n.ctx) + len(n.clause)
        if n.rule == "SRC":
            counts["source_reads"] += 1
            if n.ctx or n.parents or n.source_index is None or clauses[n.source_index] != n.clause:
                raise ValueError(f"bad SRC {i}")
        elif n.rule == "ASSUME":
            if n.parents or len(n.clause) != 1 or n.clause[0] not in n.ctx:
                raise ValueError(f"bad ASSUME {i}")
        elif n.rule == "RES":
            if len(n.parents) != 2 or any(p >= i for p in n.parents):
                raise ValueError(f"bad RES parents {i}")
            a, b = (nodes[p] for p in n.parents)
            counts["parent_reads"] += 2
            counts["context_subset_tests"] += 2
            if not set(a.ctx) <= set(n.ctx) or not set(b.ctx) <= set(n.ctx):
                raise ValueError(f"context leak {i}")
            if resolve_exact(a.clause, b.clause, n.pivot) != n.clause:
                raise ValueError(f"bad resolvent {i}")
        elif n.rule == "MERGE":
            if len(n.parents) != 2 or any(p >= i for p in n.parents):
                raise ValueError(f"bad MERGE parents {i}")
            a, b = (nodes[p] for p in n.parents)
            counts["parent_reads"] += 2
            if a.clause != n.clause or b.clause != n.clause:
                raise ValueError(f"merge clause mismatch {i}")
            x = n.pivot
            if set(a.ctx) != set(n.ctx) | {x} or set(b.ctx) != set(n.ctx) | {-x}:
                raise ValueError(f"omitted/noncomplementary branch {i}")
        else:
            raise ValueError(f"unknown rule {n.rule}")
    if final != len(nodes) - 1 or nodes[final].ctx or nodes[final].clause:
        raise ValueError("final is not empty-context contradiction")
    return counts


@dataclass
class RWTLine:
    rule: str
    clause: tuple[int, ...]
    parents: tuple[int, ...] = ()
    pivot: Optional[int] = None
    source_index: Optional[int] = None

    def obj(self):
        d = {"rule": self.rule, "clause": list(self.clause)}
        if self.parents:
            d["parents"] = list(self.parents)
        if self.pivot is not None:
            d["pivot"] = self.pivot
        if self.source_index is not None:
            d["source_index"] = self.source_index
        return d


def compile_rwt(nodes):
    lines: list[RWTLine] = []
    out = []

    def add(line):
        lines.append(line)
        return len(lines) - 1

    for n in nodes:
        target = guard(n.ctx, n.clause)
        if n.rule == "SRC":
            lid = add(RWTLine("SRC", n.clause, source_index=n.source_index))
        elif n.rule == "ASSUME":
            lid = add(RWTLine("TAUT", target))
        elif n.rule == "RES":
            parent_lines = []
            for p in n.parents:
                pid = out[p]
                wanted = guard(n.ctx, nodes[p].clause)
                if lines[pid].clause != wanted:
                    pid = add(RWTLine("WEAKEN", wanted, (pid,)))
                parent_lines.append(pid)
            lid = add(RWTLine("RES", target, tuple(parent_lines), n.pivot))
            if resolve_exact(lines[parent_lines[0]].clause, lines[parent_lines[1]].clause, n.pivot) != target:
                raise AssertionError("RWT RES compilation failed")
        elif n.rule == "MERGE":
            # Positive branch guard contains -x; negative branch guard contains
            # +x, so orient the Resolution parents as (negative, positive).
            pos, neg = (out[p] for p in n.parents)
            a, b = neg, pos
            lid = add(RWTLine("RES", target, (a, b), n.pivot))
            if resolve_exact(lines[a].clause, lines[b].clause, n.pivot) != target:
                raise AssertionError("RWT MERGE compilation failed")
        else:
            raise AssertionError(n.rule)
        out.append(lid)
    return lines, out[-1]


def verify_rwt(lines, final, clauses):
    for i, line in enumerate(lines):
        if line.rule == "SRC":
            if line.source_index is None or clauses[line.source_index] != line.clause:
                raise ValueError(f"bad RWT SRC {i}")
        elif line.rule == "TAUT":
            if not taut(line.clause):
                raise ValueError(f"non-taut TAUT {i}")
        elif line.rule == "WEAKEN":
            if len(line.parents) != 1 or line.parents[0] >= i:
                raise ValueError(f"bad WEAKEN parent {i}")
            if not set(lines[line.parents[0]].clause) <= set(line.clause):
                raise ValueError(f"bad WEAKEN {i}")
        elif line.rule == "RES":
            if len(line.parents) != 2 or any(p >= i for p in line.parents):
                raise ValueError(f"bad RWT RES parents {i}")
            if resolve_exact(lines[line.parents[0]].clause, lines[line.parents[1]].clause, line.pivot) != line.clause:
                raise ValueError(f"bad RWT resolvent {i}")
        else:
            raise ValueError(f"bad RWT rule {line.rule}")
    if lines[final].clause:
        raise ValueError("RWT final nonempty")


def eliminate_rwt(lines, final, clauses):
    """Map every RWT line to a Resolution subclause or None for tautologies."""
    ordinary: list[RWTLine] = []
    image: list[Optional[int]] = []
    stats = {"inherit": 0, "taut_drop": 0, "ordinary_res": 0, "source": 0}

    def add(line):
        ordinary.append(line)
        return len(ordinary) - 1

    for i, line in enumerate(lines):
        result: Optional[int]
        if line.rule == "SRC":
            result = add(RWTLine("SRC", line.clause, source_index=line.source_index))
            stats["source"] += 1
        elif line.rule == "TAUT":
            result = None
            stats["taut_drop"] += 1
        elif line.rule == "WEAKEN":
            result = image[line.parents[0]]
            if result is not None and not set(ordinary[result].clause) <= set(line.clause):
                raise AssertionError("weakening image not a subclause")
            stats["inherit"] += 1
        elif line.rule == "RES":
            if taut(line.clause):
                result = None
                stats["taut_drop"] += 1
            else:
                a, b = (image[p] for p in line.parents)
                candidates = [x for x in (a, b) if x is not None]
                if not candidates:
                    raise AssertionError(f"non-taut line {i} has two taut images")
                if a is not None and b is not None and line.pivot in ordinary[a].clause and -line.pivot in ordinary[b].clause:
                    c = resolve_exact(ordinary[a].clause, ordinary[b].clause, line.pivot)
                    if taut(c) or not set(c) <= set(line.clause):
                        raise AssertionError(f"bad strengthening resolution at {i}")
                    result = add(RWTLine("RES", c, (a, b), line.pivot))
                    stats["ordinary_res"] += 1
                else:
                    valid = [x for x in candidates if set(ordinary[x].clause) <= set(line.clause)]
                    if not valid:
                        raise AssertionError(f"no inheritable strengthening at {i}")
                    result = min(valid, key=lambda x: (len(ordinary[x].clause), x))
                    stats["inherit"] += 1
        else:
            raise AssertionError(line.rule)
        if result is not None and not set(ordinary[result].clause) <= set(line.clause):
            raise AssertionError(f"image invariant fails at {i}")
        image.append(result)
    ofinal = image[final]
    if ofinal is None or ordinary[ofinal].clause:
        raise AssertionError("empty RWT line did not yield ordinary empty")
    return ordinary, ofinal, image, stats


def verify_ordinary(lines, final, clauses):
    parent_reads = 0
    for i, line in enumerate(lines):
        if line.rule == "SRC":
            if line.source_index is None or clauses[line.source_index] != line.clause:
                raise ValueError(f"bad ordinary source {i}")
        elif line.rule == "RES":
            if len(line.parents) != 2 or any(p >= i for p in line.parents):
                raise ValueError(f"bad ordinary parents {i}")
            parent_reads += 2
            if resolve_exact(lines[line.parents[0]].clause, lines[line.parents[1]].clause, line.pivot) != line.clause:
                raise ValueError(f"bad ordinary resolution {i}")
            if taut(line.clause):
                raise ValueError(f"ordinary tautology {i}")
        else:
            raise ValueError(f"non-Resolution rule remains {i}")
    if lines[final].clause:
        raise ValueError("ordinary final nonempty")
    return {"lines": len(lines), "parent_reads": parent_reads}


def depth_typed(nodes):
    depths = []
    for n in nodes:
        depths.append(0 if not n.parents else 1 + max(depths[p] for p in n.parents))
    return depths[-1]


def strict_dump(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def main():
    t0 = time.perf_counter_ns()
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.parent.mkdir(parents=True, exist_ok=True)
    src, clauses, edges = k4_tseitin()
    nvars, parsed = parse_dimacs(src)
    assert parsed == clauses and nvars == 6
    assert not sat_masks(clauses, nvars)

    even_src, even_clauses, _ = k4_tseitin((0, 0, 0, 0))
    even_models = sat_masks(even_clauses, 6)
    assert len(even_models) == 8

    nodes, final, leaves = build_typed(clauses)
    typed_counts = verify_typed(nodes, final, clauses)
    rwt, rwt_final = compile_rwt(nodes)
    verify_rwt(rwt, rwt_final, clauses)
    ordinary, ordinary_final, image, elim_stats = eliminate_rwt(rwt, rwt_final, clauses)
    ordinary_counts = verify_ordinary(ordinary, ordinary_final, clauses)

    source_hash = hashlib.sha256(src).hexdigest()
    trace_obj = {"format": "LSPV5-BCTX-1", "source_sha256": source_hash,
                 "source_utf8": src.decode(), "nodes": [n.obj() for n in nodes], "final": final}
    trace_bytes = strict_dump(trace_obj)
    trace_path = OUT / "k4_tseitin_typed_branch_referee367.json"
    trace_path.write_bytes(trace_bytes)

    ordinary_obj = {"format": "LSPV5-RES-1", "source_sha256": source_hash,
                    "source_utf8": src.decode(), "lines": [x.obj() for x in ordinary],
                    "final": ordinary_final}
    ordinary_bytes = strict_dump(ordinary_obj)
    ordinary_path = OUT / "k4_tseitin_resolution_referee367.json"
    ordinary_path.write_bytes(ordinary_bytes)

    paid_typed = sum(n.rule != "SRC" for n in nodes)
    typed_rule_counts = {rule: sum(n.rule == rule for n in nodes)
                         for rule in ("SRC", "ASSUME", "RES", "MERGE")}
    rwt_rule_counts = {rule: sum(x.rule == rule for x in rwt)
                       for rule in ("SRC", "TAUT", "WEAKEN", "RES")}

    # Hostile controls, each required to reject.
    controls = {}
    bad = list(nodes)
    m = next(i for i, n in enumerate(bad) if n.rule == "MERGE")
    x = bad[m]
    bad[m] = Node(x.rule, x.ctx, x.clause, (x.parents[0], x.parents[0]), x.pivot)
    try:
        verify_typed(bad, final, clauses)
        controls["omitted_and_branch"] = False
    except ValueError:
        controls["omitted_and_branch"] = True

    bad = list(nodes)
    r = next(i for i, n in enumerate(bad) if n.rule == "RES")
    x = bad[r]
    bad[r] = Node(x.rule, (), x.clause, x.parents, x.pivot)
    try:
        verify_typed(bad, final, clauses)
        controls["cross_context_leak"] = False
    except ValueError:
        controls["cross_context_leak"] = True

    try:
        verify_typed(nodes, final, even_clauses)
        controls["opposite_label_source_replay"] = False
    except ValueError:
        controls["opposite_label_source_replay"] = True

    bad_o = list(ordinary)
    ri = next(i for i, x in enumerate(bad_o) if x.rule == "RES")
    x = bad_o[ri]
    bad_o[ri] = RWTLine(x.rule, x.clause, x.parents, -x.pivot)
    try:
        verify_ordinary(bad_o, ordinary_final, clauses)
        controls["corrupt_resolution_pivot"] = False
    except ValueError:
        controls["corrupt_resolution_pivot"] = True

    try:
        parse_dimacs(src.replace(b"p cnf 6 16", b"p cnf 6 15"))
        controls["malformed_source"] = False
    except ValueError:
        controls["malformed_source"] = True
    controls["even_charge_has_8_models"] = len(even_models) == 8
    assert all(controls.values())

    elapsed = time.perf_counter_ns() - t0
    raw = {
        "status": "COMPUTATIONAL/DECLARED-CALCULUS",
        "source": {"family": "K4 odd-charge Tseitin", "nvars": 6, "clauses": 16,
                   "source_bytes": len(src), "source_sha256": source_hash, "edges": edges,
                   "odd_charge_models": 0, "even_charge_models": len(even_models)},
        "typed": {"nodes_total": len(nodes), "paid_distinct_nodes": paid_typed,
                  "rule_counts": typed_rule_counts, "leaves": leaves,
                  "critical_path_unit_inferences": depth_typed(nodes),
                  "trace_bytes": len(trace_bytes), "trace_evidence_bits": 8 * len(trace_bytes),
                  "trace_sha256": hashlib.sha256(trace_bytes).hexdigest(), **typed_counts},
        "rwt": {"lines": len(rwt), "rule_counts": rwt_rule_counts,
                "encoded_literal_occurrences": sum(len(x.clause) for x in rwt)},
        "ordinary_resolution": {**ordinary_counts, "inference_lines": sum(x.rule == "RES" for x in ordinary),
                                "proof_bytes": len(ordinary_bytes),
                                "proof_sha256": hashlib.sha256(ordinary_bytes).hexdigest(),
                                "encoded_literal_occurrences": sum(len(x.clause) for x in ordinary)},
        "elimination": elim_stats,
        "controls": controls,
        "implementation": {"elapsed_ns": elapsed,
                           "ru_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                           "python": sys.version.split()[0], "pid": os.getpid()},
        "disclaimers": [
            "Independent declared checkers, not the authoritative historical R_mix341 checker.",
            "Construction/search time is separate from minimum logical work.",
            "Critical path is a unit-inference parallel span, not physical machine time.",
            "The full R_mix341 GF(2) shortcut is outside this branch-only theorem."
        ]
    }
    RAW.write_bytes(strict_dump(raw))
    print(json.dumps(raw, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
