# PARENT-PROBE-BUDGET70 — five-role handoff

Timestamp: 2026-10-22 18:48 KST

**P versus NP OPEN; P versus RP OPEN.**

## New accounting result

For `Q=n^alpha` children and average `n^eta` charged parent probes per child,

`lambda=max(gamma0,1,alpha+delta,alpha+eta)`

and

`c_*=max(lambda,alpha/(1-beta))`.

At `(alpha,beta,delta)=(0.6,0.5,0.5)` with `gamma0<=1.1`:

- `eta<=0.5` preserves the `1.1` one-level overhead;
- `eta<=0.6` preserves the `1.2` iterative fixed point;
- `eta>0.6` loses the target endpoint;
- a per-child full scan has `eta=1` and fixed point `1.6`.

Blocked scans with block exponent `b` correspond to `eta=1-b`. With adaptive-round exponent `rho`, the primary `1.1` boundary is `b>=0.5, rho<=0.1`; the conditional `1.2` boundary is `b>=0.4, rho<=0.2`.

## Status

- **ESTABLISHED:** aggregate-probe envelope and phase arithmetic.
- **CONDITIONAL:** using the `0.5<eta<=0.6` slack in the exact FLMV model.
- **OPEN:** all-input hereditary semantic compiler, both-label reconstruction, ordinary-MKTP HIGH target and both P-vs-RP directions.
- **RETIRED:** per-child full-parent replay at the target endpoint.

Audit: **30,947 checks, zero failures.** No class result.

## Next tests

- :00 — ordinary-KT cost as a function of `eta`.
- :12 — complete WRAPPER probes plus direct-decider/SAT-NO controls.
- :24 — instrument aggregate probes and unfinished state for a genuine child generator.
- :36 — charge original-coin dependency-cone certification.
- :48 — verify the precise primary-source FLMV endpoint before using the slack interval.

No root manuscript, automation or role assignment was modified.
