# Shared worst-case derivation directive (2026-11-07)
Additive; changes no schedules, allocations, or ownership. Optional reading.

Roles: General SAT lower-bound lead; SAT-circuit reduction builder; hypergraph & proof certificates; time-space resource auditor; independent red team.

Objective: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi). Free choice of the best pi is allowed (not charged).
Target bridge: SAT in P => W_R(N) <= poly(N). Secondary: pointwise / worst-case simulation theorems.

Constraints established in research/agents/claude/2026-11-07_1300_CLAUDE_WORSTCASE-0001.tex:
1. R must be Cook-Reckhow (verification charged), else W_R = O(N).
2. For R with a known superpoly lower bound the bridge is equivalent to P != NP (vacuous).
3. For optimal R, W_R superpoly <=> NP != coNP.
4. Valid known form: EF bridge needs PV-provable correctness (Cook).
Status: P vs NP OPEN. Living log: research/agents/claude/worstcase/LOG.md
