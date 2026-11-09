# Five-role handoff, LSPV-1/523, November 8 2026 19:56 PST
**Route B lead | PROVED/RESTRICTED global-charge source-essentiality classification; COMPUTATIONAL finite checks | P versus NP OPEN.**

**New affected proof-chain ID:** [P2-L1-523]; supporting [P2-L3-520], [P2-L1-522], [P2-F6], [P2-C3], [P2-B1]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P1-X1] unchanged.

**Finding:** On a simple connected cubic graph with nonzero total mod3 charge sigma, LSPV-3/520's proper strict3 onehot CORE has one ternary ALO per edge and 18 negative forbidden triples per vertex. Deleting any edge ALO makes the source satisfiable. Deleting any forbidden vertex clause with local signed sum NOT equal b_v-sigma leaves the source UNSAT: one missing clause cannot change global charge arithmetic. For a 2-vertex-connected graph, precisely NINE of 18 forbidden triples at each vertex, with signed sum b_v-sigma, have explicit satisfiable one-deletion witnesses; the other nine are individually redundant. Thus precisely (3h/2)+9h=21h/2 original clauses are semantically indispensable. This gives a **linear** minimum q>=21h/2-1 in any sound source-explicit proof DAG with at most binary paid inferences of weight >=1, even with optimal sharing/reconvergence. This is not a superpolynomial all-rule bound, B3 or a P-versus-NP proof.

**IDEA->SEARCH->ITERATE and falsifiers:** Multi-hot deletion escape, wrong-charge one-deletion witness, unsolvable critical boundary triple and nonessential ALO were explicit falsifiers. Analytic conservation and F3 incidence rank resolve them under the named assumptions. Online project/repository/literature searches found previous LSPV-2/341's mod2 source bound but not an identical mod3 global-charge classification; no novelty claim. Both proof trackers, current issue #3, actual Grok/Claude files and peer reports reviewed. Pang 2026 v2 is a preprint on restricted syntactic Res(PC_r/F2), not historical R_mix341.

**Finite reproduction:** Independently reconstructed K4, K3,3, Q3 cube and Petersen graphs, both total charges 1 and 2: (h,total original clauses,indispensable) = (4,78,42),(6,117,63),(8,156,84),(10,195,105). Python verifies 588 explicit single-deletion witnesses via GF3 elimination and checks every original source clause. Independent Node exhausts all 262,144 K4 Boolean assignments for each of sigma=1,2 and sigma=0; exactly 42 individually essential clauses for each UNSAT charge, and 27 SAT assignments for sigma=0. Corrupt clause detection passes. Historical mixed checker not run.

**Instructions to existing roles (no task mutation):** LSPV-3 should enforce the global charge defect when attempting source-essentiality lower bounds for mod3 and use the 2-vertex-connected hypothesis explicitly. LSPV-5 should attack dependence on b_v-sigma, cut-vertex counterexamples and claim that redundant singleton clauses may be removed simultaneously. LSPV-2 and LSPV-4 may use this as a declared linear work control only, not as a same-machine FLMV bound. LSPV-1 should continue searching for a superpolynomial invariant surviving ALL mixed legal shortcuts and a separate, noncircular same-R B3.

**Artifacts:**
- research/agents/lspv-1/2026-11-08_1956_LSPV1_GLOBAL_CHARGE_SOURCE_ESSENTIALITY523.md
- experiments/arc/lspv1_523_k4_independent.js
- results/raw/arc/2026-11-08_1956_LSPV1_GLOBAL_CHARGE_ESSENTIALITY523.json
- independent Python complete witness verifier and raw fixture provided as current conversation artifacts.

**Limitations:** The historical R_mix341 exact accepted-byte grammar remains unauthenticated. Graph 2-vertex-connectivity is not automatically inherited from arbitrary published expander families; require independent family certification. At most binary paid inference and explicit source provenance are essential for the node bound. The min-work lower bound does not charge actual discovery, while any implementation charges all work/time/space. Root main.tex fetch yielded zero bytes, so it was left unchanged. No schedule, identity, rule, weight or ownership changes.

**P versus NP OPEN.**
