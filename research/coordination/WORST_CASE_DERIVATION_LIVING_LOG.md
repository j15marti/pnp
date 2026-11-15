# Worst-case minimum derivation cost — living log

Shared target: W̄_R(N) = max over UNSAT F with |F| ≤ N of min over R-refutations π of cost_R(π); bridge: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).
**P versus NP remains OPEN.** Append newest entries at the top.

## 2026-11-15 — WCD-0001 (scheduled Claude run)
- Report: `research/agents/claude/2026-11-15_0000_CLAUDE_WCD-0001.tex`
- KNOWN: once its rules are fixed and checkable in polynomial time, W̄_R is the Cook–Reckhow proof-size function. Superpolynomial W̄_R for every R is equivalent to NP ≠ coNP.
- PROVED/EXACT (elementary): whenever R already has an unconditional superpolynomial lower bound (Resolution, Cutting Planes, AC0-Frege, Polynomial Calculus), Bridge(R) ⇔ SAT ∉ P. That bridge is a restatement of the goal, not progress. A resolution-like multisign hypergraph calculus is in this case.
- KNOWN/CONDITIONAL: the bridge holds for Extended Frege (EF) if the hypothetical algorithm's correctness is provable in the weak arithmetic theory PV (Cook 1975). No superpolynomial lower bound is known for Frege or EF; the 2025–26 literature check found none.
- COMPUTATIONAL: exact minimum tree-like Resolution sizes, with the optimal derivation given for free. PHP^4_3: 85; Tseitin on Q3: 255. Script: `experiments/claude/wcd_treeres_exact.py`; data: `results/raw/claude/2026-11-15_WCD0001_treeres_exact.jsonl`.
- Hostile controls: Tseitin is easy over F2 (Gaussian elimination) and PHP is easy in Cutting Planes and EF. Neither survives a switch of reasoning method.
- Next step: write down the exact multisign DAG rules and decide whether the calculus p-simulates EF, where extension corresponds to naming shared hyperedges.
