# TMR-2/071 | 2026-11-17 16:12 PST | Adaptive read-once T5 obstruction via exact two-palette projection

**Owner:** TMR-2 / PNP Information Necessity. **Status:** PROVED/EXACT within the stated pointwise read-once representation model, using the original Razgon NROBP and LPS expander theorems; external independent mathematical review OPEN. Finite source tests COMPUTATIONAL. **P versus NP OPEN.**

## Candidate, exact quantifiers and prospective falsifiers

**D2-T5-PALETTE-ADAPTIVE-NROBP-TRANSFER**, as an intermediate part of **D2-T5-MIXED-DECISION-FBDD-OBSTRUCTION**: exhibit an explicit, authentic family of original five-symbol CSP sources for which every syntactic adaptive read-once branching program representing the **pointwise assignment predicate** has exponential size, even if nondeterministic. Separately give the same family a correct, inexpensive authentic-source SAT decider. The mixed YES/NO and all-algorithm bridge remain OPEN.

Falsifiers stated before source/literature audit: (F1) no two-element palette pair yields a true 3-of-4 Boolean constraint; (F2) palette restriction cannot be applied to adaptive / nondeterministic branching-program paths without requerying or exponential growth; (F3) the chosen graph family fails bounded degree, uniform source construction or linear matching width; (F4) the pointwise lower bound is mistaken for source SAT work, exact counting or a field-dependent tensor rank bound. F1-F4 are resolved within the restricted model.

## Authentic construction and exact semantic reduction

Let R(a,b)=[(b-a mod 5) in {1,3}] on Sigma=Z5. Its two **vertex-dependent** palettes are

    left palette U=(0,3), with Boolean 1->0 and Boolean 0->3;
    right palette V=(1,3), with Boolean 1->1 and Boolean 0->3.

Their exact relation submatrix is

    R|_(U x V) = [[1,1],[1,0]].

For any simple bipartite graph H=(L disjoint_union V,E), orient **all** edges from L to V. Output its complete ordinary canonical T5 source: `p t5 n m`, all `v i` declarations and sorted `a u v` arc records, with no externally pinned symbols. Let P_H(x) be the original five-valued full-assignment indicator.

Restrict the domain of every vertex on L to U and every vertex on V to V, mapping binary bits to the positions in their respective palettes. Then for **every** binary input b,

    P_H(palette(b)) = phi_H(b) := product_{ {u,v} in E } (b_u OR b_v).

This is literal **pointwise equality** on a 2^n-assignment subcube. It is NOT existential projection, averaging, auxiliary summation, a counting reduction, or a change to the actual encoded CSP. There are no added T5 vertices and no extension multiplicity. For a directed graph with source/sink partition the original five-way SAT answer is YES by the fixed witness 0 on every source and 1 on every sink. Exact original T5 counts differ from the binary restricted counts.

## From arbitrary adaptive T5 read-once representations to NROBPs

Define a syntactic five-symbol read-once nondeterministic branching program to be a finite rooted acyclic graph with a rejecting/accepting interpretation, edge labels of the form `(vertex = symbol)` (or unlabeled epsilon edges), and no repeated test of a vertex on any root-to-sink path. Acceptance is existential over complete label-consistent paths; its language is exactly the five-way function P_H.

Given **any** such program B of s nodes/edges, delete every labelled edge outside the assigned palette of its vertex, replace each retained five-symbol literal by the corresponding binary literal, and leave epsilon edges unchanged. Prune unreachable nodes if desired. Every old path remains read-once, and the resulting binary NROBP accepts exactly phi_H. The transformation takes O(s+n) description work and at most s nodes/edges. This remains valid for path-dependent variable order, sharing, epsilon transitions, guessing and arbitrary nondeterministic branches, not just fixed-order OBDDs. If necessary, Razgon's uniformization for binary NROBPs has at most O(n) multiplicative edge overhead. Thus

    size_NROBP(phi_H) <= O(n) * size_T5_readonce(P_H).

Razgon, *On the Read-Once Property of Branching Programs and CNFs of Bounded Treewidth* (2014; arXiv:1411.0264), **Theorem 3.2**, gives for a graph of maximum degree Delta

    size_NROBP(phi_H) >= 2^{mw(H)/f(Delta)},

