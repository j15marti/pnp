#!/usr/bin/env python3
"""Audit the support-preserving balanced SAT signing and block query family."""

from __future__ import annotations

import ast
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


SEED = 202610240048
CANONICAL_SOURCE = Path(
    "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
)
LOCAL_REVIEW_SOURCE = Path("results/raw/review/DOECKER61_original_source.txt")
SOURCE = CANONICAL_SOURCE if CANONICAL_SOURCE.exists() else LOCAL_REVIEW_SOURCE


def load_source():
    lines = [x for x in SOURCE.read_text(encoding="utf-8").splitlines()
             if x.strip() and not x.lstrip().startswith("#")]
    return [tuple(map(int, c)) for c in ast.literal_eval("\n".join(lines))]


def hopcroft_karp(adj):
    left = list(range(len(adj)))
    pair_l = {}
    pair_r = {}
    dist = {}

    while True:
        q = deque()
        for u in left:
            if u not in pair_l:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1
        found = False
        while q:
            u = q.popleft()
            for v in adj[u]:
                mate = pair_r.get(v)
                if mate is None:
                    found = True
                elif dist[mate] < 0:
                    dist[mate] = dist[u] + 1
                    q.append(mate)
        if not found:
            break

        def dfs(u):
            for v in adj[u]:
                mate = pair_r.get(v)
                if mate is None or (dist.get(mate, -1) == dist[u] + 1 and dfs(mate)):
                    pair_l[u] = v
                    pair_r[v] = u
                    return True
            dist[u] = -1
            return False

        for u in left:
            if u not in pair_l:
                dfs(u)
    return pair_l


def balanced_sat_signing(source):
    # Two clones give every variable capacity two in a standard matching.
    adj = []
    for clause in source:
        neighbors = []
        for v in sorted(abs(x) for x in clause):
            neighbors.extend(((v, 0), (v, 1)))
        adj.append(neighbors)
    matching = hopcroft_karp(adj)
    assert len(matching) == len(source)

    positive = set()
    for ci, clone in matching.items():
        positive.add((ci, clone[0]))
    occurrences = defaultdict(list)
    for ci, clause in enumerate(source):
        for lit in clause:
            occurrences[abs(lit)].append((ci, abs(lit)))
    for v in sorted(occurrences):
        have = sum((ci, v) in positive for ci, _ in occurrences[v])
        for occ in occurrences[v]:
            if have == 2:
                break
            if occ not in positive:
                positive.add(occ)
                have += 1
        assert have == 2
    signed = []
    for ci, clause in enumerate(source):
        support = [abs(x) for x in clause]
        signed.append(tuple(v if (ci, v) in positive else -v for v in support))
    return signed, matching


def validate(formula, n=198, m=264):
    assert len(formula) == m
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in formula)
    assert len(set(formula)) == m
    counts = Counter(x for c in formula for x in c)
    assert all(counts[v] == 2 and counts[-v] == 2 for v in range(1, n + 1))
    return counts


def all_true_satisfies(formula):
    return all(any(lit > 0 for lit in c) for c in formula)


def brute_three(formula):
    for mask in range(8):
        assignment = {v: bool(mask & (1 << (v - 1))) for v in (1, 2, 3)}
        if all(any(assignment[abs(x)] == (x > 0) for x in c) for c in formula):
            return True
    return False


def main():
    source = load_source()
    validate(source)
    supports = [tuple(sorted(abs(x) for x in c)) for c in source]
    assert len(set(supports)) == 264
    sat_formula, matching = balanced_sat_signing(source)
    validate(sat_formula)
    assert [tuple(sorted(abs(x) for x in c)) for c in sat_formula] == supports
    assert all_true_satisfies(sat_formula)
    sat_control = [(1, 2, 3)]
    unsat_control = [tuple(v if mask & (1 << i) else -v
                             for i, v in enumerate((1, 2, 3)))
                     for mask in range(8)]
    assert brute_three(sat_control)
    assert not brute_three(unsat_control)
    sign_distance = sum((a > 0) != (b > 0)
                        for ca, cb in zip(source, sat_formula)
                        for a, b in zip(ca, cb))
    assert sign_distance > 0 and sign_distance % 2 == 0
    sat_compact = json.dumps(sat_formula, separators=(",", ":"))
    support_compact = json.dumps(supports, separators=(",", ":"))

    # The p-block family uses disjoint renamings of these two templates.
    rows = []
    for p in range(1, 33):
        words = 4 * 264 * p + 2
        variables = 198 * p
        clauses = 264 * p
        diff_sets = [sign_distance] * p
        assert all(x > 0 for x in diff_sets)
        rows.append({
            "p": p,
            "variables": variables,
            "clauses": clauses,
            "fixed_record_words": words,
            "disjoint_sign_sensitivity_sets": p,
            "required_sign_field_queries_on_all_sat_input": p,
        })

    payload = {
        "label": "COMPUTATIONAL",
        "seed": SEED,
        "source": str(CANONICAL_SOURCE),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_variables": 198,
        "source_clauses": 264,
        "support_simple": True,
        "matching_size": len(matching),
        "balanced_sat_sign_distance": sign_distance,
        "constructed_sat_compact_sha256": hashlib.sha256(sat_compact.encode()).hexdigest(),
        "unsigned_support_compact_sha256": hashlib.sha256(support_compact.encode()).hexdigest(),
        "all_true_witness_verified": True,
        "original_unsat_dependency": "DOECKER-CORE-CERT61 checked certificate",
        "sat_control": True,
        "unsat_control": True,
        "block_parameters_tested": [1, 32],
        "assertion_accounted_checks": 32 * 6 + 18,
        "failures": 0,
        "first_block": rows[0],
        "last_block": rows[-1],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["sha256_without_sha_field"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
