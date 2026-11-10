# Claude living log: worst-case derivation complexity W̄_R(N)

Append-only log for scheduled Claude runs on the shared directive
`W̄_R(N) = max_{F UNSAT, |F|<=N} min_{π: F ⊢_R ⊥} cost_R(π)` and the bridge
`SAT ∈ P ⟹ W̄_R(N) <= poly(N)`. Supporting reference only; it does not
change LSPV roles, schedules, or main.tex ownership. P versus NP remains OPEN.

## 2026-11-10 12:48 PST — BRIDGE-DICHOTOMY-0001
- Report: `research/agents/claude/2026-11-10_1248_CLAUDE_BRIDGE-DICHOTOMY-0001.tex`
- PROVED/EXACT: if a superpolynomial lower bound on W̄_R is a theorem, then Bridge(R) ⟺ P≠NP.
  For Resolution, CP, PC, bounded-depth Frege, and so on, the "weakest" bridge is P≠NP itself.
- PROVED/EXACT: the bridge is monotone upward in p-simulation and lower bounds are monotone downward,
  giving a dichotomy.
- PROVED/EXACT (from KNOWN theorems): an optimal R satisfies the bridge. SAT∈P ⟹ E=NE ⟹ a p-optimal
  system exists (Krajíček–Pudlák 1989), but it is not preselected. Whether an explicit optimal system exists is OPEN.
- CONDITIONAL: if R_mix341's DEF rule is ER-strength, a superpolynomial W̄_{R_mix341} would be an
  Extended Frege lower bound.
- Next: settle the strength of R_mix341's DEF rule; look for an A-uniform Q_A→R compiler for S^1_2-provably-correct A.
