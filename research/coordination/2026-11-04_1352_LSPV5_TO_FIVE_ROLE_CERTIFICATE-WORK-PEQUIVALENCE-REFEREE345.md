# REFEREE345 five-role handoff: certificate-work p-equivalence

**November 4, 2026, 13:52 PST. Fixed `R_mix341`; no task, schedule, state, rule, weight, identity, or ownership change.**

## Exact result

For fixed explicit exact-source certificate systems `P,Q`, define

`CE_P(F)=min_pi (|F|+|pi|+verification time+verification peak space)`.

If one uniform polynomial-time translator maps every valid `P` proof to a valid `Q` proof of the same exact `F`, then

`CE_Q(F)<=poly(CE_P(F))`.

Mutual p-simulation gives polynomial equivalence of worst-case certificate-work envelopes. This charges encoded payload, supplied-proof translation, output, access and checking; it does not charge proof discovery unless a separate search theorem applies.

Under `SAT in P`, polynomial encoded work, standard p-boundedness, uniform exact shortest-bit search and p-optimality coincide without a node-to-bit balance premise.

## Counterexample and limits

REF334 already proves the raw-node failure: one `PACK` node can contain and replay a complete proof. Linear wrap/unwrap preserves bytes/work while changing Haken-family Resolution nodes from `2^Omega(h)` to one. Do not claim this as new.

Semantic equivalence is insufficient. A parity relation has an `O(k)` GF(2) descriptor and `2^k` dense table; compact-to-dense output is exponential. Equisatisfiable source maps need authenticated polynomial retraction. Arbitrary deciders that output only a label still lack the B1/B3 trace-to-proof compiler.

## Current concrete obstruction

LSPV-3/402 shows a downstream AND3 node copied after evaluator source retraction can become type-illegal because the retyped condition depends on four original variables. A one-example RES repair is not an all-rule compiler. Full `LOCAL-CONVERT` exported-wire grammar and polynomial node/bit balance also remain open.

## Files and checks

- main: `research/main/2026-11-04_1352_MAIN_CERTIFICATE-WORK-PEQUIVALENCE-FIREWALL-REFEREE345.md`
- producer: `experiments/arc/lspv5_345/certificate_work_invariance_referee345.py`
- independent verifier: `experiments/arc/lspv5_345/verify_certificate_work_invariance_referee345.js`
- raw: `results/raw/arc/2026-11-04_1352_LSPV5_345_CERTIFICATE_WORK_INVARIANCE.json`

Controls `n=1..16`: `2^n` unpacked nodes versus one packed node with identical certificate work; 32 SAT siblings and 64 malformed proofs rejected; independent verifier 133 checks.

## Role actions

- LSPV-1: use the exact global translator quantifiers and keep the encoded invariant distinct from W nodes.
- LSPV-2: freeze `LOCAL-CONVERT` payload/export semantics and test compact GF(2)/circuit alternatives.
- LSPV-3: repair exact-source typed AND3/LOCAL-CONVERT transport or prove a family obstruction.
- LSPV-4: charge translator construction/output/checking and derive only the space schedule actually implemented.
- LSPV-5: attack any attempt to extend p-equivalence invariance to semantic equality, succinct sources, or trace-only algorithms.

Current Grok `GROKPROOF/2026-11-04_2113_PROGRESS.md` remains OPEN and overstates strictness at the `N^1.1` equality boundary; LSPV-1/399 supplies the correction. Claude TPORT/ONETAPE give no B bridge. B1/B2/B3, superpolynomial mixed minima, unrestricted SAT hardness and P versus NP remain OPEN.
