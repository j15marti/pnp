#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE246 raw results."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path

RAW = Path("results/raw/arc/2026-10-31_1048_LSPV5_FIXED_SLOT_ACCESSOR_REFEREE246_raw.json")
OUT = Path("results/summaries/arc/2026-10-31_1048_LSPV5_FIXED_SLOT_ACCESSOR_REFEREE246_verification.json")


def truth(lit, bits):
    return bits[abs(lit) - 1] == (lit > 0)


def sat(cnf, bits):
    return all(any(truth(x, bits) for x in c) for c in cnf)


def modes(c, d):
    vs = sorted({abs(x) for x in c + d})
    out = {x: False for x in ("SS", "SU", "US", "UU")}
    for b in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, b))
        tc = sum(a[abs(x)] == (x > 0) for x in c)
        td = sum(a[abs(x)] == (x > 0) for x in d)
        out["SS"] |= tc == 3 and td == 3
        out["SU"] |= tc == 3 and td == 0
        out["US"] |= tc == 0 and td == 3
        out["UU"] |= tc == 0 and td == 0
    return out


def verify(data):
    checks = 0
    assert data["status"] == "PASS"; checks += 1
    assert data["global_status"].startswith("P versus NP OPEN"); checks += 1
    assert data["gadget_truth_table_checks"] == 16; checks += 1
    assert len(data["records"]) == 4; checks += 1
    for r in data["records"]:
        cnf = r["source_clauses"]
        models = [b for b in itertools.product((False, True), repeat=r["source_n"]) if sat(cnf, b)]
        assert (len(models) > 0) == (r["expected"] == "SAT"); checks += 1
        assert len(models) == r["models"]; checks += 1
        assert any(row["and"] for row in r["join_rows"]) == bool(models); checks += 1
        assert r["source_bits"] == 32 + 51 * len(cnf); checks += 1
        assert len(r["occurrences"]) == 3 * len(cnf); checks += 1
        for o in r["occurrences"]:
            assert o["S_variable"] != o["U_variable"]; checks += 1
            assert o["invert_S_is_U"] == o["U_variable"]; checks += 1
            assert o["invert_U_is_S"] == o["S_variable"]; checks += 1
        for p in r["pair_modes"]:
            got = modes(cnf[p["j"]], cnf[p["k"]])
            assert got == p["modes"]; checks += 4
        z = r["endpoints_flips"]["zero"]["counts"]
        o = r["endpoints_flips"]["one"]["counts"]
        assert all(x + y == 3 for x, y in zip(z, o)); checks += len(z)
        for proof in r["resolutions"]:
            a, b = (cnf[i] for i in proof["parents"])
            pivot = proof["pivot"]
            assert pivot in a and -pivot in b; checks += 1
            res = sorted(set(x for x in a + b if abs(x) != pivot), key=lambda x: (abs(x), x < 0))
            want = sorted(proof["resolvent"], key=lambda x: (abs(x), x < 0))
            assert res == want; checks += 1
        for ch in r["children"]:
            assert ch["clauses"] == 8 * (ch["span"][1] - ch["span"][0]); checks += 1
            assert ch["physical_bits"] == 32 + 51 * ch["clauses"]; checks += 1
    # Mutation tests: each named corruption must be rejected by a direct invariant.
    corruptions = 0
    rejected_kinds = []
    for kind in range(8):
        d = copy.deepcopy(data)
        if kind == 0: d["status"] = "FAIL"
        elif kind == 1: d["records"][0]["models"] += 1
        elif kind == 2:
            for row in d["records"][0]["join_rows"]:
                row["and"] = False
        elif kind == 3: d["records"][0]["occurrences"][0]["U_variable"] = d["records"][0]["occurrences"][0]["S_variable"]
        elif kind == 4: d["records"][0]["pair_modes"][0]["modes"]["SS"] ^= True
        elif kind == 5: d["records"][0]["children"][0]["clauses"] += 1
        elif kind == 6: d["records"][0]["resolutions"][0]["pivot"] += 100
        else: d["gadget_truth_table_checks"] = 15
        try:
            verify_shallow(d)
        except AssertionError:
            corruptions += 1
            rejected_kinds.append(kind)
    assert corruptions == 8, rejected_kinds; checks += corruptions
    return checks, corruptions


def verify_shallow(d):
    assert d["status"] == "PASS"
    assert d["gadget_truth_table_checks"] == 16
    r = d["records"][0]; cnf = r["source_clauses"]
    models = [b for b in itertools.product((False, True), repeat=r["source_n"]) if sat(cnf, b)]
    assert len(models) == r["models"]
    assert any(x["and"] for x in r["join_rows"]) == bool(models)
    o = r["occurrences"][0]; assert o["S_variable"] != o["U_variable"]
    p = r["pair_modes"][0]; assert modes(cnf[p["j"]], cnf[p["k"]]) == p["modes"]
    ch = r["children"][0]; assert ch["clauses"] == 8 * (ch["span"][1] - ch["span"][0])
    pr = r["resolutions"][0]; a, b = (cnf[i] for i in pr["parents"])
    assert pr["pivot"] in a and -pr["pivot"] in b


def main():
    text = RAW.read_text()
    data = json.loads(text)
    checks, corruptions = verify(data)
    result = {"run_id": data["run_id"], "status": "PASS", "checks": checks,
              "corruptions_rejected": corruptions,
              "producer_imported": False,
              "raw_sha256": hashlib.sha256(text.encode()).hexdigest()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
