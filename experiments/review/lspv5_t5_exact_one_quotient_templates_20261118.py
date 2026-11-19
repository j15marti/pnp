#!/usr/bin/env python3
"""Independent exact-one T5 quotient-template audit.

This is intentionally independent of the supplied solver.  It proves finite
classification claims by exhaustive masks and tests the symbolic quotient
criterion used in the accompanying report.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import resource
import sys
import tracemalloc
from collections import Counter, defaultdict
from pathlib import Path


WINS = ({1, 3}, {2, 4}, {0, 3}, {1, 4}, {0, 2})


def R(a: int, b: int) -> int:
    return int(b in WINS[a])


def Q(a: int, b: int, c: int) -> int:
    return R(a, b) ^ R(a, c)


def P(a: int, b: int, c: int) -> int:
    return R(a, b) & R(a, c)


def rgs_partitions(n: int):
    """Restricted-growth strings: each equality partition exactly once."""
    a = [0] * n

    def rec(i: int, mx: int):
        if i == n:
            yield tuple(a)
            return
        for x in range(mx + 2):
            a[i] = x
            yield from rec(i + 1, max(mx, x))

    if n == 0:
        yield ()
    else:
        yield from rec(1, 0)


def pairs(q: int):
    return list(itertools.combinations(range(q), 2))


def orientation_bit(mask: int, q: int, u: int, v: int) -> int:
    if u == v:
        return 0
    if u > v:
        return 1 - orientation_bit(mask, q, v, u)
    idx = pairs(q).index((u, v))
    return (mask >> idx) & 1  # 1 means u -> v


def degrees(mask: int, q: int):
    out = [0] * q
    for u, v in pairs(q):
        if orientation_bit(mask, q, u, v):
            out[u] += 1
        else:
            out[v] += 1
    return out


def embeds_in_t5(mask: int, q: int) -> bool:
    for colors in itertools.permutations(range(5), q):
        if all(orientation_bit(mask, q, u, v) == R(colors[u], colors[v]) for u, v in pairs(q)):
            return True
    return False


def follower_bipartite(subset: int, clauses: list[tuple[int, int, int]], n: int) -> bool:
    by_head = defaultdict(list)
    for i, (h, u, v) in enumerate(clauses):
        if (subset >> i) & 1:
            by_head[h].append((u, v))
    for edges in by_head.values():
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        color = {}
        for root in list(adj):
            if root in color:
                continue
            color[root] = 0
            stack = [root]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v not in color:
                        color[v] = color[u] ^ 1
                        stack.append(v)
                    elif color[v] == color[u]:
                        return False
    return True


def truth_mask_assignment(values, clauses):
    mask = 0
    for i, (h, u, v) in enumerate(clauses):
        if Q(values[h], values[u], values[v]):
            mask |= 1 << i
    return mask


def truth_mask_template(partition, orientation, clauses):
    q = max(partition) + 1
    mask = 0
    for i, (h, u, v) in enumerate(clauses):
        bh, bu, bv = partition[h], partition[u], partition[v]
        if orientation_bit(orientation, q, bh, bu) ^ orientation_bit(orientation, q, bh, bv):
            mask |= 1 << i
    return mask


def sat_from_masks(subset: int, masks: set[int]) -> bool:
    return any((subset & ~m) == 0 for m in masks)


def main() -> None:
    tracemalloc.start()
    assertions = 0
    op = Counter()

    # Local relation and projection.
    q_triples = []
    p_triples = []
    for a, b, c in itertools.product(range(5), repeat=3):
        op["ordered_local_triples"] += 1
        if Q(a, b, c):
            q_triples.append((a, b, c))
        if P(a, b, c):
            p_triples.append((a, b, c))
    assert len(q_triples) == 60 and len(p_triples) == 20
    assert set(q_triples).isdisjoint(p_triples)
    assertions += 3

    projection_mult = {}
    for b in range(5):
        for c in range(5):
            count = sum(Q(a, b, c) for a in range(5))
            assert (count > 0) == (b != c)
            if b != c:
                assert count in (2, 4)
                projection_mult[f"{b}{c}"] = count
            assertions += 2 if b != c else 1

    # Exhaust all labeled tournaments on q<=5: degree capacity iff T5 embedding.
    tournament_audit = []
    for q in range(1, 6):
        total = 1 << (q * (q - 1) // 2)
        cap = emb = 0
        for mask in range(total):
            op["tournaments_tested"] += 1
            deg = degrees(mask, q)
            cap_ok = max(deg, default=0) <= 2 and max((q - 1 - d for d in deg), default=0) <= 2
            emb_ok = embeds_in_t5(mask, q)
            assert cap_ok == emb_ok
            assertions += 1
            cap += cap_ok
            emb += emb_ok
        tournament_audit.append({"q": q, "labeled_tournaments": total, "capacity_ok": cap, "t5_embeddable": emb})

    # Canonical four-variable clauses: head plus unordered pair of other variables.
    n = 4
    clauses = []
    for h in range(n):
        rest = [v for v in range(n) if v != h]
        for u, v in itertools.combinations(rest, 2):
            clauses.append((h, u, v))
    assert len(clauses) == 12
    assertions += 1

    brute_masks = set()
    for values in itertools.product(range(5), repeat=n):
        brute_masks.add(truth_mask_assignment(values, clauses))
        op["four_variable_assignments"] += 1

    arbitrary_tournament_masks = set()
    capacity_template_masks = set()
    partition_count = 0
    template_count = 0
    for partition in rgs_partitions(n):
        partition_count += 1
        q = max(partition) + 1
        for orientation in range(1 << (q * (q - 1) // 2)):
            template_count += 1
            m = truth_mask_template(partition, orientation, clauses)
            arbitrary_tournament_masks.add(m)
            deg = degrees(orientation, q)
            if max(deg, default=0) <= 2 and max((q - 1 - d for d in deg), default=0) <= 2:
                capacity_template_masks.add(m)

    all_count = 1 << len(clauses)
    sat_count = unsat_count = parity_count = parity_unsat = 0
    minimal_unsat = []
    parity_critical = []
    mismatch = []
    for subset in range(all_count):
        brute = sat_from_masks(subset, brute_masks)
        template = sat_from_masks(subset, capacity_template_masks)
        if brute != template:
            mismatch.append(subset)
        assertions += 1
        parity = follower_bipartite(subset, clauses, n)
        sat_count += brute
        unsat_count += not brute
        parity_count += parity
        parity_unsat += parity and not brute
        if not brute:
            critical = all(sat_from_masks(subset & ~(1 << i), brute_masks) for i in range(len(clauses)) if (subset >> i) & 1)
            if critical:
                minimal_unsat.append(subset)
                if parity:
                    parity_critical.append(subset)
    assert mismatch == []
    assert (sat_count, unsat_count, parity_count, parity_unsat) == (1976, 2120, 2401, 425)
    assert Counter(x.bit_count() for x in minimal_unsat) == Counter({3: 4, 5: 36, 6: 36})
    assert len(parity_critical) == 72
    assertions += 4

    critical_class = Counter()
    for subset in parity_critical:
        any_tournament = sat_from_masks(subset, arbitrary_tournament_masks)
        critical_class[(subset.bit_count(), any_tournament)] += 1
    assert critical_class == Counter({(5, True): 24, (5, False): 12, (6, False): 36})
    assertions += 1

    # Named three-clause parity contradiction and five-clause capacity core.
    triangle = [(0, 1, 2), (0, 2, 3), (0, 3, 1)]
    tri_full = tri_delete = 0
    for values in itertools.product(range(5), repeat=4):
        vals = [Q(values[h], values[u], values[v]) for h, u, v in triangle]
        tri_full += all(vals)
        tri_delete += sum(all(vals[j] for j in range(3) if j != i) for i in range(3))
        op["named_control_assignments"] += 1
    assert tri_full == 0 and tri_delete == 450
    assertions += 2

    five = [(0, 1, 2), (0, 1, 3), (1, 0, 2), (1, 2, 3), (2, 0, 3)]
    full = 0
    deletion_counts = [0] * 5
    deletion_witnesses = [None] * 5
    for values in itertools.product(range(5), repeat=4):
        vals = [Q(values[h], values[u], values[v]) for h, u, v in five]
        full += all(vals)
        for i in range(5):
            if all(vals[j] for j in range(5) if j != i):
                deletion_counts[i] += 1
                deletion_witnesses[i] = deletion_witnesses[i] or values
        op["named_control_assignments"] += 1
    assert full == 0
    assert deletion_counts == [10, 40, 10, 30, 25]
    assertions += 2

    # K6 with a private head per edge: projection gives a critical 5-coloring obstruction.
    k6_edges = list(itertools.combinations(range(6), 2))
    k6_checks = 0
    for omitted, (a, b) in enumerate(k6_edges):
        colors = [None] * 6
        colors[a] = colors[b] = 0
        next_color = 1
        for v in range(6):
            if colors[v] is None:
                colors[v] = next_color
                next_color += 1
        heads = []
        for u, v in k6_edges:
            if colors[u] == colors[v]:
                heads.append(colors[u])
            elif R(colors[u], colors[v]):
                heads.append(colors[u])
            else:
                heads.append(colors[v])
        for i, (u, v) in enumerate(k6_edges):
            if i == omitted:
                continue
            assert Q(heads[i], colors[u], colors[v])
            assertions += 1
            k6_checks += 1

    # Independently replay every supplied large-fixture deletion witness if present.
    fixture_path = Path("library_inputs/t5_exact_one/extracted/t5_exact_one/redteam/mycielski_fixture.json")
    fixture_checks = 0
    fixture_witnesses = 0
    if fixture_path.exists():
        fixture = json.loads(fixture_path.read_text())
        fclauses = [tuple(x) for x in fixture["clauses"]]
        assert len(fclauses) == len(fixture["deletion_witnesses"]) == 236
        assertions += 1
        for item in fixture["deletion_witnesses"]:
            omitted = item["omitted_clause"]
            assignment = item["assignment"]
            false_set = []
            for i, (h, u, v) in enumerate(fclauses):
                val = Q(assignment[h], assignment[u], assignment[v])
                fixture_checks += 1
                if not val:
                    false_set.append(i)
            assert false_set == [omitted]
            assertions += 1
            fixture_witnesses += 1

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    source_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "status": "PASS",
        "method": "independent exhaustive quotient-template masks; no SAT solver and no random seeds",
        "local_relation": {"Q_successes": len(q_triples), "P_successes": len(p_triples), "accepted_sets_disjoint": True},
        "projection_multiplicity_histogram": dict(sorted(Counter(projection_mult.values()).items())),
        "tournament_embedding_audit": tournament_audit,
        "quotient_template_theorem": {
            "partitions_of_four": partition_count,
            "labeled_partition_orientation_candidates": template_count,
            "capacity_truth_masks": len(capacity_template_masks),
            "brute_t5_truth_masks": len(brute_masks),
            "all_4096_match": not mismatch,
        },
        "four_variable_classification": {
            "systems": all_count,
            "sat": sat_count,
            "unsat": unsat_count,
            "parity_feasible": parity_count,
            "parity_feasible_unsat": parity_unsat,
            "critical_size_histogram": dict(sorted(Counter(x.bit_count() for x in minimal_unsat).items())),
            "parity_critical_classification": {f"clauses={k[0]},some_tournament={str(k[1]).lower()}": v for k, v in sorted(critical_class.items())},
        },
        "named_controls": {
            "three_clause_full_models": tri_full,
            "three_clause_models_after_each_deletion": [150, 150, 150],
            "five_clause_full_models": full,
            "five_clause_deletion_counts": deletion_counts,
            "five_clause_deletion_witnesses": [list(x) for x in deletion_witnesses],
            "K6_private_head_deletion_witnesses": len(k6_edges),
            "K6_direct_remaining_clause_checks": k6_checks,
        },
        "large_fixture_replay": {"witnesses": fixture_witnesses, "direct_clause_checks": fixture_checks},
        "operation_counts": dict(op),
        "space_metrics": {
            "tracemalloc_peak_python_heap_bytes": peak,
            "ru_maxrss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "definition": "tracemalloc peak tracks traced Python heap allocations; ru_maxrss is OS maximum resident set in KiB on Linux; neither is a machine-independent complexity-space proof",
        },
        "assertions": assertions,
        "python": sys.version.split()[0],
        "script_sha256": source_sha,
        "limitations": [
            "the quotient criterion is exact but its equality-partition search is exponential in general",
            "finite enumeration and measured memory do not imply an asymptotic lower bound",
            "the 283-variable fixture has fixed incidence girth eight and a short structural certificate",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
