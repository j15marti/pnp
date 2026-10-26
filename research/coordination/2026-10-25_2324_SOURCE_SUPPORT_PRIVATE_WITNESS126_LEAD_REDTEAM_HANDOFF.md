# LSPV-3 SOURCE-SUPPORT-PRIVATE-WITNESS126 | Lead and Red-Team Handoff
Timestamp: 2026-10-25 23:24 America/Los_Angeles. Existing five agents and their scheduling and ownership are unchanged.

Status: PROVED/EXACT restricted source-supported branching lemma; computational finite controls; bounded all-UNSAT certificate existence OPEN; ARC-EDGE-90 OPEN; P versus NP OPEN.

The result is the private-witness provenance conservation theorem. On UNSAT source F, let E be individually essential original clauses; choose a full assignment alpha_i satisfying all source clauses except C_i for each i in E. In any accepted full original-variable branching tree whose terminal at sigma certifies UNSAT using an audited subset I of original clauses, the leaf reached by alpha_i MUST cite i in I. Therefore E subset union of terminal I, sum over leaves |I intersect E| >= |E|, and if every terminal has at most K source clauses, height h obeys K*2^h >= |E|. This applies to any sound checked source-subset terminal proof system, including CP, PC, resolution, source-audited affine, and actual fixed-A UNSAT checks. It does NOT automatically extend to transformed children or arbitrary JOIN DAGs.

Hard controls: strict signed exact-(2,2) source W1 has 15 vars, 20 unique proper ternaries, all 20 clauses essential; odd K4 has 16/16 essential and exact finite optimal pure-DPLL 28 leaves (697 ternary states, depth 6); odd K3,3 has 24/24 essential. K4 has an efficient degree-three GF(2) PC proof with one leaf using all source clauses, confirming the theorem does NOT imply long proof or high decision time. Two disjoint odd K4 cores have 32 clauses and ZERO individually essential clauses, negating extrapolation to all UNSAT formulas. SAT/UNSAT, source ID mutation, Horn, 2SAT, even-parity, two true DIMACS descendants were controlled.

This is an explicit obstacle to cheap source-subformula-only certificates with too few branch leaves or source axioms, NOT a near-boundary $N^{1.4008}$ leaf-volume lower bound. Source-provenance incidence cannot be silently charged as physical child bytes, and may be packed/represented implicitly. A nonlinear target would have to survive derived constraints, perfect boundary joins, affine and resolution bypasses, and same-A bit/peak-space accounting.

Artifacts:
- research/agents/lspv-3/2026-10-25_2324_LSPV-3_SOURCE_SUPPORT_PRIVATE_WITNESS126.tex
- research/agents/lspv-3/2026-10-25_2324_SOURCE_SUPPORT_PRIVATE_WITNESS126_compact.py
- research/agents/lspv-3/2026-10-25_2324_SOURCE_SUPPORT_PRIVATE_WITNESS126_raw.json

For LSPV-1, ask for a derived-child invariant provably not discharged by a one-terminal short PC/CP/refutation. For LSPV-4, audit whether the source-supported terminal proof unrolling preserves the indexed RTM model and whether reused DAG proof nodes change the support accounting. For LSPV-5 red team, try an accepted cheap proof with terminal original-source support less than the number of essential clauses, or expose a wrong-name dependency, and audit the coNTIME clock. An independently checked counterexample would falsify the theorem as scoped; if derived children change the scope, label this as a new problem rather than contradiction.
