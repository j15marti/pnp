# LSPV-3 GUARD-SUM-EXACT350 | November 2, 2026, 18:44 PST

**PROVED/EXACT: new uniform source-once Resolution tree saturates the lower bound in the unchanged at-most-binary, source-authenticated unit-weight Rmix341 calculus.** This sharpens earlier GRID348 and GUARD-SUM349 intervals.

For r>=2, k=r^2, the permuted-grid minimally UNSAT F_r has m_F=2k+2 sources and **W_Resolution(F_r)=W_Rmix341(F_r)=2k+1**. Proof: resolve x0 forward with each guarded x transition to obtain xk OR all y literals; resolve -xk; resolve the y-chain clauses **backwards** (j=k down to 2); resolve -y1. Every source occurs exactly once in a binary Resolution tree.

For the selector-guarded sum G_r=(s OR F_r) AND (!s OR K), where K is the four signed (u,v) clauses, n=2k+4, m=2k+6, L=7k+15, and its grid minor and non-renamable Horn/dual-Horn properties are retained. The two lifted source-once trees plus one final pivot give

    W_Rmix341(G_r) = W_Resolution(G_r) = 2k+5 = m-1.

This is an **exact global minimum** over all valid adaptive, shared-DAG, algebraic and paid conservative-definition choices in the FIXED source-authenticated binary-premise calculus. The premise-arity/source dependency rule is essential: this is NOT a theorem for an unapproved source-factor high-arity macro.

**Proof-evidence Pareto observation:** the exact-optimal source-once proof has k^2+4k+6 explicitly written derived literal occurrences, and a maximum derived clause width k+2. The older longer 3k+4-node proof has width at most 3 and O(k) literal occurrences. Therefore this particular optimal-node proof occupies Theta(k^2 log k) flat evidence bits, while the older proof uses O(k log k). **No universal minimum physical proof-byte lower bound is claimed**; compression and lazy representations can change the relationship.

**Independent finite checks:** separate Python generator and Node verifier replayed r=2,3,4,5, verifying 128 exact-optimal proof nodes, all 132 source-deletion SAT witnesses, all 438 occurrence-sign-flip SAT witnesses, 20 malformed DIMACS and 12 corrupted proofs rejected, plus exhaustive 4096 assignments on the r=2 UNSAT and single-flip SAT controls. Symbolic producer also ran r=8,12. This does not establish superpolynomial worst-case Wbar_R or any B3 transfer.

**Artifacts (all fixed role-owned paths):**
- [Complete exact theorem](../agents/lspv-3/2026-11-02_1844_LSPV-3_GUARD_SUM_EXACT350.tex)
- [Re-executable proof-producing JavaScript](../../experiments/arc/lspv3_350_guarded_sum_exact.js)
- [Exact numerical/evidence ledger](../../results/raw/arc/2026-11-02_1844_LSPV3_GUARD_SUM_EXACT350_public.json)
- Prior [GUARD-SUM349](../agents/lspv-3/2026-11-02_1829_LSPV-3_GUARD_SUM_NONHORN349.tex) remains as a valid non-optimal low-width alternate proof.
- A user-facing ZIP has the independently implemented full Python and Node verifier, proofs, and manifests.

**Next gap:** Find an extension-resistant family with shortest binary-source DAG necessarily *strictly above* the m-1 floor, and then a superpolynomial mixed minimum, for the preselected R. Prove B3 independently. P versus NP remains OPEN.
