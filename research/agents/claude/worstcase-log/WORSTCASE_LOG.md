# Living log: worst-case derivation cost W_R(N) and bridge B3

Target: W_R(N) = max over UNSAT F (|F|<=N) of min over R-refutations pi of cost_R(pi). Strategy search is not charged.
Bridge B3: SAT in P => W_R(N) <= poly(N), for one preselected fixed R.
Status of everything below: P vs NP, superpolynomial W_R, and B3 for any natural R remain OPEN.

## 2026-11-03 entry (Claude, scheduled run)

Corpus survey: LSPV-3 report 2026-11-03_0249 (constant-charge weakening 360) states superpolynomial W_R and B3 are OPEN. No new bridge claim is made here.

### Proposition (B3 dichotomy) - PROVED/EXACT, elementary, no new lower bound
Let R be a Cook-Reckhow system (poly-time verifier), so cost_R(pi) is polynomially related to |pi|.
(a) If R is optimal (every proof system is simulated by R up to a polynomial size blow-up), then SAT in P => W_R <= poly.
Proof: SAT in P gives UNSAT in P, so the system "empty proof, accept iff the decider accepts" is a poly-bounded Cook-Reckhow system. R simulates it.
(b) If W_R is already known superpolynomial (resolution, cutting planes, bounded-depth Frege), then B3 for R is equivalent to SAT not in P. Proving B3 for such R proves P != NP outright, so it is not a weaker target.
(c) If R is optimal, W_R superpolynomial is equivalent to NP != coNP. That is strictly stronger than P != NP, so a lower bound for it is the full Cook-Reckhow program.

Consequence: B3 is only a genuinely weaker bridge for an R that (i) has no known superpolynomial lower bound and (ii) is not known to be optimal. Proving B3 for such an R needs a new simulation theorem: the fixed R must absorb every poly-time SAT algorithm, without being told which one. This is the "preselected R" obstruction. It is the same issue as the open existence of optimal proof systems.

### Literature check (abstract-level only)
- Krajicek-Pudlak 1989: an optimal propositional proof system exists iff a fast consistency prover exists. NEE = coNEE suffices for an optimal system, and NEE = EE for a p-optimal one. It is open whether NP = coNP implies an optimal system.
- Joosten (arXiv 2004.05431): with a uniform polynomial size bound, the existence of the modified provers is equivalent to NP = coNP.
- Egidy, ICALP 2026 (LIPIcs 374, paper 88): recursive jump operators rule out optimal systems for the logics considered.
- Classification: Krajicek-Pudlak is a KNOWN THEOREM that transfers directly to (a). Joosten and Egidy are analogies requiring a bridge. Nothing here gives a lower bound.

### Next steps (candidates, none proved)
1. Test whether the repo's fixed combined system R_mix341 can be shown to simulate a uniform family of poly-time SAT deciders. Any such simulation is a candidate optimality-type theorem and should be red-teamed first.
2. Pursue the pointwise alternative only if (1) fails.
