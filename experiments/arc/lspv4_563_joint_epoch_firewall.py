#!/usr/bin/env python3
"""LSPV-4/563: same-realization comparison of pre-step and post-step
storage costs on the pinned, source-sound archived-/386 proof DAG.
Run: python3 experiments/arc/lspv4_563_joint_epoch_firewall.py
No external dependencies. Entire fixed order-ideal state space is searched.
This is NOT a historical R_mix341 or a SAT lower-bound calculation.
"""
import heapq
import json

PARENTS = [
 [],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
 [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
 [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]]
SIZES = [
 13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
 14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2]
N = len(PARENTS)
assert N == len(SIZES) == 35
SUCC = [0] * N
PRED = [sum(1 << p for p in ps) for ps in PARENTS]
for j, ps in enumerate(PARENTS):
    for p in ps:
        SUCC[p] |= 1 << j
assert [i for i, v in enumerate(SUCC) if not v] == [34]
GOAL = (1 << N) - 1

def solve(primary="slot", cap=4):
    """No-recomputation, all topological orders, exact nonexpanding overwrite.
    Charge L(D) before each paid step, and convert to the same post-step
    convention used by LSPV-4/562 (last empty-sink value retained once).
    """
    assert primary in ("slot", "byte")
    best = {0: (0, 0)}
    previous = {}
    heap = [(0, 0, 0)]
    edges = 0
    while heap:
        a, b, mask = heapq.heappop(heap)
        if best.get(mask) != (a, b):
            continue
        if mask == GOAL:
            order = []
            cursor = mask
            while cursor:
                old, j = previous[cursor]
                order.append(j)
                cursor = old
            order.reverse()
            pre_slot, pre_byte = (a, b) if primary == "slot" else (b, a)
            return {
                "primary": primary, "states": len(best), "transitions": edges,
                "paid_resolution_executions": len(order),
                "pre_step_slot_steps": pre_slot,
                "pre_step_clause_byte_steps": pre_byte,
                "post_step_slot_steps": pre_slot + 1,
                "post_step_clause_byte_steps": pre_byte + SIZES[34],
                "order": order
            }
        live = [i for i in range(N) if (mask >> i) & 1 and SUCC[i] & ~mask]
        live_byte = sum(SIZES[i] for i in live)
        for j, ps in enumerate(PARENTS):
            if (mask >> j) & 1 or PRED[j] & ~mask:
                continue
            overwrite = any(
                not (SUCC[p] & ~(mask | (1 << j))) and SIZES[p] >= SIZES[j]
                for p in ps)
            if len(live) + 1 - int(overwrite) > cap:
                continue
            edges += 1
            next_mask = mask | (1 << j)
            c = (a + len(live), b + live_byte) if primary == "slot" else (
                a + live_byte, b + len(live))
            if c < best.get(next_mask, (10**15, 10**15)):
                best[next_mask] = c
                previous[next_mask] = (mask, j)
                heapq.heappush(heap, (*c, next_mask))
    raise AssertionError("Unreachable terminal")

def verify_recompute_trace(trace, residents):
    """Independent resident-set audit of the /562 36-execution witness.
    No knowledge of the original Dijkstra implementation is used."""
    assert len(trace) == len(residents) == 36
    assert sorted(set(trace)) == list(range(N))
    assert trace.count(0) == 2
    old = set()
    slot_area = byte_area = 0
    for t, (j, row) in enumerate(zip(trace, residents)):
        post = set(row)
        assert len(post) == len(row)
        assert j in post and len(post) <= 4
        assert set(PARENTS[j]) <= old, ("parent missing", t, j)
        keep = post - {j}
        assert keep <= old, ("unearned result", t, j)
        pre = keep | set(PARENTS[j])
        assert len(pre) <= 4
        if len(pre) == 4:
            assert any(p not in keep and SIZES[p] >= SIZES[j]
                       for p in PARENTS[j]), ("overwrite invalid", t, j)
        slot_area += len(post)
        byte_area += sum(SIZES[p] for p in post)
        old = post
    assert old == {34}
    return {"steps": len(trace), "distinct_paid_nodes": len(set(trace)),
            "recomputed_node": 0, "slot_steps": slot_area,
            "clause_byte_steps": byte_area}

# Published fixed W39 /562 trace and post-execution residents, independently rechecked.
TRACE = [0,1,2,3,4,5,10,15,14,22,26,27,7,19,11,16,25,30,32,0,
         6,8,20,13,18,24,29,12,21,9,17,23,28,31,33,34]
RESIDENTS = [
 [0],[1],[2],[3],[4],[5],[10],[15],[14,15],[15,22],[26],
 [27],[7,27],[19,27],[11,19,27],[16,19,27],[25,27],
 [27,30],[32],[0,32],[6,32],[8,32],[20,32],[13,20,32],
 [18,20,32],[24,32],[29,32],[12,29,32],[21,29,32],
 [9,21,29,32],[17,21,29,32],[23,29,32],[28,29,32],
 [31,32],[33],[34]]

if __name__ == "__main__":
    a = solve("slot")
    b = solve("byte")
    assert (a["pre_step_slot_steps"], a["pre_step_clause_byte_steps"]) == (82, 883)
    assert (b["pre_step_slot_steps"], b["pre_step_clause_byte_steps"]) == (82, 883)
    assert (a["post_step_slot_steps"], a["post_step_clause_byte_steps"]) == (83, 885)
    v = verify_recompute_trace(TRACE, RESIDENTS)
    assert (v["slot_steps"], v["clause_byte_steps"]) == (71, 748)
    result = {
        "status": "COMPUTATIONAL with exact finite-state recurrence and proof",
        "model": "archived /386 fixed shared signed Resolution DAG; 4 nonexpanding slots",
        "no_recompute_slot_first": a, "no_recompute_byte_first": b,
        "recompute_witness": v,
        "joint_cost_vectors_post_step": {
            "unique_once": [38, 83, 885],
            "one_recompute": [39, 71, 748]},
        "relative_improvement_post_step": {
            "slot": (83 - 71) / 83, "byte": (885 - 748) / 885},
        "main_chain": "P2-D1 -> P2-C3 -> P2-B1 OPEN"
    }
    print(json.dumps(result, indent=2))
