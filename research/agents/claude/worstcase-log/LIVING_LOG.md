# Worst-case derivation-cost program: living log

Shared objective (all five roles): superpolynomial lower bound on
`W̄_R(N) = max_{F UNSAT, |F|<=N} min_{π: F ⊢_R ⊥} cost_R(π)` for a fixed R, with the
optimal derivation chosen free of charge, plus the weakest bridge `SAT ∈ P ⇒ W̄_R(N) ≤ poly(N)`.
P vs NP remains **OPEN**. Nothing below is a proof of either the lower bound or the bridge.
Prior corpus: LSPV-1 #336–#353 (R_mix341, `Q_A(ℓ)`, RT+SC), LSPV-3 #353, LSPV-4 #350.

## Entries (newest first)

### 2026-11-03 — CLAUDE-WCBRIDGE-0001 (`../2026-11-03_CLAUDE_WCBRIDGE-0001.tex`)
- PROVED/EXACT (standard closure assumptions on R): for a fixed correct poly-time A,
  R p-bounded ⇔ R has poly-size refutations of the reflection CNFs `H_{A,ℓ}` (extends LSPV-1 #353 to an equivalence).
- Bridge diagnosis: `SAT∈P ⇒ R p-bounded` needs R to prove correctness of an *unknown* A; for natural
  R (Frege/EF) this is OPEN and is exactly the hypothesis of Pich–Santhanam (arXiv 2312.08163).
- Structural: with the optimal derivation free, `W̄_R` superpoly is a proof-size (NP vs coNP flavored) statement.
  A bridge for an *optimal* system would make the target equivalent to NP ≠ coNP, which is stronger than P ≠ NP.
- Hard-instance quantifier problem: for incorrect A, `H_{A,ℓ}` is satisfiable, so a lower bound cannot be
  exhibited independently of A.
- Next: (a) test which of R_mix341's rules admit RT+SC; (b) check whether Pich–Santhanam's anticheckers hypothesis can be phrased as a bound on `Q_A`.
