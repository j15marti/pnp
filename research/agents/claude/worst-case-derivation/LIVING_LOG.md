# Living log: worst-case derivation cost  W_R(N) = max_F min_pi cost_R(pi)

Status: P vs NP OPEN. Bridge SAT in P => W_R <= poly(N) is OPEN for every R whose W_R is not already known.

## 2026-11-03 WCD-0001 (Claude)
- Report: `research/agents/claude/2026-11-03_1200_CLAUDE_WCD-0001.tex`
- Proved/exact: free choice of optimal derivation is legitimate; for R with known unconditional lower bound (Res, CP, bounded-depth Frege), bridge B(R) is logically equivalent to P != NP (no free lunch); two-sided witnessing axioms trivialize the bridge (circular).
- Known: Cook-Reckhow; provable-soundness case gives EF poly proofs (Cook, Krajicek-Pudlak; from memory, re-verify).
- Literature clue: Pich-Santhanam "Towards P != NP from Extended Frege lower bounds" (arXiv 2312.08163) is the closest published bridge (non-uniform); warning from 2405.02232 that formalizing it implies NEXP not in P/poly.
- Hard families: nothing known hard for EF; Tseitin over GF(2) and PHP are easy for EF.
- Next: one-sided witnessing-axiom system with short refutations when SAT in P (open); EF-hardness candidates.
- Honesty note: full LSPV corpus reconciliation not performed this run; main.tex not edited.
