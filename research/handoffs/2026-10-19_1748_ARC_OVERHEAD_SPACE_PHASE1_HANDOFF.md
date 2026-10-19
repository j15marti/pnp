# ARC-OVERHEAD-SPACE-PHASE1 handoff

**Status:** P versus NP remains OPEN. The conditional phase frontier is exact; the contraction stage is missing.

For the fully charged envelope

\[
t'\le\max\{11/10,q,3/5+t/2\},\qquad
s'\le\max\{1/2,r,s/2\},
\]

the limiting certification point is

\[
C=\max\{6/5,q\},\qquad R=\max\{1/2,r\}.
\]

Finite entry into the FLMV sufficient forbidden region is certified exactly when

\[
\boxed{R<\beta(C)},\qquad
\beta(c)=\frac{(c+2)/c^2-c}{2}.
\]

Operational slices:

- If `r <= 1/2`, require `q < 1.2055694304005903117...`.
- If `q <= 6/5`, require `r < 23/45`.
- `q=1.2055, r=1/2` retains positive margin.
- `q=1.2057, r=1/2` fails this endpoint certificate.
- `q=6/5, r=23/45` is equality and has no strict margin.

This unifies earlier special-case calculations in `CTRLQUOT1`, `GLUECOVER1`, model-bridge MB3, and `FLMV-FINITE-ENTRY-GATE1`; it is not a new contraction mechanism.

## Strongest falsifier

For one concrete candidate stage, identify the first unavoidable all-input branch with charged local time exponent `q` or live-space exponent `r`. Reject the stage immediately if `max(1/2,r) >= beta(max(6/5,q))`. Then run the padded-decider query-length test on any surviving stage.

## Role assignments

- **MCSP one-tape:** exact `mu_2 -> mu_1` both-promise-side transport in the CHMY machine model.
- **Search/GapMCSP:** a one-pass workspace lower bound beyond circuit-output length, or the OPS every-small-beta circuit premise.
- **ARC:** emit a complete `(q,r)` ledger for one actual all-input hereditary stage.
- **Hostile red team:** maximize source rescans, retained children/ancestors, replay, malformed inputs, and current-scale calls.
- **Synthesis:** no more endpoint optimization until a concrete stage passes the frontier.

## Artifacts

- `research/main/2026-10-19_1748_MAIN_ARC_OVERHEAD_SPACE_PHASE1.tex`
- `experiments/review/2026-10-19_arc_overhead_phase_audit.py`
- `results/raw/synthesis/2026-10-19_1748_ARC_OVERHEAD_SPACE_PHASE1.json`

Root `main.tex` is not edited because its live body remains placeholder-truncated with unbalanced historical ownership markers.
