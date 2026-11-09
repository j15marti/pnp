# Five-role handoff: LSPV-1/543 weighted MAY source-merge ceiling

**2026-11-09 13:01 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**New affected evidence node:** [P2-L1-543]. Still-OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Support/control references: [P2-L3-536], [P2-L3-538], [P2-L1-538], [P2-L5-467], [P2-L1-542]. Neither B1/B2/B3 nor Route A universal FLMV is discharged.

**New restricted exact theorem:** In the explicit source-partition MAY relaxation with $m$ essential original-source blocks and arbitrary charged type-$j$ abstract joins of at most $r_j$ blocks, each costing $c_j\ge0$, the optimal abstract goal cost is
$$
D_J(m)=\min_{\substack{t_j\ge0\text{ integers}\\\sum_j(r_j-1)t_j\ge m-1}}\sum_j c_jt_j.
$$
This is a sharp heterogeneous arity/cost generalization of LSPV-3/538's unit binary-only case. With fixed finite priced types it is $O(m)$; it cannot certify a superlinear or superpolynomial all-native minimum. Potential $V(\pi)=\rho(m-|\pi|)$, $\rho=\min_j c_j/(r_j-1)$, is cost-sound **only** if all actual native rule types have authenticated exhaustive dependency/side-read merge bounds and charged first-use mappings. Unknown global side-reading must be conservatively overapproximated; a possible unit-cost merge of all $m$ blocks makes the MAY distance at most one, but does NOT establish such a historical rule exists.

**Independent tests and trust:** complete explicit-partition Dijkstra versus knapsack DP over seven weighted rule sets and m=2..6; JS 108 assertions, separate Python 105 grouped checks, no mismatches, max 203 states. This is the abstract model only. No native R_mix341 accepted-byte checker, no SAT/UNSAT source execution, and no solver benchmark. Zero-cost multi-source and hypothetical global macro are hostile controls.

**Artifacts verified by exact GitHub readback:**
- research/agents/lspv-1/2026-11-09_1301_LSPV1_WEIGHTED_MAY_MERGE_CEILING543.md, blob c91713012b82676a2e6161102c244e98de2ccd02
- experiments/arc/lspv1_543_weighted_source_merges.js, blob 0b30ac574647b9adcbca30747443aa223ce8c001
- experiments/arc/lspv1_543_weighted_source_merges_independent.py, blob 208bc3d46b6ba07b2ea9cbf7f6f61947169a1152
- results/raw/arc/2026-11-09_1301_LSPV1_543_WEIGHTED_MERGES_RAW.json, blob 972ee528214125b446923a164e249c87f49b0ad5

**LSPV-1:** seek a noncircular source-exact typed GF(2)/DEF/LOCAL legal-merge restriction stronger than source arity, maintain separate B3 ledger.
**LSPV-3:** construct source-authenticated typed transformers with precise side-read capacity and first-use source provenance. Every unknown native transition must remain in MAY closure.
**LSPV-5:** independently test goal preservation and full shared-DAG cost sponsor flow, including zero-cost and context discharge.
**LSPV-2 / LSPV-4:** Route A remains primary. Only use this as a model-specific caution: source-merge count cannot provide all-machine time/space lower bounds; same-machine child materialization remains separately charged.

Governance unchanged: exactly five roles, 2 Route A/3 Route B, all schedules and weights preserved. P versus NP remains OPEN.
