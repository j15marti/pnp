# TMR-1/087: Three-edge subdivision saturation, sharp two-edge obstruction, and source-authenticated path algorithm

Date: 2026-11-18 03:04 America/Los_Angeles. Owner: TMR-1 / PNP Machine Model Lead. Status: **PROVED mathematical theorem, finite COMPUTATIONAL checks, independent review OPEN; P versus NP OPEN.** Adds a sharp tractable boundary to the exact five-symbol beat-relation CSP. This does not claim a new general complexity classification.

## Primary-source classification remains unchanged

The fixed template is the regular five-vertex tournament (T_5) on (mathbb Z_5), with ((u,v)in R) iff (v-uin{1,3}pmod5). It is a semicomplete digraph with more than one directed cycle, so (T_5)-homomorphism is NP-complete by Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3) (1988), 281–298, https://doi.org/10.1137/0401029. The independent explicit C5-to-T5 parsimonious bridge appears in /080. This theorem identifies a restricted source class that is uniformly SAT despite unrestricted NP-completeness.

## Theorem C1-T5-THREE-SUBDIVISION-SATURATION087

Let (H) be **any** finite undirected multigraph (including disconnected components, loops and parallel edges). Replace each individual source edge by an internally vertex-disjoint path of length (ell_ege3). Orient each constituent path edge arbitrarily, independently of other edges. Denote the resulting oriented graph by (D(H)). Then (D(H)	o T_5): **every such input is satisfiable**. Moreover there is a source-authenticated constructive polynomial-time witness algorithm, and the statement holds even for source skeletons of unbounded chromatic number, treewidth and cycle rank.

A stronger endpoint-transfer statement holds for any path orientation word of length (ell):
* For (ell=3), equal-colored endpoints have exactly **3** internal extensions if all three path arcs are coherently oriented, and exactly **1** if the word contains both orientations.
* For (ellge4), **every pair** of endpoint colors has at least one internal extension.
Consequently, assigning one common color to all original skeleton vertices in each connected component and filling in each path gives at least
[
 5^{c(H)},3^{a(H)}
]
distinct valid (T_5) assignments for the all-length-three subdivision, where (c(H)) includes isolated vertices and (a(H)) counts coherently oriented three-edge paths. This is a **lower bound** on the total count, not an exact global count.

### Exact proof

Write the successive path vertices as (v_0,dots,v_ell), and for edge (i) let (sigma_i=+1) if its directed arc follows (v_{i-1}	o v_i), (-1) otherwise. Its allowed signed color difference is (sigma_i(1+2b_i)) with (b_iin{0,1}). If (p) edges have positive sign and (q) negative sign, the possible total differences are precisely
[
  p-q+2tpmod5,qquad t=-q,-q+1,dots,p,
]
because the difference of the two subset-sums attains every integer in that interval. The interval contains (ell+1) consecutive integers. For (ellge4), it contains representatives of every residue modulo five, and multiplication by 2 permutes (mathbb F_5). Hence every endpoint-color difference is attainable, independent of direction word.

For (ell=3), checking the four possibilities (p=0,1,2,3) shows that zero is always attainable; direct evaluation of the binomial coefficients gives multiplicity 3 if (pin{0,3}) and 1 if (pin{1,2}). An explicit table of zero-return increments in path order, using (+) for forward and (-) for backward orientation:
```
+++ : (1,1,3)      ++- : (3,3,1)
+-+ : (3,1,3)      +-- : (1,3,3)
-++ : (1,3,3)      -+- : (3,1,3)
--+ : (3,3,1)      --- : (1,1,3)
```
The listed triples mean **unsigned** allowed increments (1,3); their signs are determined by the arc word. For each component of (H), choose a common root color (five choices). Each path has equal-colored endpoints, is individually extendible by the lemma, and its internal vertices are disjoint from all other paths. Extensions therefore compose globally. Independent shifts of original root colors yield the stated solution-count lower bound.

## Sharpness: two-edge subdivision of K6 is UNSAT

Let the skeleton be (K_6), with original vertices (0,dots,5). For every unordered pair (u<v), insert a new vertex (w_{uv}) and replace that edge by the consistently directed path (u	o w_{uv}	o v). The resulting input is a DAG; rank original vertex (u) by (2u) and rank (w_{uv}) by (2u+1). Its underlying graph is bipartite, triangle-free, and of girth six.

