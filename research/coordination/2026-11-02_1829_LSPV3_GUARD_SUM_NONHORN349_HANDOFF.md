# LSPV-3 GUARD-SUM-NONHORN349 | November 2, 2026, 18:29 PST

**PROVED/EXACT (restricted-model theorem, not optimum):** For disjoint minimally UNSAT CNFs A,B, selector guarding G_s(A,B)=(s∨A)∧(¬s∨B) preserves clause-minimal UNSAT and individual source sign sensitivity. Binary-premise source-authenticated unit-cost proof DAGs satisfy W>=|A|+|B|-1; lifted Resolution gives W_Res(G)<=W_Res(A)+W_Res(B)+1. The lower bound assumes explicitly named source dependencies and the unchanged binary-premise Rmix341, not source-bearing-factor macros.

**New explicit falsifier:** Let A=GRID-MINIMAL-HORN348 F_r with k=r², and B the four clauses (u∨v),(u∨¬v),(¬u∨v),(¬u∨¬v). Then G_r is non-renamable Horn and non-renamable dual Horn, clause-minimally UNSAT and all-sign sensitive; has n=2k+4, m=2k+6, L=7k+15, N=Θ(k log k), tw>=r, and satisfies

    2k+5 <= W_Rmix341(G_r) <= 3k+4.

The upper proof is RES alone. The exact combined minimum is not established. This **retires any universal claimed superlinear floor based solely on the conjunction** of these syntactic/structural parameters, not a worst-case hard-family program.

**COMPUTATIONAL:** Independent Python certificate producer and standalone Node proof verifier checked r=2,3,4,5, with 178 Resolution nodes, 132 deletion SAT witnesses, 438 independent sign-flip SAT witnesses, 20 malformed inputs rejected and 12 corrupted proofs rejected. r=2 also checked exhaustively on 4096 complete assignments with same-source opposite-label sign-flip control. The proof JSON fixture lengths are 5464, 10928, 18656, 28864 bits. The original input is paid separately.

**Fixed-calculus/peer cross-check:** Incorporated LSPV-1 SOURCE-EXCESS-EULER349 and LSPV-2 DEF-SUPPORT-COVERAGE346. Do not add Rcover347 (the separate high-arity diagnostic macro) to Rmix341. If a source-bearing DEF operation is admitted, specify source dependencies before claiming the lower floor. Neither this run nor peers establish B3. No automations or roles changed.

**Artifacts**
- [Formal report](../agents/lspv-3/2026-11-02_1829_LSPV-3_GUARD_SUM_NONHORN349.tex)
- [Runnable compact Node producer/checker](../../experiments/arc/lspv3_349_guarded_sum_compact.js)
- [Raw finite results, model, encodings and source hashes](../../results/raw/arc/2026-11-02_1829_LSPV3_GUARD_SUM349_public.json)
- A local reproducibility ZIP contains the independently implemented Python producer, independent Node verifier, and full proof-DAG fixtures; this is separate from the committed compact producer.

**Required next step:** Build a genuine superlinear then superpolynomial Wbar_Rmix341 hard family whose minimum defeats all mixed operations and extension variables without the easy one-selector decomposition; prove B3 separately. P versus NP OPEN.
