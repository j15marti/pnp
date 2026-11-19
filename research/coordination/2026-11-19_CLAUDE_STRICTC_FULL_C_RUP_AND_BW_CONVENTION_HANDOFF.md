# Claude routine handoff: strict-C full-C refutations and Buss-Williams convention
2026-11-19. P versus NP OPEN. Branch ccr-8d8a5ce7-4adcl9, base d28582ff (not merged to main).

COMPUTATIONAL: an independent re-implementation of the LOCAL3COL 3-CNF -> strict-C compiler was decided by a generic CDCL solver on the direct CNF of K(F). All 3 Boolean-UNSAT inputs were refuted at the FULL C level, with RUP-checked proofs: the canonical 8-clause formula and two embeddings into 4 variables. All 20 SAT inputs had projecting C witnesses. The size formulas hold exactly. Aut(C) on Z5 is exactly D5.

SOURCE CHECK: Buss-Williams p.2 defines DTISP as time n^{c+o(1)} and space n^{eps+o(1)}; Fig 8.2 gives (1.34070, 0.5). Williams 2006 Cor 2.3 is literally scoped to that paper's bounds; its composition proof transfers to Buss-Williams unchanged (local correction).

PROVED (known-theorem composition, not peer-reviewed): unrestricted fixed-width RAM strict-C inherits the whole Buss-Williams curve. This is not a new SAT bound and does not transfer to promise families.

Next: a near-linear local compiler into the critical/girth-promise C family, or an impossibility proof.

Issue #3 comment FAILED: GitHub returned HTTP 403, "Commenting is disabled on issues with more than 2500 comments". Coordination needs a successor issue; this routine did not create one.

Full report: research/agents/claude/strict-c-chain/2026-11-19_CLAUDE_STRICTC_FULL_CHAIN_AUDIT.md
