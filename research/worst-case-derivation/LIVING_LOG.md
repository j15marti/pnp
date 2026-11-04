# Worst-case derivation complexity — living log

Target quantity: `W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)`.
Priority bridge: `SAT in P  =>  W_R(N) <= poly(N)`. Strategy discovery is not charged.
Status: P versus NP remains OPEN. Nothing below is a proof of a separation.

Roles: Lower-Bound Lead; Reduction Builder; Hypergraph & Proof Certificates; Time-Space Auditor; Red Team.

## Entry 2026-11-04 (run 1)

### Corpus reviewed
Repo survey; no prior file on `W_R` existed (grep of research/ for "overline W_R" / "worst-case derivation" hits only unrelated LSPV text). AGENTS.md, root main.tex ownership regions not edited this run (this task is not an LSPV-owned region; no root change).

### Structural findings (PROVED/EXACT unless stated, elementary)
1. **Cook–Reckhow normalization (KNOWN THEOREM).** For R with poly-time-checkable proofs, `W_R <= poly` iff R is p-bounded on UNSAT, which implies NP = coNP. So any superpolynomial lower bound for a Cook–Reckhow R is *not* a consequence of P != NP alone; it is a statement about R.
2. **The bridge is vacuous for weak R.** If R is Resolution, bounded-depth Frege (and similar), `W_R` is known unconditionally to be exponential (Haken; Ajtai/Bounded-depth lower bounds). Then "SAT in P => W_R <= poly" is logically equivalent to "SAT not in P", i.e. it is P != NP itself. It has content only for R strong enough that no unconditional lower bound is known (EF, Frege, stronger).
3. **For strong R the bridge is a simulation statement.** `SAT in P` gives NP = coNP, hence *some* p-bounded system exists (Cook–Reckhow), but the bridge needs *this fixed* R to be p-bounded. That is the open question "P = NP => EF (or Frege) p-bounded"; known routes need the SAT algorithm's correctness to be provable inside EF/PV (a feasible-provability hypothesis not implied by SAT in P). Literature search found no unconditional proof; I could not confirm such an implication. Status: OPEN, and it is the weakest sufficient transfer theorem's real content.
4. **Optimal systems.** Krajíček–Pudlák: NE = coNE implies an optimal propositional proof system exists; P = NP implies E = NE = coNE-type collapses via padding, so an optimal system exists under the antecedent, but it is defined non-explicitly through enumeration of all machines, so lower bounds for it cannot be proved by combinatorial means directly. Egidy–Glaßer (STOC 2025) give oracle barriers against relativizing proofs of these implications; a 2026 Egidy arXiv paper (SPARSE-relativization) continues this. Treat any bridge proof as needing non-relativizing input.
5. **max-min versus min-max (the key quantifier hazard).** `W_R` is instance-wise. Allowing the derivation to depend on F with free strategy choice makes machine-trace systems degenerate: a "derivation" consisting of a machine hard-coding F's answer costs O(|F|). So computation-trace costs must be quantified uniformly (min over a single decider, max over F), which is the ordinary time complexity of UNSAT and gives no gain over direct lower bounds. A meaningful `cost_R` must keep per-step poly-time checkability, which returns us to item 1.
6. **Consequence for hard-instance searches.** Hard UNSAT families for EF/Frege cannot come from combinatorial counting alone (EF lower bounds are an open problem, and Natural-proofs/feasible-interpolation barriers apply). Candidate families (e.g. signed-hypergraph instances) should be tested first against Resolution, Polynomial Calculus, Res(lin), cutting planes and bounded-depth Frege; surviving only those is a necessary, not sufficient, filter.

### Literature checked this run
- Krajíček–Pudlák optimal proof systems and follow-ups (Köbler–Messner–Torán; Messner): confirmed NE=coNE => optimal system; P=NP => optimal acceptor iff p-optimal system (Messner). No source found for "P=NP => EF p-bounded".
- Egidy–Glaßer, STOC 2025, oracle barriers; Egidy 2026 arXiv 2602.02294 (SPARSE-relativization), excerpts only.
- Khaniki–Pich–Sokolov, "Efficient Adversaries" (CCC 2026): known lower bounds are constructive adversary strategies; a constructive EF lower bound plus EF proving anticheckers' correctness would separate the canonical pair of EF. Relevant barrier for any EF lower bound.
- Alekseev, PC with extension rule (Theory of Computing 22, 2026): exponential lower bound for the binary value principle in a system simulating EF-like algebraic reasoning only in the extended-PC sense; not an EF lower bound.
No new Frege/EF superpolynomial lower bound found.

### Open arrows (all load-bearing; P != NP not proved)
- A1: explicit Cook–Reckhow R, strong enough for the bridge, with a proved superpolynomial `W_R`.  OPEN.
- A2: bridge `SAT in P => W_R <= poly` for that R (needs provability or simulation of the SAT algorithm).  OPEN.
- A3: hard family surviving all weaker systems.  OPEN.

### Next steps
Red Team: audit item 3 for a gap (can P=NP be used non-uniformly with advice to simulate?). Reduction Builder: fix a concrete combined system (EF + counting + algebraic rules) and record shortest-DAG certificates for small N by exhaustive search (chunked <30s runs). Time-Space Auditor: define the cost vector (size, width, peak memory) and check the bridge direction for each.
