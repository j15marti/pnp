#!/usr/bin/env python3
"""LSPV-4/574: exact packed semantic-value retention on the original /341 trees.

Run from the j15marti/pnp checkout root:
  python3 experiments/arc/lspv4_574_native341_packed_semantic_area.py
Only Python's standard library is needed. Original checkers/rule weights are NOT changed.
This is a restricted derived-value storage proxy, not verifier RAM or full R_mix341.
"""
import hashlib
import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
PRIOR = ROOT / "results/raw/arc/2026-11-12_1736_LSPV4_573_NATIVE341_WEIGHTED_RECORD_AREA_RAW.json"
PIN = "fe27fe1011d0021e721ccaeb747ed58da65d7464"
EXPECTED = {"K4": 40, "K33": 88, "CUBE": 120,
            "PETERSEN": 198, "PRISM6": 240, "PRISM16": 1346,
            "BRIDGE_K4x2": 198}


def source_check(f):
    """Check all original 3-local AND truth tables, affine aliases and XOR rows."""
    p = f["proof"]
    clauses = {c["id"]: c for c in f["clauses"]}
    by_id = {x["id"]: x for x in p}
    h = f["graph"]["n"]
    e = len(f["graph"]["edges"])
    assert len(p) == 4 * h - 1
    assert len(clauses) == 4 * h
    assert all(x["id"] == f"d{i}" for i, x in enumerate(p))
    asserts = 0
    for i, x in enumerate(p):
        if i < 3 * h:
            assert x["rule"] == "AND3"
            assert x["kind"] == "factor"
            v, k = divmod(i, 3)
            expected_parents = ([f"s{4*v}", f"s{4*v+1}"] if k == 0 else
                                ([f"d{i-1}", f"s{4*v+2}"] if k == 1 else
                                 [f"d{i-1}", f"s{4*v+3}"]))
            assert x["parents"] == expected_parents
            support = x["support"]
            assert len(support) == len(set(support)) == 3
            assert all(type(z) is int and 0 <= z < e for z in support)
            table = 0
            for assignment in range(8):
                def value(parent):
                    if parent in clauses:
                        c = clauses[parent]
                        return any(((assignment >> support.index(abs(l)-1)) & 1) ==
                                   (1 if l > 0 else 0) for l in c["literals"])
                    old = by_id[parent]
                    assert old["support"] == support
                    return bool((old["table"] >> assignment) & 1)
                if all(value(a) for a in x["parents"]):
                    table |= (1 << assignment)
                asserts += 2
            assert table == x["table"], (f["graph"]["name"], x["id"])
            if k == 2:
                r = x["row"]
                mask = int(r["mask"], 16)
                assert mask < (1 << e)
                for a in range(8):
                    bits = sum((a >> j & 1) for j, z in enumerate(support)
                               if (mask >> z) & 1)
                    assert ((x["table"] >> a) & 1) == (bits % 2 == r["rhs"])
                    asserts += 1
            else:
                assert "row" not in x
        else:
            assert x["rule"] == "XOR" and x["kind"] == "affine"
            j = i - 3 * h
            assert x["parents"] == ([f"d2", "d5"] if j == 0 else
                                    [f"d{i-1}", f"d{3*(j+1)+2}"])
            left, right = (by_id[a]["row"] for a in x["parents"])
            assert int(x["row"]["mask"], 16) == (int(left["mask"], 16) ^
                                                  int(right["mask"], 16))
            assert x["row"]["rhs"] == (left["rhs"] ^ right["rhs"])
            asserts += 2
    assert int(p[-1]["row"]["mask"], 16) == 0
    assert p[-1]["row"]["rhs"] == 1
    return asserts


def packed_weights(f):
    """One tag bit; factor = 8-table bits + 3 indices; row = E coefficients + rhs."""
    e = len(f["graph"]["edges"])
    b = (e - 1).bit_length()
    fbytes, rbytes = (9 + 3*b + 7)//8, (e + 2 + 7)//8
    weights = []
    for node in f["proof"]:
        if "row" in node:
            rhs, mask = node["row"]["rhs"], int(node["row"]["mask"], 16)
            assert rhs in (0, 1) and 0 <= mask < (1 << e)
            payload = 1 | (rhs << 1) | (mask << 2)
            assert (payload & 1) == 1
            assert ((payload >> 1) & 1) == rhs
            assert ((payload >> 2) & ((1 << e)-1)) == mask
            assert payload.bit_length() <= 2 + e
            weights.append(rbytes)
        else:
            support, table = node["support"], node["table"]
            assert 0 <= table <= 255
            payload = table << 1
            for j, z in enumerate(support):
                payload |= z << (9+j*b)
            assert (payload & 1) == 0
            assert ((payload >> 1) & 255) == table
            assert [((payload >> (9+j*b)) & ((1 << b)-1))
                    for j in range(3)] == support
            assert payload.bit_length() <= 9 + 3*b
            weights.append(fbytes)
    return weights, fbytes, rbytes


