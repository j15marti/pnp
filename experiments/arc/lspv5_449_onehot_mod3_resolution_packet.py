#!/usr/bin/env python3
"""Materialize a local ordinary-Resolution packet for a signed-AND mod-3 adder.

This is a verifier/generator for the separately declared ER2 fragment used by
LSPV-1/520.  It is not the historical R_mix341 checker.  Every gate has two
distinct absolute input IDs and a fresh output.  The packet derives the four
exact one-hot clauses for the sum of two exact one-hot F3 inputs using only
ordinary oriented Resolution over input clauses and paid definition facets.
"""

from __future__ import annotations

import json
import hashlib
import resource
import time
from dataclasses import dataclass
from itertools import combinations, product


def canon(xs):
    c = frozenset(xs)
    if any(-x in c for x in c):
        raise ValueError("tautology")
    return c


def ordered(c):
    return tuple(sorted(c, key=lambda x: (abs(x), x)))


def lit_value(lit, values):
    v = values[abs(lit)]
    return v if lit > 0 else 1 - v


def holds(c, values):
    return any(lit_value(x, values) for x in c)


@dataclass(frozen=True)
class Line:
    clause: frozenset
    kind: str
    left: int | None = None
    right: int | None = None
    pivot: int | None = None
    label: str = ""


class Packet:
    def __init__(self):
        self.lines = []
        self.gates = []
        self.known = set(range(1, 7))
        self.next_id = 7

    def source(self, clause, label):
        self.lines.append(Line(canon(clause), "SOURCE", label=label))
        return len(self.lines) - 1

    def and_gate(self, a, b, label):
        if abs(a) == abs(b):
            raise ValueError("same absolute input ID")
        if abs(a) not in self.known or abs(b) not in self.known:
            raise ValueError("non-ancestral input")
        q = self.next_id
        self.next_id += 1
        self.known.add(q)
        self.gates.append((q, a, b, label))
        self.source((-q, a), f"DEF:{label}:left")
        self.source((-q, b), f"DEF:{label}:right")
        self.source((q, -a, -b), f"DEF:{label}:back")
        return q

    def extend(self, inputs):
        values = dict(inputs)
        for q, a, b, _ in self.gates:
            values[q] = lit_value(a, values) & lit_value(b, values)
        return values


def build_adder():
    p = Packet()
    P, Q = (1, 2, 3), (4, 5, 6)
    p.source(P, "P:atleast1")
    p.source(Q, "Q:atleast1")
    for name, group in (("P", P), ("Q", Q)):
        for a, b in combinations(group, 2):
            p.source((-a, -b), f"{name}:atmost1:{a}:{b}")

    terms = [[p.and_gate(P[i], Q[j], f"t{i}{j}") for j in range(3)] for i in range(3)]
    outputs = []
    for k in range(3):
        bucket = [terms[i][j] for i in range(3) for j in range(3) if (i + j) % 3 == k]
        n12 = p.and_gate(-bucket[0], -bucket[1], f"nor{k}:12")
        n123 = p.and_gate(n12, -bucket[2], f"nor{k}:123")
        outputs.append(-n123)
    targets = [canon(outputs)] + [canon((-outputs[i], -outputs[j])) for i, j in combinations(range(3), 2)]
    return p, tuple(outputs), targets


def resolve(a, b, pivot):
    if pivot not in a or -pivot not in b:
        raise ValueError("bad oriented pivot")
    out = (a - {pivot}) | (b - {-pivot})
    if any(-x in out for x in out):
        return None
    return frozenset(out)


