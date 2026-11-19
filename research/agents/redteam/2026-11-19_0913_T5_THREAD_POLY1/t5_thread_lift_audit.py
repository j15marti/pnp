#!/usr/bin/env python3
"""Independent T5 thread quotient and witness-lifting audit.

No external solver is used.  The only search is five-valued AC/DFS on the
branch core; internal degree-two vertices are reconstructed canonically.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


def rel(a: int, b: int) -> bool:
    return (b - a) % 5 in (1, 3)


def parse(path: Path):
    raw = path.read_bytes()
    n = None
    arcs = []
    declared = set()
    for line in raw.decode("ascii").splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "p":
            assert fields[1] == "t5"
            n, expected_m = map(int, fields[2:])
        elif fields[0] == "v":
            declared.add(int(fields[1]))
        elif fields[0] == "a":
            arcs.append((int(fields[1]), int(fields[2])))
    assert n is not None and declared == set(range(n))
    assert len(arcs) == expected_m and len(set(arcs)) == len(arcs)
    assert all(u != v for u, v in arcs)
    return raw, n, arcs


def suppress(n, arcs):
    adj = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(arcs):
        adj[u].append(eid)
        adj[v].append(eid)
    branches = sorted(v for v in range(n) if len(adj[v]) != 2)
    branch_set = set(branches)
    assert branches
    seen = set()
    threads = []
    edge_location = {}
    for start in branches:
        for first_eid in adj[start]:
            if first_eid in seen:
                continue
            path = [start]
            edge_ids = []
            prev_v, eid = start, first_eid
            while True:
                assert eid not in seen
                seen.add(eid)
                edge_ids.append(eid)
                u, v = arcs[eid]
                nxt = v if u == prev_v else u
                path.append(nxt)
                if nxt in branch_set:
                    break
                choices = [x for x in adj[nxt] if x != eid]
                assert len(choices) == 1
                prev_v, eid = nxt, choices[0]
            tid = len(threads)
            word = "".join(
                "F" if arcs[e] == (path[i], path[i + 1]) else "B"
                for i, e in enumerate(edge_ids)
            )
            thread = {
                "path": path,
                "edge_ids": edge_ids,
                "word": word,
                "allowed_diffs": sorted(path_diffs(word)),
            }
            threads.append(thread)
            for pos, original_eid in enumerate(edge_ids):
                edge_location[original_eid] = (tid, pos)
    assert seen == set(range(len(arcs)))
    assert len(edge_location) == len(arcs)
    return branches, threads, edge_location


def path_ok(word, colors, skipped=None):
    for i, direction in enumerate(word):
        if i == skipped:
            continue
        a, b = colors[i], colors[i + 1]
        if direction == "F":
            if not rel(a, b):
                return False
        elif not rel(b, a):
            return False
    return True


def path_diffs(word):
    length = len(word)
    out = set()
    for internal in itertools.product(range(5), repeat=max(0, length - 1)):
        for endpoint in range(5):
            colors = (0,) + internal + (endpoint,)
            if path_ok(word, colors):
                out.add(endpoint)
    return out


def canonical_path_fill(word, left, right, skipped=None):
    for internal in itertools.product(range(5), repeat=max(0, len(word) - 1)):
        colors = (left,) + internal + (right,)
        if path_ok(word, colors, skipped):
            return colors
    return None


def solve_core(branches, threads, omitted=None):
    index = {v: i for i, v in enumerate(branches)}
    constraints = []
    for tid, thread in enumerate(threads):
        if tid == omitted:
            continue
        i = index[thread["path"][0]]
        j = index[thread["path"][-1]]
        constraints.append((i, j, frozenset(thread["allowed_diffs"])))
    stats = {"nodes": 0, "propagation_rounds": 0, "value_trials": 0}

    def propagate(domains):
        while True:
            stats["propagation_rounds"] += 1
            changed = False
            for i, j, allowed in constraints:
                di, dj = domains[i], domains[j]
                ni = {a for a in di if any((b - a) % 5 in allowed for b in dj)}
                nj = {b for b in dj if any((b - a) % 5 in allowed for a in ni)}
                if not ni or not nj:
                    return None
                if ni != di:
                    domains[i] = ni
                    changed = True
                if nj != dj:
                    domains[j] = nj
                    changed = True
            if not changed:
                return domains

    def dfs(domains):
        stats["nodes"] += 1
        domains = propagate([set(x) for x in domains])
        if domains is None:
            return None
        undecided = [i for i, d in enumerate(domains) if len(d) > 1]
        if not undecided:
            return [next(iter(d)) for d in domains]
        var = min(undecided, key=lambda i: (len(domains[i]), -sum(
            1 for a, b, _ in constraints if a == i or b == i
        ), i))
        for value in sorted(domains[var]):
            stats["value_trials"] += 1
            child = [set(x) for x in domains]
            child[var] = {value}
            answer = dfs(child)
            if answer is not None:
                return answer
        return None

    initial = [set(range(5)) for _ in branches]
    if omitted is None:
        initial[0] = {0}  # quotient global fivefold rotation
    else:
        # Every solution of the omitted-thread core must violate the omitted
        # relation, or it would color the full UNSAT core.  Anchor its left
        # endpoint and enumerate only complementary endpoint differences.
        thread = threads[omitted]
        left = index[thread["path"][0]]
        right = index[thread["path"][-1]]
        initial[left] = {0}
        initial[right] = set(range(5)) - set(thread["allowed_diffs"])
    answer = dfs(initial)
    if answer is None:
        return None, stats
    return {v: answer[index[v]] for v in branches}, stats


def lift(n, arcs, threads, branch_colors, omitted_tid, omitted_pos):
    colors = [None] * n
    for v, color in branch_colors.items():
        colors[v] = color
    for tid, thread in enumerate(threads):
        path = thread["path"]
        skipped = omitted_pos if tid == omitted_tid else None
        fill = canonical_path_fill(
            thread["word"], colors[path[0]], colors[path[-1]], skipped
        )
        assert fill is not None
        for v, color in zip(path, fill):
            if colors[v] is not None:
                assert colors[v] == color
            colors[v] = color
    assert all(c is not None for c in colors)
    omitted_eid = threads[omitted_tid]["edge_ids"][omitted_pos]
    for eid, (u, v) in enumerate(arcs):
        if eid != omitted_eid:
            assert rel(colors[u], colors[v])
    u, v = arcs[omitted_eid]
    assert not rel(colors[u], colors[v])
    return colors


def verify_path_formula():
    relation_sets = {}
    checked = 0
    unrestricted_l4 = True
    for length in range(1, 5):
        for bits in itertools.product("FB", repeat=length):
            word = "".join(bits)
            actual = path_diffs(word)
            # Along traversal: F contributes {1,3}=1+{0,2};
            # B contributes {-1,-3}={4,2}=2+{0,2}.
            offset = sum(1 if bit == "F" else 2 for bit in word) % 5
            predicted = {(offset + 2 * j) % 5 for j in range(length + 1)}
            assert actual == predicted
            # Compact GF(5) equation: the relation holds exactly when the
            # degree-(L+1) polynomial has a root at the endpoint difference.
            for difference in range(5):
                value = 1
                for j in range(length + 1):
                    value = value * (difference - offset - 2 * j) % 5
                assert (value == 0) == (difference in actual)
            checked += 1
            if length <= 3:
                relation_sets.setdefault(tuple(sorted(actual)), []).append(word)
            else:
                unrestricted_l4 &= actual == set(range(5))
    assert len(relation_sets) == 9 and unrestricted_l4
    return {
        "orientation_words_checked": checked,
        "nontrivial_relations_lte3": len(relation_sets),
        "all_length4_words_unrestricted": unrestricted_l4,
        "gf5_polynomial_normal_form_verified": True,
        "relations": {
            ",".join(map(str, key)): words for key, words in sorted(relation_sets.items())
        },
    }


def main():
    source = Path(__file__).with_name("source079.t5")
    raw, n, arcs = parse(source)
    branches, threads, edge_location = suppress(n, arcs)
    assert max(len(t["edge_ids"]) for t in threads) <= 3
    full, full_stats = solve_core(branches, threads)
    assert full is None
    per_thread = {}
    for tid in range(len(threads)):
        assignment, stats = solve_core(branches, threads, omitted=tid)
        assert assignment is not None
        per_thread[tid] = (assignment, stats)
    witnesses = {}
    for eid in range(len(arcs)):
        tid, pos = edge_location[eid]
        assignment, _ = per_thread[tid]
        witnesses[str(eid)] = lift(n, arcs, threads, assignment, tid, pos)
    # Exact theorem check: every omitted-thread assignment violates its relation.
    complement_check = []
    for tid, (assignment, _) in per_thread.items():
        t = threads[tid]
        delta = (assignment[t["path"][-1]] - assignment[t["path"][0]]) % 5
        assert delta not in t["allowed_diffs"]
        complement_check.append(delta)
    out = {
        "source": {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "n": n,
            "m": len(arcs),
        },
        "path_formula": verify_path_formula(),
        "core": {
            "branch_vertices": len(branches),
            "threads": len(threads),
            "thread_length_histogram": dict(sorted(Counter(
                len(t["edge_ids"]) for t in threads
            ).items())),
            "full_unsat": True,
            "full_solver_stats": full_stats,
            "omitted_thread_searches": len(per_thread),
            "candidate_space_upper_bounds": [
                (4 - len(threads[i]["edge_ids"])) * (5 ** (len(branches) - 2))
                for i in range(len(threads))
            ],
            "nodes_by_thread": [per_thread[i][1]["nodes"] for i in range(len(threads))],
            "max_nodes": max(x[1]["nodes"] for x in per_thread.values()),
            "total_nodes": sum(x[1]["nodes"] for x in per_thread.values()),
            "omitted_endpoint_differences": complement_check,
        },
        "lifting": {
            "original_edge_deletions_verified": len(witnesses),
            "distinct_core_searches": len(per_thread),
            "fivefold_rotation_fixed": True,
            "canonical_lexicographic_internal_fill": True,
            "witnesses": witnesses,
        },
        "scope": (
            "Exact exhaustive path-language check; independent AC/DFS and canonical "
            "lifting on one authenticated 33-vertex obstruction. Finite instance "
            "evidence is not an asymptotic runtime lower or upper bound."
        ),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
