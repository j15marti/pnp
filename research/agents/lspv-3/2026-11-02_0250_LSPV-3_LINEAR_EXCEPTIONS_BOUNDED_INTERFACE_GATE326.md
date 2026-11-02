# LSPV-3 GATE326: linear exception distance does not force exponential SAT decision work

**2026-11-02 02:50 PST. PROVED/EXACT restricted corollary of established bounded-interface #CSP DP; independently COMPUTATIONAL; external review pending. P versus NP OPEN.**

## One obstruction, three falsifiers

Prior GATE325's source-authenticated exception-clause inclusion/exclusion costs 2^k poly(N), where k is the number of added source clauses relative to connected canonical G_t. We tested: (F1) linear k forces exponential SAT decision work, **FALSIFIED** by the family here; (F2) source-verified cyclic two-block support admits exact paid polynomial transfer when block size b and interface h are logarithmic, **PROVED restricted**; (F3) source-acquired partition implies a uniformly polynomial selector for ALL canonical originals, **OPEN**.

## Exact transfer theorem

Partition a VALID proper duplicate-free Döcker M22 original F into t consecutive b-variable ORIGINAL blocks B_i. Reject malformed strings. Source-authenticate every clause and check that its variables lie either in one block or in a cyclically adjacent pair. For t=2 assign all two-block clauses to one of the two cyclic edges to avoid duplication. Let H_i be variables of B_i appearing in a cross-block original clause, h=max|H_i|, and let C_i^loc and C_i^edge partition original clause IDs.

For coherent pins p, set

L_i(s)=sum_{z in {0,1}^{B_i\H_i}} [s,z extend p] product_{C in C_i^loc}[C(s,z)=1],

E_i(s,s')=product_{C in C_i^edge}[C(s,s')=1], W_i(s,s')=L_i(s)E_i(s').

Then #SAT(F|p)=tr(W_0 W_1 ... W_{t-1}). The exact equation uses W_i(s,s')=L_i(s)E_i(s,s'). Each source clause is evaluated exactly once. Summing over boundary sequences and private variables bijects with full original satisfying assignments. A nonzero trace yields an original-clause-checked witness by backtracking. A zero trace plus the independently checked tables yields a complete counted UNSAT proof, not a SAT-label oracle. Reverse-order transposed factors are equally exact.

Paid acquisition enumerates <=t2^b local block assignments and <=t2^{2h} boundary pairs; cyclic multiplication by fixed starting boundary costs O(t2^{3h}) O(n)-bit arithmetic operations. Including source authentication, grammar, signed quotas, index/head reads, proof/table acquisition and verification, caching, witness/output, bit writes and integer complexity, time is poly(N)*(1+t2^b+t2^{2h}+t2^{3h}) with poly(N)*t2^{2h} simultaneous peak bits for the materialized implementation. No other adaptive policies or guests are invoked here, hence no uncharged failed strategies, switching or DELAY/COPY/RECOMP; a universal controller must add all such costs.

## Independent forward/reverse arithmetic-profile audit

Under the **declared local integer transfer representation**, the first cross-block matrix W_0 has 15 distinct forward integer rows versus nine distinct reverse integer columns for F_2. For F_4,F_6,F_8,F_10 the corresponding independently reconstructed counts are 14 rows versus six columns. Reverse transposed matrix products preserve the same trace, but immediate arithmetic profile diversity differs. This is a representation-specific weighted boundary observation, **not** full Boolean cofactor equivalence, unrestricted circuit minima, or necessary decision work for arbitrary SAT deciders. No free variable-order selector is used.

## Connected canonical infinite counterfamily

Starting from previously authenticated cyclic F9 G_t with n=9t,m=12t, for every even t swap the positive x_{9i+1} signed occurrences in the TWO original local C3=(x1,x3,x5) clauses of adjacent block pair i,i+1 for i=0,2,...,t-2. The unchanged C1 cyclic splice preserves connectivity. Every signed variable still occurs twice positive and twice negative, no clause duplicates or repeated variables arise. Exactly k=t=n/9 original clauses differ from G_t, but every source clause is supported on a cyclic adjacent pair and all source-derived |H_i|=4. Thus a polynomially authenticated, polynomial-TOTAL-work exact terminal handles EVERY coherent pin of this **recognized family**, even though GATE325's explicit 2^k exceptional-subset expansion grows exponentially. k alone is not a necessary-decision-work lower-bound invariant.

Independent producer and no-producer-import verifier agree at (t,k,#SAT)=(2,2,4952),(4,4,23260326),(6,6,112060476824),(8,8,540246471390034),(10,10,2604591598112749432). Source local enumeration is exactly 512t trials and source interface size is exactly 4.

On SAME original F_2, p={x1=1,x2=1,x3=1,x5=1} has UNSAT0 with NO immediately falsified source clause; flip only x1 to zero to obtain SAT184 and an original-clause-checked witness. Independent exhaustive 2^18 source assignments, 2^14 source-clause UNSAT leaves, all 2^18 rows of 71-gate fan-in-two C_F, F9/Y6 model counts (70/20), 376 signed clause-pair S/U modes, 6656 complement identities and seven malformed-source rejects passed. UP-first source DPLL needed 1 node/168 literal probes UNSAT and 6 nodes/936 SAT: transfer is not shown advantageous on these tiny controls. F15/U198/V198 inherited, not freshly rerun.

## Relation to prior work and limitations

Bounded-interface counting/knowledge compilation is KNOWN (LSPV-2 BLOCK-TRANSFER-STREAM212, GATE324; Amarilli et al. arXiv:1811.02944). This run contributes a checked, connected, canonical linear-exception family with same-source both-label controls, not a new general width theorem. Source/circuit function compilation does NOT measure necessary work of arbitrary SAT deciders. No universal all-input polynomial aggregate policy, unknown-exponent arbitrary-A hereditary ARC contraction or strict numerical SAME-MACHINE FLMV transfer. Physical XOR is offline only. P versus NP OPEN.

Sources: Döcker, arXiv:1912.08032; Amarilli et al., arXiv:1811.02944; de Colnet et al., arXiv:2502.00434. Search: project GitHub transfer matrix, openai GitHub OBDD/SAT, primary web pathwidth/#SAT. Full independently reproducible code, proofs, raw and manifest are in the run archive.

No identities, schedules or enabled states altered.
