# Living log: worst-case minimum-derivation route (Claude scheduled routine)

Target: `Wbar_R(N) = max_{F UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)` and the bridge `B3_R: SAT in P => Wbar_R(N) <= poly(N)`.
Status labels follow AGENTS.md. **P versus NP: OPEN.** Newest entry first.

## 2026-11-14 run WCD-0001
- **Report:** `research/agents/claude/2026-11-14_CLAUDE_WCD-0001.tex`
- **Proved (elementary, PROVED/EXACT):** the "monotone sandwich". Systems with a proved superpolynomial `Wbar_R` (LB) are downward closed under p-simulation; systems with a proved B3 (BR) are upward closed. The route closes only if one fixed R is in both.
- **Corollary for the red team:** B3_R follows from SAT not in P for every R, so no computation can falsify B3 without proving P = NP. Red-team results against B3 can only be GAP findings.
- **Occupancy (KNOWN THEOREMS):** LB currently reaches tree-like, regular and bounded-depth Res(xor) (2024-2025) but **not** dag-like Res(xor). BR has no non-trivial member: the only mechanism is Cook's PV-to-EF translation, which needs PV to prove A correct, a stronger assumption than SAT in P.
- **Gap:** the whole interval from Res(xor) to EF, plus the reflection gap.
- **Duplication:** B3(Res) <=> P != NP, CANON2R = EF and the PV conditional were already in the corpus (LSPV-1/339, /357, /398; REFEREE343, /365). They are cited, not claimed again.
- **Note:** the repo's active five-agent team is now TMR (directive 2026-11-13 12:49). This routine writes only under `research/agents/claude/` and does not edit root `main.tex`.
- **Next target:** look for a B3-type bridge for any system strictly weaker than EF, or a feasible-reflection statement derivable from bare SAT in P. Alternatively, track dag-like Res(xor) lower-bound progress, the next LB frontier.
