# Living log: worst-case minimum derivation cost and the conditional bridge

Shared objective: Wbar_R(N) = max over UNSAT F with |<F>| <= N of min over pi: F |-_R bot of cost_R(pi).
The bridge (corpus label B3, P2-B2) is: SAT in P implies Wbar_R(N) <= poly(N).
**P versus NP remains OPEN.**

## 2026-11-11: WORSTCASE-BRIDGE-0001
- Report: `2026-11-11_CLAUDE_WORSTCASE-BRIDGE-0001.tex`.
- PROVED/EXACT (collapse lemma): if the lower bound LOWER(R) holds, then BRIDGE(R) is equivalent to SAT not in P.
  - So for Resolution, CP, PC, AC0-Frege and R_clock, the bridge is equivalent to P != NP. It is not a weaker target.
- Consequence: a noncircular bridge must be a uniform compiler into a system whose lower bound is currently unprovable (EF or stronger).
- Literature checked:
  - Cook 1975: PV-provable correctness gives polynomial-size EF proofs.
  - Pich–Santhanam, arXiv:2312.08163: if EF is not p-bounded, P != NP follows under S^1_2 provability hypotheses (CONDITIONAL).
  - Pich–Santhanam, FOCS 2019: barriers to EF lower bounds.
  - Jeřábek 2025: Frege lower bounds are still only quadratic in size.
- Rejected: the external claim "P=NP implies EF p-bounded". This is not known.
- COMPUTATIONAL: exact minimum tree-like Resolution leaves are 3, 11 and 43 for PHP(2,1), PHP(3,2) and PHP(4,3), and 28 for Tseitin K4 odd. See `worstcase/`.
- Next: decide whether R_mix341 p-simulates EF, then relabel B3 accordingly.
