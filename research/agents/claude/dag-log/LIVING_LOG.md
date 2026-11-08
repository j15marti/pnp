# Living log: worst-case minimum-derivation program (DAG proof routine)

Directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
Target: superpolynomial lower bound on Wbar_R(N) for a fixed R, plus bridge B3 (SAT in P => Wbar_R poly).
**P versus NP remains OPEN. B3 is unproved. No hard family for a fixed combined R is proved.**

## 2026-11-08 04:48 UTC (scheduled run)
- Survey: existing worst-case work in `research/agents/lspv-1` (335, 350, 395), `lspv-4` (341, 409), `lspv-3` (381, 446), `lspv-2` (424), `lspv-5` (294, 366), coordination handoffs through 2026-11-07 (470, P2 outbox items). No new proofs added this run.
- Literature check (status: CONTEXT, not transfer): no new Frege/Extended Frege lower bound found in a single search.
  Related items: Khaniki–Pich–Sokolov, "Efficient Adversaries", CCC 2026 (constructive lower bounds; EF conditional separation of canonical pair);
  Alekseev, polynomial calculus with extension rule, Theory of Computing 22 (2026); Metamathematics of Resolution Lower Bounds, arXiv 2411.15515.
  Classification: ANALOGY needing a new transfer theorem. Relevant to B3: the constructive/"efficient adversary" view is the closest literature
  to the reflection/translation step that B3 needs (computation-to-proof with provable correctness); the missing theorem is that for the preselected R the
  correctness of an arbitrary poly-time SAT decider is provable in R with poly overhead (not just in some proof system).
- Reminder from 395: Wbar_R can be a noncomputable function for a contrived R; hardness claims must be for a natural, fixed R.
- Next step: audit whether KPS "efficient adversary" formalization yields a usable B3 for a fixed R; otherwise record B3 as the sole gating gap.
