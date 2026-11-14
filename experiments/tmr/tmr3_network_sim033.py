#!/usr/bin/env python3
"""TMR-3/029: independent finite tests for synchronous one-tape networks.

Tests a bounded local transition model. This is NOT a compiled physical single-tape
universal simulator, and does NOT establish the asymptotic simulation theorem.
"""
from __future__ import annotations
import copy
import json
import random
from collections import deque
from itertools import product


def graphs(k):
    return {
        'empty': set(),
        'line': {(i, i + 1) for i in range(k - 1)},
        'ring': {(i, (i + 1) % k) for i in range(k) if k > 1},
        'star': {(0, j) for j in range(1, k)} | {(j, 0) for j in range(1, k)},
        'complete': {(i, j) for i in range(k) for j in range(k) if i != j},
    }


def local_step(state, src, inbox_bit, tick, pid):
    # Deterministic sample of a one-work-tape program, one local tape read/write.
    cell = state['tape'].get(state['head'], 0)
    st = state['control']
    seen = src[state['readhead']] if state['readhead'] < len(src) else 0
    v = (cell ^ seen ^ inbox_bit ^ (st & 1) ^ (pid & 1)) & 1
    state['tape'][state['head']] = v
    state['control'] = (3 * st + 2 * seen + inbox_bit + v + 1) % 7
    state['head'] += (-1, 0, 1)[state['control'] % 3]
    if state['readhead'] < len(src) and (state['control'] % 2):
        state['readhead'] += 1
    # One-bit network output, copied to each outgoing edge during paid delivery.
    return (v ^ (state['control'] & 1)) & 1


def initial(k):
    return [dict(tape={0: i & 1}, head=0, readhead=0, control=i % 7) for i in range(k)]


def reference(src, k, edges, rounds):
    # Simultaneous round semantics using frozen snapshots and immutable outgoing list.
    states = initial(k)
    inboxes = [deque() for _ in range(k)]
    edge_index = sorted(edges)
    trace = []
    max_visited = sum(len(x['tape']) for x in states)
    for t in range(rounds):
        next_states = copy.deepcopy(states)
        old_inboxes = [deque(q) for q in inboxes]
        delivered = []
        for i in range(k):
            b = old_inboxes[i].popleft() if old_inboxes[i] else 0
            output = local_step(next_states[i], src, b, t, i)
            delivered.extend((j, output) for a, j in edge_index if a == i)
        inboxes = old_inboxes
        for j, bit in delivered:
            inboxes[j].append(bit)
        states = next_states
        max_visited = max(max_visited, sum(len(x['tape']) for x in states))
        trace.append((copy.deepcopy(states), [list(q) for q in inboxes]))
    return trace, max_visited


def serial(src, k, edges, rounds):
    # Independently arranged sequential processor loop, no snapshot of full states.
    st = initial(k)
    queues = [[] for _ in range(k)]
    outgoing = [[] for _ in range(k)]
    for a, b in edges:
        outgoing[a].append(b)
    for nbr in outgoing:
        nbr.sort()
    trace = []
    emitted = 0
    visited_peak = sum(len(x['tape']) for x in st)
    pending_peak = 0
    for t in range(rounds):
        phase = [[] for _ in range(k)]
        for i in range(k):
            input_bit = queues[i].pop(0) if queues[i] else 0
            output = local_step(st[i], src, input_bit, t, i)
            for j in outgoing[i]:
                phase[j].append(output)
                emitted += 1
        for j in range(k):
            queues[j].extend(phase[j])
        pending_peak = max(pending_peak, sum(len(q) for q in queues))
        visited_peak = max(visited_peak, sum(len(x['tape']) for x in st))
        trace.append((copy.deepcopy(st), copy.deepcopy(queues)))
    assert emitted == len(edges) * rounds
    return trace, visited_peak, pending_peak, emitted


def run():
    checks, cases, transmissions, max_queue = 0, 0, 0, 0
    by_shape = {}
    for k in range(1, 7):
        for shape, edges in graphs(k).items():
            for bits in product((0, 1), repeat=4):
                for rounds in (0, 1, 2, 3, 5, 8):
                    src = list(bits)
                    a, va = reference(src, k, edges, rounds)
                    b, vb, pq, sent = serial(src, k, edges, rounds)
                    assert a == b, (k, shape, bits, rounds)
                    # Each transition visits <= 1 new writable cell.
                    assert va <= k + k * rounds
                    assert vb <= k + k * rounds
                    assert pq <= len(edges) * rounds
                    assert sent == len(edges) * rounds
                    checks += 4
                    cases += 1
                    transmissions += sent
                    max_queue = max(max_queue, pq)
                    by_shape[shape] = by_shape.get(shape, 0) + 1
    rng = random.Random(20261114)
    randomized = 0
    for _ in range(300):
        k = rng.randint(1, 10)
        edges = {(i, j) for i in range(k) for j in range(k) if i != j and rng.random() < 0.35}
        src = [rng.randrange(2) for _ in range(rng.randint(0, 15))]
        rounds = rng.randint(0, 18)
        a, va = reference(src, k, edges, rounds)
        b, vb, pq, sent = serial(src, k, edges, rounds)
        assert a == b
        assert max(va, vb) <= k * (rounds + 1)
        assert pq <= len(edges) * rounds
        assert sent == len(edges) * rounds
        randomized += 1
        max_queue = max(max_queue, pq)
        checks += 4
    # Numerical illustration: a quadratic simulation cannot transfer alpha <= 2
    # into a superlinear bound on the network's aggregate charged budget.
    illustrative = []
    for alpha in (1.01, 1.99):
        illustrative.append({'one_tape_exponent': alpha,
                             'implied_aggregate_budget_exponent': round(alpha / 2, 4),
                             'strictly_above_input_length_exponent_1': alpha / 2 > 1})
    return dict(label='NETSIM33',status='COMPUTATIONAL',seed=20261114,
                exhaustive_cases=cases, randomized_cases=randomized,
                checks=checks,failed_assertions=0,by_shape=by_shape,
                total_message_transmissions=transmissions,
                largest_pending_queue=max_queue,
                numerical_exponent_controls=illustrative,
                limitations='Native Python semantic reference vs independent sequential implementation; no compiled one-tape universal-machine trace or clocked cost measurement; symbolic theorem has separate proof.')

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
