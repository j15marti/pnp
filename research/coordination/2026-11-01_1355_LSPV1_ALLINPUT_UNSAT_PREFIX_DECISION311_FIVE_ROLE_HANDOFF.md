# LSPV-1 to five existing roles: ALLINPUT-UNSAT-PREFIX-DECISION311
**November 1, 2026, 13:55 PST. Status: PROVED/EXACT scoped theorem, COMPUTATIONAL no-import controls, external referee pending. All-input P versus NP OPEN.**

## Exact obstruction and completed theorem
The established near-linear full-source payload observation floor in LSPV-1 310 applies only to valid **SAT** originals when malformed strings must reject. Valid **UNSAT** originals can be rejected with dramatically less source reading because malformed and UNSAT are both reject labels.

Fix the independently certified canonical 198-variable/264-clause UNSAT original U198. For each t>=0, append t disjoint nine-variable F9 source copies after all 264 U198 original clauses. The resulting valid original F_t has n=198+9t, m=264+12t and is UNSAT. A **single fixed**, all-binary-input-correct deterministic program first decodes gamma(n),gamma(m) and checks the U198 source prefix. On success, it rejects without checking the tail; on failure, it authenticates the full grammar and exhaustively decides. The prefix is sound even if the unread tail is malformed. No recovered assignment, syntactic pin key, free semantic representative or best-policy oracle is needed.

Under the source encoding used in LSPV-1 310, the complete source length is N_t=|gamma(n_t)|+|gamma(m_t)|+m_t*(1+3*bit_length(n_t)). The exact inspected bit count on F_t is q_t=|gamma(n_t)|+|gamma(m_t)|+264*(1+3*bit_length(n_t))=O(log N_t). A conservative native indexed multi-tape implementation uses O(log^2 N_t) time and O(log N_t) simultaneous writable/index bits **on this family only**. At t=256 the complete source has 123478 bits but the uniform machine reads only 9814 bits.

This is distinct from historical POINTINF1 (nonuniform, one enormous per-length machine). It **falsifies** any proposed for-every-valid-UNSAT-instance Omega(N^epsilon) work or full-grammar-scan lower bound, even for one fixed correct all-input machine. It does **not** refute a worst-case lower bound with forall D exists arbitrarily large hard F, does not establish a polynomial total-work solver, and does not transfer numeric FLMV.

## Verification and repository artifacts
The complete fresh old independent U198 refutation replay passed 6717 assertion groups, 64 separator rows, 152 module calls, and 493674 bitmask-DPLL nodes. New producer + separate no-import checker reconstructed target sources and checked 6466 independent assertions, F9 70 and Y6 20 full models, same-original F9 SAT/UNSAT partial cubes 2/0, all 264 original SS/SU/US/UU modes, all 6144 complement identities and malformed-suffix early rejection. Exact source-probe cases t=0,1,2,4,8,16,64,256 are in raw JSON. These are byte probes, **not** a native FLMV transition trace.

[Formal role theorem](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-01_1355_LSPV-1_ALLINPUT_UNSAT_PREFIX_DECISION311.tex) · [Runnable uniform full-decider producer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_311/decision_unsat_prefix311.py) · [No-import independent verifier](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_311/verify_decision_unsat_prefix311.py) · [Machine-readable raw](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-01_1355_LSPV1_ALLINPUT_UNSAT_PREFIX_DECISION311_summary.json).

Root main.tex LSPV-1-only append reconciled and exact-readback verified at commit 5ee264cb25b06348936bfae89147ab7ab864902d. All five marker pairs were preserved and every byte outside the inserted LSPV-1 material was identical.

## Next obligations by existing role
**LSPV-1 Formal Proof Lead:** Quantify worst-case total decision work with a fixed decider and potentially hard valid originals, not every-input grammar/UNSAT floors. Retain signed source and proof-carrying typed AND/OR recurrence, unknown K,L, and separately numerical FLMV.

**LSPV-2 Circuit/Reduction:** Investigate whether the absorbing UNSAT-core prefix survives canonical reordering and source-matching under a paid recognizer, and measure actual worst-case overhead; do not claim all inputs have such a core.

**LSPV-3 Certificate Theorems:** Study exact source-authenticated short contradictory subformula detection and distinguish provable acquisition cost from the existence of a small UNSAT core; retain both-label controls.

**LSPV-4 Resource Auditor:** Translate the prefix comparison to actual indexed read-only input and head/index tapes; test DELAY/COPY/RECOMP wrappers, program-size fixed constants and simultaneous space. The grammar floor cannot extend to every UNSAT rejecting execution.

**LSPV-5 Red Team:** Verify source U198 certificate and bit-position/order details; attack all-native-machine bounds and any implicit post-decision oracle; distinguish the present infinite fixed-machine family from old per-length hardwiring.

**Global status:** The universal all-input polynomial-work controller, arbitrary-correct-decider hereditary A-to-Phi(A) power-short construction, and strict same-machine quantitative FLMV reduction/transport remain OPEN. P versus NP remains OPEN. Exactly five existing tasks, enabled states, titles and hourly Pacific stagger unchanged; no task management action taken.
