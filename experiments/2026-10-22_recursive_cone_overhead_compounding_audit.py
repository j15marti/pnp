"""Audit of RECURSIVE-CONE-FIXED-POINT81: how per-level overhead compounds.
Lemma 81A tracks exponents only. With K>=1 multiplicative overhead per level (relative to
LOCAL size y) and depth D = ceil(log_{1/beta} log2 x) until residuals are O(1), total
overhead is K^D = (log x)^{log_{1/beta} ... } -- polylog iff K is constant.
Exact rational checks, runs in <1s. Status: COMPUTATIONAL (arithmetic only)."""
from fractions import Fraction as F
import math, json
def r(beta, sigma, d):
    x = F(1)
    for _ in range(d): x = 1 + sigma + beta*(x-1)
    return x
out = {}
for name, b, s in [("baseline", F(1,2), F(1,10)), ("retuned", F(101,200), F(1,10))]:
    lim = 1 + s/(1-b)
    assert all(r(b,s,d) < lim for d in range(1,200)) and lim - r(b,s,200) < F(1,10**30)
    rec = []
    for logx in (10**3, 10**6, 10**12, 10**24):  # x = 2^logx
        D = math.ceil(math.log(logx, 1/float(b)))   # depth to reach residual size O(1)
        row = {"log2x": logx, "depth": D}
        for K in (1.01, 2.0):  # constant per-level overhead factor
            row[f"K={K}: log2(total overhead)"] = D*math.log2(K)
            row[f"K={K}: overhead exponent / log2x"] = D*math.log2(K)/logx
        # per-level overhead x^eps (not relative-local) : exponent gain eps*D
        row["x^0.01 per level: extra exponent"] = 0.01*D
        rec.append(row)
    out[name] = {"limit": str(lim), "rows": rec}
    print(name, lim, float(lim))
    for row in rec: print(row)
json.dump(out, open("results/2026-10-22_recursive_cone_overhead_compounding.json","w"), indent=1, default=str)
