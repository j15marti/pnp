#!/usr/bin/env python3
"""Independent verifier for ARC-PARETO-CRITICAL-REFEREE239 raw output."""
from fractions import Fraction as F
import hashlib, json


def p(c): return 5*c**3 + 10*c**2 - 11*c - 10
def h(c): return 1 - F(3,5)/c
def d2(c): return (c+2-c**3)/(2*c**2)


with open("2026-10-31_0348_ARC_PARETO_CRITICAL_REFEREE239_raw.json", encoding="utf-8") as f:
    raw = json.load(f)
lo, hi = map(F, raw["coarse_root_isolation"])
assert p(lo) < 0 < p(hi)
assert hi-lo == F(1,1000000)
assert float(h(lo)) < float(raw["critical_lambda_decimal"]) < float(h(hi))
c = F(6023,5000); lam = F(5019,10000)
assert F(3,5)/(1-lam) < c and lam < d2(c)
assert F(251,500) > h(hi)
for case in raw["hostile_original_clause_controls"]:
    assert (case["models"] > 0) == case["expected_sat"]
    for clause in case["clause_extremes"]:
        assert clause["S"] == clause["invert_U"]
        assert clause["U"] == clause["invert_S"]
    for pair in case["pair_compatibility"]:
        assert set(pair["modes"]) == {"SS","SU","US","UU"}
digest = hashlib.sha256(open("2026-10-31_0348_ARC_PARETO_CRITICAL_REFEREE239_raw.json", "rb").read()).hexdigest()
result = {"verified": True, "raw_sha256": digest, "cases": len(raw["hostile_original_clause_controls"]),
          "pair_matrices": sum(len(x["pair_compatibility"]) for x in raw["hostile_original_clause_controls"])}
with open("2026-10-31_0348_ARC_PARETO_CRITICAL_REFEREE239_check.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, sort_keys=True); f.write("\n")
print(json.dumps(result, indent=2))
