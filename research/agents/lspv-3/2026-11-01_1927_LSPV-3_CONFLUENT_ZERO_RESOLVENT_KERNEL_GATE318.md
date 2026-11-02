# LSPV-3 GATE318: Confluent zero-resolvent SAT forgetting and hostile canonical kernels

**November 1, 2026, 19:27 PST. Status: PROVED/EXACT elementary theorem and restricted construction; COMPUTATIONAL no-import verification; external mathematical review pending. P versus NP OPEN.**

## Exact obstruction, scope and falsifiers

The uniform all-input adaptive controller still lacks a polynomial bound on total selection, certificate acquisition, failed policies, switching, output and recursive work. The target language remains ALL valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) originals (malformed encodings rejected); ordinary source-indexed pinned residuals may be noncanonical. No variable-value recovery or injective syntactic pin key is assumed.

F1: Every connected canonical root has an eligible zero-resolvent variable, **FALSIFIED** by the high-width paired-support toroidal originals below. F2: Exhaustive zero-resolvent deletion has policy-dependent final kernels, **FALSIFIED** by a general confluence proof. F3: Bounded original M22 occurrences guarantee clause-nonexpanding elimination forever, **FALSIFIED** on the same F9 root by pivots 1,2,9 (12→11→10→11). F4: The previously published C_t family of LSPV-2 320 requires residual SAT search after its t original x_i pivots, **FALSIFIED** by an explicit 3t-step all-clause deletion certificate.

## Theorem A: exact decision-only forgetting, confluent paid saturation

For every CNF residual R and an unpinned variable x, write R=H ∧ ∧_i(x∨A_i) ∧ ∧_j(¬x∨B_j). Assume all cross-resolvents A_i∨B_j are tautological (allow either polarity family empty). Then, **for every assignment z of all variables except x**:

    H(z) ⇔ (∃b∈{0,1}) R(z,x=b).

The identity is the standard Davis–Putnam existential distribution: ∃x R = H ∧ ∧_{i,j}(A_i∨B_j), and all resulting conjunction terms are tautologies. This is exact decision-only forgetting, not pointwise equality of x-cofactors and not a #SAT identity. A proof ticket gives each original source clause-ID cross-pair and its opposing-literal tautology witness. The identity continues to hold under every future pin context **not mentioning forgotten x**; allowing x pins later requires paid source replay or excluding x from the protected elimination set.

Repeated deletion of all clauses containing an eligible x has a **unique final source-clause subset**, independent of legal pivot order. For a clause subset S let E(S) denote its zero-resolvent eligible occurring variables and T(S) remove every clause incident to E(S). If A⊆B, every pivot eligible in B is eligible in A whenever it appears in A, so T(A)⊆T(B). T is monotone and contracting. Its greatest fixed point K=T^m(R) is preserved throughout any sequential legal deletion, since deleting a clause of K would imply an eligible incident variable in K, contradicting T(K)=K. Every terminal sequential outcome is a fixed point contained in K, hence equals K. The same holds when a declared set of future variables is protected from deletion.

The **well-founded potential Ψ=number of active clauses** decreases after every productive step and has at most min(n,m) steps, regardless of increases in signed delta. All-original canonical degree 2P+2N means at most four cross-pairs per examined pivot and at most four source tickets per deletion. A naive fully paid implementation with source scanning, failed candidate probes and re-scans costs O(n²m) literal/record visits, plus explicitly charged grammar, indexing/head movement, policy switching, proof replay and output; its stored active mask/indices and certificates use polynomial simultaneous space, **not** the strict FLMV target space. A nonempty irreducible kernel means UNRESOLVED, never UNSAT.

When the kernel is empty, its decision-only certificate is the exact forgetting ticket sequence. To satisfy the all-input controller's stronger SAT-terminal contract, reconstruct a complete source assignment by reversing the ticket order: set x TRUE if some positive x-clause otherwise fails, FALSE otherwise, then check **all original source clauses**. This reconstructive work is separately paid; no witness is forced on a decision-only output.

## Theorem B: complete linear-ticket terminal on the previously known C_t family

LSPV-2 CROSSTAUTO-FORGET320 already constructed a connected valid canonical cyclic source C_t with six variables (x_i,a_i,b_i,c_i,d_i,e_i) and eight clauses per block, including a shifted e_{i+1} link:

positive: (x_i,a_i,b_i), (x_i,c_i,d_i), (a_i,c_i,e_{i+1}), (b_i,d_i,e_i);
negative: (¬x_i,¬a_i,¬c_i), (¬x_i,¬b_i,¬d_i), (¬a_i,¬c_i,¬e_i), (¬b_i,¬d_i,¬e_i).

**New increment beyond LSPV-2 320:** the explicit sequence (x_i,a_i,b_i) for each i removes **all 8t clauses with exactly 3t source-authenticated zero-resolvent pivots**. First x_i has four complementary witnesses a_i,b_i,c_i,d_i; next a_i has a complementary c_i witness and b_i has d_i. No derived clause is needed. Thus every C_t has a polynomially acquired **complete SAT terminal**, with optional reverse-checked original-variable witness. Root model counts for t=1,2,3 are respectively **22,466,10054**; existential forgetting does NOT preserve model count. The ascending-variable greedy producer (different valid order) uses 3t+1 pivots for t≥2; confluence proves it reaches the same empty kernel.

