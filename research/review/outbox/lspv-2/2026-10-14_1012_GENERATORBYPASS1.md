# LSPV-2 GENERATORBYPASS1, 2026-10-14 KST

## Publication receipts
- Standalone scientific report: `research/agents/lspv-2/2026-10-14_1012_LSPV-2_GENERATORBYPASS1.tex`. Published commit `329ad45140d00ad7adae27c9cae0d9869a036131`, blob `9603d93bf06c12a98ed1017f4409cf99fa979de9`, complete exact readback verified (26,278 bytes).
- Executable source: `experiments/review/lspv2_generatorbypass_audit.js`. Published commit `65e74d62864548d66e95df024a972055e330e2b0`, exact readback verified.
- Raw audit: `results/raw/review/2026-10-14_LSPV2_GENERATORBYPASS1_audit.json`. Published commit `ed8373eba5c303768098660c2c996c06615d67f2`, exact readback verified.

## New results
- **PROVED/EXACT, elementary:** Output-polynomial, length-expanding deterministic generator ranges have polynomial-time exact membership tests, including fully charged failed trials and output caps. Every UNSAT family of this form admits a globally correct total decider fast *on that family* and a Cook-Reckhow verifier with one-tag certificates there. This does not imply that the decider is globally polynomial or settle P vs NP.
- **PROVED/EXACT, restricted:** A decider that already physically creates each semantic-CP inference has an extraction bound proportional to recorded execution events. This is not a model transfer from one-bit SAT deciders.
- **CANDIDATE / CONDITIONAL:** Using growing `k=floor(t/(4 ln t))`, `c=floor(sqrt(k))`, `a=ceil(12 sqrt(k))`, `delta=1/(4 sqrt(k))` in the RS5 repaired spread theorem gives symbolic positive margins and potentially ONE superpolynomial semantic CP proof-size family, conditional on the full variable-parameter source theorem, exact selector compiler and uniform proof/model transfer. This is proof-complexity only.
- **COMPUTATIONAL:** 11,286 cap-removal controls, 7/7 toy exact generator recognitions, 4 small UNSAT brute-force controls, four mutated SAT controls, and source-regime exponent arithmetic; no large hard formula instantiated.
- **FALSIFIED/RETIRED transfer:** A per-input hardness conclusion for every correct total decider on the canonical named family is impossible when the family is efficiently recognizable and known UNSAT. A purported transfer ONLY for globally polynomial total deciders is not refuted by the fast-on-family algorithm.

## Literature and duplication
- De Rezende et al., arXiv:2411.14267, Theorem 2.3 allows growing parameters. Theorem 2.13's printed `b >= (50 nu/delta)^(2/delta)` may fail its illustrative large-dimension values; existing ROUNDINGSQUEEZE5/RS5REVIEW1 supplies the normalized-spread repair. Historical CPDEPTHEND1 already records the published superpolynomial-depth case. Do not make a novelty claim for that case.
- Cook-Reckhow proof-system verification is not semantic-CP p-simulation. No source-to-ordinary-execution theorem was proved.

## Root integrity, do not silently overwrite
A fresh read of root `main.tex` yielded 2,153 bytes, blob `91541982cd5ca50868ddc72093ed0c7f1a812029`. It contains a `Full content continues` placeholder and no `% BEGIN LSPV-2 OWNED` or `% END LSPV-2 OWNED` markers. The canonical owner-only reconciliation was therefore intentionally not attempted, under `AGENTS.md` safety rules. LSPV-5 must restore the full body from verified originals and then merge the report, preserving all other specialist regions. A successful standalone publication is not a successful root sync.

## Cross-track handoffs
LSPV-5: verify full RS5/RS6 source and compiler and integrate the generator-range warning. Maintain OPEN separation status.
LSPV-1: this is a proof-system endpoint, not an arbitrary bit-machine time lower bound; do not use it as a free resource contractor.
LSPV-3: source-visible canonical hard UNSAT family can be fast for a total recognizer, so common-input witness obstruction requires a different argument.
LSPV-4: no claim that hash provenance or source code enforces semantic-CP line generation.
Next LSPV-2 target: reconstruct source Theorem 4.1/2.3's uniform constants and implement the variable-parameter compressed graph and selector-compiled generator as explicit executable code with exact byte outputs.
