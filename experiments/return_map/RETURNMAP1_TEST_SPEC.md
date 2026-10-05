# RETURNMAP1 test specification

Status: COMPUTATIONAL / CANDIDATE. P versus NP remains OPEN.

Purpose: attack any proposed source-specific relation R_ret(x,S,Q) before it is admitted to the proof spine.

Mandatory candidate record:
- exact input SAT size T and representation;
- exact SU/vMS state S and how it is acquired;
- exact ordinary-CNF Q and proof that x is satisfiable iff Q is satisfiable;
- zeta from actual written length |Q| = T^(zeta+o(1));
- number of inherited SAT calls and their maximum T-scale;
- construction, classification, setup, generator, writing and workspace exponents;
- SAME_REALIZATION identity and repeatability statement.

Tests:
1. TYPE: reject if Q is only an RMV child, extractor output, oracle-address list, Boolean-coordinate list, circuit, proof, or succinct descriptor without a proved ordinary-CNF conversion.
2. FULLCARRY: if Q or any inherited SAT query explicitly contains T^(1-o(1)) bits of the original formula, reject any claimed direct coefficient below one.
3. DELAY: if construction invokes the original SAT decider on T^(delta+o(1)) input, retain the delta*K term. Reject claims that erase K.
4. GENERICENC: if Q is obtained by generic encoding of a computation of time tau, charge the full encoding size. Robson gives O(tau log tau); RETURNSQUEEZE1 shows this is not the missing contraction.
5. QUERYVOLUME: for q=T^(eta+o(1)) explicit queries of size T^(theta+o(1)), charge eta+theta*K before recursive substitution.
6. CYCLE: scale-one edges are allowed only in a well-founded typed graph whose every complete return cycle has multiplicative scale gain below one and whose local costs are charged.
7. SUCCINCT: do not charge logical ambient size as materialization. Conversely, do not treat a pointer to a long formula as a short ordinary SAT query.
8. REPEAT: returned Q must satisfy the same eligibility hypotheses needed to apply R_ret recursively.
9. EASY: run Horn, dual-Horn, 2-SAT, affine/Tseitin, bounded-treewidth and independent-product controls. Compact return structure is not itself hardness.
10. ORACLES: rerun with maximal semantic and algebraic oracles. Identify the exact line that fails under replacement. If none fails, the candidate remains relativizing/algebrizing.
11. NORMALIZE: express every exponent on the original SAT-input T scale. In particular N=p^r=T^(nu+o(1)) must multiply source exponents by nu.
12. COMPRESSION-LITERATURE: Dell-van Melkebeek and Fortnow-Santhanam are conditional barriers and diagnostics, not terminal contradictions under P=NP.

Acceptance for the next stage requires all tests 1-12 to pass and a concrete zeta or typed cycle coefficient. Passing this battery is not a proof of hardness.
