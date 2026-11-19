# TMR-5/089: articulation-factor shortcut versus global cycle rank

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** 2026-11-18, Pacific Time. **Status:** independently derived symbolic theorem; executed standalone Python reproducer in local conversation evidence ZIP; formal kernel / external review OPEN. **P versus NP OPEN.**

## New algebraic theorem

Fix the exact loopless tournament T5 on Z5, where R(a,b) iff b-a mod 5 belongs to {1,3}. Let Z(G)=#Hom(G,T5). Since every translation a->a+t is an automorphism, fixing any selected vertex to any one symbol gives exactly Z(G)/5 satisfying assignments.

For G1,G2 meeting only at vertex v, with no other shared edge or constraint,

    Z(G1 ∪_v G2) = Z(G1)*Z(G2)/5.

For G1,G2 disjoint, joined by one directed bridge, its orientation is immaterial and

    Z(G1 + bridge + G2) = 2*Z(G1)*Z(G2)/5,

because R has exactly ten ordered pairs and both indegree and outdegree are two.

Therefore, for a connected graph whose underlying undirected biconnected blocks B1,...,Bq include bridge edges as blocks,

    Z(G) = 5^(1-q) * PRODUCT_i Z(B_i).

Derive this by deleting leaf blocks in the standard block-cut tree. For disconnected graphs multiply per-component formulas and multiply by five for each isolated vertex. These formulas remain valid when Z(B)=0 and when some edge has both directed orientations (then the corresponding two-vertex block is impossible).

A directed cycle block, on ordered vertices v0,...,v_(ell-1), has an exact 5x5 transfer-matrix formula Z(C)=trace(M0 ... M_(ell-1)), where each Mi is R or R-transpose as the source edge direction requires (for antiparallel arcs use conjunction). This costs O(ell) fixed-size integer-matrix operations. Tarjan's block decomposition plus such transfer products gives linear arithmetic-time exact counting on ALL directed cactus graphs, although bit complexity includes O(n)-bit counts. If all noncycle blocks have size at most b, direct local enumeration gives O(n+m+SUM_B poly(|B|)5^|B|) arithmetic operations. No source reconstruction or special input labelling is needed.

## Authentic mixed YES/NO counterexample

Take K4 on {0,1,2,3}. Attach h >= 0 directed triangles one by one through a single articulation vertex; each contributes two new vertices, three directed edges, and the next articulation at its newest endpoint.

YES core: orient K4 precisely as T5 restricted to {0,1,2,3}; it has exactly FIVE T5 homomorphisms (the five rotations).
NO core: orient K4 as a transitive four-tournament; it has ZERO T5 homomorphisms since every homomorphism of a complete loopless tournament is injective, whereas T5 has no vertex of outdegree three.

Each attached directed triangle has exactly fifteen homomorphisms (three allowed cyclic step patterns times five translations). Consequently

    Z(YES_h) = 5 * 3^h;       Z(NO_h) = 0.

YES_h and NO_h have identical underlying undirected graphs; both have n=4+2h, m=6+3h, undirected cycle rank r=h+3, maximum undirected degree at most five, and treewidth exactly three. Yet the same generic block-cut procedure decides both and counts their assignments in O(h) arithmetic operations. This specifically defeats the inference that global cycle rank r demands 5^r computation: the earlier Fourier-flow O(m*5^r) enumeration is a valid *upper bound for one algorithm*, not an instancewise necessity. It does not establish any general SAT time lower bound.

## Independent execution

The executed standalone standard-library Python verifier independently implements exact assignment backtracking, Tarjan biconnected components, per-block enumeration, cycle transfer matrices, and the exact block-cut product. Its tests include antiparallel constraints with AND rather than OR semantics.

* 154 seeded random graphs of 1..7 vertices checked against full global backtracking.
* 150 adversarial vertex-ID permutations and shuffled edge lists of the authentic YES/NO family preserved the counts.
* Sixteen YES/NO cases for h=0..7; full independent global backtracking also for h<=4.
* Four large cases h=40 and 400; h=400 has n=804, m=1206, r=403, 401 blocks, and its YES count has 192 decimal digits.
* Eight possible directed-triangle orientations checked with independent full backtracking and transfer matrices.
* **332 test cases, zero assertion failures.** Two independent executions produced byte-identical JSON.

Executed source SHA256: `67c73a26bd9b5cf5b42cdd866e18270bb6638425e16bd3379345e43b4c2d7924`.
Raw JSON SHA256: `872ea955c41e51be63d708446a4c6fe55c0f54c5d43ff04203ebe9a2805e4bc9`.
Complete executable, raw JSON, and extended proof report are in conversation artifact `TMR5_089_block_cut_evidence.zip`. Neither formal proof-kernel checking, external peer review nor repository-wide preflight was performed.

## Ranked synthesis

| Arrow | Status |
|---|---|
| Exact T5-CSP NP-completeness | PROVED by Barto-Kozik-Niven's primary no-sources/no-sinks dichotomy for noncycle core digraphs; T5 is a regular tournament and core |
| TMR-1's five-arc C5-to-T5 reduction | PROVED RESTRICTED, previous independently checked gadget |
| Exact T5 1-sum/bridge/block-cut counting | PROVED, explicit finite algebraic theorem |
| Exact polynomial algorithm for directed cactus and bounded-size blocks | PROVED |
| Global cycle rank implies mandatory 5^r work | FALSIFIED as instancewise lower-bound inference |
| OBDD, FBDD, tensor, local consistency, treewidth or source-blind representations imply generic machine effort | OPEN; prior false-positive controls continue |
| Unrestricted T5 superpolynomial time lower bound; Boolean-SAT transfer | OPEN |
| P versus NP | OPEN |

No identity, title, enabled state, ownership, peer manuscript, schedules, older safeguards or draft-PR merge status was changed.

Primary reference: L. Barto, M. Kozik, T. Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Computing 38(5) (2009), 1782-1802. https://doi.org/10.1137/070708093 .
