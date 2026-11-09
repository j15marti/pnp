#!/usr/bin/env python3
"""Independent typed audit of the ER2 zero used by tracker node P2-L1-520.

This is not the historical R_mix341 checker.  It implements only the signed
two-input AND definition and ordinary oriented Resolution conventions stated
in LSPV-1/358, including distinct absolute input IDs and globally fresh
outputs.  It rejects the direct z AND not-z gate, builds a legal constant-zero
factory, and checks that an all-distinct one-hot zero survives a mod-3 adder.
"""

from __future__ import annotations

import json
import resource
import time
from dataclasses import dataclass
from itertools import product


def norm(clause):
    out = sorted(set(clause), key=lambda x: (abs(x), x))
    if any(-x in out for x in out):
        raise ValueError("tautological clause")
    return tuple(out)


def lit_value(lit, values):
    bit = values[abs(lit)]
    return bit if lit > 0 else 1 - bit


def clause_holds(clause, values):
    return any(lit_value(lit, values) for lit in clause)


def resolve(left, right, pivot):
    if pivot not in left or -pivot not in right:
        raise ValueError("oriented pivot absent")
    return norm([x for x in left if x != pivot] + [x for x in right if x != -pivot])


@dataclass(frozen=True)
class Gate:
    out: int
    left: int
    right: int


class ER2:
    def __init__(self, original_ids):
        self.original_ids = set(original_ids)
        if not self.original_ids or min(self.original_ids) <= 0:
            raise ValueError("bad original IDs")
        self.known = set(self.original_ids)
        self.next_id = max(self.original_ids) + 1
        self.gates = []
        self.facets = []

    def and_gate(self, left, right):
        if abs(left) == abs(right):
            raise ValueError("ER2 requires distinct absolute input IDs")
        if abs(left) not in self.known or abs(right) not in self.known:
            raise ValueError("input is not original or earlier output")
        out = self.next_id
        self.next_id += 1
        if out in self.known:
            raise ValueError("nonfresh output")
        self.known.add(out)
        self.gates.append(Gate(out, left, right))
        facets = [norm((-out, left)), norm((-out, right)), norm((out, -left, -right))]
        self.facets.extend(facets)
        return out

    def extend(self, original_values):
        values = dict(original_values)
        if set(values) != self.original_ids:
            raise ValueError("assignment does not match original IDs")
        for gate in self.gates:
            values[gate.out] = lit_value(gate.left, values) & lit_value(gate.right, values)
        if not all(clause_holds(cl, values) for cl in self.facets):
            raise AssertionError("definition facet falsified by deterministic extension")
        return values


def false_output(builder, z, a):
    """Return o forced false without ever feeding the same ID twice to a gate."""
    u = builder.and_gate(z, a)
    v = builder.and_gate(z, -a)
    o = builder.and_gate(u, v)

    # Explicit ordinary Resolution proof of not-o from the paid facets.
    ou = norm((-o, u))
    ov = norm((-o, v))
    ua = norm((-u, a))
    vna = norm((-v, -a))
    oa = resolve(ou, ua, u)
    ona = resolve(ov, vna, v)
    unit = resolve(oa, ona, a)
    if unit != (-o,):
        raise AssertionError("false-output Resolution macro failed")
    return o, (oa, ona, unit)


def zero_group(builder, z, a):
    # Three distinct false output IDs avoid repeated ports in downstream gates.
    o0, p0 = false_output(builder, z, a)
    o1, p1 = false_output(builder, z, a)
    o2, p2 = false_output(builder, z, a)
    return (-o0, o1, o2), p0 + p1 + p2


def mod3_adder(builder, p, q):
    if len({abs(x) for x in p + q}) != 6:
        raise ValueError("adder ports must have six distinct absolute IDs")
    terms = [[builder.and_gate(p[i], q[j]) for j in range(3)] for i in range(3)]
    out = []
    for k in range(3):
        bucket = [terms[i][j] for i in range(3) for j in range(3) if (i + j) % 3 == k]
        n12 = builder.and_gate(-bucket[0], -bucket[1])
        n123 = builder.and_gate(n12, -bucket[2])
        out.append(-n123)  # complement of conjunction of the three negated terms
    return tuple(out)


