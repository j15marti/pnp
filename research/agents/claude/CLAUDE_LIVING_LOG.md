# CLAUDE scheduled routine: living log

Shared target (user directive): worst-case minimum derivation cost
`Wbar_R(N) = max_{F UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)`,
with the bridge `B3_R: SAT in P => Wbar_R(N) <= poly(N)`.

This routine is separate from the five LSPV roles. It owns no region of root
`main.tex` and does not edit `proof1.txt` / `proof2.txt`. New entries go at the top.

**Overall status: P versus NP remains OPEN.**

---

## 2026-11-10 23:51 PST: BRIDGE-CALIBRATION-0001

Report: `research/agents/claude/2026-11-10_2351_CLAUDE_BRIDGE-CALIBRATION-0001.tex`

Question this run: how much weaker is the "weakest sufficient bridge" B3_R than P != NP itself?

Results:
- **PROVED/EXACT (bridge collapse):** for every fixed R,
  `B3_R <=> (SAT not in P) OR (Wbar_R poly)` and
  `(LB_R AND B3_R) <=> (LB_R AND P != NP)`.
  So for any R whose superpolynomial lower bound is already known (Resolution, Cutting Planes,
  bounded-depth Frege, Polynomial Calculus, R_clock), **B3_R is equivalent to P != NP**: the bridge is no
  easier than the goal. This generalizes [P2-B6] and the TQBF/Haken oracle firewall.
- **PROVED/EXACT (generic-bridge test):** an argument for B3_R that uses only soundness, completeness and
  polynomial-time checkability of R also proves B3 for R_clock, and so would prove P != NP outright. A real
  bridge has to use what R specifically can simulate (compare LSPV-5/409).
- **PROVED/EXACT (monotonicity):** if R' simulates R, then B3_R implies B3_R' and LB_R' implies LB_R. As R gets
  stronger, the bridge gets easier and the lower bound gets harder.
- **KNOWN THEOREM imported (Cook 1975; Cook and Krajicek 2007):** if SAT is in P via an algorithm whose
  soundness PV proves, then EF is polynomially bounded. The remaining gap for every R at or above EF is
  H_feas, "SAT in P implies a PV-provably sound polynomial-time solver exists", which is OPEN.
- **CONDITIONAL:** if the authenticated R_mix341 simulates Extended Resolution, then [P2-B1] would be a
  superpolynomial EF lower bound, a major open problem. If it does not, a lower bound for it would make
  [P2-B2] equivalent to P != NP. Recommended classification target: does R_mix341 simulate ER?

Literature checked: Cook and Krajicek, JSL 2007; Bydzovsky, Krajicek and Oliveira, arXiv 1905.12935;
Egidy and Glasser, STOC 2025; Egidy, arXiv 2602.02294; Lu, Santhanam and Tzameret, ECCC TR25-134;
arXiv 2506.16956 (Proof Analysis Problem); PC with extension rule, ToC vol. 22 (2026).
None of them proves an EF lower bound or H_feas.

Open after this run: [P2-B1], [P2-B2], H_feas, whether R_mix341 simulates ER, and P versus NP.

Next-run candidates: (a) check, against the recovered /341 checker grammar, whether paid DEF gives a
polynomial simulation of Extended Resolution; (b) add the collapse theorem and H_feas as rows in the world
ledger (`world-ledger/build_ledger.py`).
