# Living log: worst-case minimum derivation cost W̄_R(N)

Scheduled routine (shared worst-case directive). P versus NP remains **OPEN**.

## 2026-11-15 run 0001
- Report: `research/agents/claude/2026-11-15_1500_CLAUDE_WORSTCASE-DERIVATION-0001.tex`
- PROVED (elementary): for any R with an already-known superpolynomial W̄_R (Res, tree-Res, CP, bounded-depth Frege, PC), Bridge(R) ⟺ P≠NP. The "weakest sufficient bridge" is a reformulation of the goal, not a weaker step.
- KNOWN: the bridge has real content only for strong systems (EF+). If PV proves SAT∈P, then EF is polynomially bounded (Cook; Cook–Krajíček). But superpolynomial EF lower bounds are open; the 2025–26 literature has no breakthrough.
- PROVED: ∀A ∃R is trivial (R_A). R must be fixed first; a lower bound for all R is NP≠coNP.
- COMPUTATIONAL: exact minimum tree-like resolution sizes for PHP and Tseitin. Tseitin is R-hard but solvable by Gaussian elimination, so pointwise transfer is FALSIFIED.
- Next lemma (OPEN): a constructive algorithm→EF-proof bridge without PV-provability of correctness (the uniform-reflection gap).
