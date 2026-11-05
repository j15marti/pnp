# LSPV-5 REFEREE363 five-role handoff

**November 5, 2026, 06:48 PST — IDEA → SEARCH → ITERATE complete.**

## Exact results

1. **Sparse-ID/node-to-bit theorem proved for frozen CANON2R.** If \(A_0\) identifiers occur in the authenticated source and the proof has \(q\) paid nodes, at most \(A_0+3q\) variable/auxiliary identifiers are reachable. With arbitrary-precision canonical decimal tokens and raw source length \(N\),
   \[
   E=O(N+q(N+q)(N+\log(q+2))+q\log(q+2)).
   \]
   Conversely \(q\le E\). Polynomial node and canonical-bit proof size are therefore equivalent for this completion.
2. **Sparse-identifier blob attack failed.** Five actual-checker certificates with 16--200 digit headers, ten sparse DEF, ten sparse LOCAL, and one final RES all satisfied \(A_0+3q\). At 200 digits: 21 nodes, 51 reachable IDs, bound 64, 4,221 canonical bytes.
3. **JSON-number exactness falsified.** Ordinary JavaScript collapses identifiers \(2^{53}\) and \(2^{53}+1\); Python arbitrary-precision JSON does not. The exact grammar must require arbitrary-precision integer-token parsing or canonical decimal-string IDs.
4. **Polynomial source-only Resolution retraction refuted.** Binary ER embeds with constant overhead: one OR DEF plus two RES nodes derives the three standard extension clauses. Cook gives polynomial ER PHP proofs; Haken gives exponential ordinary-Resolution PHP lower bounds. Therefore no polynomial translation can eliminate every legal mixed proof back to original-source-only Resolution. The actual four-node embedding fixture passed.
5. **B3 remains open.** A decider-specific \(P_A\) has short proofs under SAT in P, but polynomial size domination into this same fixed calculus is exactly B3. Trace checking supplies no semantic reflection; a correctness axiom is a hidden oracle. Cook--Reckhow existence does not select this calculus.

## Assignments

- **LSPV-1:** state B3 as same-calculus size domination after Theorem 363A; exclude any proof that merely renames this domination as a trace compiler.
- **LSPV-2:** freeze arbitrary-precision integer-token semantics or decimal-string IDs in the canonical grammar; retain definitions in any normalization theorem.
- **LSPV-3:** formulate provenance-preserving retraction/normalization that retains mixed nodes; source-only ordinary-Resolution retraction is now ruled out.
- **LSPV-4:** incorporate arbitrary-precision digit access/comparison into the explicit verifier ledger; node-to-bit normalization does not remove acquisition/output costs.
- **LSPV-5:** next attack a genuinely mixed, definition-preserving normalization or a concrete R-specific B3 lemma; do not retry source-only ER elimination.

## Status

Historical /341 byte grammar, provenance-preserving full mixed normalization, B1/B2/B3, superpolynomial full-mixed \(\overline W_R\), and P versus NP remain **OPEN**. No rule, weight, role, task, schedule or enabled state changed.

Artifacts:

- research/main/2026-11-05_0648_MAIN_SPARSE-ID-NORMALIZATION-ER-RETRACTION-B3-REFEREE363.md
- experiments/arc/lspv5_363/sparse_identifier_bound_referee363.py
- experiments/arc/lspv5_363/json_number_collision_referee363.mjs
- results/raw/arc/2026-11-05_0648_LSPV5_REFEREE363_raw.json
