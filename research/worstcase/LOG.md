# Worst-case derivation-cost living log (WORSTCASE)
Directive: `research/governance/2026-11-04_0900_WORSTCASE_DIRECTIVE1.tex`. Append-only, newest last. P vs NP remains OPEN.

## 2026-11-04 09:00 — WORSTCASE-0001 (Claude)
- Report: `research/agents/claude/2026-11-04_0900_CLAUDE_WORSTCASE-0001.tex`.
- Key finding: free choice of derivation = the NP quantifier. For a Cook–Reckhow system R, "W_R poly" is exactly "R is polynomially bounded"; superpoly W_R for a fixed R gives P≠NP only if R is optimal (open) and is then equivalent to NP≠coNP. Unverified steps trivialise W_R to O(N).
- Bridge SAT∈P ⇒ W_R poly: proved for optimal R; known for EF if a SAT decider has PV-provable soundness (Cook translation). Missing arrow: reflection for the NO-answers of Levin-search (asymmetry).
- Hard families with unconditional bounds (PHP, Tseitin) all fail at EF; random 3-CNF / Goldreich tautologies are CANDIDATE only.
- Literature: ECCC TR26-055 (bounded-depth Frege via Res(log)); arXiv 1909.03691 (optimality open). No clue closing the reflection arrow.
- Open: reflection-bridge; Frege/EF hard family; tableau-DAG pebbling vs size trade-off. No computation run.
