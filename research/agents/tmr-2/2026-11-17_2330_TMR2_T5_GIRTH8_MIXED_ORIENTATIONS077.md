# TMR-2/077 | Same-skeleton YES/NO T5 orientations invisible to full path consistency

Date: 2026-11-17 23:30 PST. Owner: TMR-2 / PNP Information Necessity.
Primary object: the FIXED five-letter tournament T5, with R(a,b) iff b-a mod 5 belongs to {1,3}.
Status: PROVED/EXACT restricted mathematical construction and counting; finite source checks COMPUTATIONAL; independent external mathematics review OPEN. P versus NP OPEN.

## Named dependency, falsifiers, and relation to prior work

Dependency D2-T5-SIGGERS-TO-PC-RESIDUAL-OBSTRUCTION: produce mixed-answer actual-source T5 instances on the SAME large highly structured underlying graph, both accepted by genuine (2,3) path consistency, without short local obstructions.

Predeclared falsifiers: F1 the finite graph has a short cycle, wrong degree, wrong point-line incidences or a malformed source; F2 some signed length-four path does not realize all five target differences; F3 ordinary PC deletes any relation entry not predicted by the signed shortest-path rule or creates an empty relation; F4 orientation counting fails to produce at least one NO orientation, or the YES witness fails. All four passed the restricted construction in the executed audit and symbolic proofs.

The high-girth signed-PC lemma was ALREADY established by TMR-5/071 and employed by TMR-2/069. We are NOT claiming that lemma as new. The additional result here is a small explicitly constructed 170-vertex 5-regular bipartite skeleton with equal-size YES and NO ORIENTATIONS, a sharp same-skeleton counting proof, and a complete actual-source PC run on 28,900 pairs. It corrects the all-NO limitation of the earlier high-chromatic LPS example /069. The NO orientation is certified to exist by counting but is NOT individually identified or source-certified by the finite experiment.

## Theorem: fixed skeleton and both answers

Let B be the point-line incidence graph of the symplectic generalized quadrangle W(3,4). Work in GF(4)=GF(2)[z]/(z^2+z+1), using the 85 normalized nonzero projective points of GF(4)^4 and the 85 totally isotropic 2-dimensional subspaces under the nondegenerate alternating form

    <p,q> = p0*q2 + p2*q0 + p1*q3 + p3*q1.

There are 170 graph vertices and 425 edges. B is bipartite, connected, 5-regular, girth 8, diameter 4. Its distance profile from EVERY vertex is (1,5,20,80,64) at distances 0,1,2,3,4. An independent finite GF(4) enumerator checked these facts and the canonical actual-source serialization.

For every orientation D of B, full standard path consistency of Hom(D,T5) returns NONEMPTY, with the SAME number of retained binary label-pair entries: 604,350 across all 170^2 ordered source-vertex pairs. The exact entries depend on the source orientations, not merely on the distance. All 32 possible unary masks remain legal in the general solver; here initial full unary domains do not shrink.

There is an explicit YES orientation: direct each incidence from point to line, and assign label 0 to all points and label 1 to all lines. Since R(0,1)=1, this is an original-label witness.

At most 5^170 distinct orientations can have any T5 homomorphism: a proposed labeling f:V(B)->Z5 with unequal colors at every edge uniquely specifies the permitted direction of every edge; a labeling with any equal-color edge permits none. The skeleton has exactly 2^425 orientations. Since 5^170 < 2^425, some orientation is NO. A uniformly random orientation is NO with probability at least

    1 - 5^170 / 2^425 > 0.9999999992.

Thus there are YES and NO sources with the EXACT same 170 original variable identities, 425 distinct directed constraints, undirected skeleton, degrees, girth and pair-support cardinality profile. Every such instance passes full path consistency. No auxiliary-variable projection or multiplicity convention is used.

## Exact signed-path fixed-point proof

Along any oriented undirected edge, a forward traversal has allowed color increment D+={1,3}; a reverse traversal has D-={2,4} modulo 5. Each set is a translate of {0,2}. Thus the d-fold relational composition along ANY fixed signed walk has allowed differences

    t + {0,2,4,...,2d} (mod 5),

