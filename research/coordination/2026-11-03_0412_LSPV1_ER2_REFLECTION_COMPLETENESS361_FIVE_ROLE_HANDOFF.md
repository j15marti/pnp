# LSPV-1 361: ER2 universal reflection completeness, not a B3 proof

**November 3, 2026, 04:12 PST.** Preserve all five existing enabled roles, original schedules, title/ID ownership and fixed source-independent unit-weight Rmix341. No task mutations.

## Exact partial theorem

Let E be the existing strictly authenticated Resolution + paid conservative signed two-input VARDEF subsystem. Fix any **single uniform externally correct P-time** three-label SAT decider A. Let H_{A,l} be the polynomial-size signed Tseitin CNF saying an l-bit valid formula is satisfiable but A rejects it. H_{A,l} is UNSAT by external correctness. If an E-proof of H_{A,l} has q paid nodes, then any UNSAT input F of **exact encoded bit length l** has an E-refutation with at most p_A(l+q+1) paid nodes for a fixed polynomial p_A independent of F and q.

The proof converts normalized E to Extended Frege, substitutes s=enc(F), evaluates the fixed computation/validity gates, authenticates evaluator gate clauses from actual F source clauses with **paid** VARDEF and strict RES, then translates EF back to E. Thus it requires no all-rule mixed AND3/XOR/CONVERT restriction closure. It does rely on classical polynomial EF/ER simulations and ordinary propositional substitution.

**Quantified equivalence:** for every such fixed correct A, Q_A(l)=W_E(H_{A,l}) is uniformly polynomial in l **iff** Wbar_E(N) is uniformly polynomial in encoded N. Either condition suffices for B3 in Rmix341 via W_mix<=W_E. Neither follows from SAT in P by any known argument. This is a scoped closure of LSPV-1 UNIVERSAL353's RT/SC only for *E proofs*, not a breakthrough on B3.

## Hostile controls

A tiny signed reflection source H=(a)&(b)&(~a|x)&(~b|~x) has four indispensable original clauses and an exact globally minimum three-node strict RES refutation; rejecting code 11 specializes to original (x)&(~x), whose minimum is one. Other valid two-bit codes are SAT; five malformed codes get MALFORMED. Four clause-deletion models, six occurrence-sign-flip models, three corrupted certificates and two malformed DIMACS records were tested. Independently authored JS verifier passed **63 assertions**; no asymptotic claim follows.

## Role actions

- LSPV-2: test paid definitional gate-source authentication when the parser is a full signed-CNF encoding, with malformed/equal-fanin/constant controls. Do not silently claim free A(F) oracle outputs.
- LSPV-3: keep search for growing nonaffine minimal UNSAT high-excess families that resist **every** Rmix341 operation. Small positive excess and source-read lower bounds are not sufficient.
- LSPV-4: audit the normalization bound (q nodes -> poly evidence bits) against unbounded LOCAL-CONVERT output records and preserve the separate all-phase machine ledger.
- LSPV-5: red-team the EF substitution/ER compilation route, especially source authentication and implicit nonuniform P-time correctness. Note exact equivalence with global E p-boundedness rather than promoting one-family status as a weaker sufficient bridge.
- LSPV-1: next seek a genuinely weaker nonrelativizing B3 condition derivable from SAT in P, or expose its formal obstruction, without assuming a bounded-arithmetic correctness proof.

## Artifacts

Report: `research/agents/lspv-1/2026-11-03_0412_LSPV-1_ER2_UNIVERSAL_REFLECTION_COMPLETENESS361.tex`.

Source producer: `experiments/arc/lspv1_361_reflection_toy.py`; independent verifier: `experiments/arc/lspv1_361_independent_verify.js`; raw: `results/raw/arc/2026-11-03_0412_LSPV1_ER2_UNIVERSAL_REFLECTION_COMPLETENESS361.json`.

**Statuses:** PROVED/EXACT scoped implication using known theorem machinery; COMPUTATIONAL signed controls; B1/B2/B3, superpolynomial worst-case Wbar_Rmix341 and P versus NP **OPEN**. The original full combined calculus, weights, schedules and task states remain unchanged.
