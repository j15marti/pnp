# Living log: worst-case minimum derivation cost W̄_R(N)

Status: **P versus NP remains OPEN.** Append one entry per run; newest at the bottom.

## 2026-11-14 run WCDERIV-0001
- Report: `research/agents/claude/2026-11-14_CLAUDE_WCDERIV-0001.tex`
- PROVED/EXACT: if W̄_R is unconditionally superpolynomial (resolution, cutting planes, polynomial calculus, bounded-depth Frege), then the bridge B_R ≡ SAT∉P. For those systems the "weakest bridge" is a reformulation of the goal, not a weakening.
- KNOWN: Cook–Reckhow (some polynomially bounded R exists iff NP=coNP); Krajíček–Pudlák 1989 (optimal and p-optimal proof systems); reflection (PV-provable soundness implies EF p-simulates the system).
- CONDITIONAL: B_EF holds for every SAT algorithm whose correctness is PV-provable.
- OPEN: G1 = a superpolynomial lower bound for EF, or for the DAG-hypergraph calculus if it is EF-strong. G2 = removing the PV-provability hypothesis.
- COMPUTATIONAL: exact minimum tree-like resolution sizes. PHP m=1..3 gives 5, 21, 85. Random 3-CNF UNSAT gives 21, 29, 37 for n=6, 8, 10 (`treelike_min.py`, `treelike_min_results.json`).
- Next: fix the DAG-hypergraph rules and classify the calculus (resolution-simulable or EF-strong).
