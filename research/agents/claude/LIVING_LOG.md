# CLAUDE living log: worst-case minimum derivation cost program

Target (directive 2026-11-02 12:04): LB(R): Wbar_R(N) superpolynomial, and B3(R): SAT in P => Wbar_R(N) <= poly(N), for one fixed R.
P versus NP remains OPEN. Newest entry last.

## 2026-11-11 21:51 PST: WCDERIV-0001
- Report: `research/agents/claude/2026-11-11_2151_CLAUDE_WCDERIV-0001.tex`
- PROVED/EXACT: monotonicity (B3 moves up, LB moves down the p-simulation order). The Krajicek-Pudlak system R_T is the optimal fixed R among T-provably sound systems (KNOWN THEOREM, restated). New sandwich: [SAT in P => exists T-provably sound p-bounded S] => B3(R_T) => [same with T + Pi1-soundness of T].
- Consequence: at the optimal choice, the program equals LB(R_T) (implies superpolynomial EF lower bounds; OPEN) plus the "provability gap" (OPEN). Changing the calculus cannot remove the gap.
- Hypergraph-only calculus (no extension) has Resolution strength: LB holds unconditionally, so B3 is equivalent to SAT not in P (duplicates LSPV-1/398; not progress).
- Literature: no new EF/Frege superpolynomial lower bound (2025-26). Egidy-Glasser STOC'25 oracles. Monroe arXiv 2507.13576 v3 withdrew its no-p-optimal claim (stale).
- Next target: existential shrinking of the provability gap (uniform A -> provably correct A'), with oracle obstructions as the first hostile control.
