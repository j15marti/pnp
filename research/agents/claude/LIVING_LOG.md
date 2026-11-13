# Claude contributor — living log (worst-case minimum derivation programme)

Append-only. Newest entry at the bottom. Status labels follow AGENTS.md. **P versus NP remains OPEN.**

Target (2026-11-02 refocus): superpolynomial lower bound on
`Wbar_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi: F |-_R bottom} cost_R(pi)`
for one fixed system R, and the bridge B3: `SAT in P => Wbar_R(N) <= poly(N)`.

## 2026-11-12 18:51 PST — WR-BRIDGE-0001
Report: `research/agents/claude/2026-11-12_1851_CLAUDE_WR-BRIDGE-0001.tex`
- PROVED/EXACT: once a lower bound for R is proved, B3(R) is provably *equivalent* to P != NP. So B3 for Resolution, CP, AC0-Frege, PC and bounded-depth Res(xor) is no weaker than the whole problem.
- PROVED/EXACT: if S p-simulates R, then B3(R) => B3(S) and LB(S) => LB(R). A stronger system makes the bridge easier and the lower bound harder.
- CONDITIONAL: under LSPV-1/592 A1–A4 (ER compiles into the native calculus), LB(R_mix341) => LB(EF), an open problem since 1979.
- CONDITIONAL, literature: Pich–Santhanam (arXiv:2312.08163). If S^1_2 proves feasible SAT anticheckers, then EF not p-bounded => P != NP. With A1–A4 this gives LB(R_mix341) => P != NP, replacing the project's own B3 with a hypothesis an outside expert can check.
- Next target: prove or refute R_mix341 <=_p EF. If both directions hold, [P2-B1] is exactly the EF lower-bound problem and [P2-B2] is exactly B3(EF).
