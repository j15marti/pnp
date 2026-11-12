# Living log: worst-case derivation complexity (CLAUDE scheduled runs)

Target (shared directive):
`W̄_R(N) = max_{F ∈ UNSAT, |F| ≤ N} min_{π : F ⊢_R ⊥} cost_R(π)`, with the bridge
`B_R : SAT ∈ P ⟹ W̄_R(N) ≤ poly(N)`.

**P versus NP remains OPEN.** Each entry is append-only; newest last.

## 2026-11-12 06:51 PST — WCDC-0001
Report: `research/agents/claude/2026-11-12_0651_CLAUDE_WCDC-0001.tex`

- PROVED/EXACT (Theorem 2): assuming cost and length are polynomially equivalent,
  `B_R ⟺ (P = NP ⟹ R p-optimal) ⟺ (P = NP ⟹ R optimal)`. Under P = NP the
  properties p-bounded, optimal and p-optimal coincide.
- PROVED/EXACT (Lemma 1): under P = NP, a minimum-size refutation in a p-bounded R can
  be found in polynomial time. So leaving strategy search uncharged costs nothing in
  the bridge direction, and hardness of automating proof search (Atserias–Müller) is
  irrelevant to W̄_R.
- PROVED/EXACT (Corollary 3): for any R with a known lower bound (Res, Res(k), CP, PC,
  AC0-Frege), B_R ⟺ P ≠ NP, so the bridge is a reformulation of the goal.
  Under p-simulation, bridges are inherited by stronger systems and lower bounds by
  weaker ones. Only Frege/EF-level systems leave either half open.
- PROVED/EXACT (Proposition 4): a portfolio of systems that switches strategy adaptively
  is itself one system, with W̄ = max_F min_i w_i. A hard family must be hard for every
  member at once. Tseitin is FALSIFIED/RETIRED as portfolio-hard.
- KNOWN THEOREM: Cook 1975 (a SAT algorithm with PV-provable soundness makes EF
  p-bounded); Pich–Santhanam arXiv:2312.08163 (S^1_2-feasible anticheckers plus an EF
  lower bound give P ≠ NP). Both hypotheses are OPEN.
- Next target: find the weakest feasibility hypothesis a fixed combined inference
  system R could satisfy, and check that adding its witnessing axioms preserves R's
  lower bounds.
