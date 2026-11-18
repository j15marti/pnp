# TMR-2/078: Undirected-girth amplification of an exact T5 NO source and singleton-AC obstruction

Date: 2026-11-18 00:07 PST (America/Los_Angeles). Role: TMR-2 / PNP Information Necessity. Repo: j15marti/pnp. Status: **PROVED/EXACT within the stated existential/source-local scope; independent mathematical review OPEN.** Finite tests are **COMPUTATIONAL**. P versus NP OPEN.

## Target, quantifiers and falsifiers

Target dependency: **D2-T5-SAME-SKELETON-EXPLICIT-NO-PLUS-COFACTOR** from /077, refined here to **D2-T5-UNDIRECTED-GIRTH-SINGLETON-PC-OBSTRUCTION**. The newly closed part is an independent mathematically certified *existence* of YES/NO orientations of a common bipartite, connected skeleton of arbitrarily large undirected girth. We do **not** obtain an explicit efficiently generated member of the 170-vertex W(3,4) skeleton, a polynomial-time generator for the lifted NO orientations, a general lower bound, or the requested exact large-instance OBDD/FBDD cofactor comparison. These obligations remain OPEN.

Pipeline: canonical p t5 n m source -> authentic graph and orientation -> exact six-variable negative seed -> probabilistic blown-up source existence and fiber-majority soundness -> undirected short-cycle deletion -> select a connected NO component -> compare with source orientation that directs all bipartite edges left-to-right -> exact signed-path and singleton-arc-consistency state -> strictly scoped conclusion. Falsifiers were: (i) a satisfying T5 map of the small seed; (ii) a directional-girth-only theorem substituted for underlying undirected girth; (iii) a short undirected cycle left after deletion; (iv) PC or root-pinned AC detecting some high-undirected-girth orientation.

## Lemma 1. Explicit K(2,4) original-source UNSAT certificate

Take original vertices u=0, v=1 and w_ab=2+2a+b for a,b in {0,1}. Put exactly two arcs incident to each w_ab: u->w_ab if a=1, w_ab->u if a=0; v->w_ab if b=1, w_ab->v if b=0. All four binary orientation signatures occur. This is a genuine loopless oriented K(2,4) with n=6, m=8, no auxiliary variables.

For any T5 assignment: if the colors of u and v coincide, the signature (1,0) requires both opposite arcs on the same pair of colors, impossible. If the colors of u and v differ, the four w_ab must receive four distinct colors because a single right-side color has a unique signature relative to the fixed two left colors. Each w_ab is adjacent to u and v, so none of its colors can be either of their two colors. Only 3 target colors remain, contradiction. Hence Z(NO)=0. This proof uses only that the target is a loopless five-vertex tournament.

On the identical undirected K(2,4), orient all eight arcs left-to-right. Mapping {u,v}->0 and all right vertices->1 is a witness. Exact original-label enumeration gives Z(YES)=90, independently verified by the executable. One recognizes the NO seed *as a subgraph of any authentic source* by scanning two left candidates and finding representatives of all four neighbor orientation signatures in O(n^3+m+L) conventional adjacency-table operations and O(n^2+L) words. This is a polynomial, source-authenticating UNSAT upper certificate, not a lower bound. Full generic PC rejects this small NO seed; it is a control, not the desired residual obstruction.

## Lemma 2. Undirected-girth homomorphism-preserving blow-up (probabilistic proof)

For any fixed finite oriented graph D with a bipartite underlying graph, any fixed target-size bound k>=1 and any fixed integer g>=8, there exists a finite oriented bipartite H with **undirected** girth at least g, a surjective graph homomorphism psi:H->D, and the property

    H -> C  iff  D -> C

for every oriented target C with at most k vertices.

Proof: For each vertex i of D, create a fiber V_i of size N. For each original arc i->j, include each potential arc from V_i to V_j independently with probability p=N^(-1+epsilon), where 0<epsilon<1/(4g). Let Y be the number of *undirected simple cycles* of lengths 3,...,g-1 in the random underlying graph. With a=|V(D)| fixed, their expectation is at most

    E[Y] <= sum_{s=3}^{g-1} (aN)^s p^s
          <= O_{a,g}(N^(epsilon(g-1))) = o(N^(1/4)).

