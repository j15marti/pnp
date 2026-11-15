# Living log — worst-case minimum-derivation program (Claude scheduled runs)

Target: W̄_R(N) = max over UNSAT F, |F| ≤ N, of min cost of an R-refutation;
bridge B_R: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). Append-only; newest last.
**P versus NP remains OPEN.**

## 2026-11-14 19:51 PST — BRIDGE-MONOTONE-0001
Report: `research/agents/claude/2026-11-14_1951_CLAUDE_BRIDGE-MONOTONE-0001.tex`
Code/data: `research/agents/claude/bridge-monotone/`
- PROVED/EXACT: if R' p-simulates R, then B_R ⇒ B_R' and LB_R' ⇒ LB_R. Making one
  half easier makes the other harder.
- PROVED/EXACT: if R already has a known superpolynomial lower bound (Resolution,
  Cutting Planes, bounded-depth Frege, Polynomial Calculus, and any hypergraph
  calculus that one of them p-simulates), then B_R ⇔ P ≠ NP. For these systems
  the bridge is not a weaker step.
- PROVED/EXACT (Krajíček–Pudlák style): for a consistent theory T ⊇ PA, an explicit
  system R_T is p-bounded whenever some poly-time SAT algorithm is T-provably
  correct. What is left open: the case where SAT ∈ P holds but T cannot prove it.
- COMPUTATIONAL: exact minimum tree-like Resolution sizes for PHP (5, 21, 85) and odd
  Tseitin (23, 55, 151), and GF(2) elimination refutes each Tseitin instance in
  ≤ 18 row operations (hostile control).
- Literature (2026): found no superpolynomial lower bound for Frege, AC0[p]-Frege or EF.
  Found no source showing P=NP ⇒ EF p-bounded.
- Next: either separate the multisign DAG-hypergraph + GF(2)/DEF calculus from an
  explicit system (this retires it as an intermediate), or show it p-simulates EF.
