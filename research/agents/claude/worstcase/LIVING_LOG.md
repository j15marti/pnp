# Living log: worst-case minimum derivation cost (scheduled Claude routine)

Objective: W̄_R(N) = max over UNSAT F with |F| ≤ N of min over R-refutations of cost. Bridge: SAT ∈ P ⇒ W̄_R ≤ poly.
P versus NP: **OPEN**. Append newest entries at the top. Never rewrite past entries.

## 2026-11-14 06:50 PST: WORSTCASE-DERIV-0001
- Report: `research/agents/claude/2026-11-14_0650_CLAUDE_WORSTCASE-DERIV-0001.tex`
- PROVED/EXACT, elementary:
  - Theorem 1: the free-optimal-sequence bound holds for R-trace-faithful algorithms. DPLL and CDCL are trace-faithful to Resolution (KNOWN THEOREM), so they take exponential time in the worst case.
  - Theorem 2: if LB(R) is known, then Bridge(R) ⇔ SAT ∉ P. So for Resolution, Cutting Planes, AC0-Frege and Polynomial Calculus, the boxed bridge is P≠NP restated, not a weakening.
  - Theorem 3: both the bridge and the lower bound are monotone under p-simulation.
- A bridge strictly weaker than the separation can only live beyond the lower-bound frontier: AC0[p]-Frege, TC0-Frege, Frege, EF, or unrestricted Res(⊕). In the 2025–26 literature, Res(⊕) lower bounds are still depth-restricted.
- COMPUTATIONAL (`wc_min_derivation.py`, raw files `raw_php.json` and `raw_tseitin_a.json`):
  - Exact minimum tree-like Resolution size is 5, 21, 85 for PHP with n = 1..3, and 95, 255 for Tseitin on CL3 and Q3.
  - Fully charged F2 elimination costs 90 and 169 bit-ops on the same two Tseitin instances.
  - Every instance is minimally unsatisfiable, so the minimal reduced state is the input itself.
  - Bounded-treewidth Tseitin is easy for DAG Resolution, so this family does not survive shared DAGs.
- Next target: exact minimum DAG-Resolution length via SAT encoding (PHP^3_2, Tseitin K_{3,3}), and the reflection obligation for Res(⊕).
