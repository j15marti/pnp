# Worst-case minimum-derivation living log (Wbar_R, B1/B2/B3)

Append-only by run. Governing directives: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` and the user's multisign-DAG-hypergraph worst-case directive. **P versus NP remains OPEN.** Every item below is labelled with the strict status vocabulary.

## Run 2026-11-09 ~19:49 UTC (scheduled, role-agnostic general run)

### Literature check (clues for the B3 bridge)
- Pich & Santhanam, arXiv:2312.08163: conditional lower bounds. If Extended Frege (EF) is not p-bounded and S^1_2 has certain self-provability or witnessing properties, then P != NP. This is the same *shape* as B3 + hardness for a fixed R. KNOWN THEOREM (their paper); the exact hypotheses have not been re-verified here.
- Atserias-Muller line (automatability): P = NP implies every proof system is automatable relative to *its own* short proofs. This is the wrong direction for B3: it gives search from existing short proofs, not existence of short proofs.
- Search did not find "SAT in P implies EF p-bounded" as a theorem. Treat as unestablished.

### Result 1 (PROVED/EXACT, standard Cook-translation argument, restated for B3)
Reflection sufficiency. Let R be a proof system and A a deterministic poly-time decider that is correct for SAT. Suppose the propositional translations Sound_A[N] of "A(F)=0 and F(x) -> false" have R-proofs of size poly(N). Then Wbar_R(N) <= poly(N): for UNSAT F, evaluate A on the hardwired F (a poly-size computation trace, which EF-style rules derive), then substitute into Sound_A[N]. So B3 for R follows from poly-size R-proofs of the soundness of *every* correct poly-time decider. (Sufficient only. Necessity is not claimed.)
Corollary (KNOWN THEOREM, Cook/Krajicek-Pudlak): if PV or S^1_2 proves A correct, then EF has poly proofs of all tautologies.

### Result 2 (PROVED/EXACT, trivial but clarifying)
For resolution, Haken/Urquhart give Wbar_Res(N) exponential unconditionally. Hence B3(Res) is *equivalent* to SAT not in P. A B3 for a weak R is as hard as the goal and carries no information. B3 is informative only for R strong enough that reflection is plausible (EF or stronger). Also: B3(R) transfers upward, since if R' p-simulates R then B3(R) implies B3(R').

### Result 3 (CANDIDATE, barrier)
A lower bound on Wbar_R for one fixed R separates P from NP only through B3(R), i.e. through the claim that R can feasibly certify the correctness of an unknown poly-time SAT algorithm. Any proof of B3 must therefore either (a) use that correctness is automatically R-provable (not known; it fails in a relativized or independence-style countermodel), or (b) use a specially built R containing a universal-search or Levin-type rule whose charge is genuinely accounted. Option (b) collides with the earlier noncomputability/PACK finding (LSPV-1/395): hidden payload or universal-machine wrappers must be fully charged in the physical cost, which makes the hardness side unprovable by the same token. Status: OPEN. No conditional or unconditional lower bound is claimed.

### Role-targeted next steps
- General SAT Lower-Bound Lead: state B3 for EF with the exact Sound_A[N] formulation above; check whether Pich-Santhanam hypotheses are implied by SAT in P (probably not).
- SAT-Circuit Reduction Builder: certify shortest DAG for small UNSAT instances in the combined R, as a finite sanity set.
- Hypergraph & Proof Certificates: hard families must beat resolution, polynomial calculus, and circuit/Frege-style compression; remember Res/PC lower bounds are already known and are no evidence for EF.
- Time-Space Resource Auditor: charge reflection-proof size and trace evaluation to physical time and peak space.
- Red Team: look for a countermodel to "SAT in P implies B3(EF)" (A correct but its correctness unprovable in the corresponding theory).

### Not done this run
No new experiment, no full corpus reconciliation, and no root main.tex edit. This is a log entry only. Root main.tex ownership regions were not touched.
