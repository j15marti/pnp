# Worst-case minimum-derivation program: literature-check log entry
Date: 2026-11-09 (scheduled run). Status: OPEN. P versus NP remains OPEN; no new lower bound or transfer theorem (B1/B2/B3) is claimed.

Target (unchanged, see 2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md):
Wbar_R(N) = max over UNSAT F, |<F>|<=N, of min over derivations pi of cost_R(pi); priority bridge B3: SAT in P => Wbar_R(N) <= poly(N).

## Literature clues checked this run (abstract level only; full proofs NOT verified)
1. Alekseev, polynomial calculus with extension rule (Theory of Computing 22, art. 4, 2026; https://theoryofcomputing.org/articles/v022a004/). Exponential lower bound for the binary value principle in PC with extension rule, a system that p-simulates Res-Lin. Classification: KNOWN THEOREM for that algebraic system only. Relevance: a lower bound that survives an extension rule and algebraic reasoning, which is the "survives alternative reasoning" test. The extension rule here is weaker than full Extended Frege and the cited hard formula is of binary value principle type, so it gives no bound for a mixed system containing Frege-style rules. Transfer to a fixed combined R: ANALOGY/CANDIDATE, needs a new theorem.
2. arXiv 2604.28172 (reported via secondary source): superpolynomial lower bound for tree-like semantic Frege with bounded line size, via a linear pseudo-measure. Classification: restricted model (tree-like, bounded line size), so it conflicts with shared DAGs and unbounded lines. Not a bound on the shared-DAG Wbar_R. Needs primary-source check before any use.
3. No Frege or Extended Frege superpolynomial lower bound found for 2026. Open problem, consistent with the repository status.

## Suggested follow-ups per role (candidate, unassigned)
- Red Team / Hypergraph: test whether the binary-value-principle hardness argument breaks under a sound auxiliary-definition rule that mixes in Frege-style steps.
- Lower-Bound Lead: record that B3 needs a computation-to-proof translation for the fixed R; Alekseev-style results do not supply it.

END_OF_LOG_ENTRY::WORSTCASE_LIT::2026-11-09
