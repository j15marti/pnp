#!/usr/bin/env python3
"""Independent audit of the finite K4 modulo-three strict-3CNF controls.

This script is not an implementation of the historical R_mix341 byte checker.
It reconstructs the source without importing peer generator code, replays the
published signed binary-Resolution packet, and produces exact finite source-core
certificates (Boolean deletion witnesses plus an integral compatibility graph).
"""

from __future__ import annotations

import argparse
import copy
import json
import resource
import time
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path


def canon(lits):
    vals = set(int(x) for x in lits)
    if any(-x in vals for x in vals):
        raise AssertionError("tautological clause")
    return tuple(sorted(vals, key=lambda x: (abs(x), x)))


def build_source(charge=(1, 0, 0, 0)):
    vertices = range(4)
    edges = [(u, v) for u in vertices for v in vertices if u < v]
    inc = [[i for i, e in enumerate(edges) if v in e] for v in vertices]
    clauses, meta = [], []
    r_groups, e_groups = [[] for _ in vertices], [[] for _ in vertices]
    for ei in range(6):
        clauses.append(canon((3 * ei + 1, 3 * ei + 2, 3 * ei + 3)))
        meta.append(("A", ei, None))
    for v in vertices:
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    lab = (a, b, c)
                    div = 0
                    for k, ei in enumerate(inc[v]):
                        div += (1 if edges[ei][0] == v else -1) * lab[k]
                    div %= 3
                    if div == charge[v]:
                        continue
                    clause = canon(-(3 * ei + lab[k] + 1) for k, ei in enumerate(inc[v]))
                    idx = len(clauses)
                    kind = "R" if div == (charge[v] + 1) % 3 else "E"
                    clauses.append(clause)
                    meta.append((kind, v, lab))
                    (r_groups if kind == "R" else e_groups)[v].append(idx)
    assert len(clauses) == 78
    assert all(len(c) == 3 for c in clauses)
    assert all(len(g) == 9 for g in r_groups + e_groups)
    assert len(set(clauses)) == 78
    return edges, inc, clauses, meta, r_groups, e_groups


def resolve(left, right, pivot):
    pivot = abs(int(pivot))
    if pivot in left and -pivot in right:
        pass
    elif -pivot in left and pivot in right:
        left, right = right, left
    else:
        raise AssertionError("pivot does not occur with opposite signs")
    return canon([x for x in left if x != pivot] + [x for x in right if x != -pivot])


def replay(raw, source):
    proof = raw["proof"]
    lines = proof["lines"]
    assert proof["source_count"] == 78
    assert proof["original_var_count"] == 18
    assert len(lines) == 252
    clauses, parents, depths = [], [], []
    source_seen = Counter()
    for i, line in enumerate(lines):
        clause = canon(line["clause"])
        if line["kind"] == "SOURCE":
            assert i < 78
            assert clause in source
            source_seen[clause] += 1
            parents.append(())
            depths.append(0)
        elif line["kind"] == "RES":
            assert i >= 78
            left, right = int(line["left"]), int(line["right"])
            assert 0 <= left < i and 0 <= right < i and left != right
            expected = resolve(clauses[left], clauses[right], line["pivot"])
            assert clause == expected
            parents.append((left, right))
            depths.append(1 + max(depths[left], depths[right]))
        else:
            raise AssertionError("unknown line kind")
        clauses.append(clause)
    assert source_seen == Counter(source)
    root = int(proof["root"])
    assert root == 251 and clauses[root] == ()
    live, stack = set(), [root]
    while stack:
        i = stack.pop()
        if i in live:
            continue
        live.add(i)
        stack.extend(parents[i])
    src_live = sorted(i for i in live if not parents[i])
    res_live = sorted(i for i in live if parents[i])
    assert len(src_live) == 70
    assert len(res_live) == 174
    assert len(live) == 244
    assert sum(len(parents[i]) for i in live) == 348
    assert depths[root] == 16
    assert max(len(clauses[i]) for i in live) == 6
    # Published literal count is over all 252 records, not only root ancestry.
    assert sum(map(len, clauses)) == 949
    return {
        "records": len(lines),
        "paid_RES": sum(x["kind"] == "RES" for x in lines),
        "root": root,
        "live_records": len(live),
        "live_source_ancestors": len(src_live),
        "live_RES": len(res_live),
        "premise_references": sum(len(parents[i]) for i in live),
        "root_depth": depths[root],
        "max_width": max(map(len, clauses)),
        "literal_occurrences": sum(map(len, clauses)),
        "source_indices": src_live,
        "omitted_source_indices": sorted(set(range(78)) - set(src_live)),
    }


def adversarial_rejections(raw, source):
    """Require independent replay to reject representative trace corruptions."""
    tests = {}

    def rejected(name, mutate):
        bad = copy.deepcopy(raw)
        mutate(bad)
        try:
            replay(bad, source)
        except (AssertionError, KeyError, TypeError, ValueError):
            tests[name] = True
            return
        raise AssertionError(f"corruption accepted: {name}")

    rejected("forged_source", lambda d: d["proof"]["lines"][0].update(clause=[1, 2, 4]))
    rejected("future_parent", lambda d: d["proof"]["lines"][78].update(left=251))
    rejected("false_pivot", lambda d: d["proof"]["lines"][78].update(pivot=18))
    rejected("mutated_resolvent", lambda d: d["proof"]["lines"][78].update(clause=[-3, 4, 5]))
    rejected("nonempty_root", lambda d: d["proof"]["lines"][251].update(clause=[18]))
    assert len(tests) == 5
    return tests


def clause_false(clause, mask):
    for lit in clause:
        bit = (mask >> (abs(lit) - 1)) & 1
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return False
    return True


