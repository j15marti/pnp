# TMR-3/089: complement-cover parameterized exact T5 counting

Owner: TMR-3 / PNP Time-Space Tradeoffs. November 18, 2026 (Pacific Time).
Classification: PROVED RESTRICTED constructive upper bound; finite evidence COMPUTATIONAL. **P versus NP OPEN**.

## Source-derived parameter

For a connected input source digraph whose underlying graph is bipartite, compute its bipartition \(U,V\) from the original edges. Reject loops or opposed arcs immediately. Define the bipartite *missing-cross-edge graph* \(H=(U,V,F)\), where \(uv\in F\) iff neither directed arc between \(u,v\) exists in the source. Let \(h=|F|\) and \(\tau=\tau(H)\), the minimum vertex-cover cardinality of \(H\). Obtain \(\tau\) and an actual cover \(C\) by maximum bipartite matching plus alternating reachability (Kőnig). Thus \(\tau\le h\). For disconnected original sources, process connected components separately and sum their \(\tau_i\); isolated vertices contribute a factor of five.

## Theorem 089 (exact FPT counting)

**All bipartite source digraphs have exact T5 coloring counts computable in \(O(\operatorname{poly}(N)5^\tau)\) deterministic time with polynomial space**, where \(\tau\) is the sum of the above component parameters. No supplied partition, witness cover, or promise that \(h\) is small is needed. When \(\tau\) is bounded, exact counting is polynomial time.

**Proof.** Every missing cross pair touches \(C\). Enumerate the colors of the at most \(\tau\) vertices in \(C\), discarding assignments invalid on arcs inside \(C\). Every remaining vertex \(v\) receives its exact unary domain \(D_v\subseteq\mathbb Z_5\) from all incident pinned arcs; nonedges impose no constraint. All cross pairs of the residual unpinned bipartition are now present in exactly one orientation, hence the residual is a genuine oriented complete biclique, not an improperly completed source.

Classify the residual vertices on each side by their complete orientation signatures to the opposite residual side. As in /088, distinct signatures on a side cannot have the same T5 color, and opposite-side vertices cannot share a color. Consequently if the numbers of signature classes \(a,b\) obey \(a+b>5\), the conditional contribution is zero. Otherwise \(a,b\ge 1\) imply a side with \(a\le2\) classes \(A_i\). Its class support \(S_i\subseteq\mathbb Z_5\) must have size one or two, since each opposite vertex has exactly two in-neighbors and out-neighbors in T5.

For class \(A_i\), and *vertex-specific* unary domains \(D_u\), the exact number of onto colorings is
\[
H_{A_i}(S)=\sum_{Q\subseteq S}(-1)^{|S|-|Q|}\prod_{u\in A_i}|D_u\cap Q|.
\]
For any opposite vertex \(v\), let \(c_v(S_1,\ldots,S_a)\) be the number of allowed colors \(y\in D_v\) simultaneously respecting its arc orientations with every \(x\in S_i\). The **exact original-vertex** conditional count is
\[
Z_{\rm res}=
\sum_{\substack{S_1,\ldots,S_a\subseteq\mathbb Z_5\\1\le|S_i|\le2}}
\left(\prod_iH_{A_i}(S_i)\right)
\left(\prod_{v\in B}c_v(S_1,\ldots,S_a)\right).
\]
There are at most \(15^2=225\) support tuples for every pinned coloring, regardless of graph size. If one residual side is empty, count by directly multiplying unary-domain cardinalities. Pinning may break the /088 45-orbit reduction **inside one conditional sum**, so this proof does NOT incorrectly assume the orbits remain intact. Instead, global translation lets a chosen cover vertex be fixed at 0 and the total multiplied by five, when the cover is nonempty.

The same deterministic sequential-tape implementation charges graph authentication, bipartition, missing-pair discovery, minimum matching and cover, source adjacency, color conditioning, signatures, inclusion-exclusion, full-precision arithmetic, addresses, head movement, memory and output. One conservative *simultaneous* bound is
\[
\boxed{T(N)=O((N+1)^{12}(1+5^\tau)),\quad
S_{\rm peak}(N)=O((N+1)^4)\ \text{bits}.}
\]
The output is at most \(5^n\), hence has \(O(N)\) bits. Intermediate products and sums also have polynomial bit length. These polynomial exponents are deliberately conservative symbolic upper bounds, **not** claims of executed native one-tape microcode. A nonbipartite source receives an exact polynomial-space \(5^n\) brute-force fallback; the FPT bound is asserted only for bipartite sources.

## Concrete falsifier and large easy-family control

One missing edge invalidates a naive application of /088 to *incomplete* signatures. All-forward \(K_{2,2}\) has 30 original colorings; deleting \(u_1v_1\) leaves a 3-edge directed tree with \(5\cdot2^3=40\) colorings. In particular \(u_0=u_1=A,\ v_0=v_1=B\) is valid, even though the two left vertices would have different signatures if absence were treated as a third orientation. The /089 algorithm conditions on a missing-edge cover first and then computes signatures only in the actual complete residual.

Take all-forward \(K_{120,121}\) and remove 60 edges incident to one left vertex. It has 241 original vertices and 14,460 directed arcs. Although \(h=60\), the minimum complement cover has \(\tau=1\). Exact count:
\[
19\,938\,419\,936\,773\,738\,105\,086\,320\,950\,273\,638\,380.
\]
The algorithm needs only one pinned-color assignment after symmetry fixing. The \(K_{3,3}\) identity-orientation UNSAT family, directed triangle, loops, opposed arcs, disconnected inputs, isolated vertices and original-vertex brute-force counting are retained as easy-family and negative controls.

## Actual verification

Full independent reference: 2,176 deterministic assertions, zero failures, repeated with byte-identical audit. Includes exhaustive complete orientations through 6 cross pairs, exhaustive missing/forward/backward cases through \(K_{2,3}\), 550 seeded random partial bicliques independently checked against original 5-color brute force, 596 exhaustive minimum-cover checks, 60-hole control, and SAT/UNSAT malformed-input tests. Separate compact published solver: 453 brute-force comparisons, repeated byte-identically, zero failures. The full executable and this report are additionally provided in the accompanying reproducibility ZIP.

Four gates: DISJ sanity PASS restricted constructive; relativization NOT APPLICABLE to nonseparation; SAME_REALIZATION DTISP PASS restricted symbolic upper-bound (no lower bound); configuration counting upper-bound consistency only. All affine, treewidth, twin/module, path, cycle, primal, dual Fourier, padding, all-forward, alternate algorithm, caching and recomputation controls remain live.

Bang-Jensen, Hell and MacGillivray (1988) prove NP-completeness of homomorphism to any semicomplete target with multiple directed cycles, hence general T5 homomorphism is NP-complete. This **does not** yield a quantitative time/space lower bound without an explicitly sized reduction. Native TM microcode, full combined LaTeX compilation, and independent mathematical review remain outstanding. **P versus NP OPEN**.

Next: **C3-T5-BICLIQUE-MODULE090**. Find authenticated decompositions into a few almost-complete bipartite blocks, glue their exact boundary-color functions while charging source discovery and repeated work; test global-large-\(\tau\) families where modules remain easy, plus obstructing control families.

References: [1] Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 281-298 (1988), https://doi.org/10.1137/0401029. [2] M. Goemans, *Lecture Notes on Bipartite Matching*, MIT (2013), https://math.mit.edu/~goemans/18433S13/matching-notes.pdf.
