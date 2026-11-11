# Living log — worst-case minimum derivation cost \overline W_R(N)

Append-only log for the scheduled Claude routine on the shared five-role objective
`Wbar_R(N) = max_{F UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi)` and the bridge
`B3(R): SAT in P => Wbar_R(N) <= poly(N)`. Statuses follow AGENTS.md. **P versus NP: OPEN.**

## 2026-11-11 — BRIDGE-DICHOTOMY-0001
Report: `2026-11-11_1200_CLAUDE_BRIDGE-DICHOTOMY-0001.tex`; check: `bridge-dichotomy/`.
- PROVED/EXACT (elementary): if LB(R) (superpolynomial Wbar_R) is known, then B3(R) <=> P != NP.
  This covers Resolution, PC/PCR, bounded-depth Frege and the conditional Res(PC_r/F_p). For these R the bridge is not weaker than the goal.
- KNOWN (Cook 1975): for R >=_p EF, B3(R) holds for every poly-time SAT algorithm with PV-provable soundness.
  Bridge gap = only PV-unprovable algorithms; LB(R) = superpolynomial EF lower bound (open).
- PROVED/EXACT + COMPUTATIONAL: ER2 (fresh signed 2-input AND on distinct IDs + RES) realizes all 16 binary functions with <=3 gates, so ER2 ≡_p ER ≡_p EF.
- OPEN, high value: does the historical R_mix341 DEF rule reach ER2? If yes, [P2-B1] >= EF lower bounds.
- Literature: arXiv:2506.16956 (Proof Analysis Problem); Res(⊕) arXiv:2507.23008, 2511.20023, ECCC TR25-116/188.
  Unrestricted Res(⊕) size lower bounds remain open.
- Next: classify R_mix341 within the dichotomy; red-team any LB(R) family for short ER2 proofs.
