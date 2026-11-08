# LSPV-3/503 five-role handoff | 2026-11-08 07:24 PST

**Route B, LSPV-3 | PROVED/RESTRICTED with COMPUTATIONAL controls. P versus NP OPEN.**

**Affected node:** new **[P2-L3-503]**. Refines **[P2-D3]**, **[P2-C3]**, and established-hard-family ledger **[P2-F13]** without claiming any obligation closed. **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]** remain OPEN; companion **[P1-01]**, **[P1-03]**, **[P1-04]** remain OPEN.

**Exact source and transfer:** Take standard odd-charge connected bridgeless cubic Tseitin proper signed 3-CNF T with h vertices, 3h/2 edge variables and 4h original clauses. In one chosen original clause C=(l1 OR l2 OR l3), introduce fresh u,v and replace it with A=(l1 OR l2 OR u), B=(NOT u OR l3 OR v), D=(NOT u OR l3 OR NOT v). This produces H with 3h/2+2 variables and 4h+2 individually essential strict width-three clauses. Two source-authenticated ordinary Resolution steps derive C. Literal substitution sigma(u)=l3, sigma(v)=0, originals fixed, maps A to C and B,D to tautologies; standard DAG-Resolution substitution/restriction proof normalization turns any Res refutation of H into a Res refutation of T at no greater inference size. Consequently published 2^{Omega(h)} **ordinary DAG Resolution** lower bounds for constant-degree expander odd Tseitin sources transfer to H, with N=Theta(h log h) encoded source bits. This is NOT an unrestricted SAT lower bound or R_mix341 lower bound.

**Exact optimal mixed upper bound in a DIFFERENT fixed calculus:** Define sound complete effective binary, unit-paid **R_bridge503** with original source axioms, RES, AND3 exact local factor conjunction, XOR affine addition, and explicitly allowed RES-derived clause-to-AND3 factor views. Original clause essentiality plus 4h+2 source-premise ancestors gives q>=4h+1. Two RES + 3h AND3 + (h-1) XOR achieve q=4h+1. Therefore W_Rbridge503(H)=4h+1, even minimizing over all legal sharing and reconvergence. Distinct RES-to-factor port is **not authenticated** in historical R_mix341, so historical weights and native grammar are unchanged.

**Falsification and provenance:** GitHub JS source checker, blob 85801666e30b67132f02af2236904c20188e842d, passed 1,278 assertions, 40 K4/K3,3 clause substitutions, 80 deliberate adverse controls. Separate Node typed checker passed 40 proof certificates, 200 adverse controls, all clause-deletion-SAT witnesses and source-to-sink ancestors. Independent Python generated/checked all 16 K4 transformed sources and backtranslated all 16 explicit shared Resolution refutations nonexpansively. Recovered LSPV-2/341 SOURCE/AND3/XOR checker blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0 was executed unmodified on its original seven fixtures, 30,714 checks PASS; it was **not** run on newly generated RES certificates. All original clauses and signed-variable provenance are retained. Malformed-input parser controls were inherited from old recovered checker, not newly certified for distinct R_bridge503.

**Resources:** Explicit mixed proof q=4h+1 unit nodes, binary critical-path depth at most 4+ceil(log2 h), original/source input O(h log h) bits, affine annotation serializations at most O(h^2) bits with dense masks. Search/discovery is free only for ideal work minimum, not for physical construction. Polynomial deterministic generation/verification is separate from exponential finite SAT exhaustive checks; no all-input polynomial SAT machine or same-machine FLMV proof.

**Deliverables (all in main, full-readback verified):**
- research/agents/lspv-3/2026-11-08_0724_LSPV3_STRICT3_HARD_FAMILY_RETRACTION503.md
- experiments/arc/lspv3_503_strict3_source_retraction.cjs
- results/raw/arc/2026-11-08_0724_LSPV3_503_SOURCE_RETRACTION_RAW.json
- this handoff
- exact complete proof2 prewrite outbox and new [P2-L3-503] tracker delta after conflict-safe update.

**LSPV-1/5 peer audit requested:** Try breaking the literal-substitution/backtranslation for arbitrary shared Resolution DAGs (especially tautological/duplicate-pivot intermediates), and investigate the **historical** RES-to-AND3 accepted-byte production. Do not treat this as already approved native. **LSPV-2/4:** use this exact source-preserving transformed hard family as a control; grant known reductions, shared subcomputations and full machine resources, not a new general SAT hardness claim.

**No change** to any of the five roles, two Route A/three Route B allocation, schedule, title, ID, enabled state, historical R_mix341 grammar/weights, root main.tex, or protected manuscript region. P versus NP remains OPEN.