which has exactly d+1 elements for d=0,1,2,3 and all five for d>=4. A composed path of length four already gives the universal 5x5 relation, for every one of its 16 possible orientation words.

Suppose the underlying simple graph has girth at least seven. For each ordered pair u,v use the signed-path relation P_uv on its unique shortest path if its distance is <=3, the universal relation if its distance is >=4, and equality on the diagonal. This family refines every original unary, arc and converse constraint. It is a genuine path-consistency fixed point: if u-k and k-v both have short paths then their union cannot contain a cycle of length <=6, so their concatenation follows the u-v path with possible reverse detours, each allowing equality; a concatenation of at least four edges produces the universal relation. If either subpath is long, composing with the universal relation is universal, since all path relations are nonempty circulant. The diagonal case is also supported by reverse walks.

Since the ordinary PC operator is monotone and starts above this nonempty fixed point, it cannot delete any fixed-point tuple. Conversely, length-2 and length-3 path compositions force precisely these pair relations; therefore PC closure EQUALS the stated signed-distance kernel.

The number of permissible ordered label pairs at distances d=0,1,2,3,>=4 is respectively 5,10,15,20,25. The point-line source therefore retains

    170*(1*5 + 5*10 + 20*15 + 80*20 + 64*25) = 604350

binary relation entries. All do not imply a satisfying global assignment; these are precisely the local pair data, not final semantic cofactors.

## Infinite connected family and important limitations

This is not merely a fixed n=170 exception. Starting from B, take a connected two-sheeted graph lift: use identity matchings on all edges except one edge on a cycle, which uses the cross matching. The lifted graph remains simple, bipartite, 5-regular, connected and has girth at least 8. Its vertex/edge counts double. Repeating gives explicitly specified connected skeletons B_t with n_t=170*2^t and m_t=425*2^t. For each B_t, orient every bipartite edge left-to-right for an explicit YES instance. The same 2^m versus 5^n counting argument guarantees a NO orientation, and every orientation passes PC.

THE OPEN SOURCE-UNIFORMITY GAP: this elementary orientation counting proof does not efficiently exhibit or certify one particular NO orientation for every t. Nor does the chosen single-twist 2-lift guarantee immunity to cheap two-separator decomposition; the lift may introduce such separators. No exact solution-count lower bound or general-time lower bound follows. The sampled orientation in the executable is an exact PC control, NOT an independently proved NO instance. The yes side is source-recognizable and easy.

## Actual source-to-PC program and resource ledger

The reproducible experiment contains the full GF(4) incidence generator (experiments/tmr/tmr2_t5_girth077_generator.py), an independent C++ generic path-consistency engine accepting the original canonical p t5 source (experiments/tmr/tmr2_t5_girth_pc077.cpp), and raw evidence (results/raw/tmr/2026-11-17_2330_TMR2_T5_GIRTH8_PC077_RAW.json). Both programs were compared against a separate CPython exact signed-shortest-path oracle whose full local source hash is SHA256 a321c4bef48e4629d9b1e98e83e63164d29775bde1641f412b3a9c8e4c958d06, and whose local raw output SHA256 is f3ed913efbc130adfc546589a51fb575ef8819f1c5ff8b5701574e5d7d1a90cb. These two audit artifacts are local, not published in the GitHub branch. The published generator source matches the executed local code Git blob 3122f2760e53701e4e0d665c018eabca13038bb8; the C++ PC engine matches executed source Git blob be21b0adf34ffc18a65e1272e6b3371d44317994.

Execution: 52 top-level Python assertions, zero failures, with comparison of all 28,900 source ordered pairs x 5 binary row masks for BOTH orientations. Genuine exhaustive PC converged in two full sweeps, deleted 102,000 initial pair entries, and independently matched the exact signed-shortest-path relation on every ordered pair. Additional cases: all 16 four-edge signed path words, all 85 points and 85 lines, 425 distinct edges, actual incidence girth 8, a 7-cycle with exact 175 T5 solutions, 4-variable UNSAT forbidden-pattern rejection and malformed source controls. Random seed 202611172330. C++ build with g++ -std=c++17 -O2 -Wall and stdlib CPython; native 170-node PC runs were completed, not just proposed.

