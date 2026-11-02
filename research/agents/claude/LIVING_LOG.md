# Living log: worst-case minimum-derivation program (Claude role)

Target: Wbar_R(N)=max_{F UNSAT,|F|<=N} min_{pi} cost_R(pi); priority bridge B3 (SAT in P => Wbar_R poly). P vs NP OPEN.

## 2026-11-02 TIER-ER-0001
- Proved: W_Rmix341 <= 4*S_ER, so Rmix341 p-simulates Extended Resolution (= EF). LB(Rmix341) would imply an EF lower bound.
- Proved: B3 is monotone upward under p-simulation, LB downward; if LB(R) is a theorem then B3(R) <=> SAT not in P (Tier 1 circular).
- Literature: dag Res(+) lower bound still open; depth-restricted bounds only (2024-25).
- Next: lower-bound target below EF, or feasible-correctness bridge at EF. Report: 2026-11-02_CLAUDE_TIER-ER-0001.tex
