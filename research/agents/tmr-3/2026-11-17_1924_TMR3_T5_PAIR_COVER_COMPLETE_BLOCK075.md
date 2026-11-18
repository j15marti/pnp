# TMR-3/075: polynomial exact T5 counting beyond the missing-triple threshold

Date: 2026-11-17 19:24 PST, America/Los_Angeles. Owner: TMR-3 / PNP Time-Space Tradeoffs. Named dependency **C3-T5-RAINBOW-EDGESET-SIGNATURE** strengthened for a new restricted original-input family. Status: **PROVED/EXACT restricted** by symbolic argument, external mathematical review OPEN; finite tests COMPUTATIONAL; P versus NP OPEN.

## Exact domain and falsifiers

For every k>=3 and F subset of binom([k],3), form the actual directed graph I(k,F): k hub vertices, one distinct private sink L_S for each present triple S in E_H=binom([k],3)\F, and actual arcs i->L_S for i in S. The graph is given in the full unary-header, low-bit-first fixed-width binary digraph encoding, not a hypergraph oracle. Require (1) **pair coverage**, every pair of hubs lies in some present triple, and (2) **complete-block holes**, with F the disjoint union of all triples contained within each connected component B_i of the missing-triple primal graph. Both properties are discovered and authenticated from the original graph. Missing count d=|F| may be Theta(k^3); block sizes s_i may be k-1.

Falsifiers: F1 three legal hub colors despite pair coverage; F2 incorrect private-sink completion multiplicity for compatible colors; F3 duplicated monochrome contributions from binary palette assignments; F4 uncharged exponential component-mask enumeration or hidden access to a preloaded hypergraph. All four are resolved by the following exact construction.

## Pair-coverage lemma

For the fixed T5 tournament, Out(a)={a+1,a+3} modulo five. Distinct a,b share a successor exactly when b-a is +2 or -2 modulo five. The undirected graph of compatible distinct colors is a chordless C5 and therefore has clique number two. Every pair of differently colored hubs occurs together in a present triple and must have a common successor assigned to that triple's leaf. Any three distinct colors globally would form a triangle of compatible colors, impossible. Hence each legal hub assignment is monochromatic or uses exactly one of the **five unordered compatible pairs**. A private sink has exactly two extensions when its incoming hubs are monochrome, one when two distinct compatible colors occur, and zero otherwise. This is independent of d and proves F1/F2.

## Exact counting and block-polynomial theorem

Let m_3=|E_H|, d=|F|. For a binary assignment a to k hubs, put p(a)=number of ones, j_F(a)=number of missing triples monochromatic under a, and A[p,j]=number of assignments with these values. Then the count of **all original hub and sink labels** is

    Z(I(k,F)) = 5*2^m_3
       + 5 * sum_{p=1}^{k-1} sum_{j=0}^d A[p,j]
                  * 2^(C(p,3)+C(k-p,3)-j).

The first term counts five all-equal hub choices, each with two choices for every genuine sink. For every fixed compatible unordered palette, a nonconstant binary hub assignment has exactly C(p,3)+C(k-p,3)-j present monochrome triples and all other present triples have one sink extension. Every nonconstant original coloring has exactly one compatible pair palette, so F3 is excluded.

For each complete missing block B_i of size s_i, define

    P_i(z,u) = sum_{a=0}^{s_i} C(s_i,a) z^a
                        u^(C(a,3)+C(s_i-a,3)).
    PRODUCT_i P_i(z,u) = sum_{p,j} A[p,j] z^p u^j.

The identity holds because the ones count and missing-monochrome triple count add across disjoint blocks. Each block contributes **s_i+1 terms rather than 2^s_i**, and sum_i(s_i+1)<=2k. The rolling coefficient table has at most (k+1)(d+1)=O(N^4) entries, each at most 2^k, using only polynomial construction work even when max s_i grows linearly. This proves F4.

## Large exact example and independent formula

Take two missing components of sizes (s,1), meaning F consists of **all C(s,3) triples within a block of s hubs**, with one hub outside. Every present triple is the external hub plus a pair within the big block, so pair coverage holds. For a fixed external hub color, all internal hubs must be either that color or one single compatible partner color. The two possible partner choices are incompatible with each other. Hence an **independent** one-variable count is

    Z = 5*2^C(s,2) + 10*sum_{p=1}^s C(s,p)*2^C(s-p,2).

It agreed with the block DP for s=3,4,7,19,39. For s=39, the authentic original graph has **781 vertices**, **2223 arcs**, **9139 missing triples**, a missing-primal component of 39 hubs, only **79** nonzero DP states, and an exact **744-bit** count. The old /074 component-mask DP would visit 2^39 binary masks; the new algorithm is polynomial for this family. Other checked block sizes include (20,20), (18,1,1) and (12,12,12). The largest checked original graph had 7640 vertices and 22800 arcs, with a 7603-bit answer.

## Full same-machine time/space ledger

