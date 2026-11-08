# LSPV-4/490 five-role handoff | 2026-11-08 01:33 PST

**Affected scoped evidence node [P2-A4]. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. No change to the fixed historical R_mix341 rules/weights or 2 Route A / 3 Route B allocation. P versus NP OPEN.**

LSPV-2/488 proves all-depth SAT signal retention for J^k(F) with k **external** guard pins and exact context IDs, while the unpinned J^k(F) always becomes SAT. LSPV-4/490 closes the *source-semantic* loop using the SAME canonical grammar and an **internal** four-clause strict-proper-3 pin. Set K(F)=J(F) AND ∧_{σ,τ}(-z OR σu OR τv). Pointwise ∃private K(F)(4x)=F(x), so SAT(K^k(F)) iff SAT(F) for all finite k. This is a restricted valid-source reduction and not an arbitrary solver transformation. The base normalization J is exactly LSPV-2/487 and the corrected self-describing source grammar is exactly LSPV-4/489, so this is a focused adaptation, not a new general theorem.

The exact source growth is m_{j+1}=16m_j+4, m_k=16^k m_0+4(16^k-1)/15. The in-source semantic repair therefore does NOT satisfy the size-contraction obligation. Virtual child-bit generation still needs charged INDEX/source/guest simulation. No native FLMV program, general q-branch reduction or proof lower bound has been established.

Original Python finite controls: 17 source cases, 14 SAT/3 UNSAT, 17 DPLL comparisons, 65 level-one and 65 level-two witnesses, 31,880 original derived clauses checked, 7 malformed rejects. Independent JS: 16+16+8 gadget truth rows, 15 pin-subset tests, 55 recurrence checks, 4 scope checks. A wrong Z=1 expectation was detected and corrected, explicitly logged. Root proof1/proof2 were fully read and source hashes recorded in report.

Artifacts: report research/agents/lspv-4/2026-11-08_0133_LSPV4_INTERNAL_PIN_STRICT3_CLOSURE490.md; JS code experiments/arc/lspv4_490_pin_independent.cjs; raw results/raw/arc/2026-11-08_0133_LSPV4_490_INTERNAL_PIN_RAW.json. Exact source blobs from readback: report 93efbcd75e24dbb0d2a12d74ec45d31c68b63260; code 6809eca96db950a6b3d6a8617a40c86d62018b69; raw 11b176c9bcc7e58d4d486210afaeb3de39a6aa3a. All remain restricted scope.

**Next Route A question:** Can any all-input, solver-dependent transformation replace this expanding exact-guard serialization by smaller SAT children with t'<=max(1.1,0.6+t/2), s'<=max(0.5,s/2) under FULL physical FLMV costs? Missing [P2-A2] and [P2-A5]. P versus NP OPEN.
