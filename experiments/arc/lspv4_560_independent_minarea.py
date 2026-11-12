#!/usr/bin/env python3
"""Independent forward-Dijkstra cumulative storage auditor for LSPV-4/560.

Run at repository root:
  python experiments/arc/lspv4_560_independent_minarea.py

Reads original and published signed /386 certificates. Original SOURCE and DEF
records are read-only. Every RES occurrence is executed exactly once. Logical
work and actual Python heap memory are distinct from abstract clause slots.
"""
from __future__ import annotations
import heapq
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json"
WITNESS = ROOT / "results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json"
OPTIMAL = ROOT / "results/raw/arc/2026-11-12_0436_LSPV4_560_W38_MINAREA_ACCEPTED.json"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def charged_graph(packet):
    records = packet["records"]
    paid = [i for i, r in enumerate(records) if r["kind"] == "RES"]
    reverse = {v: j for j, v in enumerate(paid)}
    parents = [[reverse[p] for p in records[v]["parents"] if p in reverse] for v in paid]
    sizes = [len(json.dumps(records[v]["c"], separators=(",", ":"), ensure_ascii=False)) for v in paid]
    return parents, sizes, paid

def exact_forward_dijkstra(parents, sizes, cap):
    n = len(parents)
    target = (1 << n) - 1
    successors = [0] * n
    pred_masks = []
    for j, ps in enumerate(parents):
        bitmask = 0
        for p in ps:
            bitmask |= 1 << p
            successors[p] |= 1 << j
        pred_masks.append(bitmask)
    best = {0: (0, 0)}
    previous = {}
    heap = [(0, 0, 0)]
    transitions = 0
    while heap:
        slot_area, byte_area, mask = heapq.heappop(heap)
        if (slot_area, byte_area) != best.get(mask):
            continue
        if mask == target:
            order = []
            while mask:
                before, v = previous[mask]
                order.append(v)
                mask = before
            return dict(slot_steps=slot_area, byte_steps=byte_area,
                        states=len(best), transitions=transitions,
                        schedule_paid_indices=list(reversed(order)))
        live = [j for j in range(n)
                if (mask >> j) & 1 and successors[j] & ~mask]
        live_bytes = sum(sizes[j] for j in live)
        for j in range(n):
            if ((mask >> j) & 1) or (pred_masks[j] & ~mask):
                continue
            # Reuse an output register only if a paid parent is last used,
            # and its canonical clause-array payload is no smaller.
            overwrite = any(
                not (successors[p] & ~(mask | (1 << j)))
                and sizes[p] >= sizes[j] for p in parents[j]
            )
            if len(live) + 1 - int(overwrite) > cap:
                continue
            transitions += 1
            nxt = mask | (1 << j)
            candidate = (slot_area + len(live), byte_area + live_bytes)
            if nxt not in best or candidate < best[nxt]:
                best[nxt] = candidate
                previous[nxt] = (mask, j)
                heapq.heappush(heap, (*candidate, nxt))
    return dict(infeasible=True, states=len(best), transitions=transitions)

def check_grammar_and_construction(original, new):
    assert new["spec"] == original["spec"]
    assert new["gate_defs"] == original["gate_defs"]
    assert len(new["records"]) == len(original["records"]) + 1
    for i in range(23):
        assert new["records"][i] == original["records"][i]
    assert new["records"][23]["c"] == [-4, -5, -7, -8]
    assert new["records"][29] == dict(kind="RES", c=[-1,-4,-5,-7],
                                     parents=[22,23], pivot=8)
    assert new["records"][31]["parents"][0] == 29
    assert all(new["records"][j]["kind"] == "RES" for j in range(23, 58))
    assert new["summary"] == dict(source=17, resolution=35, def_views=6,
                                  paid_gates=3, paid_total=38, live_records=58)
    # Confirm original SOURCE is not semantically identical to the shared lemma.
    assert not any(r["kind"]=="SOURCE" and r["c"]==new["records"][23]["c"]
                   for r in new["records"])

def main():
    base, new, opt = load(SOURCE), load(WITNESS), load(OPTIMAL)
    check_grammar_and_construction(base, new)
    from collections import Counter
    def signatures(packet):
        return Counter((r["kind"], tuple(r["c"]), r.get("pivot"),
                        r.get("source"), r.get("gate")) for r in packet["records"])
    assert signatures(new) == signatures(opt), "reordered evidence changed an inference"
    assert len(new["records"]) == len(opt["records"]) == 58
    for i, r in enumerate(opt["records"]):
        assert all(0 <= parent < i for parent in r["parents"]), "forward parent"
    output = {}
    for label, packet in [("base_571", base), ("new_560", new)]:
        parents, sizes, paid = charged_graph(packet)
        output[label] = {str(cap):exact_forward_dijkstra(parents,sizes,cap)
                         for cap in (3,4,5)}
        assert len(paid) == (34 if label=="base_571" else 35)
    assert (output["base_571"]["4"]["slot_steps"], output["base_571"]["4"]["byte_steps"]) == (66,700)
    assert output["new_560"]["3"].get("infeasible") is True
    assert (output["new_560"]["4"]["slot_steps"],output["new_560"]["4"]["byte_steps"]) == (82,883)
    assert (output["new_560"]["5"]["slot_steps"],output["new_560"]["5"]["byte_steps"]) == (82,883)
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