For arbitrary binary input, one deterministic blank-start locally headed multitape machine reads and authenticates unary n,m, exactly m fixed-width endpoint pairs, lengths and address validity, and normalizes duplicate arcs. Loops or opposed arcs imply exact zero. It constructs actual incoming/outgoing neighborhoods, verifies every vertex is a valid hub or distinct degree-three private sink, checks all private parent triples and all C(k,3) possible triples, pair coverage, primal components and complete-block closure. These checks charge failed recognition and all source seeks. On recognition, it builds P_i and a rolling exact integer coefficient table, calculates and emits the actual count and its zero-test. On valid nonfamily inputs it executes the previously proved exact 2^(n-c) spanning-forest fallback, with c weak components, instead of declaring them unsatisfiable. Malformed inputs reject.

For a complete recognized run, parsing/canonical storage costs O((N+1)^6) bit steps, discovery/verification O((N+1)^8), at most O(k^2 d)<=O(N^5) exact coefficient updates including retained-table head seeks and O(N)-bit operations conservatively O((N+1)^12), and final exact powers/output O((N+1)^8). One **simultaneous** workspace ledger includes copied source, graph, triple membership, component indices, both coefficient tables, addresses, arithmetic buffers, caches and final output. All integers have at most O(N) bits since Z<=5^n. Therefore

    T_family(N)=O((N+1)^12),
    S_peak_family(N)=O((N+1)^5) writable bits.

The single all-input machine with failed recognition plus actual forest fallback has T_all(N)=O((N+1)^12*(1+2^(n-c))) and S_peak_all(N)=O((N+1)^5). These are upper bounds on the same sequential execution, not separate minima. No free random-access oracle, preloaded checkpoint, uncharged structural recognizer, or parallel speedup is assumed.

## Evidence, source revisions and unexecuted checks

The readable published all-input solver is experiments/tmr/tmr3_t5_blockholes075_readable.py, independently **executed locally** against the full original reference on 102 cases, zero failures; source Git blob 0ee0fd2eb8d3f3dd488bd201dd7773f1b525f8ba, SHA-256 b39c6bec9ab54380a873540e313cd32bd4a4f69d9f7455380cb8100a7dc2b327. The *separate larger audit source*, revision tmr3-t5-blockholes075-v1, seed 202611171924, source SHA-256 d2b6227530d68b32ade4b415e624d838d06ccbfc3c008b5cb81dfcfbbe83e404, ran twice in local CPython (15.4 and 15.2 seconds), with **185 assertions, zero failures**, byte-identical raw JSON SHA-256 a176dd96f950d820f6a665f29a811dcfc49b8774134c2234f310bade13587cc5. It independently compared original five-color sink enumeration on small graphs, all small block partitions, vertex renamings, 60 arbitrary fallback graphs, source malformed controls and the four large families. The full audit source is a separate local conversation file; it is **not** falsely represented as the compact published code. Immutable captured raw JSON is results/raw/tmr/2026-11-17_1924_TMR3_T5_BLOCKHOLES075_PY_RAW.json.

The new LaTeX theorem fragment compiled successfully as an isolated three-page document. Native Turing-machine microcode, complete repository preflight and full owned-manuscript compilation have **not** been run, nor has independent external mathematical review. Local GitHub checkout was blocked by DNS; connected repository full-file reads were available.

## Four gates, barriers and controls

**DISJ sanity: PASS restricted:** positive source-aware exact counting, no static rank-to-mandatory-work inference. **Relativization: NOT APPLICABLE WITH REASON** to a separation; BGS/algebrization/Natural Proofs guards remain. **Simultaneous DTISP: PASS restricted upper** for the complete same-run cost account, with no time-space lower bound transferred. **Deterministic configurations: PASS upper-bound consistency only**, not a work lower bound or a randomized/quantum claim.

All legal Horn/2SAT, affine, bounded-treewidth, equality, autarky, product, padding/auxiliary, selector, unique-solution, field/local-basis, module, cached/recomputed and other compact source-aware alternatives remain admitted. Historical /341 FAIL as full logical UNSAT authority; /386 RESTRICTED. General T5 homomorphism remains NP-complete under the original 1988 semicomplete-digraph theorem, but this constructive restricted upper bound establishes neither general SAT/T5 exponent lower bounds nor P versus NP.

## Original references and ONE next dependency

[1] Bang-Jensen, Hell and MacGillivray (1988), The Complexity of Colouring by Semicomplete Digraphs, SIAM J. Discrete Math. 1(3):281-298, https://doi.org/10.1137/0401029 . Original abstract directly checked.
[2] TMR-3/074 prior component-DP report: research/agents/tmr-3/2026-11-17_1824_TMR3_T5_HOLES_COMPONENTS074.md, blob 77cc4b559abde47e4225fa1e4e4f7304cabd78b7, draft PR #241.
[3] TMR-1/078 explicit directed-acyclic T5 hardness gadget, issue #3 comment 6967863556, restricted proof and independent review OPEN.

**Next load-bearing lemma C3-T5-RAINBOW-BOUNDARY-DEFECT076:** drop pair coverage, parameterize the graph of hub pairs sharing no present triple, and give a source-discoverable exact signature for surviving three-or-more-color hub assignments, or a concrete minimal counterexample to one proposed state. All true query/discovery/retention/output costs must be charged. **P versus NP OPEN.**
