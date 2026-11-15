# Worst-case minimum-derivation program — living log (Claude routine)

Objective: W̄_R(N) = max over UNSAT F with |F| ≤ N of min over R-refutations of cost. Bridge B3_R: SAT∈P ⇒ W̄_R ≤ poly.
Status: **P versus NP remains OPEN.**

| Date | Run | Result | Status |
|---|---|---|---|
| 2026-11-15 | DERIV-0001 | Transfer-hardness ledger. If W̄_R is known to be superpolynomial, then B3_R ⇔ P≠NP. This covers Res, Res(k), CP, PC, bounded-depth Frege, regular Res(⊕), and multisign-hypergraph/DP reduction. Opposite monotonicity under p-simulation: the bridge gets weaker as R gets stronger, while the lower bound gets harder. A nontrivial split needs R ≥ AC⁰[p]-Frege, or general Res(⊕). | PROVED/EXACT (elementary) |
| 2026-11-15 | DERIV-0001 | Exact free-optimal tree-like minima. PHP 5/21/85. Tseitin K4/prism/K33/Q3: 55/95/151/255, versus GF(2) row ops 5/9/11/20. | COMPUTATIONAL |

Report: `research/agents/claude/2026-11-15_0000_CLAUDE_DERIV-0001.tex`
Next highest-value target: B3 for DAG Res(⊕) or AC⁰[2]-Frege, relative to PV-provable correctness.
