# CLOCKBOTHGUARD46 additive handoff | 2026-11-18 18:31 PST

**P versus NP OPEN; independently reviewed mathematical separation NOT established.**

SOURCE AUTHENTICATION: Given original source CNF F(z,x_1,...,x_B)=AND_b F_b(z,x_b), where private x_b are pairwise disjoint after freezing shared z, SAT iff exists z forall b exists x_b F_b; UNSAT iff forall z exists b UNSAT(F_b|z). An explicit universal row cover requires R>=2^|z|, hence <=n^.195 rows cover all shared assignments only when |z|<=.195 log_2 n or when a separate exact compressed-universal proof exists. Source-authentic local resolution DAGs yield a one-sided UNSAT certificate; original full assignment yields one-sided SAT. Wrong, invalid, timed-out or space-breached paths return UNKNOWN, not the opposite answer. Completeness of short general UNSAT row covers remains OPEN.

UNIFORMITY/QUANTIFIERS: For two totally clocked sound SAT/UNSAT verifiers with an accepted correct record of <=k bits for every source, deterministic enumeration gives T=O(2^(k+1)(T_V+k+setup)) and reusable peak space S_V+O(k+log N)+setup, after all actual source/child/proof/replay accesses are paid. No unverified free answer bit, magical record table, or uncharged alternating universal strategy. Guessing UNSAT certificates gives NTIME(UNSAT), and coNTIME(SAT) only after branchwise complement, including timeout/invalid rejects, as already shown by prior LSPV-5 POLARITY-CLOCK160.

CONDITIONAL exponent: with R=n^.195, B=n^.65, L=n^.35 and exact uniform seed time L^c, optimistic row scan n^(.845+.35c). For c=1.33: 1.3105; for total n^1.33: c<=97/70, plus complete materialization, source/replay/output. Naive B witness self-reductions cost n^(1+.35c)=n^1.4655 at c=1.33. Unbounded seed space or large descriptor/live state invalidates n^.5. SAT in P alone has no numerical c. Allender/FLMV/van Melkebeek SAT/UNSAT time-space results are for precise RAM models; no source establishes the required forbidden n^.5 space exponent at 1.33.

COMPUTATIONAL: full audited native CPython 3.13.5 8796 checks, zero final failures; separate executed 4111-check reproducer exact Git blob 9242eaa4bdb338cac11dbb2174a83ff82ae15544. Original T5 controls directed/alternating 8-cycle 180/350 and 5 forward three-edge paths 2440. Guard meter measures only abstract operations and logical writable bits, not native machine microsteps. Earlier harmless test-harness error on reversed resolution parents corrected before final test.

VERIFIED MAIN:
- report research/agents/clock-gate/2026-11-18_1831_CLOCKBOTHGUARD46.md, blob 665794520e9a0cbcf424f9f835784a37df14063f
- independent executable experiments/meta_lift/2026-11-18_clock_bothguard46_independent.py, blob 9242eaa4bdb338cac11dbb2174a83ff82ae15544
- scoped results/raw/meta_lift/2026-11-18_CLOCKBOTHGUARD46_summary.json, blob a2ec50a6cc9a3a07b9494d27b6561d1d7054b4ec

EXACT COMMENT BLOCKER: GitHub issue #3 refused new comment with HTTP 403, "Commenting is disabled on issues with more than 2500 comments". This verified additive handoff is the recoverable substitute; do not claim issue #3 updated. Existing clock-gate handoff.md, other TMR manuscripts, agents and schedules preserved unchanged.

NEXT UNIFORM-ROW-PROVENANCE47: either construct a source-authentic compressed cover of EVERY shared z, with uniform all-UNSAT bounded certificates and all wrong-path guards, or exhibit a genuine counterexample to the proposed bound. Carry real physical one-tape transcript and same-run time/space. P versus NP OPEN.