def exact_dp(f, weights):
    """Exact no-recomputation post-step frontier with <=2 live paid results."""
    p = f["proof"]
    n = len(p)
    ix = {x["id"]:i for i, x in enumerate(p)}
    pred = [sum(1 << ix[x] for x in rec["parents"] if x in ix) for rec in p]
    succ = [0]*n
    for i, m in enumerate(pred):
        while m:
            bit = m & -m
            succ[bit.bit_length()-1] |= 1 << i
            m -= bit

    def live(mask):
        slots = cost = 0
        for i in range(n):
            if (mask >> i) & 1 and (succ[i] == 0 or
                                   (succ[i] & mask) != succ[i]):
                slots += 1
                cost += weights[i]
        return slots, cost

    q = deque([0])
    cost = {0: 0}
    path = {0: ()}
    edges = 0
    while q:
        mask = q.popleft()
        for i in range(n):
            bit = 1 << i
            if mask & bit or pred[i] & mask != pred[i]:
                continue
            nxt = mask | bit
            k, w = live(nxt)
            if k > 2:
                continue
            edges += 1
            candidate = cost[mask] + w
            if nxt not in cost:
                cost[nxt] = candidate
                path[nxt] = path[mask] + (i,)
                q.append(nxt)
            elif candidate < cost[nxt]:
                cost[nxt] = candidate
                path[nxt] = path[mask] + (i,)

    complete = (1 << n) - 1
    assert complete in cost

    def score(order):
        mask = 0
        area = slot_area = peak = 0
        for i in order:
            assert (mask & 1 << i) == 0 and pred[i] & mask == pred[i]
            slots, before = live(mask)
            peak = max(peak, before + weights[i])  # fresh result before releases
            mask |= 1 << i
            slots, after = live(mask)
            assert slots <= 2
            area += after
            slot_area += slots
        assert mask == complete
        return {"area": area, "slot_area": slot_area,
                "fresh_output_payload_peak": peak}

    return {"states": len(cost), "edges": edges,
            "optimum": score(path[complete]),
            "optimal_order": [p[i]["id"] for i in path[complete]],
            "score": score, "index": ix}


def main():
    data = SOURCE.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() +
                        b"\0" + data).hexdigest()
    assert blob == PIN, blob
    fixtures = json.loads(data)["fixtures"]
    earlier = {x["fixture"]:x for x in json.loads(PRIOR.read_text())["fixtures"]}
    rows = []
    for f in fixtures:
        name = f["graph"]["name"]
        e, v = len(f["graph"]["edges"]), f["graph"]["n"]
        semantic = source_check(f)
        weights, factor, row = packed_weights(f)
        state = exact_dp(f, weights)
        out = state["optimum"]
        original_order = [state["index"][id] for id in
                          earlier[name]["optimal_order_paid_node_ids"]]
        prior_score = state["score"](original_order)
        formula = 2*factor*v + (5*v-4)*row - max(0, 2*row-3*factor)
        peak_formula = max(row+2*factor, factor+2*row, 3*row)
        assert out["area"] == formula == EXPECTED[name]
        assert out["fresh_output_payload_peak"] == peak_formula
        assert out["slot_area"] == 7*v-4
        assert state["states"] == earlier[name]["reachable_order_ideals"]
        assert state["edges"] == earlier[name]["admissible_transitions"]
        rows.append({"fixture": name, "vertices":v, "edges":e,
                     "paid":4*v-1, "parent_applications":2*(4*v-1),
                     "factor_bytes":factor, "row_bytes":row,
                     "original_full_record_area":
                         earlier[name]["byte_weighted_optimum"]
                                       ["post_step_retained_record_byte_steps"],
                     "packed_optimum":out,
                     "packed_area_at_prior_optimum":prior_score["area"],
                     "packed_formula":formula, "peak_formula":peak_formula,
                     "states":state["states"], "transitions":state["edges"],
                     "semantic_assertions":semantic,
                     "optimal_order":state["optimal_order"]})
    assert sum(x["paid"] for x in rows) == 321
    assert sum(x["parent_applications"] for x in rows) == 642
    print(json.dumps({"tag":"LSPV-4/574", "authority_blob":blob,
          "scope":"original seven separate archived /341 fixed paid trees",
          "model":"two live atomic packed semantic-value slots, input proof read-only, no recomputation; packed payload only",
          "warning":"NOT physical RAM, not full historical R_mix341, not all-proof lower bound",
          "status":"PROVED/RESTRICTED model theorem and independently auditable finite data",
          "rows":rows, "P2_D1":"OPEN", "P2_C3":"OPEN", "P2_B1":"OPEN",
          "P_vs_NP":"OPEN"}, indent=2))


if __name__ == "__main__":
    main()
