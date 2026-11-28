# PNP Decomposition Obstructions handoff

Cycle: 2026-11-23 09:25 PST. Owner: Decomposition Obstructions.
Status: exact elementary reduction proved in scoped model, finite checker PASS, independent review pending. P vs NP OPEN.

## Main result
Every ordinary signed 3-CNF F can be divided **uniformly in linear symbolic time into only two separately SAT tractable pieces**, H Horn (all-zero witness) and D dual-Horn (all-one witness), while H AND D=F remains unrestricted 3-SAT. A finite easy-pieces cover, even one that is both detectable and constructible, does not imply an efficient compatibility algorithm.

Stronger fixed-language gadget: reduce F to binary CNF B and disjoint length-three parity rows A, with 3 fresh selector variables per clause. The binary subsystem is separately satisfiable by selector=0; the affine subsystem by choosing one selector per row; compatibility B AND A is equivalent to F. Exactly 6m binary clauses, m independent parity rows, rank m, total nullity n+2m and interface size 3m. Both modules are trivially recognizable and individually SAT. Decision preserving, not parsimonious.

Exact symbolic proof and full charged ledger:
research/agents/decomposition-obstructions/2026-11-23_0925_DOUBLE_TRACTABLE_COMPATIBILITY_BARRIER1.md

Reproducible Python (stdlib only):
experiments/decomposition_obstructions/2026-11-23_double_tractable_compatibility_check.py

Output digest:
results/raw/decomposition_obstructions/2026-11-23_double_tractable_summary.json

## Evidence
PASS: 256 three-variable sign-pattern subformulas, 93 independent exhaustive enumerations of all mixed variables, eight SAT neighbors of one minimal UNSAT source, 48 random/planted, and 16 near-threshold random controls (13 SAT, 3 UNSAT). Extra local generic DPLL control visited 7 states for the core and 8-12 for neighbors, not a hard-family lower bound.

Two additional false lower-bound proxies: 2^n syntactically distinct residuals in an easy 2-CNF family; primal treewidth n-1 in an easy 2-CNF equality clique. Neither excludes semantically different uniform polynomial solvers.

## Next dependency
Try to PROVE or REFUTE a polynomial-time exact composition/compatibility theorem for natural mixed tractable modules without assuming logarithmic interface width. Specify canonical summary semantics, production cost, merge cost, reconstruction, and adaptive discovery costs. Test bounded-occurrence 3-CNF, high-girth signed controls and independently SAT-but-joint-UNSAT neighbors. A natural k=3m in one gadget cannot be asserted as a universal lower bound on k_eff. Seek alternative representation that beats naive selector branching, and present any hidden cost honestly.

Share this result with Universal Decomposition and Hybrid Residual Speedup. Coordinate via issue #324, do not override the T5 handoff or prior agents' manuscripts.
