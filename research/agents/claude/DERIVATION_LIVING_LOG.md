# Claude routine: living log for the worst-case minimum-derivation target

Shared target: Wbar_R(N) = max over UNSAT F with |<F>| <= N of the minimum cost_R(pi) over refutations pi of F in R. The inner minimum grants free knowledge of the best reduction sequence. Primary bridge: B3(R), SAT in P => Wbar_R(N) <= poly(N). Directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.

**P versus NP remains OPEN.** Each entry lists its strict status labels.

## 2026-11-11 09:55 PST — DERIVBRIDGE-0001
- Report: `2026-11-11_0955_CLAUDE_DERIVBRIDGE-0001.tex`. Ledger rows L41–L49 are in `world-ledger/`.
- PROVED/EXACT: if a system has a proved superpolynomial Wbar (Resolution and similar), its B3 is literally P != NP (duplicates LSPV-1/398).
- PROVED/EXACT: B3(R) <=> [P = NP => R is size-optimal].
- CONDITIONAL: B3 moves upward under simulation. With R_mix341 ≡_p ER ≡_p EF (REFEREE350), B3(R_mix341) <=> B3(EF). That is the long-open question of whether an EF lower bound implies P != NP.
- PROVED/EXACT: B2 for Resolution forces every SAT algorithm to take 2^{N^{1/3-o(1)}} time (an ETH-type claim), so B2 is strictly beyond P != NP.
- Literature clue: Pich–Santhanam (arXiv 2312.08163) prove "EF not p-bounded => P != NP" under S^1_2 provability hypotheses, i.e. a conditional B3(EF). AKPS (ICALP 2024) warn that an unconditional connection of this kind already carries NEXP ⊄ P/poly-strength consequences (CANDIDATE barrier).
- Next missing implication: the S^1_2 feasible-antichecker hypothesis, or a sub-EF system that P = NP provably makes optimal. OPEN.
