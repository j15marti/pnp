# ARC-SOURCE-BLOCKER-COMPRESSION-FIREWALL232 — five-role handoff

Date: 2026-10-30 20:48 America/Los_Angeles. Role: LSPV-5 independent red team / synthesis. P versus NP remains OPEN. No task, schedule, identity, enabled state, or ownership changed.

## Exact result

Let `F` be an explicit CNF and let every learned clause `D_i` satisfy `F entails D_i`.

1. `F AND all D_i` is equivalent to `F`, but an append-only explicit encoding retains every source bit. It cannot be a physical `N^lambda` child for fixed `lambda<1`.
2. `B = AND_i D_i` is only a relaxation: `F entails B`. `UNSAT(B)` certifies `UNSAT(F)`, but `SAT(B)` does not determine `SAT(F)`.
3. Therefore a source-valid learned blocker is not automatically an exact shorter ordinary-SAT child. Source deletion requires an independently checked completeness/equivalence theorem.

## Matched counterfamily

For `b` disjoint triples, the SAT source has the seven clauses excluding assignments other than `111` plus a duplicate `000` clause in every block; it has unique model `1^(3b)`. The UNSAT source replaces the duplicate in its first block by the missing eighth clause. The pair has equal clause count and the same unsigned support multiset.

Both sources entail the same unit-blocker conjunction `x1 AND ... AND x_(3b)`, which is SAT. Every `xi=0` residual is UNSAT on both labels, but those cubes miss the all-one completion—the SAT witness for one source and the final conflict for the other. Exact residual answers and globally valid blockers still require a complete proof or exact uncovered fallback.

Independent checker: PASS, 822 assertions. At `b=5`, parent UP-DPLL selected work was 2,526/517 (SAT/UNSAT), while the residual-plus-completion controller used 20,355/8,251. These are host-language event proxies, not FLMV transitions.

## Peer reconciliation

- **LSPV-1:** ARC-AFFINE-CUBE-COVER261 is independently certified under its raw-syntactic-cofactor hypotheses. Its exponential cover count is valid but the affine source is directly easy, so no arbitrary-algorithm lower bound follows.
- **LSPV-2:** source-only assumption discharge is sound; blocker acquisition may be exponential, and appending the blocker does not shrink the source.
- **LSPV-3:** parity-moment camouflage is a sound selector falsifier; a paid signed-source scan and GF(2) elimination escape it.
- **LSPV-4:** ARC-COVER-GATE-SCOPE262 has valid report markers and resolves the predecessor publication issue. Its coNP cover reduction is correct. Its citation-scope correction is adopted: FLMV Theorem 3.4 is a specific Cook-formula local-generation simulation, not a generic arbitrary-child total-accessor theorem. The project head-shadow lemma is retained as an independently proved lemma under its stated accessor hypotheses.
- **LSPV-5:** reject any ARC step that silently replaces `F` by satisfiable learned consequences.

## Artifacts

- Report: `research/main/2026-10-30_2048_MAIN_ARC-SOURCE-BLOCKER-COMPRESSION-FIREWALL232.tex`
- Producer: `experiments/arc/2026-10-30_2048_source_blocker_compression_audit.py`
- Independent checker: `experiments/arc/2026-10-30_2048_source_blocker_compression_check.py`
- Raw: `results/raw/arc/2026-10-30_2048_source_blocker_compression_audit.json`
- Check: `results/raw/arc/2026-10-30_2048_source_blocker_compression_check.json`

## Next OPEN lemma

After source-valid learning, either construct a separately verified answer-preserving ordinary SAT re-encoding of physical length `N^(1/2+o(1))`, or close the source with a complete checked proof, while charging acquisition, failures, source reads, proof checking, output/access and simultaneous retained state in the native ARC/FLMV recurrence.

Publication/readback provenance: PENDING.
