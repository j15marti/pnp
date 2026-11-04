# Living log: worst-case derivation-cost program (W_R)

Target: superpolynomial worst-case lower bound for min derivation cost in a fixed strong R, plus the bridge SAT in P => Wbar_R(N) <= poly(N). P vs NP remains OPEN.

## 2026-11-04 — WORSTCASE-BRIDGE-0001
Report: `research/agents/claude/2026-11-04_CLAUDE_WORSTCASE-BRIDGE-0001.tex`
- Free strategy costs only a polynomial under SAT in P (Prop 1): justifies not charging strategy search.
- Bridge for any R with a known unconditional lower bound (Resolution etc.) is equivalent to SAT not in P: circular (Prop 2). Only R without known bounds (EF-level, Rmix341) are informative.
- Bridge for fixed R = "R weakly simulates every R_A" = exists-R-forall-A; crux is reflection (Thm). Lower bound for reflective R_T only gives independence, not P != NP.
- Literature: Atserias–Müller PAP (FOCS 2025) noted as a clue (CANDIDATE, unread). 
- Next: PV-provable fragment of Corr(e,k) for an explicit Levin-type machine.
