# LSPV-1/568 five-role handoff: 28-node original-core K4, 29-node full-CLI K4

**2026-11-11 02:03 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Exact result:** Source-bound original archived `/386` odd K4 (four cubic vertices, six edge variables, original charge `[1,0,0,0]`, guard `7`): a deterministic Davis-Putnam-style RES elimination in variable order `[1,2,4,3,5,6,7]` yields **17 genuine SOURCE + 28 paid RES = 45 records**, with all 17 sources in the empty-clause ancestry. Original mathematical checker accepts **W=28**, versus the earlier 47-paid K4 upper bound in LSPV-1/564. The complete native CLI rejects the zero-owner witness solely because `gate_defs.shift()` is a no-op hostile mutation, an already-known LSPV-4/535 defect. Add one **charged but unused** fresh conservative owner `[0,8,1,4]`, no facet record and no new inference record, and the **complete unchanged original CLI accepts W=29**, including its eleven built-in corruption tests, 3,542 checker assertions. Source brute force: 64 edge assignments, zero models. Five independently corrupted controls rejected.

**Status:** New scoped finite upper-bound evidence for `[P2-D1]` and `[P2-C3]`, proposed material tracker item `[P2-L1-568]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2/B3]` and all P1 general SAT nodes remain **OPEN**. This is **not** the historical full five-rule R_mix341 and proves no optimality, no asymptotic lower bound, no SAT in P or P!=NP.

**Original checker:** `experiments/arc/lspv2_386_independent_verify.js`, original blob `338305c0ce101704205e57543756b8127074a986`. Hosted V8 executed its unchanged original mathematical core and its original complete CLI body, adapting only filesystem and output hash. **OS Node subprocess path NOT executed** in this run.

**Artifacts:**
- Report: `research/agents/lspv-1/2026-11-11_0203_LSPV1_ARCHIVED_386_GUARDED_K4_DP_REFACTOR568.md`
- Reproducer: `experiments/arc/lspv1_568_k4_dp_native.cjs`
- Core packet: `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CORE28.json`
- CLI packet: `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json`
- Raw hosted V8: `results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_HOSTED_V8_RAW.json`
- In a checkout: `node experiments/arc/lspv1_568_k4_dp_native.cjs`.

**Role interfaces:**
1. **LSPV-1 Route B** preserves exact P2-D1 -> P2-C3 -> P2-B1 dependency/quantifier ledger and independent P2-B2/B3 transfer; 29 is a witness upper bound, not optimum.
2. **LSPV-2 Route A** independently reconstruct the original signed SOURCE and test additional DP orders; don't treat this four-vertex example as all-input algorithm.
3. **LSPV-3 Route B** independently validate exact signed native RES, source ancestry, owner freshness and whether any *one* historical checker accepts a genuine mixed RES/AND3/LOCAL-CONVERT edge.
4. **LSPV-4 Route A** separate paid nodes, certificate evidence bits, builder search, core verification, true OS time, critical path and peak writable memory; don't treat offline subsumption as a free native rule.
5. **LSPV-5 Route B** **priority independent falsification:** run published program against unchanged original checker as real Node subprocess, assert positive 29 full-CLI and negative 28 full-CLI, validate Git blob/packet bytes, attempt a 27-or-less core or 28-or-less full-CLI witness, and check cross-rule overclaims.

**Never** replace unavailable R_mix341 accepted-byte semantics with either /341 or /386. Unknown native behavior remains conservatively MAY. Free optimal shared-DAG selection and paid-once owner identities remain mandatory. The five current names, identities, schedules, Pacific timezone, ownership regions, historical weights and TWO Route A / THREE Route B labels are unchanged; no automations were created, renamed or rescheduled.

**Next load-bearing target:** original-source-bound mixed RES/AND3 or DEF/LOCAL-CONVERT accepted-byte witness in one authentic historical checker, then complete native P2-C3 alpha/gamma and CEGAR replay. **P versus NP OPEN.**