No allowed pair of T5 increments can sum to zero in two forward steps:
[
{1,3}+{1,3}={2,4,1}pmod5.
]
Thus every original pair (u,v) must have distinct colors. (K_6) needs six distinct colors while T5 has five, contradiction. This yields an explicit NO instance with (n'=6+15=21) vertices, (m'=30) directed arcs, canonical bit length
(L'=21+30+2+2(30)w(21)=353), (w(21)=5).
For comparison, the three-edge subdivision of the same K6 has (n'=6+2(15)=36), (m'=45), (w(36)=6), canonical length (L'=36+45+2+2(45)(6)=623), and is provably YES with all path orientations.

Therefore **three constituent edges per replaced original edge is a sharp uniform sufficient threshold** under arbitrary path orientations. This is not a characterization of all YES instances, and individual two-edge paths may be harmless.

## Canonical bit model and SAME_REALIZATION accounting

Follow the existing authenticated original-source format: unary (n), zero, unary (m), zero, followed by lexicographically sorted distinct directed endpoint pairs, each coded with (w(n)=max(1,lceillog_2max(2,n)ceil)) bits per endpoint, low-bit-first. Exact length (L=n+m+2+2mw(n)). Any witness has exactly (3n) bits with allowed codewords 0..4. Loops and opposite arcs remain accepted as source words but may fail the subdivision-class recognizer; malformed source words are rejected.

For an arbitrary skeleton with (n) vertices and (m) edges, uniform three-subdivision has (n'=n+2m) and (m'=3m), hence exact target encoding length
[
 L'=n+5m+2+6m,w(n+2m).
]
For arbitrary lengths (ell_ege3), set (n'=n+sum_e(ell_e-1)), (m'=sum_eell_e) and use the same canonical formula (L'=n'+m'+2+2m'w(n')).

Given a proposed path decomposition, check that each input arc appears exactly once, path interiors are vertex-disjoint, edge orientations match, and each path length is at least three. Parse and authenticate the full source first; reject promises violated by the decomposition. Output a branch-constant coloring and reconstruct each internal path via five-state dynamic programming in (O(ell_e)) abstract constant-domain operations, not search over all (5^{ell_e}) labelings. All rejected candidates, validation, arithmetic, witness printing, and writable storage are charged. A conservative simultaneous bound on a sequential bit implementation is (O((L+1)^4)) time and (O((L+1)^2)) peak writable space, including an explicitly supplied polynomial-size decomposition. This is an **upper** resource bound, not an unrestricted lower bound.

For a useful **unannotated sufficient-class recognizer** on loopless single-orientation input, form its underlying simple graph, choose all degree-not-two vertices as branch vertices, and decompose maximal degree-two chains; for a pure cycle component choose its smallest-index vertex as an artificial branch. If every resulting chain has length at least three, the constructive proof applies. This recognizer can reject other satisfiable graphs and is not claimed complete for T5-SAT.

## Finite computational verification

A dependency-free local Node.js verifier was executed on **all 126 direction words of lengths 1 through 6**. It independently formed complete five-by-five endpoint-transfer matrices, checked translation invariance and path witness construction, and verified all 3-edge zero-return multiplicities and 4–6-edge full support. It additionally tested 203 small source skeleton graphs, 2,612 actual oriented three-edge gadget extensions, 7,836 constructed arcs, and exhaustively enumerated the (5^6=15,625) possible K6 branch colorings for the two-step NO example. Total **14,606 assertions, zero failures**. Raw local result SHA-256: `fc0cdfba9c87c9cb975847079770c61a7ef0360a22d85ea34f64486c486055e8`. The shorter independently executed publication certificate made **6,564 assertions, zero failures**, including all direction words and the K6 pigeonhole control. Tests are COMPUTATIONAL; the arbitrary-size theorem follows from the separate symbolic proof above.

## Scientific consequence and limitations

Uniform long edge subdivision, even with high-girth/high-treewidth skeletons, destroys rather than preserves T5-CSP hardness: every image becomes YES. This blocks any proposed hardness-preserving reduction based only on subdividing each original edge into at least three unconstrained directed steps. It is consistent with /080's NP-hard bipartite triangle-free DAG gadgets, since those gadgets have extra shared shortcut constraints and are **not** simple subdivisions.

Do not claim this theorem rules out NP-hardness on all high-girth inputs, all bipartite DAGs, or all graph classes with similar geometry. Do not turn high chromatic number, feedback rank, treewidth, cycle count, or long paths into a mandatory computation lower bound. In particular no superpolynomial machine lower bound follows; P versus NP OPEN. Preserve algebraic/Fourier, propagation, polymorphism, quotient, graph-homomorphism, and compact-representation shortcuts. Independent mathematical review, full LaTeX compilation and Lean/nanoda replay OPEN. Next dependency: test mixed YES/NO non-subdivision authentic hard-source images after full residue consistency and binary-cycle Gaussian constraints, with exact SAME_REALIZATION cost accounting.
