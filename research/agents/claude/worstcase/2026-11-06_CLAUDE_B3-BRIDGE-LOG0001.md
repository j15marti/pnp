<!-- CLAUDE LOG::B3-BRIDGE-LOG0001::2026-11-06 -->
# Living log: worst-case minimum derivation cost (Wbar_R), bridge B3

**Status: OPEN. P versus NP remains OPEN. No lower bound or transfer theorem is claimed.**

## Corpus reviewed
`AGENTS.md`; `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (the shared directive: B1 => B2 => B3); newest LSPV handoffs (2026-11-06); `GROKPROOF/2026-11-06_0415_PROGRESS.md`. Not re-read in full: individual LSPV reports and root `main.tex` (about 1.7 MB). Root `main.tex` was not edited, since this run is not an LSPV role.

## Quantifier audit (restating the directive, nothing new)
- Wbar_R(N) = max over UNSAT F with |enc F| <= N of min over R-refutations pi of cost_R(pi).
- Target: for all k, C, N0 there is N >= N0 with Wbar_R(N) > C(N+1)^k.
- B3 (primary bridge): SAT in P => exists C, k with Wbar_R(N) <= C(N+1)^k, for the SAME preselected R.
- Lower bound plus B3 would give SAT not in P. Neither half is proved.

## Observations (labels: KNOWN or CANDIDATE only)
1. KNOWN (Cook-Reckhow 1979). A polynomially bounded propositional proof system exists iff NP = coNP. SAT in P implies NP = coNP, so SOME p-bounded system exists. This does not identify the preselected R. A fixed R satisfies B3 only if it simulates the witnessing system. That is the "R is p-optimal, conditional on P = NP" gap, and the directive already flags it.
2. KNOWN (Krajicek-Pudlak). An optimal proof system is equivalent to a fast consistency prover. NP = coNP implies a fast consistency prover (the Joosten source says the converse is open). Whether optimal systems exist unconditionally is open. So B3 for a concrete R such as Extended Frege is not a consequence of known theorems. A web search did not find that Extended Frege is p-bounded under NP = coNP. I regard that step as unverified.
3. CANDIDATE route to B3 (conditional restatement, not new proof). Suppose SAT is decided by a fixed A in time p(N), and R proves the reflection statement "A is correct" with polynomial-size overhead. Then R refutes F in poly(N + T_A(F)) steps. This is B1-style simulation under a reflection hypothesis. Whether R has the reflection property is exactly the gap. For R = Extended Frege it relates to whether bounded arithmetic can prove that A is correct, and nothing in the corpus establishes that.
4. Barrier ledger. Proving the lower-bound half for a strong R such as Extended Frege is itself a known open problem. It is stronger than anything proved for Frege. Any hard family must survive mixed-rule use, algebraic escapes (Tseitin over GF(2)) and compact circuits, as the directive says. Easy-family controls (parity recognizer plus exhaustive fallback) refute B1 for resolution but not B2 or B3, as the directive says.

## Proposed next obligations (CANDIDATE, for the five roles)
- (a) State exactly which reflection hypothesis on R suffices for B3. Prove it is also necessary, or exhibit a countermodel. This distinguishes a conditional restatement from progress.
- (b) Show that no weaker R (resolution, Nullstellensatz, cutting planes, Frege) can have B3 plus a known unconditional lower bound without already implying P != NP. This audits relativization and natural-proofs risk.
- (c) Time-space auditor: charge proof-DAG encoding size and peak space whenever B3 is used inside the FLMV transfer.

## Sources
- https://en.wikipedia.org/wiki/Propositional_proof_system
- https://ar5iv.labs.arxiv.org/html/2004.05431
- https://arxiv.org/pdf/1607.00443

<!-- END_OF_VERIFIED_LOG::B3-BRIDGE-LOG0001 -->
