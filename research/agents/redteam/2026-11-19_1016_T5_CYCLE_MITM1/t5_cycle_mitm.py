#!/usr/bin/env python3
"""Exact GF(5) cycle-space meet-in-the-middle finder for T5 deletions.

The input is an explicit oriented graph.  Degree-two threads are suppressed.
For each omitted thread, the surviving endpoint-increment choices are reduced
to a multi-choice subset-sum instance in the fundamental-cycle space.  Every
reported branch candidate is lifted and checked on the original arcs.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import resource
import time
from collections import Counter, deque
from pathlib import Path


def rel(a: int, b: int) -> bool:
    return (b - a) % 5 in (1, 3)


def parse(path: Path):
    raw = path.read_bytes()
    n = expected_m = None
    declared = set()
    arcs = []
    for line in raw.decode("ascii").splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "p":
            assert f[1] == "t5"
            n, expected_m = map(int, f[2:])
        elif f[0] == "v":
            declared.add(int(f[1]))
        elif f[0] == "a":
            arcs.append((int(f[1]), int(f[2])))
    assert n is not None and expected_m == len(arcs)
    assert declared == set(range(n))
    assert len(set(arcs)) == len(arcs)
    assert all(u != v for u, v in arcs)
    return raw, n, arcs


def path_diffs(word: str):
    length = len(word)
    backward = word.count("B")
    offset = length + backward
    return {(offset + 2 * j) % 5 for j in range(length + 1)}


def suppress(n, arcs):
    adj = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(arcs):
        adj[u].append(eid)
        adj[v].append(eid)
    branches = sorted(v for v in range(n) if len(adj[v]) != 2)
    branch_set = set(branches)
    seen = set()
    threads = []
    edge_location = {}
    for start in branches:
        for first_eid in adj[start]:
            if first_eid in seen:
                continue
            path = [start]
            edge_ids = []
            previous, eid = start, first_eid
            while True:
                assert eid not in seen
                seen.add(eid)
                edge_ids.append(eid)
                u, v = arcs[eid]
                nxt = v if u == previous else u
                path.append(nxt)
                if nxt in branch_set:
                    break
                choices = [x for x in adj[nxt] if x != eid]
                assert len(choices) == 1
                previous, eid = nxt, choices[0]
            word = "".join(
                "F" if arcs[e] == (path[i], path[i + 1]) else "B"
                for i, e in enumerate(edge_ids)
            )
            assert 1 <= len(word) <= 3
            tid = len(threads)
            threads.append({
                "path": path,
                "edge_ids": edge_ids,
                "word": word,
                "offset": (len(word) + word.count("B")) % 5,
                "domain": len(word) + 1,
                "allowed": sorted(path_diffs(word)),
            })
            for position, original_eid in enumerate(edge_ids):
                edge_location[original_eid] = (tid, position)
    assert seen == set(range(len(arcs)))
    return branches, threads, edge_location


def verify_full_core_unsat(branches, threads):
    """Independent five-domain AC/DFS check of the full compressed source."""
    index = {vertex: i for i, vertex in enumerate(branches)}
    constraints = []
    for thread in threads:
        constraints.append((
            index[thread["path"][0]],
            index[thread["path"][-1]],
            frozenset(thread["allowed"]),
        ))
    stats = {"nodes": 0, "value_trials": 0, "propagation_rounds": 0}

    def propagate(domains):
        while True:
            stats["propagation_rounds"] += 1
            changed = False
            for left, right, allowed in constraints:
                dl, dr = domains[left], domains[right]
                nl = {a for a in dl if any((b - a) % 5 in allowed for b in dr)}
                nr = {b for b in dr if any((b - a) % 5 in allowed for a in nl)}
                if not nl or not nr:
                    return None
                if nl != dl:
                    domains[left] = nl
                    changed = True
                if nr != dr:
                    domains[right] = nr
                    changed = True
            if not changed:
                return domains

    def dfs(domains):
        stats["nodes"] += 1
        domains = propagate([set(domain) for domain in domains])
        if domains is None:
            return None
        undecided = [i for i, domain in enumerate(domains) if len(domain) > 1]
        if not undecided:
            return [next(iter(domain)) for domain in domains]
        variable = min(undecided, key=lambda i: (len(domains[i]), i))
        for value in sorted(domains[variable]):
            stats["value_trials"] += 1
            child = [set(domain) for domain in domains]
            child[variable] = {value}
            answer = dfs(child)
            if answer is not None:
                return answer
        return None

    initial = [set(range(5)) for _ in branches]
    initial[0] = {0}
    answer = dfs(initial)
    assert answer is None
    return stats


def cycle_matrix(branches, threads, omitted):
    """Return surviving tids, a spanning tree, and a fundamental-cycle matrix."""
    surviving = [tid for tid in range(len(threads)) if tid != omitted]
    incident = {v: [] for v in branches}
    for tid in surviving:
        u, v = threads[tid]["path"][0], threads[tid]["path"][-1]
        incident[u].append((tid, v))
        incident[v].append((tid, u))

    root = branches[0]
    parent = {root: None}
    parent_tid = {}
    order = [root]
    queue = deque([root])
    tree_tids = set()
    while queue:
        u = queue.popleft()
        for tid, v in incident[u]:
            if v in parent:
                continue
            parent[v] = u
            parent_tid[v] = tid
            tree_tids.add(tid)
            order.append(v)
            queue.append(v)
    assert len(parent) == len(branches), "surviving branch core disconnected"

    pos = {tid: i for i, tid in enumerate(surviving)}
    q = len(surviving)
    potential = {root: [0] * q}
    for child in order[1:]:
        par = parent[child]
        tid = parent_tid[child]
        vec = potential[par].copy()
        left, right = threads[tid]["path"][0], threads[tid]["path"][-1]
        sign = 1 if (par, child) == (left, right) else -1
        vec[pos[tid]] = sign % 5
        potential[child] = vec

    non_tree = [tid for tid in surviving if tid not in tree_tids]
    rows = []
    for tid in non_tree:
        left, right = threads[tid]["path"][0], threads[tid]["path"][-1]
        # d_tid - (x_right - x_left) = 0.
        row = [
            ((1 if i == pos[tid] else 0)
             - potential[right][i] + potential[left][i]) % 5
            for i in range(q)
        ]
        rows.append(row)
    assert len(rows) == q - len(branches) + 1
    return surviving, tree_tids, parent, parent_tid, order, rows


def balanced_split(variables, domains):
    left, right = [], []
    lp = rp = 1
    for var in sorted(variables, key=lambda x: (-domains[x], x)):
        if lp <= rp:
            left.append(var)
            lp *= domains[var]
        else:
            right.append(var)
            rp *= domains[var]
    # Store the smaller side; enumeration time is symmetric.
    if lp > rp:
        left, right, lp, rp = right, left, rp, lp
    return left, right, lp, rp


def enumerate_store(variables, domains, columns, beta):
    table = {}
    syndrome = [0] * beta
    choices = [0] * len(variables)
    leaves = 0

    def rec(k):
        nonlocal leaves
        if k == len(variables):
            leaves += 1
            table.setdefault(bytes(syndrome), bytes(choices))
            return
        var = variables[k]
        col = columns[var]
        base = syndrome.copy()
        for value in range(domains[var]):
            choices[k] = value
            for r in range(beta):
                syndrome[r] = (base[r] + col[r] * value) % 5
            rec(k + 1)
        syndrome[:] = base

    rec(0)
    return table, leaves


def enumerate_match(variables, domains, columns, target, table, beta):
    syndrome = [0] * beta
    choices = [0] * len(variables)
    leaves = 0
    answer = None

    def rec(k):
        nonlocal leaves, answer
        if answer is not None:
            return
        if k == len(variables):
            leaves += 1
            need = bytes((target[r] - syndrome[r]) % 5 for r in range(beta))
            first = table.get(need)
            if first is not None:
                answer = (first, bytes(choices))
            return
        var = variables[k]
        col = columns[var]
        base = syndrome.copy()
        for value in range(domains[var]):
            choices[k] = value
            for r in range(beta):
                syndrome[r] = (base[r] + col[r] * value) % 5
            rec(k + 1)
            if answer is not None:
                break
        syndrome[:] = base

    rec(0)
    return answer, leaves


def solve_omission(branches, threads, omitted):
    start_time = time.perf_counter()
    (surviving, tree_tids, parent, parent_tid, order,
     rows) = cycle_matrix(branches, threads, omitted)
    beta = len(rows)
    q = len(surviving)
    domains = [threads[tid]["domain"] for tid in surviving]
    offsets = [threads[tid]["offset"] for tid in surviving]
    columns = [
        [2 * rows[r][i] % 5 for r in range(beta)]
        for i in range(q)
    ]
    target = [
        -sum(rows[r][i] * offsets[i] for i in range(q)) % 5
        for r in range(beta)
    ]
    active = [i for i in range(q) if any(columns[i])]
    inactive = [i for i in range(q) if not any(columns[i])]
    left, right, left_product, right_product = balanced_split(active, domains)
    table, stored_leaves = enumerate_store(left, domains, columns, beta)
    match, probed_leaves = enumerate_match(
        right, domains, columns, target, table, beta
    )
    assert match is not None
    first, second = match
    values = [0] * q
    for var, value in zip(left, first):
        values[var] = value
    for var, value in zip(right, second):
        values[var] = value
    for var in inactive:
        values[var] = 0
    diffs = [(offsets[i] + 2 * values[i]) % 5 for i in range(q)]
    for row in rows:
        assert sum(c * d for c, d in zip(row, diffs)) % 5 == 0

    diff_by_tid = {tid: diffs[i] for i, tid in enumerate(surviving)}
    colors = {order[0]: 0}
    for child in order[1:]:
        par = parent[child]
        tid = parent_tid[child]
        left_v, right_v = threads[tid]["path"][0], threads[tid]["path"][-1]
        d = diff_by_tid[tid]
        colors[child] = (colors[par] + d) % 5 if (par, child) == (left_v, right_v) else (colors[par] - d) % 5
    for tid in surviving:
        u, v = threads[tid]["path"][0], threads[tid]["path"][-1]
        assert (colors[v] - colors[u]) % 5 == diff_by_tid[tid]
        assert diff_by_tid[tid] in threads[tid]["allowed"]
    u, v = threads[omitted]["path"][0], threads[omitted]["path"][-1]
    omitted_diff = (colors[v] - colors[u]) % 5
    assert omitted_diff not in threads[omitted]["allowed"]
    return colors, {
        "cycle_rank_after_omission": beta,
        "surviving_threads": q,
        "active_choice_variables": len(active),
        "inactive_choice_variables": len(inactive),
        "full_choice_product": math.prod(domains),
        "stored_half_product": left_product,
        "probed_half_product": right_product,
        "stored_leaves": stored_leaves,
        "distinct_stored_syndromes": len(table),
        "probed_leaves_until_match": probed_leaves,
        "elapsed_seconds": time.perf_counter() - start_time,
        "omitted_endpoint_difference": omitted_diff,
        "choice_values": {str(tid): values[i] for i, tid in enumerate(surviving)},
    }


def path_ok(word, colors, skipped=None):
    for i, direction in enumerate(word):
        if i == skipped:
            continue
        a, b = colors[i], colors[i + 1]
        if direction == "F" and not rel(a, b):
            return False
        if direction == "B" and not rel(b, a):
            return False
    return True


def canonical_fill(word, left, right, skipped=None):
    for internal in itertools.product(range(5), repeat=max(0, len(word) - 1)):
        colors = (left,) + internal + (right,)
        if path_ok(word, colors, skipped):
            return colors
    return None


def lift_and_verify(n, arcs, threads, branch_colors, omitted_tid, omitted_pos):
    colors = [None] * n
    for vertex, color in branch_colors.items():
        colors[vertex] = color
    for tid, thread in enumerate(threads):
        path = thread["path"]
        skipped = omitted_pos if tid == omitted_tid else None
        fill = canonical_fill(
            thread["word"], colors[path[0]], colors[path[-1]], skipped
        )
        assert fill is not None
        for vertex, color in zip(path, fill):
            if colors[vertex] is not None:
                assert colors[vertex] == color
            colors[vertex] = color
    assert all(color is not None for color in colors)
    omitted_eid = threads[omitted_tid]["edge_ids"][omitted_pos]
    checks = 0
    for eid, (u, v) in enumerate(arcs):
        if eid == omitted_eid:
            assert not rel(colors[u], colors[v])
        else:
            assert rel(colors[u], colors[v])
            checks += 1
    return colors, checks


def main():
    overall_start = time.perf_counter()
    source = Path(__file__).with_name("source079.t5")
    raw, n, arcs = parse(source)
    branches, threads, edge_location = suppress(n, arcs)
    full_unsat_stats = verify_full_core_unsat(branches, threads)
    per_thread = {}
    per_edge = {}
    total_arc_checks = 0
    for omitted_tid, thread in enumerate(threads):
        branch_colors, stats = solve_omission(branches, threads, omitted_tid)
        witnesses = {}
        for position, original_eid in enumerate(thread["edge_ids"]):
            colors, checks = lift_and_verify(
                n, arcs, threads, branch_colors, omitted_tid, position
            )
            total_arc_checks += checks
            witnesses[str(original_eid)] = colors
            per_edge[str(original_eid)] = {
                "thread": omitted_tid,
                "position": position,
                "colors": colors,
            }
        per_thread[str(omitted_tid)] = {
            "length": len(thread["edge_ids"]),
            "word": thread["word"],
            "branch_colors": {str(k): v for k, v in sorted(branch_colors.items())},
            "stats": stats,
            "witnesses": witnesses,
        }
    assert set(map(int, per_edge)) == set(range(len(arcs)))
    payload = {
        "status": "COMPUTATIONAL_EXACT_FINITE_SOURCE",
        "source": str(source.name),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "vertices": n,
        "arcs": len(arcs),
        "branches": len(branches),
        "threads": len(threads),
        "thread_length_histogram": dict(sorted(Counter(
            len(t["edge_ids"]) for t in threads
        ).items())),
        "cycle_rank_full_core": len(threads) - len(branches) + 1,
        "full_core_unsat_AC_DFS": full_unsat_stats,
        "deletion_witnesses": len(per_edge),
        "retained_arc_checks": total_arc_checks,
        "maximum_stored_half_product": max(
            x["stats"]["stored_half_product"] for x in per_thread.values()
        ),
        "maximum_probed_half_product": max(
            x["stats"]["probed_half_product"] for x in per_thread.values()
        ),
        "maximum_actual_stored_leaves": max(
            x["stats"]["stored_leaves"] for x in per_thread.values()
        ),
        "total_actual_stored_leaves": sum(
            x["stats"]["stored_leaves"] for x in per_thread.values()
        ),
        "total_actual_probed_leaves": sum(
            x["stats"]["probed_leaves_until_match"] for x in per_thread.values()
        ),
        "elapsed_seconds": time.perf_counter() - overall_start,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "per_thread": per_thread,
        "per_edge": per_edge,
        "P_vs_NP": "OPEN",
    }
    output = Path(__file__).with_name("t5_cycle_mitm_results.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in payload.items()
                      if k not in ("per_thread", "per_edge")}, indent=2))


if __name__ == "__main__":
    main()
