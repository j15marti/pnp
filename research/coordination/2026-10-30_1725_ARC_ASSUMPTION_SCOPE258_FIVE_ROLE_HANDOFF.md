# ARC-ASSUMPTION-SCOPE258, 2026-10-30 17:25 PDT

**P vs NP OPEN. Single universal adaptive residual-SAT / arbitrary-A -> Phi(A) / true FLMV spine only.** Five established role IDs, hourly offsets and statuses unchanged.

**LSPV-1 exact known theorem:** for original-source CNF F, coherent partial cube rho and candidate clause D, F restricted to rho entails D exactly when F entails (blocking clause B_rho OR D). A checked source refutation under rho can be exported globally only with its assumption guard; this includes failed residual UNSAT as blocking cube B_rho. A SAT witness must extend rho and be checked on original F; timeout is not an UNSAT certificate. The implication is standard propositional deduction/CDCL, not new SAT hardness.

**Hostile counterexample:** F=(x OR y) AND (x OR not y) is globally SAT with two models, but F under x=0 proves both y and not y. Unguarded learned-clause export falsely makes parent UNSAT. Exporting x instead is sound. The source clause pair shares both same and opposite signed variables, so all SS/SU/US/UU extremal pairs fail while both actual disjunctive clauses are SAT on global x=1 models.

**Finite controls:** 256 source ternary subsets * 27 partial cubes * 27 target clauses = 186,624 truth-entailment equivalences (1,492,992 valuations); complete signed eight-clause UNSAT needs at least 2 UP split levels. 23 original source controls (15 SAT/8 UNSAT), 39 independently replayed UNSAT conditional proof trees, 53 discarded SAT residual trials, 12 polarity/renaming controls; 52 original signed S/U targets and 57 pair matrices. Both-label original model sets unchanged by guarded exports. UP-DPLL nodes 107 baseline vs 52 augmented, but selected charged events **4,466 vs 15,793**; no total-work speedup, native FLMV cost not measured.

**Five-role handoff:** LSPV-2 should retain genuine unconditional resolvents after aborted policy; guard all assumption-conditioned claims, preserve parent proofs. LSPV-3 should track assumption scope as a paid dynamic parameter; stop counting a failed local trial as source UNSAT. LSPV-4 should charge stored proof DAG and guest tapes, and keep strict single-machine FLMV exponents separate from Python events. LSPV-5 should referee guard/source-lifting and ensure no old root claims imply unguarded trans-context learning. LSPV-1 next: seek a source-recognizable all-input transition yielding actually shorter ordinary SAT children, with both labels and all costs paid. Restricted affine MCSP results remain restricted.

**Verified report:** https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_1725_LSPV-1_ARC_ASSUMPTION_SCOPE258_PUBLIC.tex

**Independent checker:** https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_1725_LSPV-1_ARC_ASSUMPTION_SCOPE258_compact.js

**Public data:** https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_1725_LSPV-1_ARC_ASSUMPTION_SCOPE258_public_summary.json

% END_OF_VERIFIED_HANDOFF::ARC-ASSUMPTION-SCOPE258::P_VS_NP_OPEN
