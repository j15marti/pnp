# LSPV-1 BPHP3-LITERAL-ATLAS340 | November 2, 2026 15:58 PST

**Status:** PROVED/EXACT constructive signed strict-3CNF clause-minimality and fixed binary-premise Rmix341 source-capacity floor; COMPUTATIONAL independent n=4 and n=8 controls; B1/B2/B3 and P versus NP OPEN. No agent or schedule changes.

**Highest-value literature candidate:** Kamil Braun, 19 September 2026, arXiv:2609.23015, reports Lean-formalized exponential **unrestricted DAG Res(⊕)** minimum proof-size bound for original bit pigeonhole CNF with n=2^ell holes, ell>=32: refutation > exp(n/(32768 ell^2)). The author's pinned Lean theorem was inspected at `kbr-/math-research` commit `8904bf09a5376f48a00d1c25d079bf0c6441502a`, but the complete kernel build was not independently rerun. The theorem is in a DIFFERENT proof system and original clause width 2ell, not strict 3CNF.

**New exact source construction:** Give every pair of n+1 pigeons and every hole z the signed width-2ell collision-forbidding clause; convert EACH clause independently by its private implication chain using k-3 fresh auxiliary variables. Every resulting source clause is strict 3CNF and has a complete source-deletion satisfying assignment (assign selected two pigeons to z and the remaining n-1 pigeons bijectively to other holes, then flip the local chain once). Every one-occurrence literal sign reversal is SAT. The complete formula is UNSAT by pigeonhole counting. This works symbolically for all n=2^ell>=4.

**Exact minimum lower bound in Rmix341 only:** With M=n*C(n+1,2) original clauses, M3=M*(2ell-2) strict source clauses, every conservative sound refutation DAG with unit-weight at-most-binary-premise derived nodes requires >=M3-1 nodes. It is an absolute lower floor but is ONLY polynomial in source size and has no matched machine T/S interpretation. No matching optimum is claimed.

| n | variables | three-clauses | Rmix341 minimum lower |
| ---: | ---: | ---: | ---: |
| 4 | 50 | 80 | 79 |
| 8 | 891 | 1152 | 1151 |
| 16 | 10948 | 13056 | 13055 |

Full n4/n8 original signed DIMACS generated, 1,232 deletions and 3,696 polarity changes checked, independent Node verifier passed 342,380 assertions and rejected deliberate malformed/altered sources. n16 counts checked symbolically without full deletion sweep. Source acquisition, rule checking, optimizer, proof representation, time and space separately charged.

**Cross-role HIGH PRIORITY warning:** DO NOT claim Braun exponential unrestricted Res(⊕) bound for these converted 3CNFs or for extension-enabled Rmix341. A proved all-proofs reverse simulation with controlled polynomial overhead is missing. Also do not silently union the four-premise, unit-cost PARITY4 rule from Rmix,1 with binary-premise Rmix341; the existing K4 exact optimum 15 depends on the fixed rule basis. LSPV-1 335 already established MUS reduction and literal-sign sensitivity in general; do not claim novelty for those underlying lemmas.

**Priority next tests:** (1) Attempt a model-preserving reverse proof compiler for every valid Rmix341 refutation of G_n into Braun's original Res(⊕) BPHP, with explicit encoded-node costs; or exhibit a shorter extension-gate shortcut to falsify it. (2) Keep searching for a proof-system intrinsic Wbar_R superpolynomial family; hard instances may be algorithm-dependent and need not be simple polytime recognized generators. (3) Independently prove B3 (SAT in P => Wbar_R poly) for the SAME fixed R, not pointwise B1. (4) Reconcile SAT/UNSAT and malformed controls and actual all-phase peak space for every claimed transport.

**Published:** [formal standalone report](../agents/lspv-1/2026-11-02_1558_LSPV-1_BPHP3_LITERAL_ATLAS340.tex); [generator](../../experiments/arc/lspv1_340_bphp3_generator.py); [independent checker](../../experiments/arc/lspv1_340_bphp3_independent.js); [raw](../../results/raw/arc/2026-11-02_1558_LSPV1_BPHP3_LITERAL_ATLAS340_results.json). The full independent original DIMACS, plotted atlas and complete code are in the separate user conversation reproducibility archive. No new tasks or agents.
