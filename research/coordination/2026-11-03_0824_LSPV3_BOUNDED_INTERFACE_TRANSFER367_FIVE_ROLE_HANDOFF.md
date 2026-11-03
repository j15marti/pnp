# LSPV-3 handoff: Bounded-interface transfer 367
**November 3, 2026, 08:24 PST. P versus NP OPEN.** No tasks, task identities, schedules, enabled states, fixed Rmix341 grammar/weights, or owner regions changed.

## Published theorem starting points and transfer failure
1. **KNOWN THEOREM:** Haken (1985) proves exponential ordinary DAG Resolution size on PHP(n+1,n); Cook-Reckhow (1979) proves polynomial Extended Resolution for the SAME pigeonhole sources. Since Rmix341 includes paid ER2, its minimum is polynomial for that family. Backwards projection to Resolution with polynomial logical-node amplification is impossible. LSPV-2 HAKEN-ER2-NONPROJECTION364 already established this; it is not novel here.
2. **KNOWN THEOREM and prior duplication:** Alekseev, Theory of Computing 22, Article 4 (published June 21, 2026), proves exponential BIT-SIZE rational polynomial-calculus-with-extensions-and-square-root complexity of the algebraic BVP equation. The old LSPV-3 BVP-BITBLAST-COLLAPSE354 already established a faithful carry CNF with EXACT Rmix341 minimum 2n+1; this research discovered and credited the prior duplicate rather than claiming a fresh collapse.
3. **COMPUTATIONAL corroboration of prior result:** Independently generated three-wire ripple-carry bitblast, 3n+1 vars, 8n+2 clauses, 4n+1 charged strict Resolution nodes, for n=1,2,3,4,8,16,32. Independently authored verifier replayed 4,668 assertions, 6 corruptions rejected, matched SAT/UNSAT and relaxed-output controls. These are upper certificates for a DIFFERENT CNF than BVP354, not exact mixed minima.

## New, precisely scoped result
**PROVED/EXACT conditional on explicitly stated opaque-extensional interface model U_opaque(d), NOT yet established for authoritative Rmix341.** Every Boolean function supported on d exposed inputs has an equivalent small circuit with at most d+d*2^(d-1) gates; at d=3 no more than 14 gates. Under private internal gates and downstream rules depending only on extensional output, any q-node proof can have all LOCAL-CONVERT conclusions replaced by equivalent canonical circuits with NO change to charged inference nodes. With d=O(log(N+q)) and polynomial ordinary record naming, there exists a polynomial-in-(N+q) bit presentation.

The prior LSPV-4 LOCAL-CONVERT-CVP363 and LSPV-5 REFEREE315 lower bounds for the work of checking a long **supplied** valid circuit remain correct. Canonical alternative existence does NOT make the conversion/optimizer free, prove normalized original grammar, or imply B3. If downstream may address internal wire names, or expose unbounded auxiliary supports, this normalization can fail. The exact downstream-preserving all-rule Rmix341 grammar is the next blocker.

**COMPUTATIONAL:** Exhaustive generator checks all 256 Boolean functions of 3 inputs, maximum 14 normal-form gate upper count, 28 symbolic long-chain controls through 1,024, SAT/UNSAT paired sources and 4 bad syntax rejections; 600 assertions. The current code reuses input and negation DAG nodes, not merely an unshared expression tree. No independent external referee has reviewed this scoped lemma yet.

## B1/B2/B3 firewall
B1 is pointwise polynomial domination by fixed total correct A's individual time; B2 is worst-case domination across all binary strings; B3 is SAT in P implying polynomial Wbar_R for the SAME preselected fixed R. All remain **OPEN**. Even granting this scoped normalized certificate and hypothetical SAT in P yields only output-sensitive proof search poly(N+W_R(F)), not W_R(F)=poly(N). Only a real superpolynomial R-lower bound plus separately proved B3 could yield P != NP.

