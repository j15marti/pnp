<!-- CLAUDE REPORT::WORSTCASE-BRIDGE-0001::2026-11-03_1400_PST -->
# CLAUDE WORSTCASE-BRIDGE-0001: which fixed system R can carry the bridge "SAT in P => W_R poly"

Status: KNOWN THEOREM (Cook; Krajicek-Pudlak) for the classification below; CANDIDATE for the program consequence. P versus NP remains OPEN. No new lower bound is claimed.

## Corpus reviewed
AGENTS.md; LSPV-1 335 (explicit-generator barrier), 334 (TR falsified for ordinary Resolution), 367, 368, 371; the Nov-3 five-role handoffs. Not re-derived here; relied on as stated.

## Target
W_R(N) = max over UNSAT F, |F|<=N, of min over refutations of cost_R. Bridge TR(R): for every poly-time SAT decider A, W_R(N) <= poly(N). (Free choice of best derivation is allowed; no search cost is charged.)

## Classification of bridge candidates
1. Weak R (Resolution, bounded-depth Frege, cutting planes, etc.). TR(R) is FALSE: exponentially hard UNSAT families exist (Haken 1985; Urquhart/Ben-Sasson-Wigderson), and the 335 generator argument turns any such poly-time-generated family into a poly-time SAT algorithm A_g that R cannot follow. These R cannot give the bridge. (Matches 334/335.)
2. Trace system R_A (derivation = accepting trace of one fixed A). TR is trivial, but W_{R_A} is just T_A, so a superpolynomial bound for one A says nothing about other deciders. Lower bound for all A at once is exactly SAT not in P. Circular.
3. Extended Frege (EF) / Frege-type R. KNOWN THEOREM (Cook's PV translation; Krajicek-Pudlak): if SAT in P via A and PV (or S^1_2) proves "A decides SAT", then UNSAT instances have EF refutations of size poly(|F|). Hence TR(EF) holds for every decider whose correctness is feasibly provable. TR(EF) for all deciders is equivalent in effect to the missing feasible-provability step.

## Consequence for the program (CANDIDATE, not proved)
For R = EF the bridge is not unconditional but is cleanly split:
 (a) SAT in P  AND  correctness of the algorithm is PV-provable  =>  W_EF poly.
 So: superpolynomial W_EF would imply  SAT not in P  OR  no poly-time SAT algorithm has PV-provable correctness.
That disjunction is weaker than P != NP. Closing the gap needs either (i) a proof that any correct poly-time SAT algorithm is provably correct in PV (false in general for arbitrary true statements; open for this one) or (ii) a different R for which TR holds unconditionally. No such R is known. A superpolynomial EF lower bound is itself a major open problem; the Frege/EF question is unchanged.

## Literature check (this run)
- Davis-Robere, ECCC TR26-055 (2026): Res(log) proves bounded-depth Frege lower bounds; ties to non-automatability. Direct relevance: weak systems can reason about themselves, but this is about weak R, on the wrong side of item 1.
- CCC 2026 (LIPIcs 10.4230/LIPIcs.CCC.2026.8): prover-adversary games across proof systems; conditional link between a constructive EF lower bound and succinct circuit lower bounds for SAT. Supports item 3: an EF lower bound is bound up with circuit lower bounds for SAT.
- Bokov (2026): nontrivial length bound for one Frege system over {and, or, not}; narrow.
Transfer type: all three are structural analogies; none supplies the missing bridge.

## Red-team notes
- Do not treat item 3 as a derivation of W_EF poly from P = NP; the PV-provability hypothesis is essential.
- Any R weaker than EF fails item 1 only if it has hard poly-time-generated UNSAT families; p-simulation by EF of the intended R is the thing to check before adopting a new R.

END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-BRIDGE-0001
