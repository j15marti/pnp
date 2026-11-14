# Claude living log: worst-case minimum derivation cost W̄_R(N)

Append-only log of the scheduled Claude runs on the shared target
W̄_R(N) = max over UNSAT F with |<F>| ≤ N of min over R-refutations π of cost_R(π),
with the weakest bridge B3_R: SAT ∈ P ⇒ W̄_R is bounded by a polynomial.
These runs are outside the five-role LSPV/TMR stagger. They own no region of root `main.tex`.
Allowed statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## 2026-11-14 05:50 PST — WR-B3-CONSERVATION-0001
- Report: `research/agents/claude/2026-11-14_0550_CLAUDE_WR-B3-CONSERVATION-0001.tex`
- PROVED/EXACT (elementary). For every fixed system R:
  - SAT ∉ P implies B3_R, vacuously.
  - The lower bound LB_R together with B3_R implies SAT ∉ P.
  - So whenever LB_R is a known theorem, B3_R is equivalent to SAT ∉ P.
- Consequence: B3 is not an easier half for Resolution, Res(k), Cutting Planes, bounded-depth Frege, or Polynomial Calculus over a fixed field. It is only meaningful for calculi of Extended Frege strength, such as R_mix341, which contains Extended Resolution.
- KNOWN THEOREM (Cook 1975; Krajíček–Pudlák 1989), restated: if PV proves a polynomial-time A correct, then EF has short proofs of A's reflection formulas. Then W̄ is polynomial for every R that polynomially simulates EF.
- OPEN: the gap between "A is correct" and "A is feasibly provably correct". This gap is the real content of B3 for EF-strength R. It matches corpus items LSPV-1/337 and /353–354.
- Literature this run: Cook 1975; Krajíček–Pudlák 1989; Pich–Santhanam STOC'21 and ECCC TR23-199 (Extended Frege lower bounds plus witnessing axioms imply circuit lower bounds for SAT).
- Next target (CANDIDATE): find a family that is a credible hardness candidate for Extended Frege strength, after ruling out PHP and Tseitin, which have polynomial EF refutations. Alternatively, find a B3_EF argument that uses only the truth of A's correctness, not its PV-provability.
- P versus NP: OPEN.