def saturate(packet, targets, max_width=7):
    """Subsumption-saturating resolution closure, preserving all proof parents."""
    lines = list(packet.lines)
    active = set(range(len(lines)))
    by_lit = {}
    exact = {}
    for i, line in enumerate(lines):
        exact.setdefault(line.clause, i)
        for lit in line.clause:
            by_lit.setdefault(lit, set()).add(i)
    queue = list(range(len(lines)))
    target_ids = {t: exact.get(t) for t in targets}
    attempts = 0

    def add_clause(c, left, right, pivot):
        nonlocal lines
        if c in exact:
            return exact[c]
        # A present stronger clause is enough for monotone replay, but all four
        # targets below are prime under the input relation, so exact targets are
        # expected and required before returning success.
        for i in active:
            if lines[i].clause <= c:
                return i
        i = len(lines)
        lines.append(Line(c, "RES", left, right, pivot))
        exact[c] = i
        supers = [j for j in active if c < lines[j].clause]
        for j in supers:
            active.remove(j)
            for lit in lines[j].clause:
                by_lit[lit].discard(j)
        active.add(i)
        for lit in c:
            by_lit.setdefault(lit, set()).add(i)
        queue.append(i)
        return i

    qpos = 0
    while qpos < len(queue):
        i = queue[qpos]
        qpos += 1
        if i not in active:
            continue
        a = lines[i].clause
        for pivot in tuple(a):
            for j in tuple(by_lit.get(-pivot, ())):
                if j not in active or j == i:
                    continue
                attempts += 1
                b = lines[j].clause
                c = resolve(a, b, pivot)
                if c is None or len(c) > max_width:
                    continue
                k = add_clause(c, i, j, pivot)
                if c in target_ids and target_ids[c] is None and lines[k].clause == c:
                    target_ids[c] = k
        if all(v is not None for v in target_ids.values()):
            break
    if not all(v is not None for v in target_ids.values()):
        missing = [ordered(t) for t, v in target_ids.items() if v is None]
        raise AssertionError(f"targets not derived at width {max_width}: {missing}")
    return lines, target_ids, attempts, len(active)


def proof_union(lines, target_ids, source_count):
    used = set()
    def visit(i):
        if i in used:
            return
        used.add(i)
        line = lines[i]
        if line.kind == "RES":
            if not (line.left < i and line.right < i):
                raise AssertionError("non-acyclic parent")
            got = resolve(lines[line.left].clause, lines[line.right].clause, line.pivot)
            if got != line.clause:
                raise AssertionError("incorrect resolution line")
            visit(line.left)
            visit(line.right)
    for i in target_ids.values():
        visit(i)
    paid_res = sorted(i for i in used if lines[i].kind == "RES")
    sources = sorted(i for i in used if i < source_count)
    return used, paid_res, sources


def compact_certificate(lines, used, target_ids):
    order = sorted(used)
    remap = {old: new for new, old in enumerate(order)}
    out = []
    for old in order:
        line = lines[old]
        item = {"id": remap[old], "kind": line.kind, "clause": ordered(line.clause)}
        if line.kind == "SOURCE":
            item["label"] = line.label
        else:
            item.update({"left": remap[line.left], "right": remap[line.right], "pivot": line.pivot})
        out.append(item)
    targets = {str(ordered(t)): remap[i] for t, i in target_ids.items()}
    depth = []
    for item in out:
        depth.append(0 if item["kind"] == "SOURCE" else 1 + max(depth[item["left"]], depth[item["right"]]))
    target_depths = {key: depth[idx] for key, idx in targets.items()}
    encoded = json.dumps({"lines": out, "targets": targets}, sort_keys=True, separators=(",", ":")).encode()
    return out, targets, target_depths, max(target_depths.values()), hashlib.sha256(encoded).hexdigest(), len(encoded)