where f(Delta)>0 depends only on Delta, and mw(H) is the minimum, across all vertex permutations, of the largest prefix-crossing matching size. The cited source specifies syntactic read-once, allows arbitrary/adaptive read order and nondeterministic choice, and explains nonuniform-to-uniform conversion. This is a known theorem imported with its exact model; it is NOT a new NROBP lower-bound proof.

## Explicit bounded-degree expander source with quantitative matching width

Take the prior /070 nonbipartite LPS Cayley graph X_q=X^{5,q}, q prime >125 and q=1 mod20. This established family has n_q=q(q^2-1)/2 vertices, degree d=6 and all nontrivial adjacency eigenvalues in [-lambda,lambda], lambda=2sqrt5<6. Form its **bipartite canonical double cover** B_q by replacing each old vertex i by left i and right i', and replacing each undirected {i,j} by the two edges (i,j') and (j,i'). Orient every resulting edge left-to-right, and serialize all 2n_q original vertices and 6n_q arcs. The complete source length is L_q=Theta(n_q log(n_q+2)); generation involves explicit original LPS group/modular arithmetic, graph enumeration, covering edges, sorting and complete serialization, polynomial in **output** length. No binary-q-index polynomial promise is asserted.

The double-cover adjacency matrix is [[0,A_X],[A_X,0]], hence its eigenvalues are +mu_i and -mu_i. Because X_q is connected and nonbipartite, the only trivial values are +6 and -6; all others have absolute value <=2sqrt5. For any S of exactly half the N=2n_q cover vertices, the spectral bound gives

    e(S,S^c) >= (6-2sqrt5) N/4.

One crossing matching edge can exclude at most 2d-1=11 other edges in a greedy construction, so

    mw(B_q) >= (6-2sqrt5) N / 44.

**Theorem (restricted):** every exact syntactic five-way nondeterministic read-once branching program for the pointwise T5 assignment predicate of this explicitly constructed family has size

    size(B) >= 2^{(6-2sqrt5)N/(44 f(6))}/O(N) = 2^{Omega(N)} = 2^{Omega(L_q/log L_q)}.

In particular, every adaptive FBDD and every OBDD for the same pointwise predicate is exponentially large. This is quantitatively stronger in representation class than /070's fixed-order OBDD bound. The theorem is symbolic conditional only on the correctly scoped cited established results, not an empirical extrapolation.

## Source-aware cheap algorithm and same-realization ledger

For a **general canonical T5 graph source**, a single deterministic machine authenticates all source bytes, declarations, arc indices/counts, ordering, loops and duplicates. When every nonisolated vertex is a pure source (indegree zero) or pure sink (outdegree zero), assign 0 to all sources and 1 to all sinks, and 0 to isolates; verify every arc and output YES and the original-label witness. This covers **every** oriented bipartite source above without LPS identification, eigenvalue calculation, graph isomorphism testing, branch program compilation or supplied labels. On malformed input report INVALID; on a valid loop the count is zero. All other well-formed graphs retain a correct exhaustive original-label fallback.

On accepted pure-source/pure-sink sources of length L, one conventional locally headed finite-tape deterministic machine has the conservative **same-run** upper bounds T=O((L+1)^4), S_peak=O((L+1)^2) writable bits, including full input scans, degree/sort tables, bad-source guards, verification, source/witness/output buffers, head moves, and failed certificate attempts. Generic fallback is O(5^n (L+1)^4) time and polynomial workspace. No polynomial exact-original-T5-count algorithm is claimed for the expander family. Full original-variable tensor/pointwise representation must not be confused with source-decision computation. In particular all instances of this subclass are YES, so this does **not** close the intended mixed YES/NO obstruction.

For TMR-4 the named execution-sensitive invariant is **D2-T5-PALETTE-NROBP-TRACE**. The complete transition interface is READ/PARSE/GUARD, BIPARTITION-TEST, FIXED-WITNESS/VERIFY, FALLBACK/SWITCH, BRANCH-LABEL, PALETTE-RESTRICT, DELETE-OUT-OF-PALETTE, EPSILON/PATH-MERGE, CACHE/DROP/RECOMPUTE, UNIFORMIZE, CUT-MATCH, OUTPUT. The lower-bound invariant is syntactic original-variable read-once, not general physical time; it is preserved by the precise palette filtering map. A general Turing machine may reread, compute a graph certificate, or simply output the 0/1 witness, and is not forced to traverse the NROBP.

## Executed evidence and hostile controls

Hosted V8 executed exactly the published `audit071` JavaScript function, revision `tmr2-t5-palette-nrobp071.v1`, no RNG seed, **438 assertions, zero failures**. Finite authentic-source comparisons evaluated complete five-way assignments, each binary subcube and source parsing on K2,2, K3,3, the K4 bipartite crown double cover, a directed 6-cycle viewed bipartitely, and two disjoint oriented edges. Observed (original T5 count, binary restricted CNF count): K2,2=(30,7), K3,3=(70,15), K4 crown=(190,35), bipartite C6=(100,18), disjoint edges=(100,9). Exactly ten unordered 2-by-2 palette pairs have three ones. K3,3 at the left-prefix cut has eleven semantic cofactor masks including zero, rational-rank proxy 10 modulo 101, but a cheap exact original count 70. A fully exhaustive subset-DP over all 8! possible cuts/orders determined minimum matching width 3 for the K4 crown, with matching size 4 at the left/right cut. Four malformed sources rejected; a syntactically valid loop flagged for correct zero-count handling. Independent CPython complete-label checks reproduced the K2,2, K3,3 and K4 crown counts exactly. No eligible large-q LPS source was executed.

Code: `experiments/tmr/tmr2_t5_palette_nrobp071.js`.
Immutable raw: `results/raw/tmr/2026-11-17_1612_TMR2_T5_PALETTE_NROBP071_V8_RAW.json`.
Previous original: `research/agents/tmr-2/2026-11-17_1512_TMR2_T5_POSITIVE_COFACTOR_OBDD070.md`.
Original external references:
1. Razgon (2014), arXiv:1411.0264, Theorem 3.2: https://arxiv.org/abs/1411.0264
2. Lubotzky, Phillips and Sarnak (1988), *Ramanujan Graphs*, Combinatorica 8, 261-277: https://doi.org/10.1007/BF02126799

**Correction to /070's ancillary girth sentence:** The statement `girth >=28` for all q>125 is NOT established by the cited LPS lower bound. The latter provides the size-dependent `5^g >= 1+4q^2`, giving at least seven for q>125, not a uniform 28. No girth assumption is used in /071's read-once lower bound. Previous immutable /070 evidence is preserved.

## Mandatory four gates and unresolved issues

DISJ: **PASS restricted** because the theorem is explicitly for syntactic read-once representations; the linear-size source formula/circuit is a permitted cheap non-read-once method. Static-rank to arbitrary-time inference remains FAIL.

Relativization: **PASS for this restricted upper/representation argument, OPEN for any unrestricted P-vs-NP transfer**. No nonrelativizing ingredient is supplied; BGS, algebrization and Natural Proofs remain barriers to an indiscriminate conclusion.

Simultaneous DTISP: **PASS for the exact same source-decider execution upper ledger; NOT APPLICABLE to a forbidden deterministic time-space pair**. The representation size is not physical machine time.

Deterministic configuration counting: **PASS upper-bound safeguard only**. For a total standard fixed-tape deterministic decider T<=2^{O(S+log L)}; never invert it into a work lower bound or transfer without proof to randomized/quantum systems.

Other guards: Horn, 2-SAT, affine/Gaussian, equality, autarky, disconnected products, treewidth, DISJ, padding, auxiliary multiplicities, unique-solution rank one, selectors, fields/bases, cached/shared circuits, alternative orders and source recognition all remain legal. Indeed the binary subfunction is a **monotone 2-CNF**, SAT-trivial but difficult for syntactic read-once *pointwise representation*. The T5 core/NP-complete classification is unchanged. /341 FAIL as full UNSAT authority; /386 RESTRICTED.

**ONE next load-bearing lemma: D2-T5-MIXED-DECISION-SOURCE-ADAPTIVE-OBSTRUCTION (OPEN).** Find source-authenticated genuinely mixed YES/NO T5 instances and a non-artificial adaptive evaluator restriction under which a claimed quantitative resource necessity survives all authenticated source-side polynomial certificates, alternative structural recognizers, labels, multicut orders, switching, caches and recomputation. Restricting a pointwise function to an easy monotone 2-CNF is NOT a source-level decision obstruction. Independent external review remains OPEN. Native repository checkout preflight, full manuscript compilation and instruction-level TM replay were not executed; connected GitHub reads were used.
