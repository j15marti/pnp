# Worst-case minimum-derivation directive: living log

Shared objective: W̄_R(N) = max over UNSAT F with |F| ≤ N of the min-cost R-refutation; bridge SAT∈P ⇒ W̄_R(N) ≤ poly(N).
Status labels follow AGENTS.md. **P versus NP remains OPEN.**

## 2026-11-13 — BRIDGE-COLLAPSE-0001
Report: `research/agents/claude/2026-11-13_CLAUDE_BRIDGE-COLLAPSE-0001.tex`
- PROVED/EXACT: Bridge(R) ⇔ (SAT∉P ∨ R polynomially bounded). For every R with a known superpolynomial lower bound (Resolution, CP, PC, bounded-depth Frege, …), Bridge(R) ⇔ P≠NP, so it is a reformulation. ∃R[Bridge(R) ∧ LB(R)] ⇔ P≠NP.
- PROVED/EXACT, FALSIFIED: pointwise simulation PS(R) fails for every R whose hard family can be recognized in polynomial time. A decider that recognizes the family answers it in polynomial time. This generalizes REFEREE295.
- PROVED/EXACT: PS(R) ⇔ R p-simulates every clocked-algorithm system R_A. A p-optimal R would suffice; whether a p-optimal system exists is OPEN (Krajíček–Pudlák).
- The only non-trivial targets are Frege/EF-strength R. For EF the bridge would follow if correctness of a P=NP witness were provable in PV, a CANDIDATE condition that is not known. LB(EF) is OPEN.
- Next: each role works with EF-strength R, or applies the recognizer test to every proposed hard family.
