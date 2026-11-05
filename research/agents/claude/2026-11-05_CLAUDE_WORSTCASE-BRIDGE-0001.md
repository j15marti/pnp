<!-- CLAUDE REPORT::WORSTCASE-BRIDGE-0001::2026-11-05 -->
# CLAUDE / WORSTCASE-BRIDGE-0001: what the bridge "SAT in P => Wbar_R poly" can and cannot be

Status: **PROVED/EXACT** (elementary, folklore-level, not claimed novel); **OPEN**: superpolynomial Wbar_R for any strong R, the bridge for any such R, and P versus NP.

## Corpus reviewed
AGENTS.md; 2026-11-02_1204 worst-case refocus directive; LSPV-1/377 (finite-horizon firewall), LSPV-1/415 (Pi^0_1 clocked-correctness), LSPV-1/414 headers; Claude ONETAPE-0001/TPORT notes (headers). Not re-read byte-for-byte: ~855 LSPV-1 files. Duplicates: 415 already shows soundness of clocked deciders is not automatically recognizable; this note adds the *explicitness / circularity* analysis below, which I did not find stated there.

## Setting
Wbar_R(N) = max over UNSAT F, |F|<=N of min over refutations pi of cost_R(pi). Free choice of pi means this is exactly the Cook-Reckhow nondeterministic proof size (cost >= encoded length). Let B3(R) :≡ (SAT in P  =>  Wbar_R(N) <= poly(N)).

## Proposition 1 (B3 is circular for any R with a known lower bound)
If R is a Cook-Reckhow system with an *unconditional* superpolynomial lower bound (e.g. Resolution by Haken 1985, cutting planes, AC0-Frege), then B3(R) is logically equivalent to SAT not in P. Proof: the conclusion of B3(R) is false, so B3(R) <=> not(SAT in P). Hence a proof of B3(R) for such R *is* a proof of P != NP, and cannot serve as an independent bridge. Consequence for the program: the bridge is only non-circular for an R whose superpolynomial lower bound is itself still open (Extended Frege, Frege, or a combined system that contains extension + RES, such as the paid-DEF part of R_mix341). There the bridge and the lower bound are both open and must be proved by independent arguments.

## Proposition 2 (the bridge is non-constructively trivial)
Classically there is an R* with B3(R*) true: if P = NP take R_A (empty proof, verifier runs the polynomial decider A and accepts iff A(F)=UNSAT; sound and complete since A is correct); if P != NP take any R. But R* is defined by cases on the truth of P = NP, and "Wbar_{R*} is superpolynomial" is then equivalent to P != NP. So the content of the program lies entirely in **explicitness**: R must be fixed in advance, independent of A and of the truth value.

## Proposition 3 (what an explicit bridge must deliver)
For explicit R, B3(R) says: whenever a polynomial-time correct decider exists, R already proves every UNSAT instance in polynomial size. The natural way to prove this is a uniform translation: from a correct A (with a short certificate that A is sound) obtain a poly-size R-refutation of each UNSAT F. By LSPV-1/415 soundness of clocked deciders is Pi^0_1-complete, so such certificates cannot be produced or recognized automatically for all deciders; the bridge must either (i) assume a provably-sound witness for *some* decider (conditional, B3'), or (ii) argue non-uniformly. This matches the Krajicek-Pudlak picture: a fixed R that polynomially simulates every R_A would behave like an optimal proof system for the family {R_A}; whether optimal systems exist is open and widely believed false (search-reported: Egidy, arXiv 2602.02294, Feb 2026, SPARSE-relativization framework; Messner-Toran survey). CANDIDATE connection, not a proved equivalence.

## Literature clue (this run)
Web search (standard): no 2026 result settles existence of optimal / p-optimal proof systems; Krajicek-Pudlak: NE=coNE => optimal system; E=NE => p-optimal. Takeaway for the plan: aim the bridge at a *conditional* form "SAT in P via a decider with an R-provable soundness proof => Wbar_R poly" (B3', consistent with LSPV-1/357), and treat unconditional B3 as equivalent in difficulty to a statement about optimal proof systems.

## Next targets
1. State B3' precisely for R_mix341 and check which part (soundness proof translation) is the missing link.
2. Lower-bound side: restrict to R_mix341 minus paid DEF (no extension) where GF(2)+RES lower bounds (Res(lin)-type, Raz-Tzameret) might apply; keep this separate from the ER-containing system.

P versus NP remains OPEN.
<!-- END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-BRIDGE-0001 -->