By Markov's inequality Y < N^(1/4) with probability tending to 1. Independently, for every base arc i->j and every A subset V_i, B subset V_j with sizes at least N/k, the random count X(A,B) of original oriented arcs between A and B has mean at least N^(1+epsilon)/k^2. For sufficiently large N the Chernoff bound gives

    Pr[X(A,B)<N] <= exp(-N^(1+epsilon)/(8k^2)).

There are at most |E(D)| 4^N choices of a base arc and two subsets. The union-bound failure probability tends to 0. Choose one realization satisfying both properties. Delete one original arc from every undirected short cycle in that realization; at most N^(1/4) arcs are deleted. The resulting H has undirected girth >=g, and for every original arc i->j and any A,B as above there remains at least one arc A->B.

The projection psi maps each fiber V_i to its index i. If f:D->C exists then f∘psi:H->C exists. Conversely any phi:H->C gives, for each fiber, a most-frequent color f(i), used on at least N/k vertices. The surviving A->B arc for every original i->j forces f(i)->f(j) in C. Thus f:D->C. All edge directions are inherited from D, so bipartiteness of D's underlying skeleton is preserved. The proof charges no hypothetical search for a satisfying map, and does not assert an efficient deterministic construction: the realization and deletion are **existential**.

This is a scoped sparse-incomparability-style argument. It is NOT derived from Kayll and Morris's 2023 theorem by substituting its "girth": that publication explicitly defines oriented girth as **directed** cycle length (Section 2, p. 236), which is insufficient for our PC lemma. We count undirected cycles independently to repair that exact source mismatch. Related background: Nešetřil and Zhu (2004), *On sparse graphs with given colorings and homomorphisms*, JCTB 90:161-172, DOI 10.1016/j.jctb.2003.06.001; Kayll and Morris (2023), *On Colouring Oriented Graphs of Large Girth*, DOI 10.55016/ojs/cdm.v18i2.73457.

## Theorem 3. Arbitrarily high undirected-girth, same-skeleton mixed answers

Apply Lemma 2 with D the K(2,4) NO orientation from Lemma 1, k=5, any g>=8 and C=T5. The resulting H is UNSAT. Its underlying skeleton is bipartite. Direct every edge of that same skeleton from its left class to its right class, and assign T5 labels 0 on the left and 1 on the right. Since R(0,1)=1, the second orientation is YES. Vertex count and the complete undirected skeleton (including distances and girth) are identical. The NO source must have some connected UNSAT component, because a disjoint union maps to T5 iff each component maps. Restrict both orientations to this component. Any oriented forest maps to T5 by propagating along tree edges, so this connected NO component contains an undirected cycle and at least g original vertices. Thus these existential mixed pairs have unbounded source size. Their generation is not established polynomial-time and degree regularity is not established.

## Lemma 4. Exact PC and singleton-AC state for every undirected-girth >=8 orientation

For a signed oriented path of length d, each step allows two modular displacements whose difference is +/-2 modulo 5. The reachable target difference set has exactly min(d+1,5) elements. In particular **every one** of the 16 signed orientation words of length four yields the full five-element difference set; longer paths also yield full relation.

On a loopless source whose underlying undirected girth is >=8, for each ordered vertex pair (i,j) put P_ii=identity, and when graph distance d(i,j)=1,2,3 put P_ij equal to the composed T5 relation along the unique short undirected path, respecting arc direction. For distance >=4 put P_ij=Sigma×Sigma. Every P_ij is nonempty, and |P_ij|=5 min(d(i,j)+1,5). This family is exactly the standard complete binary (2,3)-path-consistency fixed point: edge/path constraints imply the distance 1/2/3 entries, and it is closed under every triple-composition because concatenations of total length >=4 give full relation; shorter concatenations reduce to the unique path, possibly with reversible backtracks whose relation contains identity. Full pair-entry counts depend only on the undirected distance distribution, not the YES/NO orientation.

More strongly, fixing ANY root variable r to ANY of its five labels a does not cause ordinary arc consistency to fail. Define S_j={b:(a,b) in P_rj}. It contains a nonempty set for each j; S_r={a}. By path consistency, every b in S_i has a support c in S_j along each original arc (i,j), and conversely. Thus S is an AC-stable nonempty domain assignment after rooting, so singleton-AC cannot produce a wipeout.

