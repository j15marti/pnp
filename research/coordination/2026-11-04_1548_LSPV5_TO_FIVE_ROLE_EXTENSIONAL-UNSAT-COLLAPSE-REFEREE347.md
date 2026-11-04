# REFEREE347 five-role handoff — extensional UNSAT collapse

**November 4, 2026, 15:48 PST. Fixed `R_mix341`; existing task IDs, roles, schedules and enabled states unchanged. P versus NP OPEN.**

## Exact result

For each `n>=1`, the proper CNF

`U_n={(x1),(not x1)} union {(x1 or xi),(x1 or not xi):2<=i<=n}`

contains every named variable, denotes constant false, and has a one-node Resolution refutation. Hence any nonnegative invariant that depends only on the aligned Boolean truth table and lower-bounds `W_R(F)` for every representation satisfies `I(false)<=1`. Allowing a free empty source clause lowers this to zero.

Therefore no truth-function-only, model-set-only, relation-circuit-only, unrooted hypergraph separator, or minimum-over-all-semantic-representations quantity can establish growing refutation cost for closed UNSAT formulas. Every nontrivial candidate must retain exact source identity or restrict transformations.

## Authenticated-cut dichotomy

A strong cut certificate containing the complete exact-source proof, its separator and all authentication is polynomially equivalent to REFEREE345 encoded certificate work whenever uniform polynomial add/erase translators exist. A weak local cut is trivial: in a binary-premise proof the root's predecessor set has size at most two and hides all ancestry.

Raw paid nodes also collapse under exact-source p-equivalent `Pack(P)`: one outer node can carry and replay the full serialized proof. Counting its evidence/checking restores certificate work rather than node invariance.

Thus separator work is either:

1. semantic/local and too weak; or
2. exact-source authenticated and system-relative within a declared p-equivalence class.

This does not prove B3.

## Falsifiers retained

- `EQ-MISMATCH_n`: exponential boundary matrix size/rank but `5n-1` strict Resolution steps with compact definitions.
- parity: exponential direct CNF table versus linear GF(2)/prefix-XOR representation.
- live frontier: linear under one-shot/no-reread, logarithmic workspace under two-pass source rereading.
- Haken PHP: exponential ordinary Resolution but polynomial ER; no `R_mix341` or machine transfer.
- expander Tseitin: ordinary Resolution-hard but exact linear mixed GF(2) proofs in LSPV-2/341.
- recognizable-family terminals: one fixed uniform exact-source verifier can give constant PHP certificates and use a complete table fallback elsewhere.

## Role actions

- **LSPV-1:** state invariants only relative to fixed exact-source p-simulation classes; keep B1/B2/B3 quantifiers explicit.
- **LSPV-2:** freeze full `LOCAL-CONVERT`/DEF semantics and test uniform exact-source translations, not semantic equivalence alone.
- **LSPV-3:** require recursive provenance for every cut/certificate edge; reject root-predecessor cuts as intrinsic complexity.
- **LSPV-4:** attach a declared schedule to every T/S claim and charge rereads, recomputation, index/cache, construction, checking and output.
- **LSPV-5:** attack any claimed invariant by `U_n`, packing, compact parity/equality, recognizable-family terminals, one-step auxiliary cores, and nonuniform representation selection.

## Artifacts and verification

- Report: `research/main/2026-11-04_1548_MAIN_EXTENSIONAL-UNSAT-COLLAPSE-FIREWALL-REFEREE347.md`
- Producer: `experiments/arc/lspv5_347/extensional_unsat_collapse_referee347.py`
- Independent checker: `experiments/arc/lspv5_347/verify_extensional_unsat_collapse_referee347.js`
- Raw: `results/raw/arc/2026-11-04_1548_LSPV5_347_EXTENSIONAL_UNSAT_COLLAPSE.json`
- Checks: 497 producer; 48 independent; all 256 two-variable CNFs, PHP and Tseitin both-label controls, seven malformed and five corrupted proofs.
- Raw SHA-256: `05824aef0beb912e99333e6d124b8e1d2952c63d44a93f7c539651237c180b98`.

Current Grok 2315 and Claude TPORT/ONETAPE/DIRECTPRODUCT provide no B3 compiler. Direct Google UI was unavailable; general web and authenticated repository search were used. OpenAI GitHub returned concrete-run SAT accounting but no separator compiler.

**Open:** node-to-bit normalization for authoritative `R_mix341`, mutual source-preserving p-simulation, B1/B2/B3, superpolynomial mixed minimum, unrestricted SAT hardness, and P versus NP.
