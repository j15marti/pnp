#!/usr/bin/env python3
"""Finite controls for SIGN-SENSITIVITY-WORD-FIREWALL171.

The mathematical lower bound is a replay argument.  This script independently
checks the prism/Tseitin source used by ARC-CONNECTED-SIGN-AUTH191 for h=3,4,
including all single-sign and quota-preserving paired-sign mutants, and records
how the sensitive coordinates occupy aligned W-bit cells under two layouts.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
RAW = HERE / "2026-10-26_2048_SIGN_SENSITIVITY_WORD_FIREWALL171_raw.json"


def prism(h: int):
    edges = set()
    for rail in range(2):
        base = rail * h
        for i in range(h):
            edges.add(tuple(sorted((base + i, base + (i + 1) % h))))
    for i in range(h):
        edges.add((i, h + i))
    edges = sorted(edges)
    assert len(edges) == 3 * h
    incidence = [[] for _ in range(2 * h)]
    for eid, (u, v) in enumerate(edges):
        incidence[u].append(eid)
        incidence[v].append(eid)
    assert all(len(x) == 3 for x in incidence)
    return edges, incidence


def odd_tseitin_cnf(h: int):
    edges, incidence = prism(h)
    charge = [0] * (2 * h)
    charge[0] = 1
    clauses = []
    clause_vertex = []
    for v, inc in enumerate(incidence):
        inc = sorted(inc)
        # The clause for a local pattern is falsified exactly by that pattern.
        # Encode all patterns whose parity disagrees with the vertex charge.
        for pattern in range(8):
            bits = [(pattern >> j) & 1 for j in range(3)]
            if (sum(bits) & 1) != charge[v]:
                clauses.append(tuple((eid + 1) if bit == 0 else -(eid + 1)
                                     for eid, bit in zip(inc, bits)))
                clause_vertex.append(v)
    assert len(clauses) == 8 * h
    return edges, clauses, clause_vertex


def satisfies(clauses, assignment: int) -> bool:
    for clause in clauses:
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause):
            return False
    return True


def first_model(clauses, nvars: int):
    for assignment in range(1 << nvars):
        if satisfies(clauses, assignment):
            return assignment
    return None


def flip_occurrences(clauses, occurrences):
    out = [list(c) for c in clauses]
    for ci, slot in occurrences:
        out[ci][slot] *= -1
    return [tuple(c) for c in out]


def quotas(clauses, nvars: int):
    pos = Counter()
    neg = Counter()
    for clause in clauses:
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit) - 1] += 1
    return [(pos[i], neg[i]) for i in range(nvars)]


def connected_after_vertex_deletion(h: int, deleted):
    edges, _ = prism(h)
    deleted = set(deleted)
    vertices = [v for v in range(2 * h) if v not in deleted]
    if not vertices:
        return True
    adj = {v: [] for v in vertices}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].append(v)
            adj[v].append(u)
    seen = {vertices[0]}
    todo = [vertices[0]]
    while todo:
        x = todo.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return len(seen) == len(vertices)


def occupied_blocks(positions, word_bits: int):
    return len({p // word_bits for p in positions})


def audit_h(h: int):
    assertions = 0
    edges, clauses, clause_vertex = odd_tseitin_cnf(h)
    nvars = len(edges)
    assert first_model(clauses, nvars) is None
    assertions += 1
    assert len(set(clauses)) == len(clauses)
    assertions += 1
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
    assertions += len(clauses)
    assert quotas(clauses, nvars) == [(4, 4)] * nvars
    assertions += nvars
    assert connected_after_vertex_deletion(h, [])
    assertions += 1
    for v in range(2 * h):
        assert connected_after_vertex_deletion(h, [v])
        assertions += 1
    for u in range(2 * h):
        for v in range(u + 1, 2 * h):
            assert connected_after_vertex_deletion(h, [u, v])
            assertions += 1

    occurrences = []
    per_edge = defaultdict(list)
    for ci, clause in enumerate(clauses):
        v = clause_vertex[ci]
        for slot, lit in enumerate(clause):
            rec = (ci, slot, v, lit > 0)
            occurrences.append(rec)
            per_edge[abs(lit) - 1].append(rec)
    assert len(occurrences) == 24 * h
    assertions += 1

    single_models = []
    for ci, slot, _, _ in occurrences:
        mutant = flip_occurrences(clauses, [(ci, slot)])
        model = first_model(mutant, nvars)
        assert model is not None
        single_models.append(model)
        assertions += 1

    edge_endpoints = {eid: set(edge) for eid, edge in enumerate(edges)}
    pairs = []
    paired_models = []
    for eid in range(nvars):
        u, v = edges[eid]
        groups = defaultdict(list)
        for ci, slot, vertex, sign in per_edge[eid]:
            groups[(vertex, sign)].append((ci, slot))
        assert all(len(groups[(vertex, sign)]) == 2
                   for vertex in (u, v) for sign in (False, True))
        assertions += 4
        local_pairs = list(zip(groups[(u, True)], groups[(v, False)]))
        local_pairs += list(zip(groups[(u, False)], groups[(v, True)]))
        assert len(local_pairs) == 4
        assertions += 1
        for a, b in local_pairs:
            mutant = flip_occurrences(clauses, [a, b])
            assert quotas(mutant, nvars) == [(4, 4)] * nvars
            assertions += nvars
            assert len(set(mutant)) == len(mutant)
            assert all(len({abs(x) for x in c}) == 3 for c in mutant)
            assertions += 2
            model = first_model(mutant, nvars)
            assert model is not None
            paired_models.append(model)
            pairs.append((a, b))
            assertions += 1
    assert len(pairs) == 12 * h
    assertions += 1

    # Canonical interleaved literal record: one sign bit followed by a w-bit ID.
    w = math.ceil(math.log2(nvars + 1))
    header = 16 + 2 * math.ceil(math.log2(h + 2))
    record = w + 1
    positions = [header + i * record for i in range(len(occurrences))]
    physical_n = header + len(occurrences) * record
    assert all(positions[i + 1] - positions[i] == record
               for i in range(len(positions) - 1))
    assertions += max(0, len(positions) - 1)

    word_sizes = sorted({1, record, 2 * record,
                         math.ceil(math.log2(physical_n + 1)),
                         4 * math.ceil(math.log2(physical_n + 1)), physical_n})
    layouts = []
    for W in word_sizes:
        inter = occupied_blocks(positions, W)
        packed_positions = [header + i for i in range(len(positions))]
        packed = occupied_blocks(packed_positions, W)
        generic_lower = math.ceil(len(positions) / W)
        assert inter >= generic_lower and packed >= generic_lower
        assertions += 2
        # For coordinates separated by record bits, one W-cell contains at most
        # floor((W-1)/record)+1 sensitive coordinates.
        cap = (W - 1) // record + 1
        spaced_lower = math.ceil(len(positions) / cap)
        assert inter >= spaced_lower
        assertions += 1
        # Every sign occurrence is in exactly one quota-preserving pair.  A
        # probed cell can hit no more pairs than the sensitive positions it
        # contains, hence this is a certificate-path lower bound on cells.
        paired_spaced_lower = math.ceil(len(pairs) / cap)
        assert inter >= paired_spaced_lower
        assertions += 1
        layouts.append({
            "W": W,
            "interleaved_occupied_cells": inter,
            "packed_occupied_cells": packed,
            "generic_ceil_p_over_W": generic_lower,
            "spaced_cap_per_cell": cap,
            "spaced_lower": spaced_lower,
            "paired_promise_spaced_lower": paired_spaced_lower,
        })

    return {
        "h": h,
        "vertices": 2 * h,
        "variables_edges": nvars,
        "clauses": len(clauses),
        "literal_sign_positions": len(occurrences),
        "quota": [4, 4],
        "single_sign_mutants_sat": len(single_models),
        "quota_preserving_pairs": len(pairs),
        "paired_sign_mutants_sat": len(paired_models),
        "record_bits": record,
        "header_bits_control": header,
        "physical_bits_control": physical_n,
        "cell_layouts": layouts,
        "assertions": assertions,
    }


def main():
    audits = [audit_h(3), audit_h(4)]
    payload = {
        "artifact": "SIGN-SENSITIVITY-WORD-FIREWALL171",
        "scope": (
            "Finite audit of connected prism odd-charge Tseitin CNFs and aligned "
            "cell occupancy. The general replay and occupied-block lemmas are proved "
            "in the accompanying report, not by finite testing."
        ),
        "audits": audits,
        "total_assertions": sum(x["assertions"] for x in audits),
        "status": {
            "finite_prism_controls": "COMPUTATIONAL",
            "general_block_replay": "proved in report",
            "full_SAT_or_ARC_edge": "OPEN",
        },
    }
    RAW.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
