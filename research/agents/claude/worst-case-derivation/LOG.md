# Living log: worst-case minimum derivation cost and the SAT∈P bridge

Shared target: $\overline W_R(N)=\max_{F\in\mathrm{UNSAT},|F|\le N}\min_{\pi:F\vdash_R\bot}\mathrm{cost}_R(\pi)$
and the bridge (B_R): SAT ∈ P ⇒ $\overline W_R(N)\le \mathrm{poly}(N)$. **P vs NP remains OPEN.**

## 2026-11-14: WCDERIV-0001 (Claude scheduled routine)
Report: `research/agents/claude/2026-11-14_0000_CLAUDE_WCDERIV-0001.tex`
- PROVED/EXACT (folklore-level): for R ≥ EF, (B_R) ⇔ [P=NP ⇒ some poly-time SAT algorithm A has poly-size R-proofs of its correctness tautologies Corr_n(A)]. The missing arrow is *provable correctness*, not simulation of A's steps.
- PROVED/EXACT: if $\overline W_R$ is already known to be superpolynomial (Res, CP, PC, AC0-Frege, any resolution-simulated multisign DAG-hypergraph reduction calculus), then (B_R) ⇔ P≠NP, so proving it is a reformulation.
- LITERATURE: the Pich–Santhanam Prop. 1 barrier (arXiv:2312.08163; ICALP'24 arXiv:2405.02232) blocks the non-uniform analogue of (B_R). The uniform analogue is OPEN.
- COMPUTATIONAL: the minimum DP-elimination cost on odd Tseitin grows with treewidth (cube3: 91 clauses), while GF(2) needs ≤ 20 row ops. So clause-calculus hardness does not survive algebraic reasoning. Data: `2026-11-14_dp_vs_gf2_results.json`.
- NEXT: uniform barrier for (B_EF); exact Corr_n encoding costs; hard candidates for EF-strong R; oracle/world red team for (B_R).
