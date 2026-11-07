# Living log: worst-case minimum-derivation program

Directive (user, scheduled): study
  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi : F |-_R bot} cost_R(pi)
with the optimal derivation chosen for free; priority bridge
  B_R :  SAT in P  ==>  W_R(N) <= poly(N).
Five roles: General Lower-Bound Lead, SAT-Circuit Reduction Builder, Hypergraph & Proof Certificates,
Time-Space Resource Auditor, Independent Red Team. P vs NP remains OPEN. Nothing below is a lower bound.
Append-only; newest entry last. Status labels per AGENTS.md.

## 2026-11-07 entry 1 (Claude, scheduled run)
Report: research/agents/claude/2026-11-07_CLAUDE_WORSTCASE-BRIDGE-0001.tex
Findings (details and proofs in report):
1. PROVED/EXACT: if W_R is already known superpolynomial (Resolution, CP, bounded-depth Frege), B_R is
   logically equivalent to SAT not in P. It cannot be used as a route to P != NP; it *is* P != NP.
2. PROVED/EXACT: for a Cook-Reckhow R, W_R poly <=> UNSAT in NP-with-R-proofs; and B_R <=> (P=NP => R p-bounded),
   because P=NP already gives NP=coNP. So B_R is non-circular only for R with no known unconditional bound
   (Frege, Extended Frege, ZFC-like). For those it is OPEN (no known proof).
3. CONDITIONAL/KNOWN (Cook 1975 style): if some poly-time SAT decider has correctness provable in PV / S^1_2,
   then EF is p-bounded. So B_EF is implied by "P=NP via a provably-correct algorithm"; not by P=NP alone.
4. PROVED/EXACT: dropping the soundness-over-all-inputs requirement collapses min to O(1) (free semantic
   answers; retired route). Any admissible R must charge a poly-time proof-verification predicate.
5. Consequence for the strategy: a lower bound for one fixed R proves P != NP only through B_R, which needs R
   strong enough that a fast SAT algorithm would be simulated. Equivalent target: a lower bound for a proof system
   that is p-optimal-for-all-poly-algorithms -- i.e. the Krajicek-Pudlak optimal proof system question.
Literature clues checked (2026-11-07): instance complexity (Ko-Orponen-Schoening-Watanabe; Fortnow-Kummer: NP-hard
sets have p-hard instances unless P=NP) -- relevant: pointwise min-over-programs is instance complexity, and the
known hard-instance results are conditional on P != NP (circular). Proof Analysis Problem (Arteche et al., FOCS 2025):
P=NP implies automatability of every proof system -- consistent with item 2, but automatability != p-boundedness.
Next targets: (a) decide whether B_EF follows from P=NP via a reflection-principle argument, or find an oracle/
model where P=NP and EF not p-bounded (Red Team); (b) formalise "multisign DAG hypergraph" derivation cost as an R
and check which known simulations it admits (Reduction Builder); (c) audit encoding overhead (Resource Auditor).
