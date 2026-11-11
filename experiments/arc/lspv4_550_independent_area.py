#!/usr/bin/env python3
"""LSPV-4/550: independent shortest-area audit on exact 60-step /549 DAG.
Pinned parent incidence and canonical clause lengths are transcribed from the
original /549 accepted-style packet, NOT derived from the JS auditor.
This verifies a finite fixed-DAG resource statement, not R_mix341 or P != NP.
"""
import json
import time
from collections import deque

P = [[],[],[],[],[],[3],[2],[1],[0],[5,8],[4],[],[11],[7,10],[],
     [14],[15,12],[],[9],[13],[16],[19,20],[17],[6,22],[23],
     [18,24],[25],[21],[27,26],[],[],[],[],[29],[32],[34,33],
     [31],[],[37],[38,36],[],[40],[35],[39],[42,43],[],[45],
     [46,41],[30],[],[49],[50,48],[47],[51],[52,53],[54],
     [44],[56,55],[57,28],[58]]
W = [19,17,19,17,17,17,19,17,18,14,18,19,18,14,17,17,
     14,19,13,13,14,10,20,16,14,10,12,11,9,16,14,16,
     14,15,14,12,17,16,16,14,16,15,12,13,10,14,14,12,
     15,14,14,12,12,13,10,11,10,8,5,2]
N = len(P)
ALL = (1 << N) - 1
assert N == len(W) == 60
pred = [sum(1 << j for j in ps) for ps in P]
succ = [0] * N
for i, parents in enumerate(P):
    for j in parents:
        assert j < i
        succ[j] |= 1 << i

def retained(mask):
    unexecuted = ALL ^ mask
    return [j for j in range(N) if mask >> j & 1 and succ[j] & unexecuted]

start = time.perf_counter()
queue = deque([0])
best = {0: 0}
parent = {}
ready_transitions = 0
legal_transitions = 0
relaxations = 0
while queue:
    mask = queue.popleft()
    unexecuted = ALL ^ mask
    count = len(retained(mask))
    proposed_area = best[mask] + count
    for i in range(N):
        if mask >> i & 1 or pred[i] & unexecuted:
            continue
        ready_transitions += 1
        bit = 1 << i
        reuse = any((succ[j] & unexecuted) == bit and W[j] >= W[i]
                    for j in P[i])
        if count + (not reuse) > 5:
            continue
        legal_transitions += 1
        dest = mask | bit
        if dest not in best:
            best[dest] = proposed_area
            parent[dest] = (mask, i)
            queue.append(dest)
            relaxations += 1
        elif proposed_area < best[dest]:
            best[dest] = proposed_area
            parent[dest] = (mask, i)
            relaxations += 1

assert ALL in best
path = []
mask = ALL
while mask:
    old_mask, i = parent[mask]
    path.append(i)
    mask = old_mask
path.reverse()
assert len(path) == 60 and len(set(path)) == 60
assert best[ALL] == 156
assert len(best) == 1129302
assert ready_transitions == 12982502
assert legal_transitions == 4107280
print(json.dumps({
    "model": "60 fixed RES nodes; cap 5 nonexpanding last-use atomic overwrite",
    "minimum_retained_slot_steps": best[ALL],
    "reachable_downsets": len(best),
    "ready_transitions": ready_transitions,
    "legal_transitions": legal_transitions,
    "relaxations": relaxations,
    "minimum_area_schedule": path,
    "elapsed_seconds": round(time.perf_counter() - start, 3),
    "historical_R_mix341_authenticated": False
}, indent=2))
