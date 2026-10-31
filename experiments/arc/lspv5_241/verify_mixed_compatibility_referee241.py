#!/usr/bin/env python3
"""Separately authored checker for MIXED-COMPATIBILITY-REFEREE241 raw JSON."""
from __future__ import annotations
import json, sys


def truth(lit, bits):
    v = bits[abs(lit)-1]
    return bool(v) if lit > 0 else not bool(v)


def main(path):
    d = json.load(open(path, encoding="utf-8"))
    assert d["run"] == "MIXED-COMPATIBILITY-REFEREE241" and d["status"] == "PASS"
    by = {s["name"]: s for s in d["sources"]}
    s = by["equal_size_unique_101_SAT"]
    u = by["equal_size_all8_UNSAT"]
    assert s["models"] == ["101"] and u["models"] == []
    assert s["m"] == u["m"] == 8
    assert s["mixed_counts"] == {"E_clauses": 96, "H_clauses": 8, "clauses": 104,
                                  "sat_extensions": 1 << 24, "variables": 51}
    assert u["mixed_counts"]["sat_extensions"] == 0 and u["mixed_counts"]["clauses"] == 104
    assert d["independent_flmv_envelope"][0]["d_star"] == "23/45"
    assert d["independent_flmv_envelope"][1]["d_star"] == "11642479/23232400"
    assert all(r["tail_strictly_below_best"] for r in d["independent_flmv_envelope"])
    checks = 0
    for src in (s, u):
        clauses = src["clauses"]
        actual=[]
        for z in range(8):
            bits=tuple((z >> (2-i)) & 1 for i in range(3))
            if all(any(truth(l,bits) for l in c) for c in clauses):
                actual.append("".join(map(str,bits)))
            checks += len(clauses)
        assert actual == src["models"]
        assert src["component_labels"]["H"] == src["component_labels"]["E"] == "SAT"
        assert src["source_dpll"]["sat"] == bool(actual)
        assert src["mixed_dpll"]["sat"] == bool(actual)
        assert len(src["occurrence_targets"]) == 24
        assert len(src["pair_extreme_matrices"]) == 28
        assert len(src["interface_join_rows"]) == 8
        assert all(r["join"] == r["source"] for r in src["interface_join_rows"])
        for p in src["pair_extreme_matrices"]:
            for mode, pred in p["predicted"].items():
                assert pred == p["enumerated"][mode]["feasible"]
                checks += 1
        for o in src["occurrence_targets"]:
            assert o["S_target"] == o["invert_U_is_S"]
            assert o["U_target"] == o["invert_S_is_U"] == 1-o["S_target"]
            checks += 1
        # Complement identity t_j(~a)=3-t_j(a) along reported trails.
        for row in src["endpoint_flip_trail"]:
            a=tuple(map(int,row["assignment"])); b=tuple(1-x for x in a)
            ca=[sum(truth(l,a) for l in c) for c in clauses]
            cb=[sum(truth(l,b) for l in c) for c in clauses]
            assert row["true_literal_counts"] == ca
            assert all(x+y==3 for x,y in zip(ca,cb))
            checks += len(clauses)
    print(json.dumps({"run": d["run"], "status": "PASS", "independent_checks": checks,
                      "guard": "P versus NP OPEN"}, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
