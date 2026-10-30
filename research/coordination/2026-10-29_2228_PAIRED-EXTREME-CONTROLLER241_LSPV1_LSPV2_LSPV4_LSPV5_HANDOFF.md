# LSPV-3 role handoff: PAIRED-EXTREME-CONTROLLER241
**Date:** 2026-10-29 22:28 PDT. **Owner:** LSPV-3, Adaptive Certificate Theorems. **Active coordination:** [issue #3](https://github.com/j15marti/pnp/issues/3). Issue #2 is paused. Neither P=NP nor P!=NP has been proved.

## Exact new restricted result
Take any proper binary CNF G = AND_j (ell_j1 OR ell_j2), with 2 distinct variables in each source binary clause, and private fresh pivot p_j. Construct original indexed proper 3CNF with source clauses C_(2j)=(ell_j1 OR ell_j2 OR p_j), C_(2j+1)=(ell_j1 OR ell_j2 OR NOT p_j). Then:
1. C_(2j) AND C_(2j+1) is logically equivalent to its binary remainder D_j, by resolution on p_j. The partial cube falsifying both literals of D_j is impossible, source-parent/pivot certified, and may be pruned without enumerating remaining pivot assignments.
2. The 4-way S/U all-literals-true/all-literals-false matrix of each pair is SS=SU=US=UU=FALSE. This follows from same-polarity two core occurrences and opposite-polarity pivot occurrence. Do **not** infer formula UNSAT: when D_j true both source clauses are disjunctively SAT.
3. Exhaustive source-occurrence S/U target construction and complement inversions, global 0^n/1^n and intermediate flips, and full source witness/refutation replay were implemented. All model tests are distinct from unrestricted 3SAT.

## Two exact specified-policy contrasts
**UNSAT source:** G_M comprises the four clauses (a OR b), (a OR NOT b), (NOT a OR b), (NOT a OR NOT b), plus M-4 copies of (a OR b), each paired. UP-DPLL ordered fresh pivots first then a,b without learning/memoization visits exactly 2^(M+2)-1 recursion states, while paired recognition + 2SAT is polynomial and even **core-first UP-DPLL uses only 7 states on identical inputs**. This is not a lower bound for general algorithms.

**SAT source:** G_M=(a OR b) AND (NOT a OR NOT b) plus M-2 copies of (a OR b), paired. Reflected Gray scanning pivots as low bits finds the first satisfying full candidate after 2^M+1 candidates, while one flip of the first literal in the source's first falsified clause repairs 0^n after both complete endpoints are checked. However the full diagnostics and pattern discovery can outweigh the saved candidate scans.

## Charged finite control (COMPUTATIONAL, not a theorem)
Seed 202610292228; 15 paired and 15 adverse controls; 16,824 pair-mode exact-truth tests and 2,352 three-clause joint-mode tests, all passed. For paired UNSAT M=14: pivot-first DPLL 65,535 recursive nodes / 4,439,948 selected-work units; adaptive controller with paired recognition 10,236 units; core-first DPLL 7 nodes. For paired SAT M=12: Gray 4,097 complete candidates, one source-directed repair flip, but controller **5,389** versus baseline **1,430** selected-work units. For strict22 W1 UNSAT: baseline 151 nodes/11,856 work versus controller 16,357 work. For strict22 S SAT: 9 baseline nodes/801 work versus controller 2,550 work. For K4 Tseitin UNSAT: 15 baseline nodes/932 work versus XOR-detecting controller 3,279 work. Values count charged selected primitive operations, not all interpreter actions. Simultaneous Python peak memory and wall time are in the separate local raw files.

## Provenance and publication boundary
Read actual [issue #3](https://github.com/j15marti/pnp/issues/3) and latest clarification; AGENTS.md blob 19656af10260, CODEX.md 754999f50de9, research skill b8df83a7b0b1, CLAUSE-EXTREME-DUALITY1 cb00592c590e, LSPV-1 EXTREME-SIGNED-CYCLE240 blob 303d077b0a68, and LSPV-2 EXTREME-CYCLE-UP240 blob c33d493e1f9f. The current main.tex was a verified substantive full 232,723-character source (pre-run blob 2166c3c239eb), not the outdated /tmp placeholder. The exact theorem overlaps standard resolution and 2SAT; no general novelty claim. Primary sources: Aspvall-Plass-Tarjan (1979), DOI 10.1016/0020-0190(79)90002-4; Davis-Putnam (1960), DOI 10.1145/321033.321034; Kullmann (2006), Sign-Sensitive Graph Representations of CNFs.

**GitHub public artifact readbacks:**
- [Formal compact report](../agents/lspv-3/2026-10-29_2228_LSPV-3_PAIRED-EXTREME-CONTROLLER241_PUBLIC.tex), commit 06963c504e582f61378d94861cd12c6d53f50a46, blob 0fed5059c25c086cf072621e84fbcacc122efd42, exact readback true.
- [Independent compact checker](../agents/lspv-3/2026-10-29_2228_LSPV-3_PAIRED-EXTREME-CONTROLLER241_spotcheck.py), commit 5cd99e6e9659f40e2e6ceeb222a56bdc0f9764a7, blob b8c568e931a6cb9ab021a5035b2389e9d84136f1, exact readback true.
- [Finite numeric summary/raw hashes](../agents/lspv-3/2026-10-29_2228_LSPV-3_PAIRED-EXTREME-CONTROLLER241_summary.json), commit 8a2d19fe2cad1df904d9319f5dff8c693a07dcaf, blob 7e186b64650f84fa7ca798a259db1f33f41fb164, exact readback true.

Complete six-page PDF and TeX, executable 31KB Python, and uncompressed 2.4MB+1.6MB raw JSON are verified local sandbox artifacts, not GitHub-published; their hashes are recorded in the published summary. Persistent Library upload attempted to /PNP/2026-10-29_LSPV-3_PAIRED-EXTREME-CONTROLLER241 but **FAILED** with container_session_unavailable. Do not count full data as shared across agent runs.

## Role-specific action
**LSPV-1:** compare signed-cycle graph lower bound on middle clauses against the paired source family. Its forced-middle SS/SU/US/UU blockage is trivial but offers no ordinary SAT contradiction; seek an additional exact SAT-side condition.

**LSPV-2:** test source-parent 2SAT resolution inference after ordinary source UP has saturated on connected strict22 instances. Preserve parent clause IDs and non-tautological resolvent proof chain; compare recognition against existing SOURCE_RUP_CHAIN164.

**LSPV-4:** audit scanner/read/write/peak overhead of endpoints, 4-way matrix, failed repair and algebraic recognition. Hostile negative controls already show controller overhead > DPLL for strict22 and Tseitin. Test same-realization actual source accesses and stronger CDCL.

**LSPV-5:** referee theorem and reuse the public report in synthesis only at restricted status; root owned LSPV-3 region may be updated separately. Avoid promoting a variable-order-specific exponential gap to an all-algorithm lower bound. Distinguish compact GitHub artifact from full local-only raw files.

**Next OPEN lemma:** connected strict signed exact-(2,2)-3CNF with both SAT and UNSAT instances, where extreme conflicts and bounded source resolution imply a new literal after saturation by UP, plus polynomial recognition and a total charged adaptive-search bound. Compare favorable core-first DPLL and CDCL/memoized baselines. Preserve the five existing schedules, task IDs, role-owned writing and OPEN status of P versus NP.
