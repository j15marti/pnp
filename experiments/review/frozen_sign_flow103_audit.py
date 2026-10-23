#!/usr/bin/env python3
"""Audit fixed-witness balanced-sign repair by min-cost circulation."""

from __future__ import annotations

import ast
import hashlib
import heapq
import itertools
import json
from collections import Counter
from pathlib import Path


SEED = 202610240148
CANONICAL_SOURCE = Path(
    "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
)
LOCAL_SOURCE = Path("results/raw/review/DOECKER61_original_source.txt")
SOURCE = CANONICAL_SOURCE if CANONICAL_SOURCE.exists() else LOCAL_SOURCE


class MinCostFlow:
    def __init__(self, n):
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap, cost):
        forward = [v, cap, cost, None]
        reverse = [u, 0, -cost, forward]
        forward[3] = reverse
        self.g[u].append(forward)
        self.g[v].append(reverse)
        return forward

    def send(self, source, sink, amount):
        n = len(self.g)
        potential = [0] * n
        total_cost = 0
        sent = 0
        while sent < amount:
            dist = [10**18] * n
            prev = [None] * n
            dist[source] = 0
            queue = [(0, source)]
            while queue:
                du, u = heapq.heappop(queue)
                if du != dist[u]:
                    continue
                for edge in self.g[u]:
                    v, cap, cost, _ = edge
                    if cap <= 0:
                        continue
                    nd = du + cost + potential[u] - potential[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        prev[v] = (u, edge)
                        heapq.heappush(queue, (nd, v))
            if prev[sink] is None:
                break
            for v in range(n):
                if dist[v] < 10**18:
                    potential[v] += dist[v]
            push = amount - sent
            v = sink
            while v != source:
                u, edge = prev[v]
                push = min(push, edge[1])
                v = u
            v = sink
            while v != source:
                u, edge = prev[v]
                edge[1] -= push
                edge[3][1] += push
                total_cost += push * edge[2]
                v = u
            sent += push
        return sent, total_cost


def load_source():
    lines = [line for line in SOURCE.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    return [tuple(map(int, clause))
            for clause in ast.literal_eval("\n".join(lines))]


def validate_exact_balanced(formula):
    variables = sorted({abs(lit) for clause in formula for lit in clause})
    counts = Counter(lit for clause in formula for lit in clause)
    assert all(len(clause) == 3 for clause in formula)
    assert all(len({abs(lit) for lit in clause}) == 3 for clause in formula)
    assert all(counts[v] == 2 and counts[-v] == 2 for v in variables)
    return variables


def min_balanced_repair(formula, assignment):
    """Return a minimum-Hamming balanced signing satisfied by assignment."""
    variables = validate_exact_balanced(formula)
    clauses = list(range(len(formula)))
    var_pos = {v: i for i, v in enumerate(variables)}
    ss, tt = 0, 1
    vbase = 2
    cbase = vbase + len(variables)
    sink = cbase + len(clauses)
    net = MinCostFlow(sink + 1)

    # Lower-bound circulation reduction:
    # each variable emits exactly two true occurrences; each clause receives
    # at least one and sends at most two surplus units to sink.
    occurrence_edges = {}
    for vi, v in enumerate(variables):
        net.add_edge(ss, vbase + vi, 2, 0)
    for ci, clause in enumerate(formula):
        net.add_edge(cbase + ci, tt, 1, 0)
        net.add_edge(cbase + ci, sink, 2, 0)
        for lit in clause:
            v = abs(lit)
            initially_true = assignment[v] == (lit > 0)
            edge = net.add_edge(vbase + var_pos[v], cbase + ci,
                                1, 0 if initially_true else 1)
            occurrence_edges[(ci, v)] = (edge, lit)
    surplus = 2 * len(variables) - len(clauses)
    assert surplus >= 0
    net.add_edge(sink, tt, surplus, 0)
    sent, additions = net.send(ss, tt, 2 * len(variables))
    if sent != 2 * len(variables):
        return None

    repaired = []
    selected = set()
    for key, (edge, _) in occurrence_edges.items():
        if edge[3][1] == 1:
            selected.add(key)
    for ci, clause in enumerate(formula):
        out = []
        for lit in clause:
            v = abs(lit)
            true_here = (ci, v) in selected
            positive = assignment[v] if true_here else not assignment[v]
            out.append(v if positive else -v)
        repaired.append(tuple(out))
    distance = sum(a != b for ca, cb in zip(formula, repaired)
                   for a, b in zip(ca, cb))
    assert distance == 2 * additions
    return repaired, distance, additions


def satisfies(formula, assignment):
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula)


def brute_min_repair(formula, assignment):
    variables = validate_exact_balanced(formula)
    occurrences = {v: [] for v in variables}
    for ci, clause in enumerate(formula):
        for pi, lit in enumerate(clause):
            occurrences[abs(lit)].append((ci, pi))
    best = None
    for choices in itertools.product(*(itertools.combinations(range(4), 2)
                                       for _ in variables)):
        positive = set()
        for v, chosen in zip(variables, choices):
            for oi in chosen:
                positive.add(occurrences[v][oi])
        candidate = []
        for ci, clause in enumerate(formula):
            candidate.append(tuple(abs(lit) if (ci, pi) in positive else -abs(lit)
                                   for pi, lit in enumerate(clause)))
        if satisfies(candidate, assignment):
            distance = sum(a != b for ca, cb in zip(formula, candidate)
                           for a, b in zip(ca, cb))
            if best is None or distance < best:
                best = distance
    return best


def main():
    source = load_source()
    variables = validate_exact_balanced(source)
    assert len(variables) == 198 and len(source) == 264
    assert all(all(lit > 0 for lit in clause) or
               all(lit < 0 for lit in clause) for clause in source)
    positive_clauses = sum(all(lit > 0 for lit in clause)
                           for clause in source)
    negative_clauses = sum(all(lit < 0 for lit in clause)
                           for clause in source)
    assert positive_clauses == negative_clauses == len(source) // 2
    assignment = {v: True for v in variables}
    result = min_balanced_repair(source, assignment)
    assert result is not None
    repaired, distance, additions = result
    validate_exact_balanced(repaired)
    assert satisfies(repaired, assignment)
    assert [tuple(abs(x) for x in c) for c in repaired] == [
        tuple(abs(x) for x in c) for c in source
    ]
    assert additions == negative_clauses
    assert distance == len(source)

    # Exhaustive reference tests: all balanced signings of a four-clause
    # three-variable support, under all eight prescribed assignments.
    small = [
        (1, 2, 3),
        (1, -2, -3),
        (-1, 2, -3),
        (-1, -2, 3),
    ]
    small_checks = 0
    for mask in range(8):
        a = {v: bool(mask & (1 << (v - 1))) for v in (1, 2, 3)}
        flow = min_balanced_repair(small, a)
        brute = brute_min_repair(small, a)
        assert flow is not None and flow[1] == brute
        validate_exact_balanced(flow[0])
        assert satisfies(flow[0], a)
        small_checks += 4

    compact = json.dumps(repaired, separators=(",", ":"))
    payload = {
        "label": "COMPUTATIONAL",
        "seed": SEED,
        "source": str(CANONICAL_SOURCE),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_variables": len(variables),
        "source_clauses": len(source),
        "source_positive_monotone_clauses": positive_clauses,
        "source_negative_monotone_clauses": negative_clauses,
        "minimum_sign_hamming_distance_to_all_true_sat": distance,
        "minimum_false_to_true_additions": additions,
        "repaired_all_true_witness_verified": True,
        "ordered_unsigned_support_preserved": True,
        "repaired_compact_sha256": hashlib.sha256(compact.encode()).hexdigest(),
        "small_exhaustive_assignments": 8,
        "small_balanced_signings_per_assignment": 216,
        "assertion_accounted_checks": small_checks + 12,
        "failures": 0,
        "original_unsat_dependency": "DOECKER-CORE-CERT61 checked certificate",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["sha256_without_sha_field"] = hashlib.sha256(
        canonical.encode()
    ).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
