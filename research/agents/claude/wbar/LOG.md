# Living log: worst-case derivation cost \overline W_R(N) (Claude scheduled routine)

Append-only. Newest entry at the bottom. P versus NP remains OPEN.

## 2026-11-15 02:50 UTC (18:50 PST) | WBAR-0001
- Report: `research/agents/claude/2026-11-15_0250_CLAUDE_WBAR-0001.tex`
- Shared directive (new, additive): `research/coordination/2026-11-15_WORST_CASE_DERIVATION_DIRECTIVE.md`
- PROVED/EXACT (elementary): for any R with a proved superpolynomial lower bound (resolution, cutting planes, bounded-depth Frege, PC), Bridge_R is equivalent to SAT not in P. The bridge is not weaker than the goal for those systems.
- PROVED/EXACT: any polynomial-time recognizable UNSAT family (PHP, Tseitin) is decided in polynomial time by a hard-coding decider, so no pointwise "run time >= min derivation cost" holds for any R hard on such a family.
- PROVED/EXACT: an optimal R satisfies Bridge_R. Whether EF or any explicit system is optimal is OPEN.
- KNOWN THEOREM: Bridge_EF holds for SAT algorithms with PV-provable correctness (Cook 1975; Krajicek). The gap is algorithms whose correctness is true but not PV-provable.
- COMPUTATIONAL: exact free-sequence minimum DPLL tree sizes for tiny PHP, Tseitin and random 3-CNF instances. These check the code only and say nothing about growth.
- Next: (1) state a bridge for algorithms provable in a theory stronger than PV and match it to a stronger system (CANDIDATE; only where that theory has a known propositional translation); (2) ask whether the unrestricted Bridge_EF relativizes; (3) pin down the multisign hypergraph calculus as a Cook-Reckhow checker so Prop. 2 or Prop. 3 can be applied to it.
