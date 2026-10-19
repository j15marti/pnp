% ROUTE1-RECHECK::CHMY_MULTIPORT_INDEP_RECHECK::2026-10-20_0400_KST
# CHMY multiport floor: independent exact recheck (hourly scheduled check)

**Status:** COMPUTATIONAL confirmation of the FLOOR3 survival bounds; no new theorem. **P versus NP remains OPEN.**

## Repository check
Branch tip f4baf3c2 (2026-10-20 03:41 KST). Last hour: FLOOR3 sharp multiport mask floor, ARC compact-history audit,
AMPLIFY-FIX-SELECTOR4, REDTEAM22 public-seed multiport TV results, hourly Grok annotations. Root `main.tex` open status unchanged.
`main.tex` not edited (ownership markers/authorization for this run uncertain; per FLOOR3 precedent).

## What was done
Re-derived the FLOOR3 proof by hand (Q_J = B_{j*}(1 xor T_{j*}R); upper bound from B_{j*}=1; lower bound from B_{j*}=1,T_{j*}=0)
-- the argument is correct as stated. Wrote an independent exact-rational enumerator
(`experiments/review/2026-10-20_CHMY_MULTIPORT_INDEP_RECHECK.py`, ~15 s, single stage, no chunking needed):
- all nonempty J, h=2..8, gamma in {0,1/10,1/4}, both bias signs: 3006 cases, 0 violations of
  (1/2-gamma)^{t+1} <= Pr[Q_J=1] <= (1/2+gamma)^t;
- 3000 random non-identically-biased independent-layer cases: 0 violations;
- attainment: single latest port hits 2^-t; adjacent pair {j*-1,j*} hits 2^-(t+1);
- control: h=3, J={1,2}, T2=T3 gives Pr=0 (cross-layer correlation breaks the bound, as FLOOR3 states).
Raw: `results/raw/separation/2026-10-20_CHMY_MULTIPORT_INDEP_RECHECK.json`.

## Scope / not claimed
Single-coordinate marginal only; does not address seed-dependent port selection, nonlinear embedding, YES/NO MCSP preservation,
one-tape cost, or the CHMY->OPS parameter descent. These stay OPEN. Nothing here moves a load-bearing arrow.

## Suggested next test (from FLOOR3's own list)
Joint (two-coordinate) behavior of Q_J on low-complexity source supports: the recheck above covers marginals only.

% END_OF_VERIFIED_REPORT::ROUTE1-RECHECK::CHMY_MULTIPORT_INDEP_RECHECK
