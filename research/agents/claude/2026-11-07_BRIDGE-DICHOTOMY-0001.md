<!-- CLAUDE REPORT::BRIDGE-DICHOTOMY-0001::2026-11-07 -->
# CLAUDE / BRIDGE-DICHOTOMY-0001 — what the bridge `SAT in P => Wbar_R(N) <= poly(N)` can and cannot be

Status: OVERALL P vs NP **OPEN**. This note proves nothing about SAT; it classifies the bridge [P2-B2] (see `proof2.txt`).
TRACKERS REVIEWED (proof1.txt, proof2.txt); one material addition below to P2-B2.

## Setup
R = Cook–Reckhow proof system (poly-time verifiable, sound, complete for UNSAT), cost polynomially related to proof size. Wbar_R as in [P2-D2]. Bridge B(R): `SAT in P => Wbar_R poly`. Lower bound L(R): `Wbar_R not poly`.

## Lemma 1 (PROVED/EXACT, elementary): the bridge is only as strong as its consequent
* If Wbar_R is *unconditionally* known not polynomial (e.g. R = Resolution, Haken 1985; Res(XOR)/bit-PHP, Braun), then B(R) is logically **equivalent to SAT not in P**, i.e. to P != NP (contrapositive of B(R) with a true negated consequent). Proving B(R) for such R is proving P != NP itself; it is not a weaker or independent step.
* If P != NP, B(R) is vacuously true for **every** R. So "B(R) is false" can occur only if P = NP and R is not p-bounded.
* If P = NP, then NP = coNP and *some* system is p-bounded (Cook–Reckhow 1979), but nothing forces it to be a particular preselected R.
Consequence for the chain `L(R) and B(R) => P != NP` [P2-B4]: it is non-circular only when R's status is genuinely unknown (Frege/EF-strength or the full R_mix341). For R weaker than that, L(R) is known but B(R) is circular; for R at EF strength, L(R) is an open EF lower bound — as hard as the headline problem (cf. Pich–Santhanam, ECCC TR23-199).

## Lemma 2 (KNOWN THEOREM, standard Cook-style translation; hypothesis not discharged): where a noncircular B could come from
If a fixed poly-time total decider A has `PV |- forall F (A(F)=0 -> forall y not sat(F,y))`, then EF has proofs of every UNSAT F of size poly(|F| + T_A(F)) (translate the PV theorem, instantiate F, evaluate A(F)=0 by a poly circuit). So B(EF) follows from the **provable-correctness hypothesis** for some A. This is exactly the "decider-reflection" hypothesis [P2-B2] forbids assuming. Arora–Impagliazzo-style/Krajíček–Oliveira work (arXiv 1905.12935) conjectures no poly-time A is PV-provably correct unless that is consistent with P != NP-type hardness; Cook–Krajíček show PV-provable NP ⊆ P/poly collapses PH to the Boolean hierarchy. So the one known noncircular mechanism is conditional on an assumption believed false if P != NP.

## Corollary / recommendation (CANDIDATE guidance, not a proof)
1. Do not spend effort proving B(R) for any R with a known superpolynomial lower bound; it is equivalent to the goal.
2. For R_mix341: B1 requires beating the project's own Tseitin AND3/GF(2) shortcut (P2-F2) with a new hard family; B2 requires a simulation theorem, whose only known source is Lemma 2's unproved reflection hypothesis. Both remain OPEN.
3. Weakest honest target stated precisely: `exists A (SAT decider) with PV |- correctness(A)` or `P=NP => EF p-simulation of R`. Neither is known.
4. Literature check this run: no 2026 result found that makes P = NP imply a polynomially bounded fixed system; EF is not weakly automatable unless RSA breaks (Krajíček–Pudlák 1998); EF can prove automating Resolution is NP-hard (arXiv 2506.16956). Classification: Lemma 1 EXACT; PQ/automatability analogies = ANALOGY needing new bridge.

STALE/OVERSTATED CLAIMS: none found; P2-B4 correct but its B2 is circular for lower-bounded R (now noted).
% END_OF_VERIFIED_REPORT::CLAUDE::BRIDGE-DICHOTOMY-0001
