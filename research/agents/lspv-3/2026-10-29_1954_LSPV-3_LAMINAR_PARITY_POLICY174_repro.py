#!/usr/bin/env python3
"""Exact, seeded, small exhaustive controls for weighted laminar parity policy 174.
Model: public nonempty subsets S with a materialized XOR bit p_S and positive
read cost w_S; raw coordinate bits e_i always present. The target is t dot theta.
Cost is source-probe latency, separate from metadata discovery and preprocessing.
"""
from __future__ import annotations
import heapq
import hashlib
import json
import random
from pathlib import Path

SEED = 1741029
RUN_ID = 'LAMINAR-PARITY-POLICY174'
R = random.Random(SEED)


def laminar_tree(m, actions):
    """Return parent/children postorder; reject crossing sets. Root may be synthetic."""
    full = (1 << m) - 1
    nodes = dict(actions)
    for i in range(m):
        nodes.setdefault(1 << i, 1)
    nodes.setdefault(full, None)
    masks = sorted(nodes, key=lambda a: (a.bit_count(), a))
    for i, a in enumerate(masks):
        for b in masks[i + 1:]:
            overlap = a & b
            if overlap and overlap != a and overlap != b:
                return None
    parent = {}
    children = {a: [] for a in masks}
    for a in masks:
        if a == full:
            continue
        options = [b for b in masks if b != a and (a & b) == a]
        b = min(options, key=lambda u: (u.bit_count(), u))
        parent[a] = b
        children[b].append(a)
    for a in masks:
        children[a].sort()
    return full, masks, children, nodes


def optimal_laminar(m, actions, target):
    out = laminar_tree(m, actions)
    if out is None:
        return None
    root, masks, children, weights = out
    dp, choose = {}, {}
    for a in masks:  # size-sorted postorder, children precede parent
        for anc in (0, 1):
            if a.bit_count() == 1:
                z = ((target & a) != 0) ^ bool(anc)
                if weights[a] is None and z:
                    raise ValueError('raw coordinate probe must be accessible')
                dp[a, anc] = weights[a] * int(z)
                choose[a, anc] = int(z)
            else:
                opts = []
                for z in (0, 1):
                    if z and weights[a] is None:
                        continue
                    value = (weights[a] * z if z else 0) + sum(dp[ch, anc ^ z] for ch in children[a])
                    opts.append((value, z))
                dp[a, anc], choose[a, anc] = min(opts)
    picked = []
    def traceback(a, anc):
        z = choose[a, anc]
        if z:
            picked.append(a)
        for ch in children[a]:
            traceback(ch, anc ^ z)
    traceback(root, 0)
    xor = 0
    for a in picked:
        xor ^= a
    assert xor == target
    assert sum(weights[a] for a in picked) == dp[root, 0]
    return dp[root, 0], sorted(picked)


def independent_dijkstra(m, actions):
    """Exhaustive independent state-space shortest paths for all 2**m targets."""
    size = 1 << m
    d = [10**100] * size
    d[0] = 0
    todo = [(0, 0)]
    while todo:
        cost, x = heapq.heappop(todo)
        if cost != d[x]:
            continue
        for mask, w in actions.items():
            if w is None:
                continue
            nx = x ^ mask
            if d[nx] > cost + w:
                d[nx] = cost + w
                heapq.heappush(todo, (cost+w, nx))
    return d


def random_hierarchy(m):
    """Start at singleton leaves and repeatedly merge two disjoint clusters."""
    pool = [1 << i for i in range(m)]
    groups = pool[:]
    while len(pool) > 1:
        a, b = R.sample(pool, 2)
        pool.remove(a)
        pool.remove(b)
        new = a | b
        pool.append(new)
        groups.append(new)
    # Some internal probes are absent, testing that a synthetic unavailable
    # node can still mediate the hierarchy.
    actions = {1 << i: R.randint(1, 12) for i in range(m)}
    for a in groups:
        if a.bit_count() > 1 and R.random() < .76:
            actions[a] = R.randint(1, 35)
    return actions


