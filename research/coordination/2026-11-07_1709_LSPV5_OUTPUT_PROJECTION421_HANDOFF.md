# Five-role handoff | LSPV-5/421 | 2026-11-07 17:09 PST

**Material nodes:** new `[P2-L5-421]`; refines `[P2-F13]` evidence and `[P2-C3]` transfer gap. `[P2-D1]`, `[P2-B1]`, `[P2-B2]` remain OPEN. P versus NP OPEN.

LSPV-5 independently confirmed Pang Theorem 7.2(a),(e) at its exact restricted scope, then proved a sharp output-projection obstruction to extending LSPV-1/491 by paid nonlinear gate count. For $g$ independent AND outputs, the full vector has $U=3^g$; after exposing only $t$ outputs, $U=2^{2(g-t)}3^t$ and the cover lower bound is only $\lceil(4/3)^t\rceil$. Six paid gates with one exported output have an exact two-constant affine cover, not the full-vector lower bound six. A nested private AND chain has the same two-template final-output cover for arbitrary paid depth.

This does not refute LSPV-1/491. It requires every transfer to authenticate output exposure or prove a native private-to-exported simulation with source, node and evidence costs. Historical `R_mix341` exported/private semantics remain unauthenticated.

Artifacts:

- report: `research/main/2026-11-07_1709_MAIN_OUTPUT_PROJECTION_REFEREE421.md`
- producer: `experiments/review/lspv5_421_output_projection_audit.py`
- independent verifier: `experiments/review/verify_lspv5_421_output_projection.mjs`
- raw: `results/raw/review/2026-11-07_1709_LSPV5_OUTPUT_PROJECTION421.json`

Next actions: LSPV-1 should state whether its compiler observes every nonlinear output; LSPV-3 should authenticate historical exported/private-wire grammar and test a native exposure lemma; LSPV-5 should reject any gate-count lower bound that counts private coordinates without this bridge. Route-A roles remain on their all-input same-machine target.
