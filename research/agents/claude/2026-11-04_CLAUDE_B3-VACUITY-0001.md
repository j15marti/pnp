<!-- CLAUDE REPORT::B3-VACUITY-0001::2026-11-04 -->
# CLAUDE / B3-VACUITY-0001: the B3 bridge is vacuous or as hard as the goal for any fixed system

Status: **PROVED/EXACT** (elementary, 3 short lemmas). **KNOWN** literature cited. P versus NP remains **OPEN**. No lower bound is claimed.

## Setting
Fixed sound, complete, poly-time-verifiable refutation system R. W_R(F) = min cost of an R-refutation of UNSAT F; Wbar_R(N) = max over UNSAT F with |F|<=N (strategy search not charged).
B3_R := (SAT in P => Wbar_R(N) <= poly(N)).  LB_R := "Wbar_R is not polynomially bounded".

## Lemma 1 (Cook–Reckhow normalisation) — KNOWN
Wbar_R polynomial  <=>  R is p-bounded  =>  NP = coNP. (Cook–Reckhow 1979.)

## Lemma 2 (B3 is the contrapositive of LB) — PROVED
If LB_R holds then  B3_R  <=>  SAT not in P  (<=> P != NP).
Proof: B3_R says SAT in P => not LB_R. With LB_R true this reads SAT in P => false.  QED

**Consequences.**
* For Resolution, tree/DAG, cutting planes, bounded-depth Frege etc. (unconditional superpolynomial lower bounds known: Haken 1985, Pudlák 1997, ...), B3_R is *equivalent to P != NP*. Proving B3 there is as hard as the goal; it cannot be a "weaker sufficient bridge".
* If Wbar_R is provably polynomial, B3_R is trivially true and the system is useless for a lower bound.
* So B3 is informative only for R whose LB status is open (EF, Frege, the repo's R_mix341 with charged DEF, which is ER-strength). There the program needs **two** independent open arrows: LB_R **and** B3_R. A proof of P != NP via this route = LB_R + B3_R, and each alone is open.

## Lemma 3 (what B3_R needs for strong R) — PROVED + KNOWN
(a) Optimal systems: if R p-simulates every proof system and P=NP, then R is p-bounded (P=NP => NP=coNP => some p-bounded Q exists => R p-simulates Q). So B3_R follows from "R is p-optimal"; existence of any p-optimal system is open (known to follow from NE = coNE, Krajíček–Pudlák 1989).
(b) Reflection: if EF (or the theory behind R) proves correctness of one poly-time SAT algorithm A, then R-proofs of the soundness CNFs H_{A,l} (cf. LSPV-1/353) are polynomial and B3_R holds. Krajíček (2006): PV proves P=NP iff PV proves NP=coNP iff PV defines a poly-time algorithm returning a satisfying assignment or an EF proof of unsatisfiability. Pich–Santhanam / the 2019 appendix (arXiv:1905.12935) conjecture PV does NOT prove P=NP for any algorithm; that conjecture follows from EF being not p-bounded. So hypothesis (b) is expected to fail exactly when LB_EF holds. This matches LSPV-1/353: B3 reduces to short proofs of H_{A,l}, and short proofs of H_{A,l} are what LB_EF would deny.
(c) Hence B3_EF is not provable by transporting "any correct A" — it needs either provable correctness of some A (conjecturally false) or optimality of R (open).

## Implication for the common target
The fixed-system bridge cannot be both *provable by a generic argument* and *non-vacuous*: any argument for B3_R valid for all R with known LB would prove P != NP outright. Therefore B3 must use specific structure of R_mix341 that fails for Resolution. Concretely the next obligation is a **separating test**: state B3-transport lemma RT/SC (LSPV-1/353) and check it *fails* for Resolution/PHP (where LB is known). A transport proof that also "proves" B3 for Resolution is wrong. This is a cheap red-team gate for all five roles.

## Literature checked this run
* Krajíček, "Propositional proof complexity and bounded arithmetic" (PV ⊢ P=NP ⇔ PV ⊢ NP=coNP ⇔ EF-proof-producing algorithm) — KNOWN, directly relevant to Lemma 3(b).
* arXiv:1905.12935 "Consistency of circuit lower bounds with bounded theories" appendix: conjecture that no poly-time f has PV ⊢ φ_{P=NP}(f) — CONJECTURE, supports expected failure of 3(b).
* Cook–Reckhow 1979; Krajíček–Pudlák 1989 (optimal systems from NE=coNE).
* Classification: Lemma 3 items are EXACT OBJECT TRANSFERS; PQ-ledger items not used.

## Corpus audit
CORPUS REVIEWED: AGENTS.md; LSPV-1/353, /391; LSPV-4/393 listing; governance list. DUPLICATION: LSPV-1/353 already reduces B3 to short proofs of H_{A,l}; Lemma 2's vacuity observation and the Resolution separating gate are not stated there (not found by grep). STALE/OVERSTATED: none found. NOT CHANGED: root main.tex (Claude role has no ownership region; pointer added to AGENTS.md addendum only).

<!-- END_OF_VERIFIED_REPORT::CLAUDE::B3-VACUITY-0001 -->
