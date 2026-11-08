# CLAUDE WORSTCASE-0001 (2026-11-08)
Status labels: PROVED/EXACT, KNOWN THEOREM, CANDIDATE, OPEN. P vs NP: OPEN.

## Setup
A proof system R (Cook-Reckhow): poly-time verifier, sound and complete for UNSAT. cost_R(pi) = |pi| (size; DAG sharing allowed) or a time-space pair. Wbar_R(N) as in the directive. Taking the min over pi without charging strategy search is a valid lower-bound convention, since it only lowers the quantity being bounded below.

## Theorem 1 (Cook-Reckhow normalization) [KNOWN THEOREM]
Wbar_R(N) <= poly(N) iff R is polynomially bounded; then NP = coNP. Hence "Wbar_R superpoly for every R" is equivalent to NP != coNP, strictly stronger than P != NP as a target. For a single fixed R, Wbar_R superpoly proves nothing about P vs NP by itself.

## Theorem 2 (bridge is vacuous or as hard as the goal) [PROVED/EXACT]
Let B(R) denote "SAT in P => Wbar_R(N) <= poly(N)".
(a) If P != NP, B(R) holds for every R (false antecedent).
(b) If R has an unconditional superpolynomial lower bound (e.g. resolution [Haken, Urquhart], bounded-depth Frege, cutting planes with bounded coefficients), then B(R) is equivalent to "SAT not in P" (consequent is false, so B(R) <=> not antecedent). Proving B(R) outright proves P != NP; any argument for B(R) must therefore already contain a P != NP proof. Weak R is a dead end for the bridge.
Proof: (b) the consequent is a known-false statement; an implication with a false consequent is equivalent to the negation of its antecedent. QED.

## Theorem 3 (bridge for strong R = optimality) [PROVED/EXACT reduction; the resulting statement is OPEN]
B(R) holds iff: for every poly-time A that correctly decides SAT, R has poly-size proofs of the sentences "A(F)=0" for UNSAT F (plus R can verify the run of A). If such A exists and PV proves A correct, Extended Frege achieves this (Cook's translation). Without provable correctness this is a soundness/reflection claim for A; by Krajicek-Pudlak it is tied to existence of optimal proof systems (known under NE = coNE; open unconditionally). So the only live bridge is for R in the Frege/EF class, where the lower-bound half is itself open.

## Theorem 4 (computation-trace system) [PROVED/EXACT, trivial]
Let R_comp have proofs = accepting traces of a fixed machine M_e. If SAT in P via M_e, R_comp is poly-bounded, so B(R_comp) is trivial; but R_comp is a proof system only if M_e is known sound, and a superpoly lower bound on Wbar_{R_comp} is exactly SAT not in P. No gain.

## Consequence for the programme
Route must pick R strong enough that (i) lower bound is open-but-plausible and (ii) the bridge is a provability-of-correctness statement. Candidate path: show that for EF, any hypothetical poly-time SAT algorithm's correctness has poly-size EF proofs on UNSAT inputs *unconditionally* -- this is a non-relativizing reflection statement; Pich-Santhanam type barriers suggest feasible proofs of strong co-nondeterministic lower bounds are impossible, so expect this to require new ideas. Status: CANDIDATE only.

## Hard-instance survey (no new claims)
Resolution: PHP, Tseitin on expanders, random 3-CNF, pebbling formulas (time-space tradeoffs, Ben-Sasson-Nordstrom). All fall to stronger systems (PHP has poly EF/Frege proofs; Tseitin has poly EF proofs), so none survives "algebraic reasoning/circuit compression" tests -- consistent with Theorem 2: unconditional hard families exist only for weak R. Automating resolution is NP-hard (Atserias-Muller), so even finding near-shortest refutations is hard, but that does not affect the min.

## Literature checked
- Krajicek-Pudlak optimal proof systems; Krajicek, "Information in propositional proofs and algorithmic proof search" (JSL/ECCC 2021/053): proof search reduces to optimality.
- Pich-Santhanam FOCS 2019 (why proof complexity lower bounds are hard): cited, not re-read this run.
- Atserias-Muller, Automating Resolution is NP-hard, arXiv 1904.02991.
- Ben-Sasson-Nordstrom 2011, space/time-space tradeoffs via pebbling.
Search tool returned abstracts only; no full-text verification.

## Red-team notes
Corpus survey was shallow this run (repo tree + existing claude/ reports; no prior worst-case directive found; AGENTS.md role/ledger protocol not fully executed -- root main.tex ownership region not updated, since this task has no LSPV owner region). No claim here strengthens any prior ledger row.

% END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-0001
