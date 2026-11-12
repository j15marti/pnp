#!/usr/bin/env python3
"""LSPV-4/559 independent exact order-ideal DP for original /386 W37 packet.
Arrays extracted from LSPV-2/571, with native legal record[30] parent[0] 7 -> 28.
No third-party dependencies. This audit is independent of the JavaScript implementation.
"""
import json

SHARED_DEPS = [
    [],[0],[1],[2],[3],[4],[],[5],[],[5],[],[],[],[],
    [9],[10],[8],[12],[6],[7],[11],[13],[20,16],[19,17],
    [15,18],[14,21],[25],[22],[23],[24],[28,27],[26,29],[30,31],[32]
]
LENGTHS = [
    13,13,14,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
    14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2
]

def exact_search(deps, cap=4, mode='nonexpand'):
    n = len(deps)
    prerequisites = [sum(1 << p for p in row) for row in deps]
    children = [0] * n
    for v, row in enumerate(deps):
        for parent in row:
            children[parent] |= 1 << v
    layers = [{0: (0, 0, ())}] + [{} for _ in range(n)]
    states = transitions = 0
    for level in range(n):
        for state, (area, byte_area, history) in layers[level].items():
            states += 1
            live = [u for u in range(n) if state & (1 << u) and children[u] & ~state]
            footprint = len(live)
            payload = sum(LENGTHS[u] for u in live)
            for v in range(n):
                bit = 1 << v
                if state & bit or state & prerequisites[v] != prerequisites[v]:
                    continue
                reuse = mode != 'fresh' and any(
                    (children[p] & ~state) == bit and
                    (mode == 'inplace' or LENGTHS[p] >= LENGTHS[v])
                    for p in deps[v]
                )
                if footprint + 1 - int(reuse) > cap:
                    continue
                transitions += 1
                next_state = state | bit
                candidate = (area + footprint, byte_area + payload, history + (v + 23,))
                previous = layers[level + 1].get(next_state)
                if previous is None or candidate[:2] < previous[:2]:
                    layers[level + 1][next_state] = candidate
    goal = layers[n].get((1 << n) - 1)
    result = {'cap': cap, 'mode': mode, 'states': states,
              'arcs': transitions, 'feasible': goal is not None}
    if goal is not None:
        result.update(area=goal[0], byte_area=goal[1], order=list(goal[2]))
    return result

def main():
    previous = [d[:] for d in SHARED_DEPS]
    previous[30 - 23] = []
    models = [('fresh',4),('fresh',5),('inplace',3),('inplace',4),
              ('nonexpand',3),('nonexpand',4),('nonexpand',5)]
    out = {'previous': exact_search(previous),
           'shared': [exact_search(SHARED_DEPS, cap, mode) for mode,cap in models],
           'unconstrained': exact_search(SHARED_DEPS, 34, 'fresh')}
    assert (out['previous']['area'],out['previous']['byte_area']) == (66,700)
    assert [r['feasible'] for r in out['shared']] == [False,True,False,True,False,True,True]
    assert (out['shared'][5]['area'],out['shared'][5]['byte_area']) == (79,839)
    assert (out['unconstrained']['area'],out['unconstrained']['byte_area']) == (79,837)
    print(json.dumps({'status':'PASS',**out},indent=2))

if __name__=='__main__':
    main()
