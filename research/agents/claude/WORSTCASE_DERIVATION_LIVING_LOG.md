<!-- CLAUDE LIVING LOG::WORSTCASE-0001::2026-11-07 -->
# Living log: worst-case minimum derivation cost (B1/B2/B3)

Additive reference log. Changes no schedules, roles or allocations. **P versus NP remains OPEN.** Nothing here is a new proved result.
Directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
Newest role evidence: LSPV-3/471 (Horn shared-DAG exact minimum, [P2-L3-471]); LSPV-4/465 (TREE3 checkpoint Pareto).

## Entry 2026-11-07 (Claude, WORSTCASE-0001)

**Status of load-bearing arrows (unchanged):** lower bound on W-bar_R (superpolynomial, fixed combined R) OPEN; bridge B3 (SAT in P => W-bar_R poly) OPEN. B1 refuted for ordinary resolution (parity recognizer + fallback); B2/B3 not refuted by that.

**Corpus check:** the reflection route to B3 is already covered by LSPV-1/353 (one universal soundness CNF H_{A,l}; conditional on RT+SC), /398 (resolution back-translation firewall), /405. No duplicate formulation added.

**Classification of the obstacle (KNOWN, no new claim):** for a fixed R, B3 needs an effective, charged translation from "A is a correct poly-time SAT decider" to R-derivations of every UNSAT instance. The standard route (Cook's PV/EF correspondence; Krajicek-Pudlak) needs the correctness of A to be provable in the theory matched to R. Mere existence of A does not give it. This is exactly the RT+SC gap in LSPV-1/353 and the "reflection assumption" the directive asks to be stated.

**Literature check (2026-11-07):**
- Alekseev, polynomial calculus with extension rule lower bound (CCC 2021; Theory of Computing 22, 2026): https://theoryofcomputing.org/articles/v022a004/ . Exponential bound for a system simulating EF-style extension in the algebraic setting; not a bound for EF/Frege. Relevance: supports testing hard families against algebraic+extension mixes (assignment: Hypergraph & Certificates, Red Team). Transfer type: analogy, needs a bridge to the fixed mixed R.
- Pich-Santhanam, ECCC TR23-199: https://eccc.weizmann.ac.il/report/2023/199 . Conditional link: lower bounds for EF plus witnessing axioms imply SAT circuit lower bounds. Relevance: closest published statement tying a proof-system lower bound to a circuit-complexity conclusion; compare its hypothesis (witnessing formulas are tautologies) with B3's reflection premise. Transfer type: analogy; direction is lower-bound => circuit lower-bound, not P != NP.
- arXiv 2604.28172 (Apr 2026): superpolynomial lower bounds for bounded-line-size semantic tree-like Frege. Restricted system; shows restricted-line-size is the frontier, so it does not touch unrestricted R. Failed transfer to unrestricted R.
- No 2026 result found giving a superpolynomial EF lower bound or a proof of B3.

**Next small targets (suggestions only):** (1) state B3's premise for R=EF as a PV-provable-correctness hypothesis and record that it is stronger than SAT in P; (2) compare Pich-Santhanam witnessing-axiom hypothesis with the RT+SC obligations of LSPV-1/353.

<!-- END_OF_VERIFIED_LOG::WORSTCASE-0001 -->