def run():
    started = time.perf_counter()
    packet, outputs, targets = build_adder()
    source_count = len(packet.lines)
    checks = 0

    # Exhaustive semantics on all 64 input vectors; exactly nine are admitted.
    admitted = 0
    invalid_witnesses = {"missing_atleast": False, "missing_atmost": False}
    for bits in product((0, 1), repeat=6):
        inputs = {i + 1: bits[i] for i in range(6)}
        values = packet.extend(inputs)
        all_sources = all(holds(line.clause, values) for line in packet.lines)
        input_onehot = sum(bits[:3]) == 1 and sum(bits[3:]) == 1
        if all_sources != input_onehot:
            raise AssertionError("source/gate semantics mismatch")
        if input_onehot:
            admitted += 1
            outbits = [lit_value(x, values) for x in outputs]
            if sum(outbits) != 1:
                raise AssertionError("output not one-hot")
            if outbits.index(1) != (bits[:3].index(1) + bits[3:].index(1)) % 3:
                raise AssertionError("wrong mod-3 output")
        # Hostile controls: dropping an input clause admits a bad output.
        if sum(bits[:3]) == 0 and sum(bits[3:]) == 1:
            invalid_witnesses["missing_atleast"] |= not holds(canon((1, 2, 3)), values) and not holds(targets[0], values)
        if sum(bits[:3]) == 2 and sum(bits[3:]) == 1:
            invalid_witnesses["missing_atmost"] |= any(not holds(t, values) for t in targets[1:])
        checks += 1
    if admitted != 9 or not all(invalid_witnesses.values()):
        raise AssertionError("hostile source controls failed")

    lines, target_ids, attempts, active = saturate(packet, targets, max_width=7)
    used, paid_res, used_sources = proof_union(lines, target_ids, source_count)
    certificate, compact_targets, target_depths, critical_path, certificate_sha256, certificate_bytes = compact_certificate(lines, used, target_ids)
    for target, i in target_ids.items():
        if lines[i].clause != target:
            raise AssertionError("only a proper subclause was produced")
        checks += 1

    # Prime-implicate check: every literal deletion from every target is
    # falsified by one of the nine valid input assignments.
    prime_witnesses = 0
    for target in targets:
        for dropped in target:
            smaller = target - {dropped}
            found = False
            for i, j in product(range(3), repeat=2):
                bits = [0] * 6
                bits[i] = bits[3 + j] = 1
                values = packet.extend({k + 1: bits[k] for k in range(6)})
                if not holds(smaller, values):
                    found = True
                    break
            if not found:
                raise AssertionError("target not prime")
            prime_witnesses += 1
            checks += 1

    # Corrupt one exact defining facet and exhibit a falsifying deterministic extension.
    q, a, b, _ = packet.gates[0]
    values = packet.extend({1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0})
    corrupted = canon((-q, -a))
    if holds(corrupted, values):
        raise AssertionError("corrupted facet not detected")
    checks += 1

    elapsed = time.perf_counter() - started
    return {
        "run": "LSPV5_449_ONEHOT_MOD3_RESOLUTION_PACKET",
        "status": "PASS",
        "scope": "declared signed-AND DEF facets plus ordinary Resolution; not historical R_mix341 bytes",
        "inputs": {"variables": 6, "onehot_source_clauses": 8, "valid_rows": admitted},
        "gates": {"count": len(packet.gates), "definition_facets": source_count - 8},
        "targets": [ordered(t) for t in targets],
        "target_line_ids": {str(ordered(t)): i for t, i in target_ids.items()},
        "compact_target_line_ids": compact_targets,
        "target_resolution_depths": target_depths,
        "proof_union": {
            "resolution_nodes": len(paid_res),
            "source_or_facet_lines": len(used_sources),
            "total_distinct_lines": len(used),
            "max_clause_width": max(len(lines[i].clause) for i in used),
            "weighted_critical_path_unit_RES": critical_path,
        },
        "search": {
            "closure_lines_created": len(lines),
            "active_subsumption_minimal_clauses": active,
            "resolution_attempts": attempts,
            "width_cutoff": 7,
        },
        "checks": checks,
        "prime_literal_deletion_witnesses": prime_witnesses,
        "hostile_controls": {
            "missing_input_atleast_clause_admits_no_output": invalid_witnesses["missing_atleast"],
            "missing_input_atmost_clause_admits_multiple_outputs": invalid_witnesses["missing_atmost"],
            "corrupted_definition_facet_rejected": True,
        },
        "resource": {
            "elapsed_seconds": elapsed,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "certificate_sha256": certificate_sha256,
        "certificate_canonical_json_bytes": certificate_bytes,
        "certificate": certificate,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
