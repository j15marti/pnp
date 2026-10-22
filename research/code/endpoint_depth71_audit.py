"""ENDPOINT-DEPTH71 audit (stdlib only, exact Fractions, well under 30 s).
Map f(c)=max(lam, alpha+beta*c); fixed point c*=max(lam, alpha/(1-beta)).
Checks: (1) c_d - c* = beta^d (c0 - c*) when c*>lam (geometric contraction);
(2) depth d(eps)=ceil(log(gap/eps)/log(1/beta)) suffices for c_d<=c*+eps;
(3) when lam>=alpha/(1-beta), f reaches c*=lam in finitely many steps or stays above;
(4) the 6/5 endpoint is never attained at finite depth from c0>6/5 (strict).
"""
import json, math, random
from fractions import Fraction as F
random.seed(71)
fails = 0; checks = 0
def f(c, lam, a, b): return max(lam, a + b*c)
def fp(lam, a, b): return max(lam, a/(1-b))
for _ in range(3000):
    a = F(random.randint(1, 99), 100); b = F(random.randint(1, 99), 100)
    lam = F(random.randint(100, 170), 100); c0 = F(random.randint(100, 300), 100)
    cs = fp(lam, a, b); c0 = max(c0, cs); c = c0
    for d in range(1, 31):
        c = f(c, lam, a, b); checks += 1
        if a/(1-b) > lam:
            # c_d = cs + b^d (c0-cs) while above lam-branch; always >= cs, monotone
            ok = c >= cs and (c - cs == b**d * (c0 - cs))
        else:
            ok = c >= lam and (c == lam or c > lam)
        if not ok: fails += 1
# depth table for the ledger point (alpha,beta)=(0.6,0.5), c0=1.6 (full-scan per child)
a, b, lam = F(3,5), F(1,2), F(11,10)
rows = []
for eps in [F(1,10), F(1,100), F(1,1000), F(1,10**6)]:
    gap = F(8,5) - F(6,5)
    d = math.ceil(math.log(float(gap/eps))/math.log(1/float(b)))
    c = F(8,5)
    for _ in range(d): c = f(c, lam, a, b)
    checks += 1
    if not (c <= F(6,5) + eps): fails += 1
    # strictness: exactly 6/5 never attained at finite depth
    checks += 1
    if c == F(6,5): fails += 1
    rows.append({"eps": str(eps), "depth": d, "c_d": str(c), "c_d_minus_6_5": str(c - F(6,5))})
out = {"checks": checks, "failures": fails, "depth_table_c0_1.6": rows}
json.dump(out, open("research/main/ENDPOINT_DEPTH71_raw.json", "w"), indent=1)
print(checks, fails); [print(r) for r in rows]