def deletion_witnesses(clauses):
    """Enumerate all Boolean assignments once and index exact violation sets."""
    exact = {}
    full_models = 0
    for mask in range(1 << 18):
        bad = tuple(i for i, c in enumerate(clauses) if clause_false(c, mask))
        if not bad:
            full_models += 1
        exact.setdefault(bad, mask)
    assert full_models == 0
    return exact


def matmul(a, b):
    n = len(a)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    out[i][j] += a[i][k] * b[k][j]
    return out


def shift(a, scalar):
    return [[z - (scalar if i == j else 0) for j, z in enumerate(row)] for i, row in enumerate(a)]


def rank_q(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    m, n = len(a), len(a[0]) if a else 0
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def compatibility_certificate(meta, r_groups, exact):
    r_flat = [idx for group in r_groups for idx in group]
    pos = {idx: i for i, idx in enumerate(r_flat)}
    edges, pair_witnesses = [], {}
    for i, u in enumerate(r_flat):
        for v in r_flat[i + 1:]:
            witness = exact.get(tuple(sorted((u, v))))
            if witness is not None:
                edges.append((pos[u], pos[v]))
                pair_witnesses[f"{u},{v}"] = witness
    assert len(edges) == 162
    a = [[0] * 36 for _ in range(36)]
    for u, v in edges:
        a[u][v] = a[v][u] = 1
    assert all(sum(row) == 9 for row in a)
    assert all(a[i][j] == a[j][i] for i in range(36) for j in range(36))
    p = matmul(matmul(matmul(a, shift(a, 9)), shift(a, 3)), shift(a, -3))
    assert not any(any(row) for row in p)
    multiplicities = {}
    for eigen in (-3, 0, 3, 9):
        multiplicities[str(eigen)] = 36 - rank_q(shift(a, eigen))
    assert multiplicities == {"-3": 15, "0": 8, "3": 12, "9": 1}
    independent = [pos[idx] for idx in r_groups[3]]
    assert len(independent) == 9
    assert all(a[u][v] == 0 for i, u in enumerate(independent) for v in independent[i + 1:])
    # Hoffman ratio bound: alpha <= n*(-lambda_min)/(d-lambda_min)=36*3/12=9.
    # Symmetry plus the exact polynomial and nullities certify lambda_min=-3.
    alpha_upper = 36 * 3 // 12
    assert alpha_upper == len(independent) == 9
    return {
        "vertices": 36,
        "edges": len(edges),
        "degree": 9,
        "integral_matrix_polynomial": "A(A-9I)(A-3I)(A+3I)=0",
        "exact_spectrum_multiplicities": multiplicities,
        "independence_number": 9,
        "minimum_vertex_cover": 27,
        "pair_deletion_witnesses": pair_witnesses,
        "explicit_independent_vertices": independent,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", type=Path)
    args = ap.parse_args()
    start = time.perf_counter()
    raw = json.loads(args.raw.read_text())
    edges, inc, clauses, meta, r_groups, e_groups = build_source()
    replay_result = replay(raw, clauses)
    rejected = adversarial_rejections(raw, clauses)
    exact = deletion_witnesses(clauses)

    essential = list(range(6)) + [idx for group in e_groups for idx in group]
    essential_witnesses = {str(i): exact[(i,)] for i in essential}
    assert len(essential) == len(essential_witnesses) == 42
    compat = compatibility_certificate(meta, r_groups, exact)

    omitted_group = set(r_groups[3])
    core = [i for i in range(78) if i not in omitted_group]
    assert len(core) == 69
    assert not any(set(bad).isdisjoint(core) for bad in exact)
    core_witnesses = {}
    for i in core:
        candidates = [(bad, mask) for bad, mask in exact.items() if bad and set(bad).intersection(core) == {i}]
        assert candidates, f"no deletion witness for core clause {i}"
        core_witnesses[str(i)] = min(mask for _, mask in candidates)
    assert len(core_witnesses) == 69

    proof_core = replay_result["source_indices"]
    assert not any(set(bad).isdisjoint(proof_core) for bad in exact)

    result = {
        "label": "LSPV-5/454",
        "status": "COMPUTATIONAL finite independent audit; not historical R_mix341 accepted-byte replay",
        "source": {
            "vertices": 4,
            "edges": [list(e) for e in edges],
            "Boolean_variables": 18,
            "strict_3CNF_clauses": 78,
            "ALO": 6,
            "essential_for_every_UNSAT_subset": 42,
            "R_clauses": 36,
            "full_Boolean_models": 0,
        },
        "published_packet_replay": replay_result,
        "adversarial_trace_corruptions_rejected": rejected,
        "source_core_lower_certificate": {
            "essential_single_deletion_witness_count": len(essential_witnesses),
            "essential_single_deletion_witnesses": essential_witnesses,
            "compatibility": compat,
            "minimum_UNSAT_source_subset": 69,
            "binary_source_explicit_inference_lower_bound": 68,
            "constructed_69_core_indices": core,
            "constructed_69_core_clause_deletion_witnesses": core_witnesses,
            "published_70_source_proof_core_is_UNSAT": True,
        },
        "scope_firewall": {
            "ordinary_RES_upper": 174,
            "source_explicit_at_most_binary_lower": 68,
            "historical_R_mix341_parser_authenticated": False,
            "asymptotic_full_mixed_lower_bound": False,
            "noncircular_B3": False,
            "P_vs_NP": "OPEN",
        },
        "resources": {
            "Boolean_assignments_indexed": 1 << 18,
            "elapsed_seconds": time.perf_counter() - start,
            "max_rss_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")


if __name__ == "__main__":
    main()