def onehot_index(group, values):
    bits = [lit_value(x, values) for x in group]
    if sum(bits) != 1:
        raise AssertionError(f"not one-hot: {bits}")
    return bits.index(1)


def run():
    started = time.perf_counter()
    checks = 0
    negatives = {}

    # Exact peer witness is illegal under the ER2 rule cited by P2-L1-520.
    bad = ER2({1, 2})
    try:
        bad.and_gate(1, -1)
        negatives["direct_z_and_not_z"] = "ACCEPTED"
    except ValueError as exc:
        negatives["direct_z_and_not_z"] = f"REJECTED: {exc}"
        checks += 1

    # Two fresh all-distinct one-hot zero groups plus one mod-3 adder.
    er2 = ER2({1, 2})
    zg1, proof1 = zero_group(er2, 1, 2)
    zg2, proof2 = zero_group(er2, 1, 2)
    summed = mod3_adder(er2, zg1, zg2)
    for z, a in product((0, 1), repeat=2):
        values = er2.extend({1: z, 2: a})
        assert onehot_index(zg1, values) == 0
        assert onehot_index(zg2, values) == 0
        assert onehot_index(summed, values) == 0
        assert all(values[abs(x)] == 0 for x in zg1[1:] + zg2[1:])
        checks += 4

    assert len({abs(x) for x in zg1 + zg2}) == 6
    assert all(abs(g.left) != abs(g.right) for g in er2.gates)
    assert all(p[-1] == (-abs(group_lit),) for group_lit, p in zip(zg1 + zg2, [proof1[0:3], proof1[3:6], proof1[6:9], proof2[0:3], proof2[3:6], proof2[6:9]]))
    checks += 3

    # Reusing one zero tuple on both sides violates the adder's distinct-port premise.
    before = len(er2.gates)
    try:
        mod3_adder(er2, zg1, zg1)
        negatives["shared_zero_tuple"] = "ACCEPTED"
    except ValueError as exc:
        negatives["shared_zero_tuple"] = f"REJECTED: {exc}"
        checks += 1
    assert len(er2.gates) == before

    # Independent truth-table control for the adder on arbitrary one-hot groups.
    generic = ER2(set(range(1, 7)))
    gout = mod3_adder(generic, (1, 2, 3), (4, 5, 6))
    for i, j in product(range(3), repeat=2):
        original = {k: 0 for k in range(1, 7)}
        original[i + 1] = 1
        original[j + 4] = 1
        values = generic.extend(original)
        assert onehot_index(gout, values) == (i + j) % 3
        checks += 1

    # Corrupting a defining facet is detected on an explicit assignment.
    corrupt = ER2({1, 2})
    q = corrupt.and_gate(1, 2)
    values = corrupt.extend({1: 1, 2: 1})
    corrupted_facet = norm((-q, -1))
    assert not clause_holds(corrupted_facet, values)
    negatives["corrupted_facet"] = "REJECTED by explicit assignment"
    checks += 1

    elapsed = time.perf_counter() - started
    return {
        "run": "LSPV5_PEER520_ZERO_FACTORY_AUDIT448",
        "classification": {
            "peer_witness": "invalid as written in declared ER2 (same absolute input ID)",
            "repair": "verified typed ER2 schema; three distinct false outputs per zero group",
            "asymptotic_effect": "O(h) additional gates/nodes, preserving O(h log h)",
            "historical_R_mix341": "not established; no authoritative accepted-byte replay",
        },
        "counts": {
            "checks": checks,
            "repair_groups": 2,
            "repair_gates_before_adder": 18,
            "repair_resolution_nodes_before_adder": len(proof1) + len(proof2),
            "adder_gates": 15,
            "total_gates": len(er2.gates),
            "source_facets": len(er2.facets),
            "generic_adder_truth_rows": 9,
        },
        "groups": {"left": zg1, "right": zg2, "sum": summed},
        "negative_controls": negatives,
        "resource": {
            "elapsed_seconds": elapsed,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