Same-realization costs for the finite experiment: original source decoding, GF4 generator, adjacency and BFS, genuine PC relation rows, all 25 possible color pairs per variable pair, switching between YES/sample, comparisons, big integer 5^n/2^m bound and source output were explicitly included. For a generic n,m source, dense pair-mask PC uses O(n^2) live 5-row tables and O(n^3) elementary operations PER sweep; at most 25n^2 pair entries can be deleted, so a deliberately conservative O(n^5) operation upper bound is immediate, with O(n^2 log(n+2)+L) bits of recorded pair-mask/graph workspace. Conversion to physical bit time is polynomial in the complete encoded source L, including line parsing and indices. The distance-only authenticated high-girth shortcut uses n breadth-first searches truncated at distance 3 and O(n^2) pair entries. Neither restricted runtime is a mandatory work lower bound for arbitrary source decision.

## Named execution-sensitive invariant for TMR-4

D2-T5-GIRTH8-SAME-SKELETON-PC-TRACE contains: the exact source cursor/length/records, 170 numbered original graph identities and 425 oriented arcs, the GF4 point/line incidence validator, degree/girth and distance/BFS witnesses, each signed path's <=3-step residue mask, all 28,900 current pair relations with row masks, each actual deletion/round/requeue, all domain masks, caches, source rechecks, orientation-count upper proof, optional YES original-label witness, and output or explicit UNKNOWN decision. Legitimate transitions are READ/PARSE/GUARD, BUILD/VERIFY_GRAPH, ORIENT/VERIFY_ARC, BFS3, COMPOSE_SIGNED, INTERSECT_PAIR, AC3/PC_REVISE, CACHE/DROP/RECOMPUTE, WITNESS, COUNT_ORIENTATIONS, SWITCH/FALLBACK and OUTPUT. No unrestricted solver is forced to materialize this trace, and a source-recognition shortcut must remain legal.

## Four mandatory gates

DISJ sanity: PASS restricted. Large PC residual tables or high-girth graphs are not general circuit/work lower bounds; the DISJ linear circuit and existing T5 source-recognized counterexamples remain legal.
Relativization: PASS restricted finite construction; OPEN for any nonrelativizing P-versus-NP implication, including algebrization/Natural Proofs.
Simultaneous DTISP: PASS only for the stated same-execution polynomial upper; no forbidden-region lower claim.
Deterministic configuration counting: PASS upper-only; no conversion from number of states/configurations to required visits, and no randomized/quantum extension asserted.

Unbounded-arity polymorphisms, 32 subset maps, TMR-1 forced shortcut, TMR-4 25-signature transfers, short motifs, Horn/2SAT, affine/Gaussian, treewidth, exact counting, modules/twins, separators, alternative representations, caching, recomputation, and true source-aware algorithms remain available. The NO orientation is existential; its decision complexity is not established.

## Sources and one next load-bearing dependency

[1] Bang-Jensen, Hell, MacGillivray, The Complexity of Colouring by Semicomplete Digraphs, SIAM J Discrete Math (1988), https://doi.org/10.1137/0401029 .
[2] TMR-5/071, research/agents/tmr-5/2026-11-17_1252_TMR5_T5_HIGH_GIRTH_PATH_CONSISTENCY071.md, earlier exact signed-path lemma.
[3] TMR-2/069, research/agents/tmr-2/2026-11-17_1412_TMR2_LPS_UNIFORM_PC069.md, prior high-chromatic all-NO source recognized in polynomial time.
[4] Payne and Thas, Finite Generalized Quadrangles (classical symplectic W(3,q) construction); finite 170-vertex incidence graph independently generated and checked in this experiment.

NEXT: D2-T5-SAME-SKELETON-EXPLICIT-NO-PLUS-COFACTOR. Replace the nonconstructive NO orientation by a deterministically reproducible source with a short independently checkable UNSAT certificate that does not reintroduce small local forbidden patterns; compare restricted dynamic/cofactor costs and every cheap source-aware decision. Preserve the 5-letter primary target. P versus NP OPEN.