Same-original C_1 pins (a,c,b,d)=(0,0,1,0) have one SAT extension, while (0,0,1,1) have no extension and four complete original-source refutation leaves. F9 pinned SAT/UNSAT counts 1/0 and F15 pinned SAT/UNSAT 2/0 were independently verified.

## Theorem C: irreducible, high-width, yet easy canonical originals

For any **simple cubic graph**, create a fully paired canonical original by emitting the positive clause containing the three incident edge variables at each vertex, and its all-negative mate. For an edge variable x=(u,v), its four source cross-resolvents comprise two tautological same-vertex pairs and two **non-tautological cross-endpoint pairs** (no parallel edge). Thus not one original variable is zero-resolvent eligible; even ordinary blocked-clause elimination finds no blocking literal.

The established LSPV-1 PAID-HIGHWIDTH-NAE314 even-k toroidal four-port-cycle graph gives connected proper originals with n=6k², m=8k², signed root defect 4k², and primal treewidth at least (k−2)/2. For k=4,6,8 independent structural controls checked 96/216/384 variable originals and **zero** zero-resolvent pivots. A checked selection of internal matching edges witnesses SAT, and a paid paired-support matching recognizer decides the family in polynomial time. Hence neither kernel size nor maximal component width is an unrestricted necessary-work lower bound.

## Theorem D: canonical first step non-growing, but not hereditary

For every canonical original variable, full Davis–Putnam removal deletes four source clauses and emits at most four non-tautological resolvents of width at most four, so **the first step never increases the number of clauses**. It may increase binary length and emits a noncanonical child, so is not a target-valid power-short ARC edge.

On F9, independent full projection checks verify pivots x1,x2,x9 with clause counts 12→11→10→11, raw cross counts 4,6,10, non-taut cross counts 3,4,9, and max widths 4,5,5. Thus the one-step bound is not hereditary. No arbitrary-correct-algorithm contraction is inferred.

## Computational and resource audit

Standalone producer and independent no-producer-import checker PASS, **9,532** independently counted assertion groups: Y6=20, F9=70, F9 same-original SAT/UNSAT 1/0, F15 opposite cubes 2/0, C1 opposite cubes 1/0; all 264 F9 and 112 Y6 four-way original-clause S/U modes; 6,656 complement clause checks; 180 seeded three-policy confluence random CNFs; six malformed grammar rejections; exact source-ID tickets and reverse-reconstructed witness checks; connected C_t through t=16 and hostile toroidal k=4,6,8. U198/V198 inherited, NOT freshly replayed; logical XOR OFFLINE, native FLMV physical XOR unmeasured.

Fully charge each executed node by

    W(R)=C_grammar+C_source/index/head+C_semantic_acquisition
      +C_selection/switching/failed+C_GE/matroid/proof
      +C_cache/replay+C_child/output/bit_access
      +C_guest_DELAY/COPY/RECOMP + Σ_{evaluated children Q} W(Q).

The simultaneous peak includes **all** live writable/index/head/ancestor/matrix/cache/proof/child/guest storage. The zero-resolvent phase alone has polynomial work and a strictly decreasing Ψ; a nonempty kernel still requires exact fallback, potentially 2^n poly(N). All-input polynomial total work, arbitrary-A→Phi(A) hereditary power-short transformation with unknown exponents and a separately strict numerical **SAME-MACHINE FLMV transfer** remain OPEN. P=NP and P≠NP remain OPEN.

## Literature and project duplication firewall

First read decision-only five-role handoff, 01:48 integrated handoff, 01:44 saturated-cycle affine theorem, issue #3, AGENTS/CODEX/pnp-research skill, LSPV-2 320/PIVOT293/COFACTOR319 and LSPV-1 314. Primary literature: Döcker (2019), Eén–Biere (SAT 2005), Heule–Järvisalo–Biere blocked clause elimination (2010), FLMV (2005). BCE confluence is known, **general** bounded VE is nonconfluent; this restricted deletion-only confluence is not claimed as a new broad preprocessing theorem. GitHub searches j15marti/pnp for tautological cross-resolvents, PIVOT293 and continuation, plus github.com/openai for Davis–Putnam SAT implementations returned no directly applicable OpenAI SAT solver. No novelty is inferred from that absence.

**Next falsifier:** combine this polynomial zero-resolvent saturation with paid signed-spill/affine/2SAT/matroid and bounded-interface checks on connected **nonpaired** canonical hard-control families; test whether the aggregate branching/work potential can be uniformly bounded rather than only per phase.

References: [1] https://arxiv.org/abs/1912.08032 ; [2] https://doi.org/10.1007/11499107_5 ; [3] https://www.cs.utexas.edu/~marijn/publications/BCE.pdf ; [4] https://doi.org/10.1145/1101821.1101822 ; [5] https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-01_1907_LSPV-2_CROSSTAUTO_FORGET320.tex ; [6] https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-01_1800_LSPV-1_PAID_HIGHWIDTH_NAE314.tex .