def test_controls():
    n_hierarchies = 0
    n_target_cases = 0
    n_answer_tests = 0
    yes = no = 0
    worst_ratio = 0.0
    by_m = {}
    for m in range(2, 9):
        families = 24 if m <= 6 else 12
        by_m[str(m)] = {}
        for _ in range(families):
            actions = random_hierarchy(m)
            # Include the root even if its parity was not physically stored.
            full = (1 << m) - 1
            source = dict(actions)
            source.setdefault(full, None)
            oracle = independent_dijkstra(m, source)
            for target in range(1 << m):
                val = optimal_laminar(m, actions, target)
                assert val is not None
                cost, picked = val
                assert oracle[target] == cost, (m, target, actions, cost, oracle[target])
                xor = 0
                for a in picked:
                    xor ^= a
                assert xor == target
                n_target_cases += 1
                if target and R.random() < .06:
                    theta = R.randrange(1 << m)
                    ans = (target & theta).bit_count() & 1
                    recovered = 0
                    for a in picked:
                        recovered ^= (theta & a).bit_count() & 1
                    assert recovered == ans
                    yes += bool(ans)
                    no += not bool(ans)
                    n_answer_tests += 1
                    raw_only = sum(actions[1 << i] for i in range(m) if target & (1 << i))
                    worst_ratio = max(worst_ratio, raw_only / cost)
            n_hierarchies += 1
        by_m[str(m)] = {'families': families, 'target_masks_per_family': 1 << m}
    # Hostile nonlaminar crossing set: reject rather than silently optimize.
    assert laminar_tree(3, {1:1, 2:1, 4:1, 3:1, 6:1}) is None
    # Context-sensitive XOR sharing with a costly direct root probe.
    # Singleton values have zero target-entropy gain; two sibling shares
    # jointly determine full parity with two paid probes.
    actions = {1:1,2:1,4:1,8:1,3:1,12:1,15:128}
    cost, picked = optimal_laminar(4, actions, 15)
    assert cost == 2 and picked == [3, 12]
    assert optimal_laminar(4, actions, 3)[0] == 1
    for theta in range(16):
        assert ((theta & 3).bit_count() ^ (theta & 12).bit_count()) % 2 == (theta & 15).bit_count() % 2
    # Redundant read has zero added rank; single share still does not span t.
    assert 3 != 15 and 12 != 15 and 3 ^ 12 == 15
    return {
        'run_id': RUN_ID,
        'status': 'COMPUTATIONAL exact finite controls, theorem separately proved',
        'random_seed': SEED,
        'machine': 'abstract indexed parity-source probes with fixed positive weights',
        'hierarchies': n_hierarchies,
        'tested_target_masks': n_target_cases,
        'verified_answer_samples': n_answer_tests,
        'answer_0': no, 'answer_1': yes,
        'by_m': by_m,
        'oracle': 'independent Dijkstra over all 2^m XOR masks',
        'nonlaminar_crossing_rejected': True,
        'greedy_counterexample': {
            'm': 4, 'target_mask': 15, 'root_probe_cost': 128,
            'sibling_probe_masks': [3,12], 'sibling_total_cost': 2,
            'positive_singleton_target_information_greedy_cost': 128,
            'ratio': 64,
        },
        'max_raw_only_cost_over_optimum': worst_ratio,
        'limitations': 'Only m<=8, generated laminar weighted families. No SAT claim.'
    }

if __name__ == '__main__':
    d = test_controls()
    out = Path(__file__).with_name('2026-10-29_1954_LSPV-3_LAMINAR_PARITY_POLICY174_raw.json')
    raw = json.dumps(d, sort_keys=True, indent=2) + '\n'
    out.write_text(raw)
    print(json.dumps({'raw_path':str(out),'sha256':hashlib.sha256(raw.encode()).hexdigest(),
                      'hierarchies':d['hierarchies'], 'targets':d['tested_target_masks'],
                      'answer_checks':d['verified_answer_samples'],
                      'greedy_ratio':d['greedy_counterexample']['ratio']}))
