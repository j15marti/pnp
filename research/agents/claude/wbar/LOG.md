# Living log: worst-case minimum derivation cost W̄_R(N)

Scheduled CLAUDE routine. P versus NP remains OPEN. Newest entry first.

## 2026-11-15 14:51 PST — WBAR-0001 (base 8e887aaa)
Report: `research/agents/claude/2026-11-15_1451_CLAUDE_WBAR-0001.tex`
- PROVED/EXACT: Bridge(R) ⟺ (P≠NP ∨ W̄_R poly). For every R with a known superpolynomial
  W̄_R (tree-like Res, Res, CP, PC, AC0-Frege) the bridge is equivalent to P≠NP.
- PROVED/EXACT: for those R the bridge cannot have a relativizing proof (BGS oracle).
- KNOWN THEOREM (Cook 1975): PV-provably sound P-time SAT algorithm ⇒ W̄_EF poly. Missing
  hypothesis (OPEN): PV-provable soundness for every P-time SAT algorithm.
- COMPUTATIONAL + KNOWN THEOREM: pointwise "time_A ≥ min_R cost" FALSIFIED for R=resolution
  by Gaussian elimination on Tseitin (exact min tree-like sizes 55, 95, 151, 255, 639 vs 5–21 row ops).
- Next lemma: a non-PV-conditional bridge for a fixed R, or proof that any such argument makes R p-optimal under NP=coNP.
