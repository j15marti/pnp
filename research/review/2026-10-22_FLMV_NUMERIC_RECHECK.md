# Hourly check: independent recheck of FLMV-PROBE-MARGIN71 / INTERFACE-FLMV-RETUNING72 numerics

**Global status: P versus NP OPEN. No proof claim is made or changed.**

Scope: arithmetic and source check only. Nothing here touches the open load-bearing arrows
(all-input hereditary transformer, both-label MKTP target, model transfer).

## Source check (KNOWN THEOREM)
Fortnow-Lipton-van Melkebeek-Viglas (ECCC TR00-028 / JACM 52:835-865) state SAT not in DTISP[n^a, n^b]
for b < (1/2)((a+2)/a^2 - a), and remark the bound is positive iff a(a^2-1)<2, i.e. a <~ 1.521.
This matches the d(c) used in MARGIN71 / RETUNING72 (the denominator is a^2, not a^2-a).

## Independent recomputation (COMPUTATIONAL; bisection, double precision, `2026-10-22_FLMV_NUMERIC_RECHECK.py`)
- d(c)=1/2 root: c = 1.2055694304..., residual of c^3+c^2-c-2 is 4e-16. Matches MARGIN71.
- d(241/200) = 0.50113 > 1/2, so 241/200 is strictly inside the feasible side. Matches.
- sigma=1/10 child-size cap: beta_cap = 0.5061384798932702, matching RETUNING72's 0.506138479893270...
- At beta=1/2: sigma < 0.10278 and eta < 0.60557 (so sigma=1/10 has slack 0.00278).
- At beta=0.506: sigma < 0.100062, nearly tight, consistent with beta_cap.

Result: no discrepancy found. This confirms the exponent bookkeeping only; Lemma 72A/72B remain
conditional on a supplied canonical complete-interface partition.

Chunking: single run, well under 30 s.
