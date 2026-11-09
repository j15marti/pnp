#!/usr/bin/env python3
"""Independent replay of the proposed ownerized /449 adapter artifact."""

import json
import sys


def norm(xs):
    if 0 in xs or any(-x in xs for x in xs):
        raise AssertionError("bad clause")
    return sorted(set(xs), key=lambda z: (abs(z), z < 0))


def main(path):
    d = json.load(open(path, encoding="utf-8"))
    assert d["status"] == "PASS"
    p = d["proposed_ownerized_packet"]
    lines = {}
    for s in p["original_sources"]:
        assert s["line_id"] not in lines
        lines[s["line_id"]] = norm(s["clause"])
    assert len(lines) == 8
    outputs = set()
    facets = 0
    for gate in p["defs"]:
        q, a, b = gate["output"], gate["left_lit"], gate["right_lit"]
        assert abs(a) != abs(b) and q not in outputs and q > max(abs(a), abs(b))
        outputs.add(q)
        expected = {"left": norm([a, -q]), "right": norm([b, -q]), "back": norm([-a, -b, q])}
        truth = []
        for av, bv in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            va = av if a > 0 else 1-av
            vb = bv if b > 0 else 1-bv
            truth.append(va & vb)
        assert truth == gate["truth_table_00_01_10_11"]
        for name, item in gate["facets"].items():
            assert norm(item["clause"]) == expected[name]
            assert item["line_id"] not in lines
            lines[item["line_id"]] = expected[name]
            facets += 1
    assert len(outputs) == 15 and facets == 45
    for n in p["resolution"]:
        lid, rid = n["left"]["line_id"], n["right"]["line_id"]
        pivot = n["pivot"]
        assert lid in lines and rid in lines
        assert pivot in lines[lid] and -pivot in lines[rid]
        got = norm([x for x in lines[lid] if x != pivot] + [x for x in lines[rid] if x != -pivot])
        assert got == norm(n["clause"])
        lines[n["line_id"]] = got
    assert len(p["resolution"]) == 131
    assert d["raw_packet"] == {
        "DEF_records": 0, "RES_records": 131, "actual_original_sources": 8,
        "nonoriginal_DEF_facets_marked_SOURCE": 45, "records_marked_SOURCE": 53, "total_lines": 184}
    assert d["cost"] == {"distinct_paid_nodes": 146, "paid_DEF": 15, "paid_RES": 131}
    assert all(d["controls"].values())
    print(json.dumps({"status": "PASS", "original_sources": 8, "owned_facets": 45,
                      "paid_defs": 15, "paid_res": 131, "historical_raw_DEF_records": 0,
                      "scope": "independent proposed-owner adapter replay; historical bytes unauthenticated"}, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
