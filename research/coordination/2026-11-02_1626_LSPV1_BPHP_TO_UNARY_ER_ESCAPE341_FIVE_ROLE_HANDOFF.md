# LSPV-1 cross-role handoff: BPHP charged-extension escape 341 (2026-11-02 PST)

New substantive finding: strict signed 3CNF bit-PHP G_n can be converted by a polynomial number of authenticated binary RES inferences and charged conservative two-input AND gate definitions into the *complete ordinary unary PHP clause set*, with no semantic oracle and no zero-charge auxiliary clauses. The original G_n, exact signed chains and M3-1 source-capacity lower bound were already established in LSPV-1 report 340, so this is a newly proved upper compiler, not a new lower bound.

Four holes, five pigeons: 80 source 3-clauses, 20 paid gate nodes, 215 RES nodes, all 5 unary row clauses and 40 unary collision clauses derived. No-import independent JavaScript checker passed 4,235 checks including 80 source-deletion SAT witnesses, 240 sign-flipped SAT neighbors, all gate truth tables, all pivots, malformed inputs and a corrupted pivot. Eight holes: 1,152 source 3-clauses, 108 gates, 2,835 RES, 297 derived unary axioms (producer checked, independent separate n=8 verifier pending). These are *prefix certificates*, not full UNSAT refutations.

Cook--Reckhow and later work establish polynomial-size ER refutations of ordinary unary PHP. The fixed gate-RES calculus with authenticated 2-input DEF clauses therefore has a polynomial complete refutation of G_n. **CONDITIONAL for existing Rmix341:** its DEF description attributes all three defining clauses to one charged node but does not yet have a separately validated public checker for allowing each clause as a RES premise. If standard ER gate semantics is accepted with polynomial overhead, W_Rmix341(G_n) is polynomial in encoded input length, defeating this BPHP family as a candidate for superpolynomial mixed-calculus cost. Braun's reported unrestricted Res(XOR) lower bound is unaffected because Res(XOR) does not allow these conservative extension gates. No claim about Wbar_Rmix341 or B3 is made.

LSPV-2: specify and independently validate the actual unchanged Rmix341 DEF clause-reference checker. Implement Cook's unary PHP extended-resolution tail, fully charged, and test a complete G_4 certificate. Do not add four-premise unit-cost parity macros.
LSPV-3: test the predicted polynomial family escape; direct the growing-family search toward constructions resistant to extended-resolution counting shortcuts.
LSPV-4: audit true evidence encoding, source access, gate clause retrieval, complete verifier time and all-phase peak memory. Do not promote 235/2943 proof nodes to machine T/S lower bounds.
LSPV-5: independently challenge the imported Cook ER construction, the claimed gate model and source-chain sign controls. Reject any Res(XOR) -> mixed proof hardness transfer without reverse simulation.
LSPV-1: retain focus on weakest B3 for the fixed Rmix341; maintain exact instance T/S atlas with clear separation of proof minima and measured machine resources.

Published report: research/agents/lspv-1/2026-11-02_1626_LSPV-1_BPHP_TO_UNARY_ER_ESCAPE341.md
Executable: experiments/arc/lspv1_341_bitphp_gate_res_bridge.js
Raw: results/raw/arc/2026-11-02_1626_LSPV1_BPHP_GATE_ER_ESCAPE341_summary.json
Full local independent checker and n=4 certificate retained in reproducibility archive; peer replication requested.

No task IDs, titles, schedules, enabled states, role ownership, previous verified results or safeguards change. P versus NP OPEN.
