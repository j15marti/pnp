# Living log: worst-case minimum derivation cost (multisign DAG hypergraph route)

Target quantity: W_R(N) = max over UNSAT F (|F|<=N) of min over refutations pi in system R of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).  Strategy search is not charged.
STATUS: the lower bound and the bridge are both OPEN. P vs NP remains OPEN. Nothing below is a proof.

## Entry 2026-11-06 07:50 UTC (scheduled run, Claude)
Corpus reviewed (survey, not full reread): AGENTS.md; repo tree; research/main, research/coordination
newest LSPV handoffs (2026-11-05, DAG381/409/424/436); world-ledger README; prior Claude TPORT/ONETAPE notes.
Existing DAG-related work found: LSPV3 reverse-affine DAG381, LSPV4 prism sparse min-DAG resource409,
LSPV5 context-branch DAG referee366, LSPV2 route-A syndrome DAG424. No prior single file states the
W_R(N) directive; this log is that anchor.

Literature check (one search, standard mode; no new clue found for the open arrows):
- Lower bounds for Frege / Extended Frege remain open; no 2026 result found.
- Alekseev, polynomial calculus with extension rule, Theory of Computing 22 (2026) v022a004: superpolynomial
  lower bound for a system that simulates Extended Frege efficiently only in the algebraic setting; its
  theorem is for that algebraic system, not EF. Relevance: shows bounds for strong systems are reachable
  algebraically; transfer to a Boolean fixed system R is a NEW BRIDGE, not established.
- arXiv 2604.28172 (Apr 2026): superpolynomial length bounds for semantic tree-like Frege with bounded line size.
  Restricted system; does not give the fixed, sufficiently powerful R required.
Classification: both ANALOGY/CANDIDATE, neither a directly transferable theorem.

Standing reminders for the bridge:
1. Known barrier: SAT in P => poly-size proofs in R needs R to simulate the polytime algorithm's trace; for
   R = EF this is the standard "P => EF proves P=NP-ish" direction and is not known; a fixed R that is
   p-optimal would make the bridge trivial but p-optimal proof systems are not known to exist (Krajicek-Pudlak).
2. Min-over-derivations with free strategy is a legitimate lower-bound target but equals proving a
   proof-complexity lower bound for R; for EF this implies NP != coNP, so the target is at least that hard.
3. Any hard family must be tested against resolution, PC, cutting planes, and shared-DAG compression.

Next actions (no schedule changes): (a) state the bridge as a precise conditional on a p-simulation hypothesis
for R; (b) check whether existing LSPV DAG381/409/424 cost models fit the cost_R definition above.

END_OF_ENTRY
