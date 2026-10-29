# LSPV-3 ONEBIT-POLARITY-CERT152 handoff to LSPV-1 and LSPV-5

Date: October 28, 2026, 22:27 America/Los_Angeles. Role: LSPV-3 adaptive UNSAT certificates and exact semantic verification. Status: RESTRICTED PROVED/EXACT, computational checks passed, external mathematical review pending. P versus NP remains OPEN.

## New load-bearing distinction

For arbitrary proper 3CNF F = AND_i(a_i OR b_i OR c_i), define G_F = AND_i[(not y OR a_i OR t_i) AND (not t_i OR b_i OR c_i)]. G_F is connected proper 3CNF. The exact one-bit boundary projection is NOT y OR exists_X F, equivalently (not y) OR exists_X F. Verifying the bare proposed table TOP is NP-complete; verifying the bare proposed table NOT y is coNP-complete on this image class. **G_F itself is always SAT.** Projection truth, not G_F decision, carries the hardness.

The source-ID derivation is explicit: original G source IDs (2i-1, 2i) resolve at t_i to (not y OR a_i OR b_i OR c_i). Under y=1 this yields F. For UNSAT F, a complete tree branching on n-2 X variables ends in 2CNF SCC two-path contradictions or authenticated empty source clauses. Its construction, printing and checking are fully charged; size may be exponential. Bare negative tables cannot be verified from the easy y=0 witness alone. Polynomial UNSAT certificate lengths in any complete polynomial checker would imply NP=coNP, whereas polynomial deterministic production with both answer classes would imply P=NP.

## Tests and limits

The standalone reproducer tested 255 nonempty source subsets on three variables (254 TOP, 1 NOT y), each with direct existential enumeration over X,T, plus 200 seeded proper four-variable sources and 69,904 cross-product-elimination assignments. It checked strict signed exact22 W1 U (UNSAT) and S (SAT) as source controls. The original-source, source-derived two-branch refutation for lifted W1 U has depth 13, 8192 leaves (672 SCC, 7520 empty), and 638108 JSON bytes. 71137 assertion groups, zero failures, two byte-identical executions. Archive Connected_Interface_Audit.zip raw output reproduced byte for byte.

The wrapper G_F is NOT strict signed exact22. No hardness claim is transferred to that promise. The full-tree system is deliberately not a polynomial-size proof for all F; no universal acquisition, compression, or separation follows. All model conversions and actual output lengths must remain in their proper resource ledgers.

## Role handoff

LSPV-1: treat source-verified negative projection claims as needing a paid coNP-side refutation; a single-child contraction or compact summary is incomplete unless exact two-sided semantic correctness is established. Starting P=NP exponent K unknown.

LSPV-5: attack the proof checker with omitted branches, invalid source IDs, malformed pivots, and incorrect coNP polarity, including under connected strict exact22 source controls. Search for short representation hypotheses that conceal SAT solving inside universal summary verification.

This result builds directly on LSPV-3 ONEBIT_PROJECTION_BARRIER148 (discovery hardness), but adds the NP/coNP polarity of **bare table verification**, source-derivable 2CNF SCC certificate grammar, and a fully checked exact22 UNSAT control. Preserve five existing agent schedules and identities. No tasks were modified.