The resulting **D2-T5-UNDIRECTED-GIRTH-PC-SINGLETON-TRACE** supplies TMR-4 with actual-source transitions READ/PARSE/GUARD, VERIFY_SKELETON/GIRTH, SIGNED_PATH_COMPOSE, PAIR_MASK_REVISE, ROOT_PIN/AC, CACHE/DROP, RECOMPUTE, CANDIDATE_WITNESS/VERIFY, FALLBACK/SWITCH and OUTPUT. No computational necessity or general-circuit lower bound follows from those semantic masks.

## Executed finite audit and cost ledger

Executed CPython 3 stdlib program tmr2-t5-ugirth078-compact.v1 at experiments/tmr/tmr2_t5_ugirth078_compact.py with **12,487 passing assertions** and zero failures, including: exact counts Z(NO)=0 and Z(YES)=90; all 256 original K(2,4) orientations (160 SAT, 96 UNSAT, and all 96 PC-detected); every 720 vertex renamings for each seed orientation; all signed paths of lengths 1..4; all 256 orientations of the undirected 8-cycle, each with full PC pair-entry count 960; 10,240 original-root and singleton-label AC attempts on those cycles, all nonrejecting; all 32 domain-mask ranges. Verified complete canonical source serialization for both seeds and all 8-cycle orientations. The executable does **not** construct the large existential H, does not search for a large certified NO orientation, and does not bound OBDD/FBDD or general solver runtime.

Independent local CPython source SHA256: 8680f5f519b22c9d00db81b230ebebf5142ac69c94ba90dd2b1b667712f4f1c3. Executed raw SHA256: 01b2cba867c9d0118c3af23bdf26dff52e8f0e0a26105a3dd13d8ab35d95c601. Git publication artifact paths: experiments/tmr/tmr2_t5_ugirth078_compact.py and results/raw/tmr/2026-11-18_0007_TMR2_T5_UGIRTH078_COMPACT_RAW.json. The program runs without third-party packages. No full LaTeX compile, physical TM microtrace or local repository preflight was performed.

The small six-vertex NO certificate detector has O(n^3+L) graph operations and O(n^2+L) words including parsing/adjacency construction. For arbitrary input, explicit binary-PC stores O(n^2) five-by-five relation entries and has O(n^3) fixed-alphabet work per global sweep; since at most 25n^2 distinct pair entries can be deleted, O(n^5) elementary operations is a conservative total upper budget, plus authentication, address bit costs and output. Singleton-AC repeated over all 5n root assignments remains polynomial. Those are actual upper algorithms, never compulsory lower work. The probabilistic-existence proof has **no claimed source-generation time bound**; testing all fiber-large subsets is exponential if performed naively. Existence is not silently turned into a polynomial-time uniform family.

## Scientific gates and controls

- DISJ: **PASS restricted**. All claimed rank/local-state facts are semantically scoped; no static rank -> arbitrary circuit/time lower inference (that transfer would FAIL the control).
- Relativization: **PASS for elementary local lemmas / OPEN for any unrestricted NP separation**. Baker-Gill-Solovay, algebrization and Natural Proofs restrictions remain active.
- Simultaneous DTISP: **PASS for explicitly paired finite-source PC/AC upper processing / OPEN for any forbidden lower resource pair**.
- Deterministic configuration counting: **PASS upper-only**. No claim of necessity or transfer to randomized/quantum algorithms.
- Easy controls retained: source-indexed signature detection, root-pinned AC, path consistency, low-degree elimination, 1/2/3-separators, Horn/2SAT, affine and Gaussian forms, symmetry, modules/twins, bounded treewidth, direct witnesses, alternative compact representations, shared subcomputations, caching and recomputation. Old /341 remains FAIL as a universal UNSAT procedure; /386 remains RESTRICTED.

## ONE next dependency

**D2-T5-UGIRTH-EXPLICIT-SOURCE-AND-ADAPTIVE-COFACTORS (OPEN):** produce a reasonably sized **explicit**, independently UNSAT-certified undirected-girth >=8 original T5 source (preferably on the previous W(3,4) 170-vertex skeleton), retain the same-skeleton YES instance, and compare root-pinned AC, complete PC, exact cofactor multiplicities, OBDD/FBDD and tensor contraction plus source-recognizing solvers on the SAME authenticated graphs. Any computational lower bound remains model-scoped until a cost-sound unrestricted transfer is proved.
