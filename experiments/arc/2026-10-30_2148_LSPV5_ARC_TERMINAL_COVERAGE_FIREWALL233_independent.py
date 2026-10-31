#!/usr/bin/env python3
"""Independent verifier for ARC-TERMINAL-COVERAGE-FIREWALL233 raw data."""
import itertools
import json
from pathlib import Path

P = Path("results/raw/arc/2026-10-30_2148_LSPV5_ARC_TERMINAL_COVERAGE_FIREWALL233_raw.json")


def lit(l, a):
    return bool((a >> (abs(l) - 1)) & 1) == (l > 0)


def cc(c, a):
    return sum(lit(x, a) for x in c)


def main():
    d = json.loads(P.read_text()); checks = 0
    assert d["run"] == "ARC-TERMINAL-COVERAGE-FIREWALL233"; checks += 1
    for case in d["cases"]:
        f = case["formula"]; n = case["nvars"]
        models = [a for a in range(1 << n) if all(cc(c, a) for c in f)]
        assert len(models) == case["exact_model_count"]
        assert bool(models) == case["controller"]["sat"] == case["exact_sat"]; checks += 2
        for rec in case["local_S_U_targets"]:
            c = f[rec["clause"] - 1]
            for o, l in zip(rec["occurrences"], c):
                assert o["variable"] == abs(l)
                assert o["S_value"] == int(l > 0)
                assert o["U_value"] == 1 - int(l > 0)
                assert o["invert_S_value"] == o["U_value"]
                assert o["invert_U_value"] == o["S_value"]; checks += 5
        for p in case["pair_extreme_compatibility"]:
            assert p["predicted"] == p["observed"]; checks += 1
        trail = case["zero_to_one_flip_trail"]
        for rec in trail:
            assert rec["counts"] == [cc(c, rec["mask"]) for c in f]; checks += len(f)
        assert trail[0]["mask"] == 0 and trail[-1]["mask"] == (1 << n) - 1; checks += 2
        for row in case["delay_firewall"]:
            expected = max(6/5, 3/5 + row["D"]/2)
            assert abs(expected - row["claimed_allowed_exponent"]) < 1e-12
            assert row["violates"] == (row["D"] > expected); checks += 2
    names = {c["name"]: c for c in d["cases"]}
    assert not names["W1_STRICT22_UNSAT"]["exact_sat"]
    assert names["SWAP6_STRICT22_SAT"]["exact_sat"]
    assert names["W1_STRICT22_UNSAT"]["controller"]["policy"] == "up-dpll-fallback"
    assert names["SWAP6_STRICT22_SAT"]["controller"]["policy"] == "up-dpll-fallback"
    assert names["XOR_K4_EVEN_SAT"]["controller"]["policy"] == "xor-quartet"
    assert names["XOR_K4_ODD_UNSAT"]["controller"]["policy"] == "xor-quartet"; checks += 6
    # Same-source both labels are present in each relevant architecture.
    for prefix in ("XOR_K4", "HORN", "KROM"):
        labels = {c["exact_sat"] for c in d["cases"] if c["name"].startswith(prefix)}
        assert labels == {False, True}; checks += 1
    print(json.dumps({"verified": True, "assertion_units": checks,
                      "cases": len(d["cases"])}, sort_keys=True))


if __name__ == "__main__":
    main()
