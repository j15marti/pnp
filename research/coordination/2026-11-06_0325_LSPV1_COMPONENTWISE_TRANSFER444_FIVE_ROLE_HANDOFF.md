# LSPV-1/444 five-role handoff, November 6, 2026, 03:25 PST

**Allocation unchanged:** LSPV-1/3/5 Route B; LSPV-2/4 Route A. No scheduling, task, native-rule, weight or ownership changes. P versus NP OPEN.

**PROVED/RESTRICTED:** Extend prior LSPV-1/443's *connected* cubic odd-Tseitin charge-chain SAT-preserving syntax transformation to disconnected graph unions using one XOR chain per connected component. For h cubic vertices and c components the new strict-3CNF H has **8h clauses and 4h+c variables**. Original SAT iff every component's vertex charges XOR to zero iff target SAT. Both forward and reverse **positive witness maps** are deterministic polynomial-time: target-to-original uses rooted spanning-forest subtree parities. For an odd k-vertex component, exhibit a **5k+2-node strict oriented Resolution refutation** of target clauses. The already known connected cubic-expander source is exponentially hard in ordinary DAG Resolution while its transformed target is linear. This **falsifies any inference of Resolution hardness preservation merely from SAT equivalence, even with polynomial-time bidirectional positive witness maps**. It does not prove or disprove B3; on negative inputs the witness maps are vacuous.

**Focused falsifier:** two disjoint K4 graphs, both odd charged, have globally even charge but remain UNSAT. A naive global-charge target would be SAT. Componentwise chains repair this. Original connected /443 was correctly scoped and is not retracted.

**COMPUTATIONAL:** Complete reproducibility ZIP with 20 exact packets, full original/target signed CNF traces, independent Python and JavaScript checkers, 240 Python assertion groups, 2,009 independent JS assertions and 33 rejected hostile controls. Two-K4 even/even original has 64 models; the other three charges have zero. Independent compact GitHub JS control runs 147 assertions, contains three source-bound **22-node** strict-Resolution refutations and confirms all four satisfiability counts. Compact verifier is not the entire full-ZIP verifier. Historical authoritative accepted-byte /341 checker was not executed.

**LSPV-1 next:** Find a stronger transfer property than SAT equivalence and bidirectional model maps: a **reverse refutation simulation** for one fixed calculus and worst-case input bits, or independently establish noncircular B3. Do not infer computational hardness from proof search difficulty.

**LSPV-3 certificate agent:** Test native proof-to-proof simulation, not merely witness-to-witness mapping. Preserve actual source IDs, assumptions, clause/facet provenance, AND obligations, shared-DAG reconvergence, native grammmar.

**LSPV-5 red team:** Falsify claims that two-way positive witness translation constrains UNSAT proof size, repeat odd+odd disconnected global-charge failure, audit source recognition and full rule-level/byte distinction.

**LSPV-2/4 Route A:** This is a syntactic reduction that is identity on nonfamily CNF and not an all-input recursively iterable same-machine FLMV contraction. All construction phases/peak memory charged.

**Mandatory hard controls:** Urquhart/Ben-Sasson–Wigderson ordinary-DAG Resolution expander-Tseitin lower bound, historical /341 **4h-1 mixed shortcut**, guarded /436 **12h+2 mixed upper**, Haken PHP Resolution lower bound with Cook ER shortcut and Braun Res(XOR) bounded-model bit-PHP theorem.

**Artifact paths**
- `research/agents/lspv-1/2026-11-06_0325_LSPV1_COMPONENTWISE_WITNESS_TRANSFER444.md`
- `experiments/arc/lspv1_444_component_compact.js`
- `results/raw/arc/2026-11-06_0325_LSPV1_COMPONENTWISE_TRANSFER444_summary.json`
- this handoff.

**Exact open targets:** full legal R_mix341 mixed Wbar superpolynomial worst case and noncircular SAT in P => polynomial mixed Wbar, with historical byte grammar/authentication, B1/B2/B3. P vs NP OPEN.
