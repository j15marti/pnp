# TASK-007 — Search-G precommitment to superpolynomial resource

**Status:** OPEN.

Supporting artifacts:
- `research/explorations/search-spine/2026-10-01_FP-FNP_PARALLEL-PROOF-SPINE.tex`
- `research/explorations/search-spine/2026-10-01_FP-FNP_G-PRECOMMITMENT-SPINE.md`
- `research/explorations/random-challenge/2026-10-01_RCCN1_ROUTED-CAUSAL-COMPUTATION-NETWORK.md`
- `research/explorations/random-challenge/2026-10-01_CCSPC1_CANONICAL-CAUSAL-SAT-POINTER-CASCADE.md`

## Exact proved core

For a pre-cut record X and future-audit family {f_B}, define the complete response signature `Sigma(X)=(f_B(X))_B`.

If one s-bit state is committed before B and must answer every future audit without new X-dependent information, then `s >= log2 max_z |{Sigma(X):Z(X)=z}|`.

If storage is smaller, post-cut X-dependent reacquisition is necessary.

Polynomial-length future bits do not force an NDTM to enumerate all branches; one nondeterministic path may guess the realized future and verify it later.

## Load-bearing target

Prove, for one fixed FNP-complete relation R* and every deterministic selector S solving R*, that a SAME_REALIZATION Search-G/RCCN audit forces

`S_persistent + C_communication + w Q_reread + C_recompute + C_sequential > n^c`

for every fixed c on some input, while fully charging input size, preprocessing, output production, static reread, recomputation, and alternate representations.

## Mandatory hostile controls

- NDTM future-guessing / quantifier order;
- static random-access reread;
- polynomial recomputation;
- branch redundancy / low response-signature diversity;
- selector choice among many witnesses;
- flatten RCCN to one DTM;
- memoization and pointer jumping;
- group/history compression;
- Horn, 2-SAT, bounded treewidth, affine/Tseitin;
- semantic and algebraic oracles;
- DEAD/COPY/DELAY/INTERP/RECOMP;
- explicit versus succinct input size;
- relativization, algebrization, Natural Proofs when applicable.

## Success criterion

A restricted online/streaming/pebbling bound is insufficient. The theorem must be paired with a model-preserving bridge from every hypothetical polynomial-time selector for the fixed FNP relation.