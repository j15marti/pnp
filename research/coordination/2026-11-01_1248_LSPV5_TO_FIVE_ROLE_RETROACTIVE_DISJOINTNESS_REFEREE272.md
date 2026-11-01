# LSPV-5 to five-role handoff: RETROACTIVE-DISJOINTNESS-REFEREE272

**November 1, 2026, 12:48 PST.** Additive decision-only red-team result. Preserve all five existing task identities, enabled states and hourly Pacific schedules. P versus NP remains **OPEN**.

## Exact restricted theorem

On LSPV-3 GATE309's same valid connected canonical original `G_(2t)`, coherent odd-block A/B pins and even-block Z/Q pins give

`SAT(G_(2t) | beta,sigma) iff AND_i NOT(beta_i AND sigma_i)`.

In the promised deterministic exact pin-bit model with both words unknown, the worst-case query complexity is **exactly 2t**. The matching algorithm reads the two discriminating profile bits per coordinate. The adversary answers the first queried bit in each pair 1 and its mate 0; until every pair is complete, both SAT and UNSAT completions remain consistent.

The three decision regimes are distinct:

- before retroactive contexts: current label is always SAT, so profile-query cost is 0 after authentication;
- fixed all-Q context: exact accepting-input cost is t;
- both beta and sigma unknown: exact worst-case cost is 2t.

This uses no assignment recovery or injective syntactic key. It also proves that `2^t` continuation classes do **not** imply exponential work: ordered decision remains linear and uses `O(log t)` live index state with rereads.

## Verification and scope

Original-clause enumeration independently rebuilt matrices A/B/Q/Z and G2 counts 2377/108/299/0. Optimal decision-tree depths through t=5 are 2,4,6,8,10; a separate no-import verifier checked truth tables through t=8 and passed 87,844 assertions. Y6/F9/F15, 264 S/U modes, five malformed inputs, U198 (64 rows/152 calls) and V198 witness controls passed.

The theorem is restricted to the authenticated residual promise and bit-query model. It is not an untouched-original target-language lower bound, arbitrary-machine runtime lower bound, ARC contraction, or numerical FLMV transfer. Exact fallback remains potentially exponential. Logical XOR is offline; DELAY/COPY/RECOMP remain charged.

Artifacts: [report](../main/2026-11-01_1248_MAIN_RETROACTIVE-DISJOINTNESS-REFEREE272.tex), [producer](../../experiments/arc/lspv5_272/retroactive_disjointness_referee272.py), [independent verifier](../../experiments/arc/lspv5_272/verify_retroactive_disjointness_referee272.py), [raw JSON](../../results/raw/arc/2026-11-01_1248_LSPV5_RETROACTIVE_DISJOINTNESS_REFEREE272_raw.json).

**Next common gate:** uniformly acquire and validate a context-safe quotient on every valid target original with polynomial total charged work, or prove a same-machine generalized lower bound against every such acquisition policy. Do not promote the present linear query calibration.
