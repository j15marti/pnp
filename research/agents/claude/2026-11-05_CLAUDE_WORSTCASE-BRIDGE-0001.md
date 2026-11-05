% CLAUDE-WC REPORT::WORSTCASE-BRIDGE-0001::2026-11-05
# Worst-case derivation cost: exact form of the weakest bridge B3

**Status:** two elementary statements PROVED/EXACT, one KNOWN THEOREM recalled. No new lower bound. **P versus NP remains OPEN.** Not an LSPV ownership edit: root `main.tex` untouched.

## Setup
R a fixed Cook-Reckhow system (poly-time proof checker, sound, complete for UNSAT), cost = proof size (or the charged cost of LSPV-1/391). W_R(N) as in the task. Free choice of optimal derivation is built into the min.

## Proposition 1 (B3 is a conditional-polynomiality statement) -- PROVED/EXACT
B3(R): SAT in P => W_R(N)=N^{O(1)}. Then B3(R) holds iff (SAT not in P) or (W_R polynomial).
*Proof.* Propositional logic: A=>B is true iff not-A or B, and "SAT in P" has a definite truth value. B3(R) fails exactly when P=NP and W_R is superpolynomial. QED.
Consequence: proving B3(R) amounts to proving P=NP => W_R poly. Combined with a superpolynomial W_R lower bound it gives P != NP, which is the intended architecture, but B3 has no independent content; it is not weaker than "R is polynomially bounded under P=NP".

## Proposition 2 (optimality suffices) -- PROVED/EXACT
If R is optimal (polynomially simulates every Cook-Reckhow system for UNSAT), then B3(R).
*Proof.* If SAT in P, the system T with empty proof and verifier running the decider is sound, complete and has constant-size proofs. R simulates T, so W_R poly. QED.
Conversely B3(R) with P=NP gives W_R poly, so R is then optimal. Hence B3(R) <=> "P=NP => R optimal".
Note: the decider's correctness is exactly what makes T sound; a proof system needs unconditional soundness, so an arbitrary unverified decider cannot be used as a rule inside R (consistent with REFEREE294).

## Known theorem recalled (KNOWN THEOREM)
If some poly-time SAT algorithm has its UNSAT-soundness provable in PV (equivalently feasibly provable), then Extended Frege has polynomial-size proofs of all tautologies (Cook 1975; Krajicek-Pudlak 1989 correspondence). Hence B3 for EF holds under *provable* P=NP. The gap between "P=NP" and "provably P=NP" is the load-bearing obstacle for any fixed R, and EF/Frege lower bounds are themselves open (Pich-Santhanam arXiv:2312.08163 derives P != NP-style consequences from EF lower bounds and conditional optimality under small SAT circuits).

## Where this leaves the five roles
- Lower-Bound Lead: B3 for natural R reduces to an optimality/provability hypothesis; a superpolynomial W_R is only possible for weak R (Resolution, Haken) where B3 is false by the fixed-island decider argument (REFEREE325).
- Reduction Builder: a combined system that is plausibly B3-true must contain extension (EF-strength); then lower bounds are out of reach with current techniques.
- Hypergraph/Certificates: hard families for weak systems do not transfer (PHP is poly in ER).
- Auditor: charging needs no change; Prop 1-2 are cost-model independent as long as cost is polynomially equivalent to proof size.
- Red Team: attempt a CANDIDATE system R with a self-contained "P=NP => R simulates decider-induced systems" proof not using PV-provability. No such candidate is known to us.

## Duplication audit
Prop 1-2 are elementary and overlap LSPV-1/391's B3 discussion and REFEREE294; they are recorded to fix the exact form, not as new mathematics.

% END_OF_VERIFIED_REPORT::CLAUDE-WC::WORSTCASE-BRIDGE-0001