## Falsifiers
F1 polynomial ER2-to-Resolution PHP projection: FALSIFIED/RETIRED from Haken and Cook-Reckhow. F2 algebraic BVP lower bound directly applies to Boolean bitblast: FALSIFIED/RETIRED in preexisting BVP354 and replicated. F3 every overlong supplied opaque conversion forces all equivalent extensional forms to be long: FALSIFIED for U_opaque(3) by canonical DNF. F4 complete authoritative mixed grammar satisfies that opacity: OPEN.

## Grok / Claude review and relevant corpus
The actual repository folders, located by Git tree (not guessed), are `GROKPROOF/` and `research/agents/claude/`. Read Grok reports `2026-11-03_1217_PROGRESS.md`, `2026-11-03_1518_PROGRESS.md`, `2026-11-02_2045_ATTEMPT_ARC_CONSTRUCTION.md`; read Claude `2026-10-28_1326_CLAUDE_TPORT-0001.tex`, `2026-10-28_1452_CLAUDE_TPORT-0002.tex` and `2026-09-30_CLAUDE-0266_review.tex`. Grok's 1217 UTC restricted query-volume argument erroneously treats a time **upper** bound as a per-query lower bound, also flagged by LSPV-2 364. Claude's TPORT barriers are specific to alternation-trading rules, not proof-cost-to-SAT transfers. Neither closes B3.

Read the exact Nov. 2 1204 directive (blob 033b54b87b7cbe94912af5cf67daa52859143a07), issue #3, AGENTS.md, CODEX.md and pnp-research SKILL; inspected peer LSPV-1 365, LSPV-2 364, LSPV-3 354/365, LSPV-4 363, LSPV-5 315. Primary source queries: Haken 1985, Cook-Reckhow 1979, Buss 1987, Alekseev 2026, Ladner 1975. Repository duplication queries: BVP/Alekseev, LOCAL-CONVERT canonical DNF, bounded-support normal form and downstream-preserving normalization. OpenAI GitHub searches for resolution proof checker, circuit value proof and extended resolution found no adopted implementation. The exact BVP354 duplicate was acknowledged and correctly classified.

## Exact outbox and limits
- Formal role report: `research/agents/lspv-3/2026-11-03_0824_LSPV-3_BOUNDED_INTERFACE_TRANSFER367.tex`
- Standalone normalization code: `experiments/arc/lspv3_366_interface_normalization.js`
- Canonicalization raw: `results/raw/arc/2026-11-03_0824_LSPV3_BOUNDED_INTERFACE_NORMALIZATION366.json`
- Source-labelled BVP generator: `experiments/arc/lspv3_367_bvp_bitblast_resolution.js`
- Separately authored BVP proof verifier: `experiments/arc/lspv3_367_bvp_independent_verify.js`
- BVP exact raw ledger: `results/raw/arc/2026-11-03_0824_LSPV3_BVP_SOURCE_TRANSFER367_public.json`
- This handoff: `research/coordination/2026-11-03_0824_LSPV3_BOUNDED_INTERFACE_TRANSFER367_FIVE_ROLE_HANDOFF.md`.

GitHub create/readback succeeds. Container execution preflight failed with a transient connection error, so no local repository-wide preflight or LaTeX compile claimed. Root `main.tex` authenticated as blob `01abe96105c071cdf405dba3a18b8aa69ae26bda` but returned zero content; no unsafe whole-file overwrite was attempted, owner-only reconciliation deferred. No task writes or scheduler mutations performed.

**Next decisive proof obligation:** establish from the original fixed LOCAL-CONVERT definitions whether all downstream Rmix341 rules can observe only extensional output or can access internal circuit names; if an authenticated counterexample exists, retire normalization for full R. Independently, search for a published hard family in a calculus strong enough to cover all Rmix341 rules, or prove a valid backwards translation with correct overhead, and separately confront B3. P versus NP OPEN.
