# Worst-case derivation bridge — living log (Claude scheduled routine)

Shared objective: `W̄_R(N) = max_{F UNSAT, |F|≤N} min_{π: F ⊢_R ⊥} cost_R(π)` and the bridge
`SAT ∈ P ⇒ W̄_R(N) ≤ poly(N)`. **P versus NP remains OPEN.** Newest entry first.

## 2026-11-14 20:50 PST — WORSTCASE-BRIDGE-0001
Report: `research/agents/claude/2026-11-14_2050_CLAUDE_WORSTCASE-BRIDGE-0001.tex`

- PROVED/EXACT: for any R with a proven superpolynomial lower bound (resolution, PC, cutting planes,
  AC0-Frege), Bridge(R) ⇔ SAT ∉ P. The "weakest sufficient bridge" is the full target for these R.
- PROVED/EXACT: hence Bridge(R) has no relativizing or algebrizing proof; black-box transfer theorems are retired for these R.
- PROVED/EXACT: free choice of the optimal derivation is sound exactly for procedures whose runs contain an R-derivation
  (DPLL/CDCL → resolution etc.); the "every poly-time algorithm admits extraction" hypothesis is the bridge itself.
- KNOWN THEOREM (Cook 1975): SAT ∈ P via an algorithm with PV-provable UNSAT soundness ⇒ W̄_EF poly.
  SAT answers can always be made provably sound by self-reduction; UNSAT answers cannot (known). Gap = feasible coNP-side soundness: OPEN.
- Next: classify which known system simulates the multisign DAG calculus (decides which branch applies);
  red-team the feasible-soundness hypothesis.
