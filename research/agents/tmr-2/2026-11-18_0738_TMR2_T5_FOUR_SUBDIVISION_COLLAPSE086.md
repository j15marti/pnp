# TMR-2/086: Four-step orientation-word quotient and exact 4-subdivision SAT collapse

Date: 2026-11-18, Pacific Time. Research owner: TMR-2 / PNP Information Necessity. Primary target is exactly R(a,b) iff b-a mod 5 is in {1,3}, with all original source variables counted. Result status: exact restricted symbolic theorems plus computational finite checks; external mathematical review OPEN. P versus NP OPEN.

## Target and mathematical proof

Let S be the 5x5 permutation matrix S[a,b]=[b-a=1 mod 5]. The authentic fixed-template adjacency matrix A is S+S^3, and its transpose is S^2+S^4=AS. Therefore, for every k-edge path with q backwards-pointing arcs, its exact original-endpoint counting cofactor is

  K_sigma=A^(k-q) (A^T)^q=A^k S^q,

and K_sigma(a,b)=(A^k)[a,(b-q) mod5]. This is a source-derived equality that sums over all k-1 internal labels. Only (k,q mod5), not the ordering of edge orientations, matters. At most five weighted cofactor matrices occur among all 2^k orientation words. This is an elementary circulant calculation and is not claimed as a new general algorithm.

The first row of A^k for k=0,1,2,3,4 respectively is

  (1,0,0,0,0); (0,1,0,1,0); (0,1,1,0,2);
  (3,0,3,1,1); (4,4,1,6,1).

Every A^k is circulant. Thus the row support sizes are exactly 1,2,3,4,5. Every path word of length <=3 misses at least one endpoint-label pair; every one of the sixteen four-edge words admits every one of the 25 endpoint pairs. Every length-four row has multiset {1,1,4,4,6}, determinant 16, and strictly positive entries. Strict positivity persists at larger lengths because no column of A is zero.

The base determinant det(A)=2 and the 5-cycle det(S)=1, giving det(K_sigma)=2^k. Exact transfer ranks are five over C and all odd-characteristic fields, but four in characteristic two for positive k. This is a particularly small, legal refutation of the inference MAXIMAL WEIGHTED TENSOR RANK => NECESSARY DIFFICULT EXISTENTIAL DECISION. The decision support for length-four paths is identically TRUE even while counting transfer retains maximal complex rank.

## Universal source-level consequence

Replace each edge of any loopless oriented simple graph G by an internally disjoint four-edge path with arbitrary segment orientations. Call the new T5 source G[4]. Choose arbitrary labels for every original vertex, even if G was UNSAT. Each replacement path has a valid extension for the chosen endpoints and paths have disjoint new variables. Therefore G[4] is always SAT and Z(G[4]) >= 5^|V(G)|. The exact count remains the nontrivial weighted sum over all original labelings of products of K_sigma, so this theorem does not make all #CSP instances tractable. Four-subdivision multiplies all undirected cycle lengths by four. Naive edge-subdivision is therefore not a valid hardness-preserving high-girth amplification strategy for this original fixed-T5 relation.

A cheap source-aware recognizer, given a parsed loopless simple orientation, suppresses degree-two chains. When every maximal junction-to-junction chain and all remaining degree-two-only cycles have length >=4, arbitrary zero junction labels and independent path extensions give a complete SAT witness in O(n+m) word operations after parsing. A non-simple orientation or shorter path must be reported UNKNOWN, not UNSAT. The full executed Python canonicalizer sorts arcs (O(m log m) comparisons) and pays for this; a streaming strict parser can check already-sorted canonical arcs in one pass.

## Reproduced finite sources and independent checks

The full locally executed CPython producer and independently implemented Node.js verifier each regenerated the earlier TMR-2/084 W(3,4) 170-variable, 425-edge, girth-eight certified NO source with canonical SHA256 cc9e6c343ca2bccfe8839a8dd077d4d543e75e2bd669100f5e87861637a10632. In each source-edge position j, the four-segment orientation word is selected using mask (7*j+3)%16. All 16 sign words are present. New original source: 1445 vertices, 1700 arcs, undirected girth 32, canonical SHA256 9aa65d433fa747f83d5245eea613795067a59f6851fa77a5b490d406d51096c0. Both implementations directly verify a full T5 SAT assignment with all 170 old colors zero, in contrast to /084's prior complete seven-node NO certificate for the original 170-source.

On the /075 four-variable five-arc UNSAT motif, the mixed-orientation 19-vertex, 20-arc four-subdivision has exact count 257280, including 144 extensions of all four old colors fixed to zero. The exact count is obtained by all 625 original assignments and explicit independent path-interior counts, not by naively enumerating all 5^19 assignments.

CPython full audit: 10003 assertions, zero failures, 775 brute original-label endpoint checks, all 16 length-four transfer determinants, two full-source girth BFS checks, strict source parsing, negative short/antiparallel controls and complete 1445-label witness. Independent Node.js full audit: 5270 assertions, zero failures, independent GF(4) arithmetic, exact source hashes, independent counting, girth BFS and complete new-source arc witness. These are computational checks; the matrix and padding results are mathematical theorems given the displayed derivation.

This GitHub publication includes a standalone compact Python reproduction of the symbolic transfer and exact 19-variable example. Full executed original-source rebuild, independent Node.js code and complete raw JSON are available as checked conversation artifacts but are not represented as copied into GitHub in this version. The compact reproduction does not independently replay the W(3,4) geometry.

## Named dynamic invariant, cost and scientific guards

D2-T5-ORIENTATION-WORD-QUOTIENT-AND-SATURATION-INDEX is the paid tuple (k, q mod5, exact K_sigma, Boolean support). Source operations include READ/PARSE/HASH, genuine arc inspection, degree-two-chain recognition, transfer product or cached powers, exact internal-label count, witness construction, direct whole-source arc validation, graph girth discovery, bigint output, storage/recomputation, and all failed recognition paths. These are upper constructions only.

DISJ: PASS restricted / FAIL any general rank-to-runtime inference. Relativization and algebrization: constructive upper only, general P-vs-NP lower OPEN. Simultaneous DTISP: scoped polynomial easy-class upper, no forbidden unrestricted tradeoff. Deterministic configuration counting: no necessary-work claim from exact weighted rank. Natural Proofs/BGS safeguards remain. All cheap alternatives including Fourier/flow, full consistency, exact elimination, adaptive gauges, separator recognition, OBDD/FBDD, caching and parallel algorithms remain admissible. /341 unrestricted UNSAT authority FAIL; /386 RESTRICTED.

Predecessors: TMR-2/075, /078, /084, /085. Related background: Bang-Jensen, Hell and MacGillivray, Complexity of colouring by semicomplete digraphs, SIAM J. Discrete Math. (1988); Horton, A polynomial-time algorithm to find the shortest cycle basis of a graph, SIAM J. Comput. 16 (1987), DOI 10.1137/0216026.

Next dependency D2-T5-ADAPTIVE-COFACTOR-GROWING-FAMILY remains OPEN, now requiring a non-saturating path gadget when attempting hardness-preserving girth amplification, and independent same-source tests against legal source-aware algorithms. External math review, complete root LaTeX compilation, repo-wide preflight, physical Turing machine resource replay and unrestricted lower-bound transfer OPEN. P versus NP OPEN.