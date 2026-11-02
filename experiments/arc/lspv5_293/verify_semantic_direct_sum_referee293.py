#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE293."""
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-11-02_1048_LSPV5_SEMANTIC_DIRECT_SUM_REFEREE293_raw.json"


def tseitin(vcount, edges):
    inc = [[] for _ in range(vcount)]
    for i, (u, v) in enumerate(edges, 1):
        inc[u].append(i); inc[v].append(i)
    out = []
    for v, scope in enumerate(inc):
        assert len(scope) == 3
        rhs = int(v == 0)
        for bits in product((0, 1), repeat=3):
            if sum(bits) % 2 != rhs:
                out.append(tuple(e if b == 0 else -e for e, b in zip(scope, bits)))
    return len(edges), tuple(out)


def build():
    k4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    k33 = [(i,3+j) for i in range(3) for j in range(3)]
    cube = [(x,x^b) for x in range(8) for b in (1,2,4) if x < (x^b)]
    pet = [(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+2)%5) for i in range(5)] + [(i,5+i) for i in range(5)]
    w1 = ((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
    return [("K4_tseitin",)+tseitin(4,k4), ("K3_3_tseitin",)+tseitin(6,k33), ("Cube_tseitin",)+tseitin(8,cube), ("Petersen_tseitin",)+tseitin(10,pet), ("W1",15,w1)]


def true_clause(c, a):
    return any(a[abs(x)-1] == (x > 0) for x in c)


def main():
    data = json.loads(RAW.read_text())
    assert data["status"] == "PASS" and data["blocks"] == 5
    assert data["combined_base_relation_size"] == 1
    checks = 0; total_L = 0; total_a = 0
    byname = {r["fixture"]: r for r in data["records"]}
    for block, (name, n, clauses) in enumerate(build()):
        witnesses = [None] * len(clauses); models = 0
        for a in product((0,1), repeat=n):
            total_a += 1
            bad = [i for i,c in enumerate(clauses) if not true_clause(c,a)]
            if not bad: models += 1
            elif len(bad) == 1 and witnesses[bad[0]] is None: witnesses[bad[0]] = a
        assert models == 0 and all(x is not None for x in witnesses)
        L = sum(map(len,clauses)); total_L += L
        r = byname[name]
        assert r["L"] == L and r["models"] == 0 and r["deletion_witnesses"] == len(clauses)
        for i,c in enumerate(clauses):
            for j,lit in enumerate(c):
                changed = list(c); changed[j] = -lit
                assert true_clause(tuple(changed), witnesses[i])
                for k,d in enumerate(clauses):
                    if k != i: assert true_clause(d, witnesses[i])
                checks += 1
        assert r["one_flip_neighbor_relation_masks"] == [0,1<<block]
        for s in r["phase_splits"]:
            assert s["compile_distinct_sign_probes"] + s["query_distinct_sign_probes"] == L
            assert s["combined_distinct_sign_probes"] == L
    assert total_L == 396 == checks == data["direct_sum_distinct_probe_lower_bound"]
    assert total_a == 70208 == data["complete_assignments_checked"]
    assert data["malformed_controls_rejected"] == 6
    print(json.dumps({"status":"PASS","independent_assertion_groups":checks+25,"signs":total_L,"assignments":total_a},indent=2))


if __name__ == "__main__": main()
