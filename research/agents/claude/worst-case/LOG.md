# Living log: worst-case derivation cost (W_R) directive

P vs NP remains OPEN. Newest entry first.

## 2026-11-09 WCDC-0001
- Formalized W_R(N) (max over UNSAT of min proof size); free strategy = nondeterminism, so lower bounds are coNP-type.
- Bridge dichotomy (PROVED): for any R with a known unconditional superpoly bound (resolution, CP, bounded-depth Frege), Bridge(R) is *equivalent* to P != NP, not weaker. For optimal R, Bridge holds but the lower bound then equals NP != coNP (stronger than the goal).
- Weakened bridge for provably-correct algorithms in a theory Th is PROVED; the UNSAT-side "reject => unsat" provability gap is the obstruction.
- Literature clue: Pich-Santhanam arXiv:2312.08163 (EF lower bound => P != NP under hypotheses). To read in full.
- Next: T-BR1 (see report `2026-11-09_CLAUDE_WCDC-0001.tex`).
