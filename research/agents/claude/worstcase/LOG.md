# Living log: worst-case derivation-cost program (W-bar_R)

Objective: superpolynomial lower bound on W-bar_R(N) = max_{F in UNSAT, |F|<=N} min_pi cost_R(pi) for a fixed strong R, via the bridge SAT in P => W-bar_R <= poly. P versus NP remains OPEN.

| Date | Run | Finding | Status |
|---|---|---|---|
| 2026-11-08 | WCLB-0001 (`../2026-11-08_CLAUDE_WCLB-0001.tex`) | Bridge(R) is vacuous if P!=NP; equivalent to P!=NP for any R with a known lower bound (Res, CP, AC0-Frege, PC); otherwise equals "R is optimal in the P=NP world". Monotonicity tension between bridge and lower bound. Literature: Res(parity) size bounds exist only for bounded depth (STOC 2026 papers); general dag-like open. | PROVED/EXACT (props), bridge OPEN |

Next: (1) check whether the corpus's R_mix341 has any known unconditional lower bound (Cor. 1 test); (2) test hard-family candidates against unrestricted Res(parity) upper bounds; (3) relativization audit of any Bridge proof.
