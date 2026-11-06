<!-- CLAUDE WORSTCASE-0001::2026-11-06 -->
# WORSTCASE-0001: what the bridge SAT in P => W_R <= poly actually requires

Scope: all five roles' shared objective. Status labels per AGENTS.md. **P vs NP remains OPEN; nothing here is a lower bound.**

Setting. R is a Cook-Reckhow proof system (sound, complete for UNSAT, verifier poly-time in |F|+|pi|); cost_R = |pi| (any cost polynomially related to verification time gives the same statements). Bridge(R) := (P=NP => W_R poly).

## Theorem 1 (trivial reformulation) — PROVED/EXACT
Bridge(R) <=> (R is polynomially bounded, i.e. W_R poly) OR P != NP.
Proof: propositional. QED.
Consequence: Bridge(R) says nothing beyond "W_R superpoly => P != NP". It is a statement about R, to be *proved*, not an assumption we may take for free.

## Theorem 2 (known lower bounds give nothing) — PROVED/EXACT
If W_R is provably superpolynomial (resolution, dag-resolution, bounded-depth Frege, cutting planes (Pudlak), polynomial calculus on suitable families), then Bridge(R) <=> P != NP. So proving Bridge for such R is as hard as the target; proving the lower bound there is already known and unhelpful.

## Theorem 3 (optimal R satisfy the bridge, at the price of NP != coNP) — KNOWN THEOREM / easy
If R is optimal (p-simulates every proof system) then Bridge(R) holds, and W_R superpoly <=> NP != coNP.
Proof: P=NP => UNSAT in P => system "pi empty, verifier runs the decider" is p-bounded => R p-simulates it => W_R poly. Conversely W_R poly gives UNSAT in NP, i.e. NP=coNP (Cook-Reckhow). QED.
Consequences: (a) through optimal R the bridge route proves **NP != coNP**, strictly stronger than P != NP; (b) existence of optimal systems is itself open (Krajicek-Pudlak: implied by NE=coNE; Kobler-Messner-Toran weaken to NEE=coNEE).

## Proposition 4 (sufficient local form of the bridge for a concrete R, e.g. EF/Frege) — CONDITIONAL (Cook/Krajicek-style, standard)
If P=NP implies a SAT algorithm A whose correctness reflection principle (formula family "A(F)=reject -> F unsatisfiable") has poly-size R-proofs, then W_R is poly: proof = poly-size computation trace of A on F + reflection instance + modus ponens. So Bridge(R) is implied by "P=NP => some algorithm is R-provably correct". Conversely the statement cannot be proved *unconditionally* without knowing which A exists; this is exactly the Cook-Krajicek PV/EF correspondence. Conclusion for the program: for a concrete strong R (EF, Frege) the bridge is equivalent in difficulty to a proof-theoretic statement about R-provability of SAT-algorithm correctness; then a W_R lower bound yields "P != NP or no SAT algorithm has short R-provable correctness".

## Why the obvious "universal reduction machine" does not give a free bridge — PROVED/EXACT (explanatory)
Let R be a rewriting machine that can simulate any TM for poly steps. A derivation of bottom must be sound without trusting A. Levin's universal search verifies SAT answers only; "no witness found in t steps" is not a certificate for UNSAT. Hence Bridge needs a soundness argument for UNSAT answers (Prop. 4), not just simulation power. Charging derivation cost to an algorithm's running time instead of to verifiable derivations is circular (it is the P vs NP question itself).

## Red-team notes on candidate hard families — KNOWN THEOREMS
- PHP: exponential for resolution (Haken), poly Frege/EF proofs (Buss), so useless against strong R.
- Tseitin on expanders: exponential for resolution, poly in Frege/EF (Urquhart/Buss-style counting), so useless against strong R.
- DAG-sharing of the multisigned hypergraph = dag-like resolution-type reuse; no new strength unless the rule set is extended (then it is a subsystem of Frege/EF). Adaptive switching between rule sets is covered by taking R to be the union system.
- Any unconditional superpolynomial lower bound for Frege/EF would prove NP != coNP's Cook program step and is far beyond current technique; no candidate family currently survives EF.

## Recommended re-targeting (for the next runs) — CANDIDATE
1. Do not treat a W_R lower bound as sufficient: decide between (A) R optimal-like => target NP != coNP; (B) concrete R + Prop. 4 => target must include an R-provability-of-algorithm-correctness lemma.
2. A genuinely P-vs-NP-relevant weakening: measure *search* (SAT-side) derivations where Levin-verifiability holds, i.e. work on the time-space side (ARC/FLMV spine) rather than the UNSAT-certificate side.
3. Time-space auditor: record for each candidate family both size and peak clause space; known resolution space/size tradeoffs (Ben-Sasson-Nordstrom) are unconditional only for weak R.

## Literature check this run
Searched optimal proof systems / Krajicek-Pudlak. Found: NE=coNE => optimal systems; E=NE => p-optimal; Kobler-Messner-Toran refinements; Cook-Reckhow: NP=coNP iff a p-bounded system exists. No source found stating P=NP implies a *fixed* system is p-bounded (consistent with Thm 1/Prop 4 being necessary). Sources: https://www.cs.umd.edu/users/gasarch/BLOGPAPERS/messnertoran.pdf ; https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.190/Mitarbeiter/toran/opt-proof.pdf . Corpus: repo already contains a Claude world ledger (research/agents/claude/world-ledger) whose rows classify "equivalent of P=NP"; Thm 3 adds: bridge route via optimal R is NP!=coNP-strength.

Not done: hard-family search, cost-model formalization for the multisigned hypergraph, mechanical verification.
<!-- END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-0001 -->
