# Worst-case minimum-derivation (W̄_R) living log — CLAUDE routine

Shared target: W̄_R(N) = max over UNSAT F, |F|≤N, of min over R-refutations of cost_R; bridge B(R): SAT∈P ⇒ W̄_R ≤ poly.

## 2026-11-14 22:51 PST — WCDERIV-0001
Report: `research/agents/claude/2026-11-14_2251_CLAUDE_WCDERIV-0001.tex`
- PROVED/EXACT: B(R) ⇔ (P≠NP ∨ R polynomially bounded). For any R with a known superpolynomial lower bound (Resolution, any Resolution-simulated multisign hypergraph calculus, CP, PC, bounded-depth Frege), B(R) **is** P≠NP. It is not a weaker lemma.
- PROVED/EXACT: B is upward-closed under p-simulation and lower bounds are downward-closed, so the bridge and the lower bound pull toward opposite ends of the simulation order. No system is known to satisfy both.
- KNOWN THEOREM (restated): an S^1_2-provably correct poly-time SAT algorithm ⇒ EF polynomially bounded. Whether P=NP alone implies EF is polynomially bounded is OPEN.
- PROVED/EXACT: relativization wall. For any lower-bounded R, "SAT∈P^TQBF ⇒ R poly-bounded" is false, so a proof of B(R) cannot treat machine steps as a black box.
- Free-optimal-sequence principle: valid, but it bounds only procedures whose traces are R-derivations.
- Next: find the weakest R* where B(R*) follows from a feasibility hypothesis weaker than S^1_2-provable correctness, and check whether R* is below the lower-bound frontier.
- P versus NP: OPEN.
