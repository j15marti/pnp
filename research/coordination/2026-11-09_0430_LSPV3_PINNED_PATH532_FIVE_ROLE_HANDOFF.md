# Five-role handoff: LSPV-3/532, 2026-11-09 04:30 PST

**Status PROVED/RESTRICTED plus COMPUTATIONAL. P versus NP remains OPEN.**

The source-authenticated original strict 3-CNF signed mod-3 *path* from [P2-L3-529] has $20k+1$ original clauses over $3(2k+1)$ indicators and a projected unpinned boundary relation with exact no-auxiliary CNF clause minimum $3^{k+1}$ [P2-L3-530]. To test whether this restricted representation minimum forces actual proof work, pin its $k+2$ boundary groups to a wrong global charge using four original proper-3CNF pin clauses (with two fresh variables) per group. All clauses remain actual source input, no free units or DEF facets.

**New symbolic explicit upper bound:** $n=8k+7$ Boolean variables, $m=24k+9$ original signed proper width-three clauses, $9k+3$ paid ordinary Resolution inferences, $18k+6$ premise references and unit-weight ideal shared-DAG span $4k+1$. Source pins cost 3 RES each; internal mod-3 transitions cost 6 RES per nonterminal vertex; final contradiction 3 RES. This is **an exhibited upper bound, not a minimum**, and changes the obligation from unpinned function representation to UNSAT of a source-pinned instance.

Independent exact source reconstruction and pivot verification for $k\in\{1,2,3,4,5,8,12\}$ passed, including 42 malformed/corrupt certificate rejections and seven SAT deletion witnesses (delete one final pin facet). A distinct repo-published compact JS generator was executed in V8 with signed RES replay. Official historical full R_mix341 checker **not** executed.

**Role routing, without role reassignment:** LSPV-1, retain hard-family/B3 quantifier distinction and full-source proof-to-proof transfer [P2-C3],[P2-B2]. LSPV-5, attack the historical acceptance/shorter-derivation question and assumption scope; never infer hardness from flat boundary size. LSPV-3, seek actual native accepted RES/AND3/GF2/LOCAL-CONVERT/DEF interface with source retraction [P2-D1]. Route A LSPV-2 and LSPV-4, use this as a bounded-width positive fallback test only; the all-input recursively iterable same-machine FLMV contraction remains OPEN.

**Established sources:** Urquhart 1987 ordinary Resolution expander-Tseitin lower bound, de Colnet-Mengel bounded-degree regular-resolution treewidth theorem, Cai-Li arXiv:2610.02047 (2026) preprint upper bounds, Pang arXiv:2610.00837v2 opposite-characteristic restricted lower bounds. This pinned path is deliberately easy, not one of their expander-hard families. No complete native grammar, all-rule superpolynomial bound, same-R B3 or P-vs-NP resolution.

**Exact ledger:** new [P2-L3-532] refines [P2-L3-529],[P2-L3-530],[P2-D3],[P2-C3]; [P2-D1],[P2-C3],[P2-B1],[P2-B2] OPEN. [P1-01],[P1-03],[P1-04] OPEN.

Evidence:
- research/agents/lspv-3/2026-11-09_0430_LSPV3_PINNED_TERNARY_LINEAR_RES532.md
- experiments/arc/lspv3_532_pinned_ternary_path_linear.cjs
- results/raw/arc/2026-11-09_0430_LSPV3_PINNED_TERNARY_PATH532_RAW.json

Both trackers read: proof1 unchanged expected; proof2 update only if verified material change. Preserve historical rules/weights and existing two Route A, three Route B agents, schedules and enabled states. P versus NP OPEN.
