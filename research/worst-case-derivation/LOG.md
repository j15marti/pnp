# Worst-case derivation-cost program: directive and living log

Objective (all five roles): study  W_R(N) = max_{F in UNSAT,|F|<=N} min_{pi: F |-_R bot} cost_R(pi); min is free (strategy discovery not charged).
Priority bridge: SAT in P  =>  W_R(N) <= poly(N). Stronger pointwise / worst-case simulation theorems are secondary.
Roles: General SAT lower-bound lead; SAT-circuit reduction builder; hypergraph & proof certificates; time-space resource auditor; independent red team.
Status: P vs NP OPEN. Entries below are not proofs of the lower bound or the bridge.

## 2026-11-08 WORSTCASE-0001 (research/agents/claude/2026-11-08_CLAUDE_WORSTCASE-0001.tex)
- PROVED: free min over derivations = nondeterministic measure; W_R poly <=> R p-bounded => NP=coNP.
- PROVED (elementary): for any R with an unconditional superpoly W_R (Resolution, Tseitin), the bridge is *equivalent* to SAT notin P, i.e. circular.
- Bridge holds trivially only for an optimal proof system R* (open existence); then the lower bound target is NP!=coNP (stronger than P!=NP).
- Provable-correctness bridge (PV proves SAT in P => EF p-bounded) is a known theorem; hypothesis is provability, stronger than SAT in P.
- Literature (search snippets only, unverified in detail): Pich-Santhanam 2021 & arXiv 2312.08163; no unconditional EF lower bound found 2025-26.
- Next: restricted bridges, time-space cost formalization, pointwise-simulation consistency check.
